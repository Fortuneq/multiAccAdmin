# Quick Start Guide

Get the backend running in 5 minutes.

## Prerequisites

- Python 3.10+
- PostgreSQL
- FFmpeg

## Step 1: Install PostgreSQL

### macOS
```bash
brew install postgresql
brew services start postgresql
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

## Step 2: Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Run these commands in psql:
CREATE DATABASE admin_panel;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE admin_panel TO admin;
\q
```

## Step 3: Install FFmpeg

### macOS
```bash
brew install ffmpeg
```

### Ubuntu/Debian
```bash
sudo apt install ffmpeg
```

### Windows
Download from https://ffmpeg.org/download.html

## Step 4: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Initialize Database

```bash
# Run initialization script
python init_db.py
```

This creates:
- All database tables
- 4 sample proxies
- 10 sample accounts with realistic data
- Sample videos for each account

## Step 6: Start Server

```bash
# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 7: Access API

Open your browser:

- **API Root**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Test the API

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Try the `/api/accounts` endpoint
3. Click "Try it out" → "Execute"
4. See the sample accounts

### Using curl

```bash
# Get all accounts
curl http://localhost:8000/api/accounts

# Get dashboard analytics
curl http://localhost:8000/api/analytics/dashboard

# Health check
curl http://localhost:8000/health
```

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Test connection
psql -U admin -d admin_panel
```

### Port 8000 Already in Use

```bash
# Find process
lsof -i:8000

# Kill process
kill -9 <PID>
```

### FFmpeg Not Found

```bash
# Verify installation
ffmpeg -version

# Add to PATH
export PATH="/usr/local/bin:$PATH"
```

## Next Steps

- Explore API documentation at http://localhost:8000/docs
- Create your own accounts via POST /api/accounts
- Upload videos via POST /api/videos/upload
- Create video projects via POST /api/generator/project
- View analytics at /api/analytics/dashboard

## Configuration

Edit `backend/.env` to customize:

- Database connection
- Upload directory
- CORS origins
- Debug mode

## Development Commands

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Format code
black app/

# Run tests
pytest
```

## Default Credentials

Database:
- **Host**: localhost
- **Port**: 5432
- **Database**: admin_panel
- **User**: admin
- **Password**: admin123

API:
- **URL**: http://localhost:8000
- **Auth**: None (development mode)

Enjoy building with the Admin Panel API!
