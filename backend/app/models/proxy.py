"""
Proxy model for database.
Manages proxy server configurations.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ProxyType(str, enum.Enum):
    """Proxy protocol types."""
    SOCKS5 = "SOCKS5"
    HTTP = "HTTP"
    HTTPS = "HTTPS"


class Proxy(Base):
    """
    Proxy server configuration model.

    Attributes:
        id: Primary key
        proxy_type: Type of proxy (SOCKS5/HTTP/HTTPS)
        address: Proxy server IP or hostname
        port: Proxy server port
        username: Authentication username (optional)
        password: Authentication password (optional)
        is_active: Whether proxy is currently active
        last_tested: Last time proxy was tested
        created_at: Creation timestamp
    """
    __tablename__ = "proxies"

    id = Column(Integer, primary_key=True, index=True)
    proxy_type = Column(Enum(ProxyType), nullable=False, default=ProxyType.SOCKS5)
    address = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_tested = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    accounts = relationship("Account", back_populates="proxy")

    def __repr__(self):
        return f"<Proxy {self.proxy_type}://{self.address}:{self.port}>"

    @property
    def full_address(self) -> str:
        """Get full proxy address with protocol."""
        protocol = self.proxy_type.value.lower()
        if self.username and self.password:
            return f"{protocol}://{self.username}:{self.password}@{self.address}:{self.port}"
        return f"{protocol}://{self.address}:{self.port}"
