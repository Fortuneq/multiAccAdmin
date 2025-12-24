"""
Pydantic schemas for API validation and serialization.
"""
from app.schemas.proxy import ProxyCreate, ProxyUpdate, ProxyResponse, ProxyTestResult
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse, AccountStats
from app.schemas.video import (
    VideoCreate,
    VideoResponse,
    VideoProjectCreate,
    VideoProjectUpdate,
    VideoProjectResponse,
    VideoProcessRequest,
    VideoProcessResponse,
)

__all__ = [
    "ProxyCreate",
    "ProxyUpdate",
    "ProxyResponse",
    "ProxyTestResult",
    "AccountCreate",
    "AccountUpdate",
    "AccountResponse",
    "AccountStats",
    "VideoCreate",
    "VideoResponse",
    "VideoProjectCreate",
    "VideoProjectUpdate",
    "VideoProjectResponse",
    "VideoProcessRequest",
    "VideoProcessResponse",
]
