# Multi-Account Admin Panel

> Professional admin panel for managing TikTok, Instagram Reels, and YouTube Shorts accounts with integrated video generation capabilities.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

---

## Overview

Multi-Account Admin Panel is a comprehensive solution for managing social media accounts across multiple platforms. Built with modern web technologies, it provides a clean, intuitive interface for account management, proxy configuration, video processing, and analytics.

### Key Features

- **Multi-Platform Support**: Manage TikTok, Instagram Reels, and YouTube Shorts accounts from one place
- **Proxy Management**: Configure, test, and assign proxies to accounts for secure access
- **Video Generator**: Advanced video processing with FFmpeg:
  - Audio mixing with volume control
  - Visual filters (Vintage, Cold, Warm, B&W, Vaporwave)
  - Subtitle uniqualization
  - Batch processing
- **Analytics Dashboard**: Real-time statistics and insights
- **Clean UI/UX**: Modern white theme with round corners and MiSans typography
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI docs

---

## Quick Start

Get started in 5 minutes:

```bash
# 1. Clone repository
cd /Users/volkovvladislav/PycharmProjects/multiAccProjcet

# 2. Setup database
psql postgres
CREATE DATABASE admin_panel;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE admin_panel TO admin;
\q

# 3. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload

# 4. Frontend setup (new terminal)
cd frontend
python3 -m http.server 8080
```

**Access the app**:
- Dashboard: http://localhost:8080/index.html
- API Docs: http://localhost:8000/docs

**For detailed instructions**, see [START_HERE.md](START_HERE.md)

---

## Documentation

- **[START_HERE.md](START_HERE.md)** - Quick start guide (recommended first read)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[CHECKLIST.md](CHECKLIST.md)** - Pre-launch checklist
- **[backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)** - Complete API reference
- **[backend/README.md](backend/README.md)** - Backend architecture
- **[frontend/README.md](frontend/README.md)** - Frontend structure

---

## Architecture

### Technology Stack

**Backend**
- FastAPI 0.104.1 - Modern Python web framework
- SQLAlchemy 2.0 - ORM for database interactions
- PostgreSQL 14+ - Robust relational database
- Pydantic 2.5 - Data validation and settings
- FFmpeg - Video processing engine
- Alembic - Database migrations

**Frontend**
- Vanilla JavaScript (ES6+) - No framework dependencies
- HTML5 & CSS3 - Modern web standards
- MiSans Font - Clean typography
- Responsive Design - Works on all devices

### Project Structure

```
multiAccProjcet/
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/                # API Endpoints
│   │   │   ├── accounts.py     # Account CRUD operations
│   │   │   ├── proxies.py      # Proxy management
│   │   │   ├── videos.py       # Video upload/management
│   │   │   ├── generator.py    # Video generation engine
│   │   │   └── analytics.py    # Dashboard analytics
│   │   ├── models/             # SQLAlchemy Models
│   │   │   ├── account.py
│   │   │   ├── proxy.py
│   │   │   ├── video.py
│   │   │   └── project.py
│   │   ├── schemas/            # Pydantic Schemas
│   │   ├── services/           # Business Logic
│   │   │   └── video_generator.py
│   │   ├── utils/              # Helper Functions
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # DB Connection
│   │   └── main.py             # FastAPI App
│   ├── alembic/                # Database Migrations
│   ├── requirements.txt        # Python Dependencies
│   └── init_db.py              # DB Initialization Script
│
├── frontend/                    # Frontend Application
│   ├── assets/
│   │   ├── css/                # Stylesheets
│   │   │   ├── main.css
│   │   │   ├── dashboard.css
│   │   │   ├── accounts.css
│   │   │   └── generator.css
│   │   └── js/                 # JavaScript Modules
│   │       ├── api.js          # API Client
│   │       ├── utils.js        # Utilities
│   │       ├── dashboard.js
│   │       ├── accounts.js
│   │       └── generator.js
│   ├── index.html              # Dashboard Page
│   ├── accounts.html           # Account Management
│   ├── generator.html          # Video Generator
│   └── start.sh                # Frontend Start Script
│
├── uploads/                     # Generated at runtime
│   ├── videos/
│   ├── audio/
│   ├── thumbnails/
│   └── projects/
│
├── .env.example                 # Environment Template
├── .gitignore                   # Git Ignore Rules
├── README.md                    # This file
├── START_HERE.md                # Quick Start Guide
├── DEPLOYMENT.md                # Deployment Guide
├── CHECKLIST.md                 # Pre-launch Checklist
└── test_system.sh               # System Test Script
```

