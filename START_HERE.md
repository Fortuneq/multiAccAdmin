# Multi-Account Admin Panel - Quick Start Guide

## What is this?

A comprehensive admin panel for managing multiple TikTok/Instagram Reels/YouTube Shorts accounts with an integrated video generator. Built with FastAPI (backend) and vanilla JavaScript (frontend), featuring proxy management, video processing with FFmpeg, and real-time analytics.

## Key Features

- Account Management (TikTok/Reels/Shorts)
- Proxy Configuration & Testing
- Video Generator with FFmpeg
  - Audio mixing with volume control
  - Visual filters and effects
  - Subtitle uniqualization
  - Batch processing
- Analytics Dashboard
- File upload management

## Technology Stack

- **Backend**: FastAPI 0.104.1, PostgreSQL, SQLAlchemy 2.0
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Video Processing**: FFmpeg
- **Database**: PostgreSQL 14+

---

## Quick Start (5 Minutes)

### Prerequisites

Before starting, ensure you have:

- Python 3.10+ installed
- PostgreSQL 14+ installed and running
- FFmpeg installed (for video processing)
- Git (optional, for version control)

### Step 1: Install PostgreSQL

#### macOS (Homebrew)
```bash
brew install postgresql@14
brew services start postgresql@14
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Windows
Download and install from: https://www.postgresql.org/download/windows/

### Step 2: Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE admin_panel;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE admin_panel TO admin;
\q
```

### Step 3: Backend Setup

```bash
# Navigate to project directory
cd /Users/volkovvladislav/PycharmProjects/multiAccProjcet/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env if needed (optional)
# nano .env

# Initialize database
python init_db.py

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will start at: **http://localhost:8000**

### Step 4: Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd /Users/volkovvladislav/PycharmProjects/multiAccProjcet/frontend

# Option 1: Use provided script
chmod +x start.sh
./start.sh

# Option 2: Python HTTP server
python3 -m http.server 8080

# Option 3: Node.js http-server (if installed)
npx http-server -p 8080
```

Frontend will start at: **http://localhost:8080**

### Step 5: Access the Application

Open your browser and navigate to:

- **Dashboard**: http://localhost:8080/index.html
- **Account Management**: http://localhost:8080/accounts.html
- **Video Generator**: http://localhost:8080/generator.html
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## Project Structure

```
multiAccProjcet/
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/                # API endpoints
│   │   │   ├── accounts.py     # Account CRUD
│   │   │   ├── proxies.py      # Proxy management
│   │   │   ├── videos.py       # Video management
│   │   │   ├── generator.py    # Video generation
│   │   │   └── analytics.py    # Dashboard stats
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   │   └── video_generator.py
│   │   ├── utils/              # Helper functions
│   │   ├── config.py           # App configuration
│   │   ├── database.py         # DB connection
│   │   └── main.py             # FastAPI app
│   ├── alembic/                # Database migrations
│   ├── requirements.txt        # Python dependencies
│   ├── init_db.py              # DB initialization
│   └── .env.example            # Environment template
│
├── frontend/                    # Vanilla JS Frontend
│   ├── assets/
│   │   ├── css/                # Stylesheets
│   │   │   ├── main.css        # Global styles
│   │   │   ├── dashboard.css
│   │   │   ├── accounts.css
│   │   │   └── generator.css
│   │   └── js/                 # JavaScript modules
│   │       ├── api.js          # API client
│   │       ├── utils.js        # Utilities
│   │       ├── dashboard.js
│   │       ├── accounts.js
│   │       └── generator.js
│   ├── index.html              # Dashboard page
│   ├── accounts.html           # Account management
│   ├── generator.html          # Video generator
│   └── start.sh                # Frontend startup script
│
├── uploads/                     # Generated at runtime
│   ├── videos/
│   ├── audio/
│   ├── thumbnails/
│   └── projects/
│
├── .env.example                 # Root environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # Main documentation
├── START_HERE.md                # This file
├── DEPLOYMENT.md                # Production deployment guide
└── CHECKLIST.md                 # Pre-launch checklist
```

