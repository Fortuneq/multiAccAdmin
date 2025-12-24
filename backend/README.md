# Admin Panel Backend API

Backend API for managing TikTok/Reels/Shorts accounts with video generation capabilities.

## Features

- **Account Management**: CRUD operations for social media accounts
- **Proxy Management**: Configure and test proxy servers
- **Video Management**: Upload and manage video content
- **Video Generator**: Process videos with FFmpeg (audio, filters, subtitles)
- **Analytics**: Dashboard statistics and account analytics
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern async web framework
- **SQLAlchemy 2.x** - ORM for database operations
- **PostgreSQL** - Relational database
- **Alembic** - Database migrations
- **Pydantic v2** - Data validation
- **FFmpeg-python** - Video processing
- **Uvicorn** - ASGI server

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   │   ├── account.py
│   │   ├── proxy.py
│   │   ├── video.py
│   │   └── project.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── account.py
│   │   ├── proxy.py
│   │   └── video.py
│   ├── api/                 # API routers
│   │   ├── accounts.py
│   │   ├── proxies.py
│   │   ├── videos.py
│   │   ├── generator.py
│   │   └── analytics.py
│   ├── services/            # Business logic
│   │   ├── video_generator.py
│   │   └── mock_data.py
│   └── utils/               # Helper functions
│       └── helpers.py
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── requirements.txt         # Python dependencies
├── init_db.py              # Database initialization script
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Installation

### 1. Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher
- FFmpeg (for video processing)

#### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### 2. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL

Create database and user:

```sql
CREATE DATABASE admin_panel;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE admin_panel TO admin;
```

### 5. Configure Environment

Copy `.env.example` to `.env` and update settings:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://admin:admin123@localhost:5432/admin_panel
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

### 6. Initialize Database

Run the initialization script to create tables and sample data:

```bash
python init_db.py
```

This will:
- Create all database tables
- Generate 4 sample proxies
- Generate 10 sample accounts
- Generate sample videos for each account

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using Python directly:

```bash
python -m app.main
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Accounts

- `GET /api/accounts` - List all accounts (with filtering)
- `POST /api/accounts` - Create new account
- `GET /api/accounts/{id}` - Get account details
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

### Proxies

- `GET /api/proxies` - List all proxies
- `POST /api/proxies` - Create new proxy
- `GET /api/proxies/{id}` - Get proxy details
- `PUT /api/proxies/{id}` - Update proxy
- `DELETE /api/proxies/{id}` - Delete proxy
- `POST /api/proxies/{id}/test` - Test proxy connection

### Videos

- `GET /api/videos` - List all videos (with filtering)
- `GET /api/videos/{id}` - Get video details
- `POST /api/videos/upload` - Upload video file
- `DELETE /api/videos/{id}` - Delete video

### Video Generator

- `POST /api/generator/project` - Create video project
- `GET /api/generator/project` - List all projects
- `GET /api/generator/project/{id}` - Get project details
- `PUT /api/generator/project/{id}` - Update project
- `POST /api/generator/project/{id}/process` - Process video
- `POST /api/generator/project/{id}/export` - Export video
- `DELETE /api/generator/project/{id}` - Delete project

### Analytics

- `GET /api/analytics/dashboard` - Dashboard overview
- `GET /api/analytics/stats` - Overall statistics
- `GET /api/analytics/account/{id}` - Account analytics

## Database Migrations

### Create New Migration

```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Video Processing

The video generator supports:

### Filters
- `cinematic` - Cinematic look with vignette
- `bright` - Increased brightness and saturation
- `cyberpunk` - Neon/cyberpunk color grading
- `vintage` - Retro/vintage effect
- `warm` - Warm color temperature
- `cool` - Cool color temperature

### Audio Mixing
- Add background music
- Volume control (0-100%)
- Automatic audio synchronization

### Subtitles
- Text overlay
- Custom styling (standard or unique)
- Positioned at bottom center

### Example Usage

```python
from app.services.video_generator import VideoGenerator

generator = VideoGenerator()

output = generator.composite_video(
    video_path="/path/to/video.mp4",
    audio_path="/path/to/audio.mp3",
    subtitle_text="Amazing content!",
    volume=80,
    filter_type="cinematic",
    uniquify=True
)
```

## Testing

Run tests with pytest:

```bash
pytest
```

With coverage:

```bash
pytest --cov=app tests/
```

## Development

### Code Formatting

```bash
black app/
```

### Linting

```bash
flake8 app/
```

## CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:3000` (React frontend)
- `http://localhost:8000` (API docs)
- `file://` (Local HTML files)

Update `CORS_ORIGINS` in `.env` to add more origins.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://admin:admin123@localhost:5432/admin_panel` |
| `SECRET_KEY` | Secret key for JWT/encryption | `your-secret-key-change-in-production` |
| `UPLOAD_DIR` | Directory for uploaded files | `./uploads` |
| `MAX_UPLOAD_SIZE` | Max file upload size (bytes) | `524288000` (500MB) |
| `DEBUG` | Debug mode | `True` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:8000,file://` |

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list                # macOS

# Test connection
psql -U admin -d admin_panel
```

### FFmpeg Not Found

```bash
# Verify FFmpeg installation
ffmpeg -version

# Add to PATH if needed
export PATH="/usr/local/bin:$PATH"
```

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use strong `SECRET_KEY`
3. Configure proper PostgreSQL credentials
4. Use reverse proxy (Nginx)
5. Enable SSL/TLS
6. Set up monitoring (Sentry, Prometheus)
7. Configure backup strategy

### Docker Deployment (Optional)

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg postgresql-client

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