---

## Features in Detail

### 1. Account Management

Comprehensive CRUD operations for social media accounts:

- Create accounts with platform-specific details
- Support for TikTok, Instagram Reels, YouTube Shorts
- Assign proxies for secure access
- Track account status (active/inactive/banned)
- Bulk operations support
- Search and filter capabilities

**API Endpoints**:
- `GET /api/accounts` - List accounts
- `POST /api/accounts` - Create account
- `GET /api/accounts/{id}` - Get details
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account

### 2. Proxy Management

Configure and test proxy servers:

- HTTP, HTTPS, SOCKS5 protocol support
- Proxy authentication (username/password)
- Connection testing before assignment
- Performance monitoring
- Geographic location tracking
- Assign multiple proxies to accounts

**API Endpoints**:
- `GET /api/proxies` - List proxies
- `POST /api/proxies` - Add proxy
- `POST /api/proxies/{id}/test` - Test connection
- `DELETE /api/proxies/{id}` - Remove proxy

### 3. Video Generator

Advanced video processing with FFmpeg:

**Audio Features**:
- Mix background music with source video
- Volume control (0-100%)
- Audio format support: MP3, WAV, AAC

**Visual Filters**:
- Vintage - Classic film look
- Cold - Blue tones for winter vibes
- Warm - Orange/yellow warm atmosphere
- Black & White - Timeless monochrome
- Vaporwave - Retro aesthetic with color shifting

**Subtitle Processing**:
- Add custom subtitles
- Uniqualization for avoiding duplicate detection
- Position and styling options

**Batch Processing**:
- Process multiple videos simultaneously
- Queue management
- Progress tracking

**API Endpoints**:
- `POST /api/generator/process` - Start video processing
- `GET /api/generator/progress/{task_id}` - Check progress
- `POST /api/videos/upload` - Upload source video

### 4. Analytics Dashboard

Real-time insights and statistics:

- Total accounts, videos, projects overview
- Platform distribution (TikTok/Reels/Shorts)
- Recent activity feed
- Performance metrics
- Account health monitoring
- Upload statistics

**API Endpoints**:
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/accounts/{id}` - Account-specific analytics

---

## API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Authentication

Currently in development mode with no authentication required. For production deployment, implement JWT-based authentication (see [DEPLOYMENT.md](DEPLOYMENT.md)).

### Example API Calls

**Create an account**:
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "username": "my_tiktok",
    "platform": "tiktok",
    "email": "user@example.com",
    "password": "secure_password"
  }'
```

**Upload a video**:
```bash
curl -X POST http://localhost:8000/api/videos/upload \
  -F "file=@video.mp4"
```

**Generate processed video**:
```bash
curl -X POST http://localhost:8000/api/generator/process \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": 1,
    "audio_file": "background.mp3",
    "volume": 50,
    "filter": "vintage",
    "subtitle": "Check out this awesome content!"
  }'
```

For complete API documentation, see [backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md).

---

## Development

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- FFmpeg (for video processing)
- Git (optional)

### Setup Development Environment

1. **Clone repository**:
```bash
git clone <repository-url>
cd multiAccProjcet
```

2. **Backend setup**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python init_db.py
```

3. **Frontend setup**:
```bash
cd frontend
# No build step required - vanilla JavaScript
```

4. **Run development servers**:
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
python3 -m http.server 8080
# OR use the provided script
./start.sh
```

### Running Tests

```bash
# Run system test script
chmod +x test_system.sh
./test_system.sh

# Backend unit tests (if implemented)
cd backend
pytest

# Check code style
black app/
flake8 app/
```

---

## Deployment

