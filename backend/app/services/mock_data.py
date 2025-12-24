"""
Mock data generator service.
Generates realistic test data for accounts, videos, and analytics.
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_username() -> str:
    """Generate random username in format @user_name_123."""
    prefixes = [
        "creative", "viral", "trending", "social", "digital", "content",
        "media", "studio", "creator", "influencer", "pro", "official"
    ]
    suffixes = [
        "star", "master", "expert", "king", "queen", "guru",
        "ninja", "wizard", "legend", "boss", "pro", "tv"
    ]

    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    number = random.randint(1, 9999)

    return f"@{prefix}_{suffix}_{number}"


def generate_followers() -> int:
    """Generate realistic follower count."""
    # 70% small accounts, 20% medium, 10% large
    tier = random.random()

    if tier < 0.7:  # Small accounts
        return random.randint(100, 50000)
    elif tier < 0.9:  # Medium accounts
        return random.randint(50000, 500000)
    else:  # Large accounts
        return random.randint(500000, 5000000)


def generate_video_stats(followers: int, videos_count: int) -> Dict[str, int]:
    """
    Generate realistic video statistics based on follower count.

    Args:
        followers: Number of followers
        videos_count: Number of videos

    Returns:
        Dictionary with total_likes and total_comments
    """
    # Engagement rate typically 2-8%
    engagement_rate = random.uniform(0.02, 0.08)

    # Average views per video (typically 10-50% of followers)
    avg_views_per_video = followers * random.uniform(0.1, 0.5)

    # Likes are about 5-15% of views
    like_rate = random.uniform(0.05, 0.15)
    avg_likes_per_video = int(avg_views_per_video * like_rate)

    # Comments are about 0.5-2% of views
    comment_rate = random.uniform(0.005, 0.02)
    avg_comments_per_video = int(avg_views_per_video * comment_rate)

    total_likes = avg_likes_per_video * videos_count
    total_comments = avg_comments_per_video * videos_count

    return {
        "total_likes": total_likes,
        "total_comments": total_comments
    }


def generate_dashboard_data() -> Dict[str, Any]:
    """
    Generate mock dashboard data with charts and metrics.

    Returns:
        Dictionary containing:
        - overview: Summary statistics
        - line_chart: Engagement over time
        - bar_chart: Platform distribution
        - radar_chart: Performance metrics
    """
    # Line chart: Engagement over last 7 days
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    line_chart = {
        "labels": dates,
        "datasets": [
            {
                "label": "Likes",
                "data": [random.randint(5000, 25000) for _ in range(7)],
                "borderColor": "#3b82f6",
                "backgroundColor": "rgba(59, 130, 246, 0.1)"
            },
            {
                "label": "Comments",
                "data": [random.randint(500, 3000) for _ in range(7)],
                "borderColor": "#10b981",
                "backgroundColor": "rgba(16, 185, 129, 0.1)"
            },
            {
                "label": "Shares",
                "data": [random.randint(200, 1500) for _ in range(7)],
                "borderColor": "#f59e0b",
                "backgroundColor": "rgba(245, 158, 11, 0.1)"
            }
        ]
    }

    # Bar chart: Platform distribution
    bar_chart = {
        "labels": ["TikTok", "Reels", "Shorts"],
        "datasets": [
            {
                "label": "Accounts",
                "data": [
                    random.randint(10, 50),
                    random.randint(10, 50),
                    random.randint(10, 50)
                ],
                "backgroundColor": [
                    "#3b82f6",
                    "#10b981",
                    "#f59e0b"
                ]
            }
        ]
    }

    # Radar chart: Performance metrics
    radar_chart = {
        "labels": ["Engagement", "Reach", "Growth", "Quality", "Consistency"],
        "datasets": [
            {
                "label": "Current Period",
                "data": [
                    random.randint(60, 95),
                    random.randint(60, 95),
                    random.randint(60, 95),
                    random.randint(60, 95),
                    random.randint(60, 95)
                ],
                "backgroundColor": "rgba(59, 130, 246, 0.2)",
                "borderColor": "#3b82f6"
            },
            {
                "label": "Previous Period",
                "data": [
                    random.randint(50, 85),
                    random.randint(50, 85),
                    random.randint(50, 85),
                    random.randint(50, 85),
                    random.randint(50, 85)
                ],
                "backgroundColor": "rgba(156, 163, 175, 0.2)",
                "borderColor": "#9ca3af"
            }
        ]
    }

    # Doughnut chart: Content types
    doughnut_chart = {
        "labels": ["Educational", "Entertainment", "Promotional", "Behind-the-Scenes", "User-Generated"],
        "datasets": [
            {
                "data": [
                    random.randint(15, 35),
                    random.randint(20, 40),
                    random.randint(10, 25),
                    random.randint(10, 20),
                    random.randint(5, 15)
                ],
                "backgroundColor": [
                    "#3b82f6",
                    "#10b981",
                    "#f59e0b",
                    "#8b5cf6",
                    "#ec4899"
                ]
            }
        ]
    }

    return {
        "overview": {
            "total_accounts": 0,  # Will be filled by real data
            "active_accounts": 0,
            "total_followers": 0,
            "total_videos": 0,
            "total_engagement": 0,
            "avg_engagement_rate": 0.0
        },
        "line_chart": line_chart,
        "bar_chart": bar_chart,
        "radar_chart": radar_chart,
        "doughnut_chart": doughnut_chart
    }


def generate_account_analytics(account, videos: List) -> Dict[str, Any]:
    """
    Generate detailed analytics for a specific account.

    Args:
        account: Account model instance
        videos: List of video model instances

    Returns:
        Dictionary with account analytics
    """
    # Growth trend (last 30 days)
    growth_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]
    base_followers = max(account.followers - random.randint(1000, 10000), 1000)

    growth_data = []
    for i in range(30):
        # Simulate follower growth
        daily_growth = random.randint(10, 500)
        base_followers += daily_growth
        growth_data.append(base_followers)

    # Video performance
    video_performance = []
    for video in videos[:10]:  # Last 10 videos
        video_performance.append({
            "id": video.id,
            "title": video.title,
            "views": video.views,
            "likes": video.likes,
            "comments": video.comments,
            "engagement_rate": video.engagement_rate,
            "created_at": video.created_at.isoformat()
        })

    # Top performing content
    top_content = sorted(
        video_performance,
        key=lambda x: x["engagement_rate"],
        reverse=True
    )[:5]

    # Engagement breakdown
    total_interactions = account.total_likes + account.total_comments
    engagement_breakdown = {
        "likes": round((account.total_likes / total_interactions * 100) if total_interactions else 0, 2),
        "comments": round((account.total_comments / total_interactions * 100) if total_interactions else 0, 2),
        "shares": round(random.uniform(5, 15), 2),  # Mock shares
    }

    # Best posting times (mock data)
    posting_times = {
        "hours": list(range(24)),
        "engagement": [random.randint(50, 100) for _ in range(24)]
    }

    # Audience demographics (mock data)
    demographics = {
        "age_groups": {
            "13-17": random.randint(10, 25),
            "18-24": random.randint(25, 45),
            "25-34": random.randint(20, 35),
            "35-44": random.randint(10, 20),
            "45+": random.randint(5, 15)
        },
        "top_countries": [
            {"name": "United States", "percentage": random.randint(30, 50)},
            {"name": "United Kingdom", "percentage": random.randint(10, 20)},
            {"name": "Canada", "percentage": random.randint(5, 15)},
            {"name": "Australia", "percentage": random.randint(5, 10)},
            {"name": "Germany", "percentage": random.randint(3, 8)}
        ]
    }

    return {
        "account": {
            "id": account.id,
            "username": account.username,
            "platform": account.platform.value,
            "followers": account.followers,
            "videos_count": account.videos_count,
            "engagement_rate": account.engagement_rate,
            "status": account.status.value
        },
        "growth_trend": {
            "labels": growth_dates,
            "data": growth_data
        },
        "video_performance": video_performance,
        "top_content": top_content,
        "engagement_breakdown": engagement_breakdown,
        "posting_times": posting_times,
        "demographics": demographics
    }
