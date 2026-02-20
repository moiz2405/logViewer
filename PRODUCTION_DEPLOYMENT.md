# 🚀 Production Deployment Guide

This guide covers deploying your Sentry clone to production with:
- **Backend** on VPS (DigitalOcean, AWS, Hetzner, etc.) via Docker
- **Frontend** on Vercel
- **Database** on Supabase (managed PostgreSQL)

---

## 📋 Prerequisites

- [ ] VPS with Docker installed (2GB RAM minimum)
- [ ] Domain name (e.g., `logsentry.io`)
- [ ] Vercel account
- [ ] Supabase account
- [ ] Google OAuth credentials

---

## 🌐 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR DOMAIN                         │
│                                                         │
│  logsentry.io (Frontend - Vercel)                      │
│      │                                                  │
│      ├─ /              → Landing page                   │
│      ├─ /register      → API key generation            │
│      ├─ /my-app/:id    → Dashboard                      │
│      └─ /api/*         → Proxied to backend            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ HTTPS
                   ▼
┌─────────────────────────────────────────────────────────┐
│  api.logsentry.io (Backend - VPS + Docker)             │
│                                                         │
│  ┌───────────────────────────────────────────┐         │
│  │  Nginx (Reverse Proxy + SSL)              │         │
│  │  - SSL termination (Let's Encrypt)        │         │
│  │  - Rate limiting                           │         │
│  └──────────┬────────────────────────────────┘         │
│             │                                           │
│             ▼                                           │
│  ┌───────────────────────────────────────────┐         │
│  │  Docker Container (FastAPI)               │         │
│  │  - Log ingestion                          │         │
│  │  - API key validation                     │         │
│  │  - Health endpoints                       │         │
│  └──────────┬────────────────────────────────┘         │
└─────────────┼───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│  Supabase (PostgreSQL)                                  │
│  - User accounts                                        │
│  - Apps & API keys                                      │
│  - Logs storage                                         │
│  - Metrics & summaries                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Step 1: Backend Deployment (VPS)

### 1.1 Setup VPS

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Install Nginx
apt install nginx -y

# Install Certbot for SSL
apt install certbot python3-certbot-nginx -y
```

### 1.2 Configure DNS

Point your domain to the VPS:

```
A    api.logsentry.io  →  YOUR_VPS_IP
```

### 1.3 Clone Repository

```bash
# Create app directory
mkdir -p /opt/sentry
cd /opt/sentry

# Clone your repo
git clone https://github.com/yourname/sentry.git .
```

### 1.4 Production Environment Variables

Create `/opt/sentry/.env.production`:

```bash
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Backend URLs
SDK_VERIFICATION_BASE_URL=https://logsentry.io
SDK_DEFAULT_DSN=https://api.logsentry.io

# Security
SDK_SCHEMA_STRICT_STARTUP=true

# Optional: AI Features
OPENAI_API_KEY=sk-...

# Optional: Email Alerts
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your-sendgrid-key
```

### 1.5 Production Docker Compose

Create `/opt/sentry/docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  sentry-backend:
    build: 
      context: ./sentry
      dockerfile: Dockerfile.prod
    container_name: sentry-backend
    restart: unless-stopped
    ports:
      - "127.0.0.1:8001:8001"  # Only expose to localhost
    env_file:
      - .env.production
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - sentry-network
    volumes:
      - ./logs:/app/logs  # For debugging
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  sentry-network:
    driver: bridge
```

### 1.6 Production Dockerfile

Create `/opt/sentry/sentry/Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./sentry/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./sentry /app

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8001

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Run with Gunicorn for production
CMD ["gunicorn", "backend.app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8001", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### 1.7 Update requirements.txt

Add to `/opt/sentry/sentry/requirements.txt`:

```txt
gunicorn==21.2.0
uvicorn[standard]==0.27.0
fastapi==0.109.0
# ... existing dependencies
```

### 1.8 Nginx Configuration

Create `/etc/nginx/sites-available/api.logsentry.io`:

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=ingest_limit:10m rate=1000r/m;

# Upstream backend
upstream sentry_backend {
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name api.logsentry.io;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.logsentry.io;

    # SSL certificates (will be configured by Certbot)
    ssl_certificate /etc/letsencrypt/live/api.logsentry.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.logsentry.io/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Max body size for log ingestion
    client_max_body_size 10M;

    # Health check (no rate limit)
    location /health {
        proxy_pass http://sentry_backend;
        access_log off;
    }

    # Log ingestion endpoint (higher rate limit)
    location /ingest {
        limit_req zone=ingest_limit burst=50 nodelay;
        
        proxy_pass http://sentry_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # SDK endpoints
    location /sdk/ {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://sentry_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://sentry_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Default location
    location / {
        limit_req zone=api_limit burst=10 nodelay;
        proxy_pass http://sentry_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and get SSL:

```bash
# Enable site
ln -s /etc/nginx/sites-available/api.logsentry.io /etc/nginx/sites-enabled/

# Test config
nginx -t

# Get SSL certificate
certbot --nginx -d api.logsentry.io

# Reload Nginx
systemctl reload nginx
```

### 1.9 Start Backend

```bash
cd /opt/sentry

# Build and start
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Verify health
curl https://api.logsentry.io/health
```

---

## 🌐 Step 2: Frontend Deployment (Vercel)

### 2.1 Prepare Frontend

Update `/frontend/.env.production`:

```bash
# NextAuth
NEXTAUTH_URL=https://logsentry.io
NEXTAUTH_SECRET=generate-a-secure-random-secret-here

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Backend API
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

### 2.2 Update Google OAuth

In Google Cloud Console:
- **Authorized JavaScript origins**: `https://logsentry.io`
- **Authorized redirect URIs**: `https://logsentry.io/api/auth/callback/google`

### 2.3 Deploy to Vercel

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# Or push to GitHub and connect to Vercel dashboard
```

In Vercel Dashboard:
1. Import your GitHub repo
2. Set **Framework Preset**: Next.js
3. Set **Root Directory**: `frontend`
4. Add all environment variables from `.env.production`
5. Deploy!

### 2.4 Configure Custom Domain

In Vercel:
1. Go to Project Settings → Domains
2. Add `logsentry.io`
3. Follow DNS instructions

---

## 📊 Step 3: Database Setup (Supabase)

### 3.1 Run Migrations

In Supabase SQL Editor, run:

```sql
-- From supabase/migrations/20250218000000_add_api_key_to_apps.sql
-- From supabase/migrations/20260218000000_add_sdk_device_sessions.sql
```

### 3.2 Setup Row Level Security

```sql
-- Enable RLS on all tables
ALTER TABLE apps ENABLE ROW LEVEL SECURITY;
ALTER TABLE app_api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;

-- Users can only see their own apps
CREATE POLICY "Users can view own apps" ON apps
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own apps" ON apps
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- API keys visible only to app owners
CREATE POLICY "API keys visible to app owners" ON app_api_keys
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM apps
      WHERE apps.id = app_api_keys.app_id
      AND apps.user_id = auth.uid()
    )
  );

-- Logs visible only to app owners
CREATE POLICY "Logs visible to app owners" ON logs
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM apps
      WHERE apps.id = logs.app_id
      AND apps.user_id = auth.uid()
    )
  );
```

---

## 🔒 Step 4: Security Hardening

### 4.1 Backend Health Check

Add to `/sentry/backend/app/main.py`:

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        # Add actual check here
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

### 4.2 Rate Limiting in Backend

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/ingest")
@limiter.limit("1000/minute")
async def ingest_logs(request: Request):
    # ...existing code
```

### 4.3 API Key Validation

Ensure API keys are validated on every request:

```python
async def validate_api_key(api_key: str) -> str:
    """Validate API key and return app_id"""
    if not api_key or not api_key.startswith("sk_"):
        raise HTTPException(401, "Invalid API key format")
    
    # Hash and check in database
    # Return app_id if valid, raise 401 if not
```

### 4.4 CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://logsentry.io",
        "https://www.logsentry.io"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## 📦 Step 5: SDK Publication

### 5.1 Prepare for PyPI

Update `/sdk/python/pyproject.toml`:

```toml
[project]
name = "logsentry-sdk"
version = "1.0.0"
description = "Official SDK for LogSentry monitoring platform"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your@email.com"}
]
keywords = ["logging", "monitoring", "observability", "logsentry"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "requests>=2.31.0",
]

[project.urls]
Homepage = "https://logsentry.io"
Documentation = "https://docs.logsentry.io"
Repository = "https://github.com/yourname/logsentry"
Issues = "https://github.com/yourname/logsentry/issues"

[project.scripts]
logsentry = "sentry_logger.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 5.2 Publish to PyPI

```bash
cd sdk/python

# Install build tools
pip install build twine

# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

Now users can install with:
```bash
pip install logsentry-sdk
```

---

## 📝 Step 6: Update Documentation

### 6.1 Update DEVELOPER_JOURNEY.md

Replace all URLs:
- `http://localhost:3000` → `https://logsentry.io`
- `http://localhost:8001` → `https://api.logsentry.io`
- `pip install sentry-logger` → `pip install logsentry-sdk`

### 6.2 Create Landing Page

The frontend should have a landing page at `/` with:
- Feature highlights
- Quick start guide
- Pricing (if applicable)
- Sign up CTA

---

## 🔍 Step 7: Monitoring & Maintenance

### 7.1 Setup Monitoring

```bash
# Install monitoring tools on VPS
apt install prometheus-node-exporter

# Monitor Docker containers
docker stats

# Setup uptime monitoring (UptimeRobot, Better Uptime)
# Monitor: https://api.logsentry.io/health
```

### 7.2 Log Rotation

```bash
# Create /etc/logrotate.d/sentry
/opt/sentry/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
```

### 7.3 Automated Backups

```bash
# Backup script: /opt/sentry/backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec sentry-backend pg_dump $DATABASE_URL > /backups/sentry_$DATE.sql
# Upload to S3 or backup service
```

### 7.4 Auto-renewal for SSL

Certbot auto-renews, but verify:

```bash
# Test renewal
certbot renew --dry-run

# Check cron
systemctl status certbot.timer
```

---

## ✅ Production Checklist

Before going live:

- [ ] Backend deployed and accessible at `https://api.logsentry.io`
- [ ] Frontend deployed at `https://logsentry.io`
- [ ] SSL certificates valid
- [ ] Database migrations run
- [ ] Google OAuth configured with production URLs
- [ ] Environment variables set correctly
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Health checks passing
- [ ] Monitoring setup
- [ ] Backup system in place
- [ ] SDK published to PyPI
- [ ] Documentation updated with production URLs
- [ ] Privacy policy & Terms of Service added
- [ ] GDPR compliance (if EU users)

---

## 🚀 User Flow (Production)

```
1. Developer visits https://logsentry.io
2. Clicks "Get Started" → Logs in with Google
3. Goes to /register → Creates app "my-production-api"
4. Copies API key: sk_prod_abc123...
5. In their app:
   pip install logsentry-sdk
6. Initializes:
   from logsentry_sdk import init
   init(api_key="sk_prod_...", dsn="https://api.logsentry.io")
7. Deploys their app
8. Logs flow to https://api.logsentry.io/ingest
9. Views dashboard at https://logsentry.io/my-app/app-id
10. Sets up alerts, views AI summaries ✅
```

---

## 💰 Optional: Monetization

Add to frontend:

```typescript
// Pricing tiers
const plans = {
  free: {
    logs: 10000,  // per month
    retention: 7,  // days
    apps: 1
  },
  pro: {
    logs: 1000000,
    retention: 30,
    apps: 10,
    price: 29  // USD/month
  },
  enterprise: {
    logs: "unlimited",
    retention: 90,
    apps: "unlimited",
    price: "custom"
  }
};
```

Integrate Stripe for payments.

---

## 🎉 You're Production Ready!

Your Sentry clone is now:
- ✅ Hosted on production infrastructure
- ✅ Secured with SSL
- ✅ Rate limited
- ✅ Monitored
- ✅ Scalable
- ✅ Ready for real users!

---

**Need help?** Check the logs:
```bash
# Backend logs
docker-compose -f docker-compose.prod.yml logs -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```
