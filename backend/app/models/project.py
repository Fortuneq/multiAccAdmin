"""
Video Project model for database.
Manages video generation projects with editing parameters.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ProjectStatus(str, enum.Enum):
    """Project status types."""
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FilterType(str, enum.Enum):
    """Video filter types."""
    NONE = "none"
    CINEMATIC = "cinematic"
    BRIGHT = "bright"
    CYBERPUNK = "cyberpunk"
    VINTAGE = "vintage"
    WARM = "warm"
    COOL = "cool"


class VideoProject(Base):
    """
    Video project model for video generation and editing.

    Attributes:
        id: Primary key
        name: Project name
        status: Project status (draft/processing/completed/failed)
        video_track_path: Path to source video file
        audio_track_path: Path to audio file (optional)
        subtitle_text: Subtitle text content (optional)
        audio_volume: Audio volume level (0-100)
        filter_type: Applied filter type
        uniquify_subtitles: Whether to apply unique styling to subtitles
        account_id: Foreign key to account
        output_path: Path to generated output video
        error_message: Error message if processing failed
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "video_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False)

    # Source files
    video_track_path = Column(String(1000), nullable=False)
    audio_track_path = Column(String(1000), nullable=True)
    subtitle_text = Column(String(5000), nullable=True)

    # Processing parameters
    audio_volume = Column(Integer, default=100, nullable=False)  # 0-100
    filter_type = Column(Enum(FilterType), default=FilterType.NONE, nullable=False)
    uniquify_subtitles = Column(Boolean, default=False, nullable=False)

    # Output
    output_path = Column(String(1000), nullable=True)
    error_message = Column(String(2000), nullable=True)

    # Relationships
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="projects")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<VideoProject {self.name} ({self.status.value})>"

    @property
    def is_processable(self) -> bool:
        """Check if project can be processed."""
        return self.status in [ProjectStatus.DRAFT, ProjectStatus.FAILED]

    @property
    def is_completed(self) -> bool:
        """Check if project is completed."""
        return self.status == ProjectStatus.COMPLETED and self.output_path is not None
