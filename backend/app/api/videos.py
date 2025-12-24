"""
API router for video management.
Handles video listing and upload operations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import shutil
import uuid

from app.database import get_db
from app.models import Video, Account
from app.schemas import VideoCreate, VideoResponse
from app.config import get_settings

router = APIRouter(prefix="/api/videos", tags=["Videos"])
settings = get_settings()


@router.get("/", response_model=List[VideoResponse])
async def get_videos(
    account_id: Optional[int] = Query(None, description="Filter by account ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get list of all videos with optional filtering.

    Args:
        account_id: Filter by account ID
        skip: Pagination offset
        limit: Maximum number of results
        db: Database session

    Returns:
        List of videos
    """
    query = db.query(Video)

    if account_id:
        query = query.filter(Video.account_id == account_id)

    videos = query.order_by(Video.created_at.desc()).offset(skip).limit(limit).all()
    return videos


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific video by ID.

    Args:
        video_id: Video ID
        db: Database session

    Returns:
        Video details

    Raises:
        HTTPException: If video not found
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail=f"Video with ID {video_id} not found")

    return video


@router.post("/upload", response_model=VideoResponse, status_code=201)
async def upload_video(
    file: UploadFile = File(..., description="Video file to upload"),
    title: str = Query(..., description="Video title"),
    account_id: Optional[int] = Query(None, description="Associated account ID"),
    platform: Optional[str] = Query(None, description="Platform name"),
    db: Session = Depends(get_db)
):
    """
    Upload a video file.

    Args:
        file: Video file
        title: Video title
        account_id: Associated account ID (optional)
        platform: Platform name (optional)
        db: Database session

    Returns:
        Created video record

    Raises:
        HTTPException: If account not found or file too large
    """
    # Validate account if provided
    if account_id:
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found")

    # Validate file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / (1024*1024)} MB"
        )

    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    upload_path = Path(settings.UPLOAD_DIR) / "videos" / unique_filename

    # Save file
    try:
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        with upload_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create video record
    video_data = VideoCreate(
        title=title,
        file_path=str(upload_path),
        size=file_size,
        account_id=account_id,
        platform=platform
    )

    new_video = Video(**video_data.model_dump())
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return new_video


@router.delete("/{video_id}", status_code=204)
async def delete_video(
    video_id: int,
    delete_file: bool = Query(False, description="Also delete physical file"),
    db: Session = Depends(get_db)
):
    """
    Delete a video.

    Args:
        video_id: Video ID
        delete_file: Whether to delete the physical file
        db: Database session

    Raises:
        HTTPException: If video not found
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail=f"Video with ID {video_id} not found")

    # Delete physical file if requested
    if delete_file:
        try:
            file_path = Path(video.file_path)
            if file_path.exists():
                file_path.unlink()

            if video.thumbnail_path:
                thumb_path = Path(video.thumbnail_path)
                if thumb_path.exists():
                    thumb_path.unlink()
        except Exception as e:
            # Log error but don't fail the deletion
            print(f"Warning: Could not delete file {video.file_path}: {str(e)}")

    db.delete(video)
    db.commit()

    return None
