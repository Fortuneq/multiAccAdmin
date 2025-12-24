"""
API router for video generation and processing.
Handles video project CRUD and processing operations.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import VideoProject, ProjectStatus, Account
from app.schemas import (
    VideoProjectCreate,
    VideoProjectUpdate,
    VideoProjectResponse,
    VideoProcessResponse
)
from app.services.video_generator import VideoGenerator

router = APIRouter(prefix="/api/generator", tags=["Video Generator"])


@router.post("/project", response_model=VideoProjectResponse, status_code=201)
async def create_project(
    project_data: VideoProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new video project.

    Args:
        project_data: Project creation data
        db: Database session

    Returns:
        Created project

    Raises:
        HTTPException: If account not found or video file doesn't exist
    """
    # Validate account if provided
    if project_data.account_id:
        account = db.query(Account).filter(Account.id == project_data.account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail=f"Account with ID {project_data.account_id} not found")

    # Create new project
    new_project = VideoProject(**project_data.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/project", response_model=List[VideoProjectResponse])
async def get_projects(
    db: Session = Depends(get_db)
):
    """
    Get all video projects.

    Args:
        db: Database session

    Returns:
        List of projects
    """
    projects = db.query(VideoProject).order_by(VideoProject.updated_at.desc()).all()
    return projects


@router.get("/project/{project_id}", response_model=VideoProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific project by ID.

    Args:
        project_id: Project ID
        db: Database session

    Returns:
        Project details

    Raises:
        HTTPException: If project not found
    """
    project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")

    return project


@router.put("/project/{project_id}", response_model=VideoProjectResponse)
async def update_project(
    project_id: int,
    project_data: VideoProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing project.

    Args:
        project_id: Project ID
        project_data: Updated project data
        db: Database session

    Returns:
        Updated project

    Raises:
        HTTPException: If project not found or is currently processing
    """
    project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")

    # Don't allow updates while processing
    if project.status == ProjectStatus.PROCESSING:
        raise HTTPException(status_code=400, detail="Cannot update project while processing")

    # Update fields
    update_data = project_data.model_dump(exclude_unset=True)

    # Validate account if updating
    if "account_id" in update_data and update_data["account_id"]:
        account = db.query(Account).filter(Account.id == update_data["account_id"]).first()
        if not account:
            raise HTTPException(status_code=404, detail=f"Account with ID {update_data['account_id']} not found")

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


@router.post("/project/{project_id}/process", response_model=VideoProcessResponse)
async def process_project(
    project_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Process a video project (add audio, filters, subtitles).

    Args:
        project_id: Project ID
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Processing status

    Raises:
        HTTPException: If project not found or not processable
    """
    project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")

    if not project.is_processable:
        raise HTTPException(
            status_code=400,
            detail=f"Project cannot be processed. Current status: {project.status.value}"
        )

    # Set status to processing
    project.status = ProjectStatus.PROCESSING
    project.error_message = None
    db.commit()

    # Process in background
    def process_video_task():
        try:
            generator = VideoGenerator()
            output_path = generator.composite_video(
                video_path=project.video_track_path,
                audio_path=project.audio_track_path,
                subtitle_text=project.subtitle_text,
                volume=project.audio_volume,
                filter_type=project.filter_type.value,
                uniquify=project.uniquify_subtitles
            )

            # Update project
            project.output_path = output_path
            project.status = ProjectStatus.COMPLETED
            db.commit()

        except Exception as e:
            project.status = ProjectStatus.FAILED
            project.error_message = str(e)
            db.commit()

    background_tasks.add_task(process_video_task)

    return VideoProcessResponse(
        success=True,
        message="Video processing started",
        project_id=project_id
    )


@router.post("/project/{project_id}/export", response_model=VideoProcessResponse)
async def export_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Export a completed project.

    Args:
        project_id: Project ID
        db: Database session

    Returns:
        Export information

    Raises:
        HTTPException: If project not found or not completed
    """
    project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")

    if not project.is_completed:
        raise HTTPException(
            status_code=400,
            detail=f"Project is not completed. Current status: {project.status.value}"
        )

    return VideoProcessResponse(
        success=True,
        message="Video ready for export",
        project_id=project_id,
        output_path=project.output_path
    )


@router.delete("/project/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a video project.

    Args:
        project_id: Project ID
        db: Database session

    Raises:
        HTTPException: If project not found or is processing
    """
    project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")

    if project.status == ProjectStatus.PROCESSING:
        raise HTTPException(status_code=400, detail="Cannot delete project while processing")

    db.delete(project)
    db.commit()

    return None
