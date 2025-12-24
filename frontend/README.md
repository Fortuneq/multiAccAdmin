# Multi-Account Admin Panel - Frontend

Professional frontend interface for managing TikTok, Instagram Reels, and YouTube Shorts accounts with integrated video generation capabilities.

## Features

- **Analytics Dashboard** - Real-time statistics, performance charts, and top video rankings
- **Account Management** - CRUD operations for social media accounts with proxy configuration
- **Video Generator** - Upload, edit, process videos with audio, filters, and subtitles
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Real-time Updates** - Auto-refresh dashboard data every 30 seconds
- **Toast Notifications** - User-friendly feedback for all actions
- **Export Functionality** - Export data to CSV

## Tech Stack

- **Vanilla JavaScript** - No frameworks, pure ES6+
- **CSS3** - Modern styling with Flexbox and Grid
- **RemixIcon** - Beautiful icon library
- **Fetch API** - RESTful communication with FastAPI backend

## Project Structure

```
frontend/
├── index.html              # Analytics Dashboard page
├── accounts.html           # Account Management page
├── generator.html          # Video Generator page
├── assets/
│   ├── css/
│   │   ├── main.css        # Shared styles (navigation, modals, notifications)
│   │   ├── dashboard.css   # Dashboard-specific styles
│   │   ├── accounts.css    # Accounts page styles
│   │   └── generator.css   # Generator page styles
│   └── js/
│       ├── api.js          # API client for backend communication
│       ├── utils.js        # Utility functions (formatters, notifications, etc.)
│       ├── dashboard.js    # Dashboard page logic
│       ├── accounts.js     # Accounts page logic
│       └── generator.js    # Generator page logic
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

1. **Backend Server Running**
   - FastAPI backend must be running on `http://localhost:8000`
   - See `/backend/README.md` for backend setup

2. **Modern Web Browser**
   - Chrome 90+
   - Firefox 88+
   - Safari 14+
   - Edge 90+

### Quick Start

#### Option 1: Simple HTTP Server (Recommended)

Using Python 3:
```bash
cd frontend
python3 -m http.server 8080
```

Using Node.js:
```bash
cd frontend
npx http-server -p 8080
```

#### Option 2: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

#### Option 3: Direct File Access (Limited functionality)

Open `index.html` directly in browser:
```bash
cd frontend
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

**Note:** CORS restrictions may prevent API calls when opening files directly.

### Access the Application

Once server is running, open your browser:

- **Dashboard**: http://localhost:8080/index.html
- **Accounts**: http://localhost:8080/accounts.html
- **Generator**: http://localhost:8080/generator.html

## Configuration

### API Endpoint

The API endpoint is configured in `assets/js/api.js`:

```javascript
const api = new APIClient('http://localhost:8000');
```

To change the backend URL, edit line 330 in `api.js`:

```javascript
const api = new APIClient('http://your-backend-url:port');
```

### Auto-Refresh Interval

Dashboard auto-refreshes every 30 seconds. To change this, edit `dashboard.js`:

```javascript
startAutoRefresh(loadDashboard, 30000); // Change 30000 to desired milliseconds
```

## Page Features

### 1. Analytics Dashboard (`index.html`)

**Features:**
- Overview cards showing total accounts, active accounts, videos, and engagement
- Platform distribution chart
- Engagement trend visualization
- Top performing videos table
- Export to CSV functionality
- Auto-refresh every 30 seconds

**Key Functions:**
- `loadDashboard()` - Load all dashboard data
- `updateOverviewCards(data)` - Update metric cards
- `loadTopVideos()` - Load and display top videos
- `exportVideos()` - Export data to CSV

### 2. Account Management (`accounts.html`)

**Features:**
- Grid view of all accounts with platform icons
- Filter by platform (TikTok/Reels/Shorts)
- Search by username
- Account details panel with statistics
- Proxy configuration
- Add/Edit/Delete accounts
- Real-time status indicators

**Key Functions:**
- `loadAccounts()` - Fetch accounts from API
- `filterByPlatform(platform)` - Filter accounts
- `showAccountDetails(id)` - Display account info
- `createAccount()` - Add new account
- `deleteAccount(id)` - Remove account

### 3. Video Generator (`generator.html`)

**Features:**
- Video preview area (360x640 mobile format)
- Drag & drop file upload
- Timeline with 3 tracks (Video/Audio/Subtitles)
- Audio volume control
- Video filter selection
- Subtitle editor with uniquification
- Target account selection
- Export to processed video

**Key Functions:**
- `handleVideoUpload()` - Upload and preview video
- `handleAudioUpload()` - Upload audio track
- `exportVideo()` - Process and export final video
- `collectSettings()` - Gather all editing settings

## API Integration

All API calls are handled through the `APIClient` class in `api.js`:

```javascript
// Get dashboard data
const data = await api.getDashboard();

