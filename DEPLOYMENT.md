# Deployment Guide - Multi-Account Admin Panel

This guide covers deploying the Multi-Account Admin Panel to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Production Checklist](#production-checklist)
- [Docker Deployment](#docker-deployment)
- [Traditional VPS Deployment](#traditional-vps-deployment)
- [Database Setup](#database-setup)
- [Nginx Configuration](#nginx-configuration)
- [SSL/TLS Setup](#ssltls-setup)
- [Environment Variables](#environment-variables)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Security Hardening](#security-hardening)

---

## Prerequisites

- Server with Ubuntu 20.04+ or similar Linux distribution
- Minimum 2GB RAM, 2 CPU cores
- 20GB+ storage (depends on video volume)
- Domain name (for SSL)
- SSH access to server

---

## Production Checklist

Before deployment, ensure:

- [ ] PostgreSQL production credentials configured
- [ ] Strong SECRET_KEY generated
- [ ] DEBUG mode disabled
- [ ] CORS origins restricted to production domains
- [ ] SSL certificates obtained
- [ ] Firewall rules configured
- [ ] Backup strategy implemented
- [ ] Monitoring tools setup
- [ ] Log rotation configured
- [ ] FFmpeg installed on server

---

## Docker Deployment

### Step 1: Create Dockerfile for Backend

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p /app/uploads/videos /app/uploads/audio /app/uploads/thumbnails /app/uploads/projects

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create Dockerfile for Frontend

Create `frontend/Dockerfile`:

```dockerfile
FROM nginx:alpine

# Copy frontend files
COPY . /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Step 3: Create docker-compose.yml

Create in project root:

```yaml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    container_name: admin_panel_db
    environment:
      POSTGRES_DB: admin_panel
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - admin_network
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: admin_panel_backend
    environment:
      DATABASE_URL: postgresql://admin:${DB_PASSWORD}@db:5432/admin_panel
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: "False"
      CORS_ORIGINS: ${CORS_ORIGINS}
    volumes:
      - ./backend/uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - admin_network
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: admin_panel_frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    networks:
      - admin_network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  admin_network:
    driver: bridge
```

### Step 4: Create .env for Docker

Create `.env.production`:

```env
DB_PASSWORD=your_strong_db_password
SECRET_KEY=your_generated_secret_key_here
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Step 5: Deploy with Docker

```bash
# Build and start containers
docker-compose --env-file .env.production up -d

# Check logs
docker-compose logs -f

# Initialize database
docker-compose exec backend python init_db.py

# Check status
docker-compose ps
```

---

## Traditional VPS Deployment

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib nginx \
    ffmpeg supervisor git

# Install Node.js (optional, for frontend build tools)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Step 2: Create Application User

```bash
# Create user
sudo useradd -m -s /bin/bash adminpanel
sudo usermod -aG www-data adminpanel

# Switch to user
sudo su - adminpanel
```

### Step 3: Deploy Application

```bash
# Clone repository or upload files
cd /home/adminpanel
git clone <your-repo> admin-panel
cd admin-panel

# Setup backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
nano .env  # Edit with production values

# Initialize database
python init_db.py
```

### Step 4: Configure Supervisor

Create `/etc/supervisor/conf.d/adminpanel.conf`:

```ini
[program:adminpanel]
directory=/home/adminpanel/admin-panel/backend
command=/home/adminpanel/admin-panel/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
user=adminpanel
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/adminpanel/backend.log
environment=PATH="/home/adminpanel/admin-panel/backend/venv/bin"
```

Start the service:

```bash
sudo mkdir -p /var/log/adminpanel
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start adminpanel
```

---

## Database Setup

### PostgreSQL Production Configuration

```bash
# Create database
sudo -u postgres psql
```

```sql
-- Create database and user
CREATE DATABASE admin_panel;
CREATE USER admin_prod WITH PASSWORD 'your_strong_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE admin_panel TO admin_prod;

-- Enable required extensions
\c admin_panel
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Database Backup Script

Create `/home/adminpanel/backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/adminpanel/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="admin_panel_$DATE.sql"

mkdir -p $BACKUP_DIR

pg_dump -U admin_prod admin_panel > $BACKUP_DIR/$FILENAME

# Compress backup
gzip $BACKUP_DIR/$FILENAME

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $FILENAME.gz"
```

Add to crontab:

```bash
crontab -e
# Add line:
0 2 * * * /home/adminpanel/backup_db.sh
```

---

## Nginx Configuration

Create `/etc/nginx/sites-available/adminpanel`:

```nginx
# Upstream backend
upstream backend_api {
    server 127.0.0.1:8000;
}

# HTTP - Redirect to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS - Main site
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend - Static files
    location / {
        root /home/adminpanel/admin-panel/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://backend_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for video processing
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }

    # API docs
    location ~ ^/(docs|redoc|openapi.json) {
        proxy_pass http://backend_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Uploads
    location /uploads {
        alias /home/adminpanel/admin-panel/backend/uploads;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # File upload size
    client_max_body_size 500M;

    # Logging
    access_log /var/log/nginx/adminpanel_access.log;
    error_log /var/log/nginx/adminpanel_error.log;
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/adminpanel /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## SSL/TLS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test renewal
sudo certbot renew --dry-run

# Auto-renewal is configured automatically
```

---

## Environment Variables

Production `.env` file:

```env
# Database - Use strong credentials
DATABASE_URL=postgresql://admin_prod:STRONG_PASSWORD_HERE@localhost:5432/admin_panel

# Security - Generate with: openssl rand -hex 32
SECRET_KEY=YOUR_GENERATED_SECRET_KEY_64_CHARS_LONG

# Algorithm
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=/home/adminpanel/admin-panel/backend/uploads
MAX_UPLOAD_SIZE=524288000

# Application
APP_NAME=Admin Panel API
APP_VERSION=1.0.0
DEBUG=False

# CORS - Restrict to your domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional: Sentry for error tracking
# SENTRY_DSN=your_sentry_dsn_here
```

Generate SECRET_KEY:

```bash
openssl rand -hex 32
```

---

## Monitoring & Logging

### Log Rotation

Create `/etc/logrotate.d/adminpanel`:

```
/var/log/adminpanel/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 adminpanel adminpanel
    sharedscripts
    postrotate
        supervisorctl restart adminpanel > /dev/null
    endscript
}
```

### Health Monitoring

Create `/home/adminpanel/healthcheck.sh`:

```bash
#!/bin/bash

# Check backend
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Backend down - restarting"
    supervisorctl restart adminpanel
    # Send alert (email, Slack, etc.)
fi

# Check disk space
DISK_USAGE=$(df -h /home/adminpanel/admin-panel/backend/uploads | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Warning: Disk usage at ${DISK_USAGE}%"
    # Send alert
fi
```

Add to crontab:

```bash
*/5 * * * * /home/adminpanel/healthcheck.sh
```

---

## Backup & Recovery

### Automated Backups

1. **Database**: Covered in Database Setup section
2. **Uploads directory**:

```bash
#!/bin/bash
BACKUP_DIR="/home/adminpanel/backups/uploads"
DATE=$(date +%Y%m%d)

rsync -av --delete \
    /home/adminpanel/admin-panel/backend/uploads/ \
    $BACKUP_DIR/uploads_$DATE/

# Keep only last 7 days
find $BACKUP_DIR -type d -mtime +7 -delete
```

### Recovery Procedure

```bash
# Restore database
gunzip < backup.sql.gz | psql -U admin_prod admin_panel

# Restore uploads
rsync -av backup/uploads/ /home/adminpanel/admin-panel/backend/uploads/

# Restart services
sudo supervisorctl restart adminpanel
```

---

## Security Hardening

### Firewall Setup (UFW)

```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# PostgreSQL (only from localhost)
sudo ufw deny 5432/tcp

# Check status
sudo ufw status
```

### Fail2ban for SSH

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### PostgreSQL Hardening

Edit `/etc/postgresql/14/main/pg_hba.conf`:

```
# Only allow local connections
local   all             all                                     peer
host    admin_panel     admin_prod    127.0.0.1/32            md5
```

---

## Performance Optimization

### Backend Workers

Adjust worker count based on CPU cores:

```bash
# In supervisor config or uvicorn command
--workers $(nproc)
```

### Database Connection Pooling

In `backend/app/database.py`, ensure:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### Nginx Caching

Add to nginx config:

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

location /api/analytics {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    # ... other proxy settings
}
```

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
sudo supervisorctl tail -f adminpanel

# Check database connection
psql -U admin_prod -d admin_panel -c "SELECT 1;"

# Test manually
cd /home/adminpanel/admin-panel/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### High memory usage

```bash
# Monitor processes
htop

# Restart workers
sudo supervisorctl restart adminpanel

# Check for memory leaks
ps aux | grep uvicorn
```

---

## Maintenance Tasks

### Regular Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
cd /home/adminpanel/admin-panel/backend
source venv/bin/activate
pip list --outdated
pip install -U <package>

# Restart services
sudo supervisorctl restart adminpanel
```

### Database Maintenance

```bash
# Vacuum database
psql -U admin_prod -d admin_panel -c "VACUUM ANALYZE;"

# Check database size
psql -U admin_prod -d admin_panel -c "SELECT pg_size_pretty(pg_database_size('admin_panel'));"
```

---

## Contact & Support

For deployment issues or questions, contact:

- Technical Lead: [your-email]
- Documentation: See README.md and API_DOCUMENTATION.md

---

**Last Updated**: December 24, 2025
**Version**: 1.0.0
