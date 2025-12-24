"""
API router for analytics and dashboard data.
Provides statistics and metrics for accounts and videos.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from app.database import get_db
from app.models import Account, Video, AccountStatus
from app.schemas import AccountStats
from app.services.mock_data import generate_dashboard_data, generate_account_analytics

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard(
    db: Session = Depends(get_db)
):
    """
    Get dashboard overview with statistics and charts.

    Args:
        db: Database session

    Returns:
        Dashboard data including:
        - Overview cards (total accounts, active, followers, etc.)
        - Line chart data (engagement over time)
        - Bar chart data (platform distribution)
        - Radar chart data (performance metrics)
    """
    # Get real statistics from database
    total_accounts = db.query(Account).count()
    active_accounts = db.query(Account).filter(Account.status == AccountStatus.ONLINE).count()
    total_followers = db.query(func.sum(Account.followers)).scalar() or 0
    total_videos = db.query(func.sum(Account.videos_count)).scalar() or 0

    # Calculate average engagement rate
    accounts_with_engagement = db.query(Account).filter(
        Account.followers > 0,
        Account.videos_count > 0
    ).all()

    if accounts_with_engagement:
        avg_engagement = sum(acc.engagement_rate for acc in accounts_with_engagement) / len(accounts_with_engagement)
    else:
        avg_engagement = 0.0

    # Generate mock chart data
    dashboard_data = generate_dashboard_data()

    # Update overview with real data
    dashboard_data["overview"] = {
        "total_accounts": total_accounts,
        "active_accounts": active_accounts,
        "total_followers": int(total_followers),
        "total_videos": int(total_videos),
        "total_engagement": int(total_followers * avg_engagement / 100) if avg_engagement else 0,
        "avg_engagement_rate": round(avg_engagement, 2)
    }

    return dashboard_data


@router.get("/stats", response_model=AccountStats)
async def get_stats(
    db: Session = Depends(get_db)
):
    """
    Get overall account statistics.

    Args:
        db: Database session

    Returns:
        Aggregated account statistics
    """
    total_accounts = db.query(Account).count()
    active_accounts = db.query(Account).filter(Account.status == AccountStatus.ONLINE).count()
    total_followers = db.query(func.sum(Account.followers)).scalar() or 0
    total_videos = db.query(func.sum(Account.videos_count)).scalar() or 0
    total_likes = db.query(func.sum(Account.total_likes)).scalar() or 0
    total_comments = db.query(func.sum(Account.total_comments)).scalar() or 0
    total_engagement = total_likes + total_comments

    # Calculate average engagement rate
    accounts_with_engagement = db.query(Account).filter(
        Account.followers > 0,
        Account.videos_count > 0
    ).all()

    if accounts_with_engagement:
        avg_engagement = sum(acc.engagement_rate for acc in accounts_with_engagement) / len(accounts_with_engagement)
    else:
        avg_engagement = 0.0

    return AccountStats(
        total_accounts=total_accounts,
        active_accounts=active_accounts,
        total_followers=int(total_followers),
        total_videos=int(total_videos),
        total_engagement=int(total_engagement),
        avg_engagement_rate=round(avg_engagement, 2)
    )


@router.get("/account/{account_id}", response_model=Dict[str, Any])
async def get_account_analytics(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed analytics for a specific account.

    Args:
        account_id: Account ID
        db: Database session

    Returns:
        Account analytics including:
        - Account details
        - Performance metrics
        - Trend data
        - Engagement breakdown

    Raises:
        HTTPException: If account not found
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found")

    # Get account videos
    videos = db.query(Video).filter(Video.account_id == account_id).all()

    # Generate analytics data
    analytics_data = generate_account_analytics(account, videos)

    return analytics_data