// Get accounts
const accounts = await api.getAccounts();

// Create account
await api.createAccount({ username: '@example', platform: 'TikTok' });

// Upload video
await api.uploadVideo(file);

// Process video
await api.processVideo(projectId, settings);
```

## Error Handling

The application includes comprehensive error handling:

- **Network Errors**: Displayed via toast notifications
- **Validation Errors**: Form field highlighting
- **API Errors**: User-friendly error messages
- **Console Logging**: Detailed error logs for debugging

## Notifications

Toast notifications appear in the top-right corner:

```javascript
showNotification('Success message', 'success');
showNotification('Warning message', 'warning');
showNotification('Error message', 'error');
showNotification('Info message', 'info');
```

## Utility Functions

Available in `utils.js`:

- `formatNumber(num)` - Format with K/M suffix
- `formatDate(date)` - Relative time (e.g., "2 mins ago")
- `formatEngagement(rate)` - Percentage formatting
- `showModal(title, content, buttons)` - Display modal dialogs
- `showLoader(message)` - Show loading overlay
- `hideLoader()` - Hide loading overlay
- `copyToClipboard(text)` - Copy text to clipboard

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Fetch API | ✅ | ✅ | ✅ | ✅ |
| ES6+ | ✅ | ✅ | ✅ | ✅ |
| CSS Grid | ✅ | ✅ | ✅ | ✅ |
| File API | ✅ | ✅ | ✅ | ✅ |

## Development

### Modifying Styles

1. **Shared styles**: Edit `assets/css/main.css`
2. **Page-specific**: Edit respective CSS files
3. **Colors**: Primary color `#0066FF` can be changed globally

### Adding New Features

1. Add UI to HTML file
2. Create JavaScript function
3. Add API call if needed
4. Update this README

### Debugging

Enable console logging:
```javascript
console.log('Debug info:', data);
```

Use browser DevTools:
- Network tab for API calls
- Console tab for JavaScript errors
- Elements tab for CSS debugging

## Troubleshooting

### API Connection Failed

**Problem**: Cannot connect to backend
**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify CORS is enabled in backend
3. Check browser console for errors

### Videos Not Loading

**Problem**: Videos table is empty
**Solution**:
1. Check API response: Open Network tab in DevTools
2. Verify database has video records
3. Check console for JavaScript errors

### Upload Failed

**Problem**: File upload doesn't work
**Solution**:
1. Check file size (max 100MB typically)
2. Verify correct file format (mp4, mov, avi)
3. Check backend upload directory permissions

### Styling Issues

**Problem**: Layout broken or misaligned
**Solution**:
1. Clear browser cache (Cmd+Shift+R / Ctrl+Shift+R)
2. Check browser compatibility
3. Verify CSS files loaded correctly

## Performance

- **Initial Load**: < 2 seconds
- **API Calls**: < 500ms (local backend)
- **File Upload**: Depends on file size
- **Auto-refresh**: 30-second intervals

## Security

- **No authentication** in this version (development mode)
- **HTTPS recommended** for production
- **Input validation** on client and server
- **XSS protection** via proper escaping

## Future Enhancements

- [ ] User authentication
- [ ] Real-time WebSocket updates
- [ ] Advanced chart library (Chart.js)
- [ ] Video preview playback
- [ ] Batch operations
- [ ] Dark mode theme
- [ ] Mobile app version

## License

Proprietary - All rights reserved

## Support

For issues or questions:
1. Check this README
2. Review backend API documentation
3. Check browser console for errors
4. Contact development team

---

**Last Updated**: 2025-12-24
**Version**: 1.0.0
