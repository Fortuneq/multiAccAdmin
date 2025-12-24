"""
Business logic services for the application.
"""
from app.services.video_generator import VideoGenerator
from app.services.mock_data import (
    generate_username,
    generate_followers,
    generate_video_stats,
    generate_dashboard_data,
    generate_account_analytics
)

__all__ = [
    "VideoGenerator",
    "generate_username",
    "generate_followers",
    "generate_video_stats",
    "generate_dashboard_data",
    "generate_account_analytics"
]
