"""
Pydantic schemas for Account model.
Validation and serialization for API requests/responses.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

from app.models.account import Platform, AccountStatus


class AccountBase(BaseModel):
    """Base schema for account with common fields."""
    username: str = Field(..., min_length=1, max_length=255, description="Account username")
    platform: Platform = Field(default=Platform.TIKTOK, description="Social media platform")
    region: Optional[str] = Field(None, max_length=100, description="Geographic region")
    status: AccountStatus = Field(default=AccountStatus.OFFLINE, description="Account status")


class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    proxy_id: Optional[int] = Field(None, description="Associated proxy ID")
    followers: int = Field(default=0, ge=0, description="Number of followers")
    videos_count: int = Field(default=0, ge=0, description="Number of videos")
    total_likes: int = Field(default=0, ge=0, description="Total likes")
    total_comments: int = Field(default=0, ge=0, description="Total comments")

    @validator('username')
    def username_must_start_with_at(cls, v):
        """Ensure username starts with @."""
        if not v.startswith('@'):
            v = f'@{v}'
        return v


class AccountUpdate(BaseModel):
    """Schema for updating an account (all fields optional)."""
    username: Optional[str] = Field(None, min_length=1, max_length=255)
    platform: Optional[Platform] = None
    region: Optional[str] = Field(None, max_length=100)
    status: Optional[AccountStatus] = None
    proxy_id: Optional[int] = None
    followers: Optional[int] = Field(None, ge=0)
    videos_count: Optional[int] = Field(None, ge=0)
    total_likes: Optional[int] = Field(None, ge=0)
    total_comments: Optional[int] = Field(None, ge=0)

    @validator('username')
    def username_must_start_with_at(cls, v):
        """Ensure username starts with @."""
        if v is not None and not v.startswith('@'):
            v = f'@{v}'
        return v


class AccountResponse(AccountBase):
    """Schema for account response."""
    id: int
    followers: int
    videos_count: int
    total_likes: int
    total_comments: int
    engagement_rate: float
    avg_likes_per_video: float
    proxy_id: Optional[int]
    last_activity: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AccountStats(BaseModel):
    """Schema for account statistics."""
    total_accounts: int
    active_accounts: int
    total_followers: int
    total_videos: int
    total_engagement: int
    avg_engagement_rate: float
