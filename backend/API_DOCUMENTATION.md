# API Documentation

Complete API reference for the Admin Panel Backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (development mode).

---

## Accounts API

### List Accounts

```http
GET /api/accounts
```

**Query Parameters:**
- `platform` (optional): Filter by platform (TikTok/Reels/Shorts)
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Max records to return (default: 100, max: 500)

**Response:**
```json
[
  {
    "id": 1,
    "username": "@creative_master_1234",
    "platform": "TikTok",
    "region": "US",
    "followers": 125000,
    "videos_count": 45,
    "total_likes": 2500000,
    "total_comments": 125000,
    "engagement_rate": 4.5,
    "avg_likes_per_video": 55555.56,
    "status": "online",
    "proxy_id": 1,
    "last_activity": "2024-12-24T10:30:00Z",
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-24T10:30:00Z"
  }
]
```

### Create Account

```http
POST /api/accounts
```

**Request Body:**
```json
{
  "username": "creative_user",
  "platform": "TikTok",
  "region": "US",
  "status": "online",
  "proxy_id": 1,
  "followers": 1000,
  "videos_count": 5,
  "total_likes": 5000,
  "total_comments": 500
}
```

**Response:** Account object (201 Created)

### Get Account

```http
GET /api/accounts/{account_id}
```

**Response:** Account object

### Update Account

```http
PUT /api/accounts/{account_id}
```

**Request Body:** Partial account data (all fields optional)

### Delete Account

```http
DELETE /api/accounts/{account_id}
```

**Response:** 204 No Content

---

## Proxies API

### List Proxies

```http
GET /api/proxies
```

**Query Parameters:**
- `skip` (optional): Pagination offset
- `limit` (optional): Max records
- `active_only` (optional): Filter active proxies only

**Response:**
```json
[
  {
    "id": 1,
    "proxy_type": "SOCKS5",
    "address": "proxy1.example.com",
    "port": 1080,
    "username": "user1",
    "password": "pass1",
    "is_active": true,
    "last_tested": "2024-12-24T10:00:00Z",
    "created_at": "2024-12-01T10:00:00Z",
    "full_address": "socks5://user1:pass1@proxy1.example.com:1080"
  }
]
```

### Create Proxy

```http
POST /api/proxies
```

**Request Body:**
```json
{
  "proxy_type": "SOCKS5",
  "address": "proxy.example.com",
  "port": 1080,
  "username": "user",
  "password": "pass",
  "is_active": true
}
```

### Update Proxy

```http
PUT /api/proxies/{proxy_id}
```

### Delete Proxy

```http
DELETE /api/proxies/{proxy_id}
```

### Test Proxy

```http
POST /api/proxies/{proxy_id}/test
```

**Response:**
```json
{
  "success": true,
  "message": "Proxy connection successful",
  "response_time": 0.234,
  "tested_at": "2024-12-24T10:00:00Z"
}
```

---

## Videos API

### List Videos

```http
GET /api/videos
```

**Query Parameters:**
- `account_id` (optional): Filter by account
- `skip` (optional): Pagination offset
- `limit` (optional): Max records

**Response:**
```json
[
  {
    "id": 1,
    "title": "Amazing Video",
    "file_path": "/uploads/videos/video_123.mp4",
    "thumbnail_path": "/uploads/thumbnails/thumb_123.jpg",
    "duration": 45.5,
    "size": 15728640,
    "size_mb": 15.0,
    "duration_formatted": "00:45",
    "views": 50000,
    "likes": 5000,
    "comments": 250,
    "engagement_rate": 10.5,
    "platform": "TikTok",
    "account_id": 1,
    "upload_date": "2024-12-20T10:00:00Z",
    "created_at": "2024-12-20T10:00:00Z"
  }
]
```

### Get Video

```http
GET /api/videos/{video_id}
```

### Upload Video

```http
POST /api/videos/upload
```

**Request:**
- Content-Type: `multipart/form-data`
- File field: `file`
- Query params: `title`, `account_id` (optional), `platform` (optional)

**Response:** Video object (201 Created)

### Delete Video

```http
DELETE /api/videos/{video_id}?delete_file=true
```

---

## Video Generator API

### Create Project

```http
POST /api/generator/project
```

**Request Body:**
```json
{
  "name": "My Video Project",
  "video_track_path": "/uploads/videos/source.mp4",
  "audio_track_path": "/uploads/audio/music.mp3",
  "subtitle_text": "Amazing content!",
  "audio_volume": 80,
  "filter_type": "cinematic",
  "uniquify_subtitles": true,
  "account_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "name": "My Video Project",
  "status": "draft",
  "video_track_path": "/uploads/videos/source.mp4",
  "audio_track_path": "/uploads/audio/music.mp3",
  "subtitle_text": "Amazing content!",
  "audio_volume": 80,
  "filter_type": "cinematic",
  "uniquify_subtitles": true,
  "account_id": 1,
  "output_path": null,
  "error_message": null,
  "is_processable": true,
  "is_completed": false,
  "created_at": "2024-12-24T10:00:00Z",
  "updated_at": "2024-12-24T10:00:00Z"
}
```

### List Projects

