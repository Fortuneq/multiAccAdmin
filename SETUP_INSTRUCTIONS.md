# Multi-Account Admin Panel - Setup Instructions

Complete setup guide for running the full-stack application: FastAPI backend + Vanilla JS frontend.

## Quick Start

### 1. Start Backend (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

### 2. Start Frontend (Terminal 2)

```bash
cd frontend
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd frontend
python3 -m http.server 8080
```

Frontend will be available at: **http://localhost:8080**

### 3. Access the Application

Open your browser:

- **Dashboard**: http://localhost:8080/index.html
- **Accounts**: http://localhost:8080/accounts.html
- **Generator**: http://localhost:8080/generator.html
- **API Docs**: http://localhost:8000/docs

## Project Structure

```
multiAccProjcet/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints (accounts, proxies, videos, generator, analytics)
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic (video generation, FFmpeg)
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── database.py        # Database configuration
│   │   └── config.py          # App configuration
│   ├── uploads/               # Uploaded files directory
│   ├── processed/             # Processed videos directory
│   ├── init_db.py             # Database initialization
│   └── requirements.txt       # Python dependencies
│
└── frontend/                   # Vanilla JS frontend
    ├── index.html             # Analytics Dashboard
    ├── accounts.html          # Account Management
    ├── generator.html         # Video Generator
    ├── assets/
    │   ├── css/               # Stylesheets
    │   │   ├── main.css       # Shared styles
    │   │   ├── dashboard.css  # Dashboard styles
    │   │   ├── accounts.css   # Accounts styles
    │   │   └── generator.css  # Generator styles
    │   └── js/                # JavaScript files
    │       ├── api.js         # API client
    │       ├── utils.js       # Utility functions
    │       ├── dashboard.js   # Dashboard logic
    │       ├── accounts.js    # Accounts logic
    │       └── generator.js   # Generator logic
    ├── start.sh               # Frontend startup script
    └── README.md              # Frontend documentation
```

## Features

### Analytics Dashboard
- Overview cards (accounts, videos, engagement)
- Platform distribution charts
- Engagement trends
- Top performing videos table
- Export to CSV
- Auto-refresh every 30 seconds

### Account Management
- CRUD operations for social media accounts
- Platform filtering (TikTok/Reels/Shorts)
- Search functionality
- Account statistics
- Proxy configuration
- Real-time status indicators

### Video Generator
- Video & audio upload (drag & drop)
- Preview area (360x640 mobile format)
- Timeline with 3 tracks
- Audio volume control
- Video filters
- Subtitle editor with uniquification
- Target account selection
- FFmpeg video processing

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
- `PUT /api/proxies/{id}` - Update proxy
- `DELETE /api/proxies/{id}` - Delete proxy
- `POST /api/proxies/{id}/test` - Test proxy connection

### Videos
- `GET /api/videos` - List all videos
- `POST /api/videos/upload` - Upload video file
- `GET /api/videos/{id}` - Get video details
- `DELETE /api/videos/{id}` - Delete video

### Video Generator
- `GET /api/generator/project` - List all projects
- `POST /api/generator/project` - Create project
- `GET /api/generator/project/{id}` - Get project details
- `PUT /api/generator/project/{id}` - Update project
- `DELETE /api/generator/project/{id}` - Delete project
- `POST /api/generator/project/{id}/process` - Process video
- `POST /api/generator/project/{id}/export` - Export video

### Analytics
- `GET /api/analytics/dashboard` - Get dashboard data
- `GET /api/analytics/stats` - Get overall statistics
- `GET /api/analytics/account/{id}` - Get account analytics

## Configuration

### Backend Configuration (`backend/app/config.py`)

```python
# Database
DATABASE_URL = "sqlite:///./multi_account.db"

# Upload directories
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

# File size limits
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
MAX_AUDIO_SIZE = 10 * 1024 * 1024   # 10MB

# CORS origins
CORS_ORIGINS = ["http://localhost:8080", "*"]
```