---

## Environment Variables

All configuration is managed through `.env` files:

```env
# Database
DATABASE_URL=postgresql://admin:admin123@localhost:5432/admin_panel

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=524288000  # 500MB

# Application
APP_NAME=Admin Panel API
APP_VERSION=1.0.0
DEBUG=True

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,file://
```

**IMPORTANT**: Change `SECRET_KEY` in production!

---

## Core Functionality

### 1. Account Management
- Add/Edit/Delete accounts
- Support for TikTok, Instagram Reels, YouTube Shorts
- Proxy assignment per account
- Status tracking (active/inactive/banned)

### 2. Proxy Management
- Add proxies with authentication
- Test proxy connectivity
- Assign proxies to accounts
- Protocol support: HTTP, HTTPS, SOCKS5

### 3. Video Generator
- Upload source videos
- Add background music with volume control
- Apply visual filters (Vintage, Cold, Warm, B&W, Vaporwave)
- Subtitle uniqualization
- Batch processing support
- Real-time progress tracking

### 4. Analytics Dashboard
- Total accounts/videos/projects overview
- Platform distribution charts
- Recent activity feed
- Quick action buttons

---

## API Endpoints

### Accounts
- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Create account
- `GET /api/accounts/{id}` - Get account details
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

### Proxies
- `GET /api/proxies` - List all proxies
- `POST /api/proxies` - Create proxy
- `POST /api/proxies/{id}/test` - Test proxy
- `DELETE /api/proxies/{id}` - Delete proxy

### Videos
- `GET /api/videos` - List all videos
- `POST /api/videos/upload` - Upload video
- `DELETE /api/videos/{id}` - Delete video

### Generator
- `POST /api/generator/process` - Process video
- `GET /api/generator/progress/{task_id}` - Check progress

### Analytics
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/accounts/{id}` - Account analytics

Full API documentation: http://localhost:8000/docs

---

## Testing the System

### Manual Testing

1. **Backend Health Check**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.0"}
```

2. **Create Test Account**
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "platform": "tiktok",
    "email": "test@example.com",
    "password": "password123"
  }'
```

3. **Check Dashboard Stats**
```bash
curl http://localhost:8000/api/analytics/dashboard
```

### Automated Testing

Run the test script (see CHECKLIST.md):
```bash
chmod +x test_system.sh
./test_system.sh
```

---

## Troubleshooting

### Backend won't start

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
- Check PostgreSQL is running: `brew services list` (macOS)
- Verify credentials in `.env`
- Test connection: `psql -U admin -d admin_panel`

---

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

---

### Frontend won't connect to API

**Error**: `Failed to fetch` or CORS errors

**Solution**:
- Verify backend is running on port 8000
- Check CORS_ORIGINS in `.env` includes `http://localhost:8080`
- Clear browser cache and reload

---

### Video generation fails

**Error**: `FFmpeg not found`

**Solution**:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

---

### Database initialization fails

**Error**: `database "admin_panel" does not exist`

**Solution**:
```bash
# Recreate database
psql postgres
DROP DATABASE IF EXISTS admin_panel;
CREATE DATABASE admin_panel;
GRANT ALL PRIVILEGES ON DATABASE admin_panel TO admin;
\q

# Reinitialize
python init_db.py
```

---

## Next Steps

1. Review full documentation in `README.md`
2. Check deployment guide in `DEPLOYMENT.md`
3. Complete pre-launch checklist in `CHECKLIST.md`
4. Explore API documentation at http://localhost:8000/docs
5. Customize design in `frontend/assets/css/`

---

## Support & Documentation

- Main README: `README.md`
- API Documentation: `backend/API_DOCUMENTATION.md`
- Backend Guide: `backend/README.md`
- Frontend Guide: `frontend/README.md`
- Deployment: `DEPLOYMENT.md`

---

## License

Proprietary - Aloda Studio

---

**Last Updated**: December 24, 2025
**Version**: 1.0.0