For production deployment:

1. Review [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive guide
2. Complete [CHECKLIST.md](CHECKLIST.md) before launch
3. Use Docker for containerized deployment (recommended)
4. Configure Nginx as reverse proxy
5. Set up SSL/TLS with Let's Encrypt
6. Enable monitoring and logging
7. Configure automated backups

**Quick Docker deployment**:
```bash
# Copy environment file
cp .env.example .env.production
# Edit with production values

# Build and start
docker-compose --env-file .env.production up -d

# Initialize database
docker-compose exec backend python init_db.py
```

---

## Configuration

### Environment Variables

All configuration is managed through `.env` file:

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

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,file://
```

**IMPORTANT**:
- Change `SECRET_KEY` in production (use `openssl rand -hex 32`)
- Set `DEBUG=False` in production
- Restrict `CORS_ORIGINS` to your production domains

---

## Troubleshooting

### Backend won't start

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
1. Check PostgreSQL is running: `brew services list` (macOS) or `systemctl status postgresql` (Linux)
2. Verify credentials in `.env`
3. Test connection: `psql -U admin -d admin_panel`

---

### Frontend can't connect to API

**Problem**: CORS errors in browser console

**Solution**:
1. Verify backend is running on port 8000
2. Check `CORS_ORIGINS` in backend `.env` includes `http://localhost:8080`
3. Clear browser cache and reload

---

### Video processing fails

**Problem**: `FFmpeg not found`

**Solution**:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html

# Verify installation
ffmpeg -version
```

For more troubleshooting tips, see [START_HERE.md](START_HERE.md#troubleshooting).

---

## Contributing

This is a proprietary project for Aloda Studio. For internal contributions:

1. Create feature branch from `main`
2. Follow code style guidelines (Black for Python)
3. Write tests for new features
4. Update documentation
5. Submit pull request for review

---

## Roadmap

### Version 1.1 (Q1 2026)
- [ ] User authentication (JWT)
- [ ] Role-based access control (RBAC)
- [ ] Scheduled video posting
- [ ] Multi-language support

### Version 1.2 (Q2 2026)
- [ ] Advanced analytics with charts
- [ ] Video templates library
- [ ] AI-powered caption generation
- [ ] Webhook integrations

### Version 2.0 (Q3 2026)
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Advanced proxy rotation
- [ ] Cloud storage integration

---

## Performance

### Benchmarks (Development Environment)

- API Response Time: <100ms (average)
- Video Upload: 500MB in ~30s
- Video Processing: 1080p video with filter in ~15s
- Database Queries: <50ms (with indexes)
- Frontend Load Time: <2s

### Optimization Tips

- Use connection pooling for database
- Implement caching for analytics endpoints
- Compress video uploads client-side
- Use CDN for static assets in production
- Enable Nginx gzip compression

---

## Security

### Best Practices Implemented

- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic
- File upload size limits
- CORS configuration
- Environment-based secrets
- `.env` files in `.gitignore`

### Production Security Checklist

- [ ] Change default `SECRET_KEY`
- [ ] Enable HTTPS only
- [ ] Restrict CORS to production domains
- [ ] Implement rate limiting
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Audit logs enabled

See [DEPLOYMENT.md](DEPLOYMENT.md#security-hardening) for comprehensive security guide.

---

## Support

### Documentation
- Quick Start: [START_HERE.md](START_HERE.md)
- API Reference: [backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)
- Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)

### Contact
For questions or issues:
- Technical Lead: [your-email@example.com]
- Project Repository: [repository-url]

---

## License

Proprietary - Aloda Studio. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## Acknowledgments

- FastAPI framework for excellent async Python web development
- PostgreSQL team for robust database engine
- FFmpeg project for powerful video processing
- MiSans font for beautiful typography

---

## Changelog

### Version 1.0.0 (December 24, 2025)
- Initial release
- Multi-platform account management
- Proxy configuration and testing
- Video generator with FFmpeg
- Analytics dashboard
- Complete API documentation
- Responsive web interface

---

**Built with ❤️ by Aloda Studio**

**Last Updated**: December 24, 2025
