"""
Account model for database.
Manages TikTok/Reels/Shorts social media accounts.
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class Platform(str, enum.Enum):
    """Social media platform types."""
    TIKTOK = "TikTok"
    REELS = "Reels"
    SHORTS = "Shorts"


class AccountStatus(str, enum.Enum):
    """Account status types."""
    ONLINE = "online"
    OFFLINE = "offline"
    SUSPENDED = "suspended"
    PENDING = "pending"


class Account(Base):
    """
    Social media account model.

    Attributes:
        id: Primary key
        username: Account username (e.g., @user_name_123)
        platform: Platform type (TikTok/Reels/Shorts)
        region: Geographic region/country
        followers: Number of followers
        videos_count: Total number of videos
        total_likes: Total likes across all videos
        total_comments: Total comments across all videos
        status: Account status (online/offline/suspended/pending)
        last_activity: Last activity timestamp
        proxy_id: Foreign key to proxy
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    platform = Column(Enum(Platform), nullable=False, default=Platform.TIKTOK)
    region = Column(String(100), nullable=True)

    # Statistics
    followers = Column(BigInteger, default=0, nullable=False)
    videos_count = Column(Integer, default=0, nullable=False)
    total_likes = Column(BigInteger, default=0, nullable=False)
    total_comments = Column(BigInteger, default=0, nullable=False)

    # Status
    status = Column(Enum(AccountStatus), default=AccountStatus.OFFLINE, nullable=False)
    last_activity = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    proxy_id = Column(Integer, ForeignKey("proxies.id"), nullable=True)
    proxy = relationship("Proxy", back_populates="accounts")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationship with videos
    videos = relationship("Video", back_populates="account", cascade="all, delete-orphan")
    projects = relationship("VideoProject", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Account {self.username} ({self.platform.value})>"

    @property
    def engagement_rate(self) -> float:
        """
        Calculate engagement rate.
        Formula: (total_likes + total_comments) / (followers * videos_count) * 100
        """
        if self.followers == 0 or self.videos_count == 0:
            return 0.0
        total_engagement = self.total_likes + self.total_comments
        return round((total_engagement / (self.followers * self.videos_count)) * 100, 2)

    @property
    def avg_likes_per_video(self) -> float:
        """Calculate average likes per video."""
        if self.videos_count == 0:
            return 0.0
        return round(self.total_likes / self.videos_count, 2)
