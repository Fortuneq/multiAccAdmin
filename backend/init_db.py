"""
Database initialization script.
Creates tables and populates with sample data.
"""
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal, init_db
from app.models import Account, Proxy, Video, Platform, AccountStatus, ProxyType
from app.services.mock_data import generate_username, generate_followers, generate_video_stats
import random
from datetime import datetime, timedelta


def create_sample_proxies():
    """Create sample proxy servers."""
    db = SessionLocal()
    try:
        proxies = [
            Proxy(
                proxy_type=ProxyType.SOCKS5,
                address="proxy1.example.com",
                port=1080,
                username="user1",
                password="pass1",
                is_active=True
            ),
            Proxy(
                proxy_type=ProxyType.HTTP,
                address="proxy2.example.com",
                port=8080,
                username="user2",
                password="pass2",
                is_active=True
            ),
            Proxy(
                proxy_type=ProxyType.HTTPS,
                address="proxy3.example.com",
                port=443,
                is_active=True
            ),
            Proxy(
                proxy_type=ProxyType.SOCKS5,
                address="192.168.1.100",
                port=1080,
                is_active=False
            ),
        ]

        db.add_all(proxies)
        db.commit()

        print(f"Created {len(proxies)} sample proxies")
        return proxies

    finally:
        db.close()


def create_sample_accounts(proxies):
    """Create sample social media accounts."""
    db = SessionLocal()
    try:
        platforms = [Platform.TIKTOK, Platform.REELS, Platform.SHORTS]
        regions = ["US", "UK", "CA", "AU", "DE", "FR", "ES", "IT", "JP", "BR"]
        statuses = [AccountStatus.ONLINE, AccountStatus.OFFLINE]

        accounts = []

        for i in range(10):
            platform = random.choice(platforms)
            followers = generate_followers()
            videos_count = random.randint(10, 200)
            stats = generate_video_stats(followers, videos_count)

            # Random last activity within last 7 days
            last_activity = datetime.now() - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23)
            )

            account = Account(
                username=generate_username(),
                platform=platform,
                region=random.choice(regions),
                followers=followers,
                videos_count=videos_count,
                total_likes=stats["total_likes"],
                total_comments=stats["total_comments"],
                status=random.choice(statuses),
                last_activity=last_activity,
                proxy_id=random.choice(proxies).id if random.random() > 0.3 else None
            )

            accounts.append(account)

        db.add_all(accounts)
        db.commit()

        print(f"Created {len(accounts)} sample accounts")
        return accounts

    finally:
        db.close()


def create_sample_videos(accounts):
    """Create sample videos for accounts."""
    db = SessionLocal()
    try:
        videos = []

        for account in accounts:
            # Create 3-8 videos per account
            num_videos = random.randint(3, 8)

            for i in range(num_videos):
                # Generate realistic stats
                views = random.randint(1000, 1000000)
                likes = int(views * random.uniform(0.05, 0.15))
                comments = int(views * random.uniform(0.005, 0.02))

                video = Video(
                    title=f"{account.username} - Video {i+1}",
                    file_path=f"/uploads/videos/sample_{account.id}_{i}.mp4",
                    thumbnail_path=f"/uploads/thumbnails/sample_{account.id}_{i}.jpg",
                    duration=random.uniform(15, 180),  # 15s to 3min
                    size=random.randint(5_000_000, 50_000_000),  # 5-50 MB
                    views=views,
                    likes=likes,
                    comments=comments,
                    platform=account.platform.value,
                    account_id=account.id,
                    upload_date=datetime.now() - timedelta(days=random.randint(1, 60))
                )

                # Calculate engagement rate
                video.calculate_engagement()
                videos.append(video)

        db.add_all(videos)
        db.commit()

        print(f"Created {len(videos)} sample videos")

    finally:
        db.close()


def main():
    """Main initialization function."""
    print("=" * 50)
    print("Database Initialization Script")
    print("=" * 50)

    # Create tables
    print("\n1. Creating database tables...")
    init_db()
    print("   ✓ Tables created successfully")

    # Create sample data
    print("\n2. Creating sample data...")

    print("\n   Creating proxies...")
    proxies = create_sample_proxies()

    print("   Creating accounts...")
    accounts = create_sample_accounts(proxies)

    print("   Creating videos...")
    create_sample_videos(accounts)

    print("\n" + "=" * 50)
    print("Database initialized successfully!")
    print("=" * 50)
    print("\nSample data created:")
    print(f"  - {len(proxies)} proxies")
    print(f"  - {len(accounts)} accounts")
    print(f"  - Videos for all accounts")
    print("\nYou can now start the server with:")
    print("  python -m app.main")
    print("  or")
    print("  uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