```http
GET /api/generator/project
```

### Get Project

```http
GET /api/generator/project/{project_id}
```

### Update Project

```http
PUT /api/generator/project/{project_id}
```

**Request Body:** Partial project data (all optional)

### Process Project

```http
POST /api/generator/project/{project_id}/process
```

**Response:**
```json
{
  "success": true,
  "message": "Video processing started",
  "project_id": 1
}
```

Processing happens in background. Check project status via GET request.

### Export Project

```http
POST /api/generator/project/{project_id}/export
```

**Response:**
```json
{
  "success": true,
  "message": "Video ready for export",
  "project_id": 1,
  "output_path": "/uploads/projects/video_20241224_123456_abc123.mp4"
}
```

### Delete Project

```http
DELETE /api/generator/project/{project_id}
```

---

## Analytics API

### Dashboard

```http
GET /api/analytics/dashboard
```

**Response:**
```json
{
  "overview": {
    "total_accounts": 10,
    "active_accounts": 7,
    "total_followers": 2500000,
    "total_videos": 450,
    "total_engagement": 125000,
    "avg_engagement_rate": 4.5
  },
  "line_chart": {
    "labels": ["2024-12-18", "2024-12-19", "2024-12-20", ...],
    "datasets": [
      {
        "label": "Likes",
        "data": [15000, 18000, 20000, ...],
        "borderColor": "#3b82f6",
        "backgroundColor": "rgba(59, 130, 246, 0.1)"
      },
      {
        "label": "Comments",
        "data": [1500, 1800, 2000, ...],
        "borderColor": "#10b981",
        "backgroundColor": "rgba(16, 185, 129, 0.1)"
      }
    ]
  },
  "bar_chart": {
    "labels": ["TikTok", "Reels", "Shorts"],
    "datasets": [
      {
        "label": "Accounts",
        "data": [25, 35, 20],
        "backgroundColor": ["#3b82f6", "#10b981", "#f59e0b"]
      }
    ]
  },
  "radar_chart": {
    "labels": ["Engagement", "Reach", "Growth", "Quality", "Consistency"],
    "datasets": [
      {
        "label": "Current Period",
        "data": [85, 78, 92, 88, 75],
        "backgroundColor": "rgba(59, 130, 246, 0.2)",
        "borderColor": "#3b82f6"
      }
    ]
  }
}
```

### Overall Stats

```http
GET /api/analytics/stats
```

**Response:**
```json
{
  "total_accounts": 10,
  "active_accounts": 7,
  "total_followers": 2500000,
  "total_videos": 450,
  "total_engagement": 125000,
  "avg_engagement_rate": 4.5
}
```

### Account Analytics

```http
GET /api/analytics/account/{account_id}
```

**Response:**
```json
{
  "account": {
    "id": 1,
    "username": "@creative_master_1234",
    "platform": "TikTok",
    "followers": 125000,
    "videos_count": 45,
    "engagement_rate": 4.5,
    "status": "online"
  },
  "growth_trend": {
    "labels": ["2024-11-24", "2024-11-25", ...],
    "data": [120000, 120500, 121000, ...]
  },
  "video_performance": [
    {
      "id": 1,
      "title": "Video 1",
      "views": 50000,
      "likes": 5000,
      "comments": 250,
      "engagement_rate": 10.5,
      "created_at": "2024-12-20T10:00:00Z"
    }
  ],
  "top_content": [...],
  "engagement_breakdown": {
    "likes": 75.2,
    "comments": 15.8,
    "shares": 9.0
  },
  "posting_times": {
    "hours": [0, 1, 2, ..., 23],
    "engagement": [50, 45, 40, ..., 95]
  },
  "demographics": {
    "age_groups": {
      "13-17": 15,
      "18-24": 45,
      "25-34": 30,
      "35-44": 8,
      "45+": 2
    },
    "top_countries": [
      {"name": "United States", "percentage": 45},
      {"name": "United Kingdom", "percentage": 15}
    ]
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already exists"
}
```

### 404 Not Found
```json
{
  "detail": "Account with ID 123 not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "Error details (if DEBUG=True)"
}
```

---

## Video Filters

Available filter types for video processing:

- `none` - No filter
- `cinematic` - Cinematic look with vignette
- `bright` - Increased brightness and saturation
- `cyberpunk` - Neon/cyberpunk color grading
- `vintage` - Retro/vintage effect
- `warm` - Warm color temperature
- `cool` - Cool color temperature

---

## Platform Types

- `TikTok`
- `Reels`
- `Shorts`

## Account Status Types

- `online` - Active and operational
- `offline` - Inactive
- `suspended` - Temporarily suspended
- `pending` - Pending verification

## Proxy Types

- `SOCKS5`
- `HTTP`
- `HTTPS`

## Project Status Types

- `draft` - Not yet processed
- `processing` - Currently being processed
- `completed` - Successfully completed
- `failed` - Processing failed

---

## Rate Limits

Currently no rate limits (development mode).

## Pagination

Default pagination:
- `skip`: 0
- `limit`: 100 (max: 500)

---

## WebSocket Support

Not currently implemented. All operations are REST-based.

---

For interactive API testing, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
