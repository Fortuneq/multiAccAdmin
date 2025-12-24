"""
Pydantic schemas for Video and VideoProject models.
Validation and serialization for API requests/responses.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.models.project import ProjectStatus, FilterType


class VideoBase(BaseModel):
    """Base schema for video with common fields."""
    title: str = Field(..., min_length=1, max_length=500, description="Video title")
    platform: Optional[str] = Field(None, max_length=50, description="Platform name")


class VideoCreate(VideoBase):
    """Schema for creating a new video."""
    file_path: str = Field(..., description="Path to video file")
    thumbnail_path: Optional[str] = None
    duration: Optional[float] = Field(None, ge=0, description="Duration in seconds")
    size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    account_id: Optional[int] = Field(None, description="Associated account ID")


class VideoResponse(VideoBase):
    """Schema for video response."""
    id: int
    file_path: str
    thumbnail_path: Optional[str]
    duration: Optional[float]
    size: Optional[int]
    size_mb: float
    duration_formatted: str
    views: int
    likes: int
    comments: int
    engagement_rate: float
    account_id: Optional[int]
    upload_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class VideoProjectBase(BaseModel):
    """Base schema for video project."""
    name: str = Field(..., min_length=1, max_length=500, description="Project name")
    video_track_path: str = Field(..., description="Path to source video")
    audio_track_path: Optional[str] = Field(None, description="Path to audio file")
    subtitle_text: Optional[str] = Field(None, max_length=5000, description="Subtitle text")
    audio_volume: int = Field(default=100, ge=0, le=100, description="Audio volume (0-100)")
    filter_type: FilterType = Field(default=FilterType.NONE, description="Video filter type")
    uniquify_subtitles: bool = Field(default=False, description="Apply unique subtitle styling")


class VideoProjectCreate(VideoProjectBase):
    """Schema for creating a new video project."""
    account_id: Optional[int] = Field(None, description="Associated account ID")


class VideoProjectUpdate(BaseModel):
    """Schema for updating a video project (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    audio_track_path: Optional[str] = None
    subtitle_text: Optional[str] = Field(None, max_length=5000)
    audio_volume: Optional[int] = Field(None, ge=0, le=100)
    filter_type: Optional[FilterType] = None
    uniquify_subtitles: Optional[bool] = None
    account_id: Optional[int] = None


class VideoProjectResponse(VideoProjectBase):
    """Schema for video project response."""
    id: int
    status: ProjectStatus
    output_path: Optional[str]
    error_message: Optional[str]
    account_id: Optional[int]
    is_processable: bool
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VideoProcessRequest(BaseModel):
    """Schema for video processing request."""
    project_id: int = Field(..., description="Video project ID to process")


class VideoProcessResponse(BaseModel):
    """Schema for video processing response."""
    success: bool
    message: str
    project_id: int
    output_path: Optional[str] = None
    error: Optional[str] = None
