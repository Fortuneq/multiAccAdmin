"""
Pydantic schemas for Proxy model.
Validation and serialization for API requests/responses.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

from app.models.proxy import ProxyType


class ProxyBase(BaseModel):
    """Base schema for proxy with common fields."""
    proxy_type: ProxyType = Field(default=ProxyType.SOCKS5, description="Proxy protocol type")
    address: str = Field(..., min_length=1, max_length=255, description="Proxy IP or hostname")
    port: int = Field(..., ge=1, le=65535, description="Proxy port (1-65535)")
    username: Optional[str] = Field(None, max_length=255, description="Authentication username")
    password: Optional[str] = Field(None, max_length=255, description="Authentication password")
    is_active: bool = Field(default=True, description="Whether proxy is active")


class ProxyCreate(ProxyBase):
    """Schema for creating a new proxy."""
    pass


class ProxyUpdate(BaseModel):
    """Schema for updating a proxy (all fields optional)."""
    proxy_type: Optional[ProxyType] = None
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    port: Optional[int] = Field(None, ge=1, le=65535)
    username: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class ProxyResponse(ProxyBase):
    """Schema for proxy response."""
    id: int
    last_tested: Optional[datetime]
    created_at: datetime
    full_address: str

    class Config:
        from_attributes = True


class ProxyTestResult(BaseModel):
    """Schema for proxy test result."""
    success: bool
    message: str
    response_time: Optional[float] = None  # in seconds
    tested_at: datetime
