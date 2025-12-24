"""
Main FastAPI application.
Admin panel API for managing TikTok/Reels/Shorts accounts and video generation.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import get_settings, init_directories
from app.database import engine, Base
from app.api import accounts, proxies, videos, generator, analytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Admin Panel API for managing social media accounts (TikTok/Reels/Shorts)
    and video generation with FFmpeg.

    ## Features

    * **Account Management** - CRUD operations for social media accounts
    * **Proxy Management** - Configure and test proxy servers
    * **Video Management** - Upload and manage video content
    * **Video Generator** - Process videos with audio, filters, and subtitles
    * **Analytics** - Dashboard and account statistics

    ## Authentication

    Currently no authentication required (development mode).
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Create directories
    init_directories()
    logger.info("Upload directories initialized")

    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on shutdown.
    """
    logger.info("Shutting down application")


# Include routers
app.include_router(accounts.router)
app.include_router(proxies.router)
app.include_router(videos.router)
app.include_router(generator.router)
app.include_router(analytics.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "accounts": "/api/accounts",
            "proxies": "/api/proxies",
            "videos": "/api/videos",
            "generator": "/api/generator",
            "analytics": "/api/analytics"
        }
    }


# Health check endpoint
@app.get("/health", tags=["Root"])
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
