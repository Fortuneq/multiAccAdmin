"""
Video model for database.
Manages uploaded and generated videos.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Video(Base):
    """
    Video content model.

    Attributes:
        id: Primary key
        title: Video title
        file_path: Path to video file
        thumbnail_path: Path to thumbnail image
        account_id: Foreign key to account
        duration: Video duration in seconds
        size: File size in bytes
        views: Number of views
        likes: Number of likes
        comments: Number of comments
        engagement_rate: Calculated engagement rate
        platform: Platform where video is uploaded
        upload_date: Date when video was uploaded
        created_at: Creation timestamp
    """
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    thumbnail_path = Column(String(1000), nullable=True)

    # Video metadata
    duration = Column(Float, nullable=True)  # in seconds
    size = Column(BigInteger, nullable=True)  # in bytes

    # Statistics
    views = Column(BigInteger, default=0, nullable=False)
    likes = Column(BigInteger, default=0, nullable=False)
    comments = Column(Integer, default=0, nullable=False)
    engagement_rate = Column(Float, default=0.0, nullable=False)

    # Platform info
    platform = Column(String(50), nullable=True)
    upload_date = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="videos")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Video {self.title} ({self.id})>"

    @property
    def size_mb(self) -> float:
        """Get file size in megabytes."""
        if self.size:
            return round(self.size / (1024 * 1024), 2)
        return 0.0

    @property
    def duration_formatted(self) -> str:
        """Get formatted duration (MM:SS)."""
        if not self.duration:
            return "00:00"
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def calculate_engagement(self):
        """Calculate and update engagement rate."""
        if self.views > 0:
            self.engagement_rate = round(((self.likes + self.comments) / self.views) * 100, 2)
        else:
            self.engagement_rate = 0.0