### Frontend Configuration (`frontend/assets/js/api.js`)

```javascript
const api = new APIClient('http://localhost:8000');
```

## Development Workflow

### Backend Development

1. Activate virtual environment:
   ```bash
   cd backend
   source venv/bin/activate
   ```

2. Run with auto-reload:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Access API docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Development

1. Start dev server:
   ```bash
   cd frontend
   ./start.sh
   ```

2. Edit files and refresh browser

3. Browser DevTools:
   - Console: JavaScript errors
   - Network: API requests
   - Elements: CSS debugging

## Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Get accounts
curl http://localhost:8000/api/accounts

# Create account
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "@testuser", "platform": "TikTok"}'
```

### Test Frontend

1. Open http://localhost:8080/index.html
2. Check browser console for errors
3. Test each feature:
   - Dashboard loading
   - Account creation
   - Video upload
   - Export functionality

## Database

### Initialize Database

```bash
cd backend
python init_db.py
```

This creates:
- SQLite database: `multi_account.db`
- All required tables
- Sample data (optional)

### Database Schema

**Accounts Table:**
- id, username, platform, status, region
- proxy_id (foreign key)
- followers, videos_count, total_likes, total_comments
- engagement_rate, created_at, updated_at

**Proxies Table:**
- id, type, host, port, username, password
- is_active, last_tested, created_at

**Videos Table:**
- id, account_id, file_path, platform
- views, likes, comments, shares
- uploaded_at

**Projects Table:**
- id, name, account_id, video_path, audio_path
- settings (JSON), status
- created_at, updated_at

## Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

**Error**: `Address already in use`
**Solution**:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Can't Connect to Backend

**Error**: CORS errors in console
**Solution**:
1. Check backend CORS settings
2. Verify backend is running
3. Check API URL in `api.js`

**Error**: 404 Not Found for API calls
**Solution**:
1. Verify backend URL: http://localhost:8000
2. Check API endpoints in docs: http://localhost:8000/docs

### Database Issues

**Error**: Database locked
**Solution**:
```bash
cd backend
rm multi_account.db
python init_db.py
```

### Video Upload Fails

**Error**: File too large
**Solution**: Reduce file size or increase limit in `config.py`

**Error**: FFmpeg not found
**Solution**:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/
```

## Production Deployment

### Backend (FastAPI)

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

Build and deploy static files to:
- Nginx
- Apache
- Vercel
- Netlify
- GitHub Pages

Update API URL in `api.js` to production backend URL.

## Environment Variables

Create `.env` file in backend:

```env
DATABASE_URL=sqlite:///./multi_account.db
DEBUG=True
CORS_ORIGINS=http://localhost:8080,https://your-domain.com
MAX_VIDEO_SIZE=104857600
MAX_AUDIO_SIZE=10485760
```

## Security Checklist

- [ ] Enable HTTPS in production
- [ ] Add authentication (JWT/OAuth)
- [ ] Validate file uploads
- [ ] Sanitize user inputs
- [ ] Rate limiting
- [ ] Secure database credentials
- [ ] Enable CORS only for trusted domains

## Performance Optimization

1. **Backend**:
   - Database indexing
   - Caching (Redis)
   - Background tasks (Celery)
   - CDN for static files

2. **Frontend**:
   - Minify CSS/JS
   - Lazy loading
   - Image optimization
   - Service workers

## Support & Resources

- **Backend Docs**: `/backend/README.md`
- **Frontend Docs**: `/frontend/README.md`
- **API Documentation**: http://localhost:8000/docs
- **Source Code**: Check individual files for inline comments

## License

Proprietary - All rights reserved

---

**Setup Complete!** 🎉

You now have a fully functional multi-account admin panel with:
- ✅ FastAPI backend
- ✅ Vanilla JavaScript frontend
- ✅ Database integration
- ✅ Video processing
- ✅ Analytics dashboard
- ✅ Account management
- ✅ Video generator

Happy coding!
