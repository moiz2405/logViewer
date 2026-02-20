# 🎯 Sentry Clone - Modular Setup

A self-hosted log monitoring platform with a beautiful dashboard, similar to Sentry.

---

## ✨ Features

- 🔐 **Google OAuth** authentication
- 📊 **Real-time log dashboard** with health metrics
- 🔑 **API key management** via web UI
- 📦 **Modular SDK** - install only when needed
- 🐳 **Dockerized backend** for easy deployment
- 🌐 **Next.js frontend** with modern UI
- 🔔 **Smart alerts** and log summaries (AI-powered)
- 🌍 **Works Anywhere** - Monitor apps running locally, in staging, or production ([ENVIRONMENTS.md](ENVIRONMENTS.md))
- 🔒 **Secure Architecture** - Frontend talks only to backend API, no direct database access

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  Frontend (Next.js) :3000                   │
│  - Dashboard UI                             │
│  - Google OAuth login                       │
│  - API key generation                       │
└──────────────────┬──────────────────────────┘
                   │
                   │ HTTP
                   ▼
┌─────────────────────────────────────────────┐
│  Docker Network                             │
│  ┌───────────────────────────────────────┐  │
│  │ sentry-backend :8001                  │  │
│  │ - FastAPI                             │  │
│  │ - Log ingestion & processing          │  │
│  │ - Supabase integration                │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  ┌───────────────────────────────────────┐  │
│  │ myapp-demo :8000                      │  │
│  │ - Sample FastAPI app                  │  │
│  │ - SDK installed on-demand             │  │
│  │ - Generates demo logs                 │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                   │
                   ▼
           ┌─────────────┐
           │  Supabase   │
           │  PostgreSQL │
           └─────────────┘
```

---

## 🚀 Quick Start

### Local Development

**Prerequisites:**
- Docker & Docker Compose
- Node.js 18+ & npm
- Supabase account (free tier works!)

**1. Configure environment:**
```bash
# Edit .env.local with your Supabase credentials
cp .env.example .env.local
```

**2. Start services:**
```bash
# Terminal 1: Backend
.\start.ps1        # Windows
# or
./start.sh         # Linux/Mac

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

**3. Visit:** http://localhost:3000

---

### Production Deployment

Deploy to production in 30 minutes:

**Quick Deploy:** See [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

**Full Guide:** See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)

```bash
# On your VPS:
curl -fsSL https://raw.githubusercontent.com/yourname/sentry/main/deploy-production.sh -o deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh

# Deploy frontend to Vercel:
cd frontend && vercel --prod
```

**Result:**
- Backend: https://api.logsentry.io
- Frontend: https://logsentry.io
- Users can install: `pip install logsentry-sdk`

---

## 🔑 Connect Your App

**Your app can run ANYWHERE** - localhost, Docker, staging, production, serverless! See [ENVIRONMENTS.md](ENVIRONMENTS.md) for details.

### Step 1: Generate API Key

1. Go to http://localhost:3000/register
2. Login with Google
3. Click **"Add App"**
4. Enter your app name
5. **Copy the API key** (shown only once!)

### Step 2: Install SDK

**In myApp demo container:**
```bash
.\install-sdk.ps1   # Windows
# or
./install-sdk.sh    # Linux/Mac
```

**In your own Python app (local or production):**
```bash
pip install sentry-logger
# or from local:
pip install ./sdk/python
```

### Step 3: Initialize SDK

**In your app code:**
```python
import sentry_logger as sentry
import os
import logging

# Simple! Just your API key
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

# Use normal Python logging
logging.info("Hello from my app!")
```

**Optional:** Override backend URL for local testing:
```bash
export LOGSENTRY_URL=http://localhost:8001  # For local backend
export LOGSENTRY_API_KEY=your-api-key
```

# Now all your logs will flow to the dashboard!
import logging
logging.info("Hello from my app!")
```

### Step 4: Set API Key in myApp

Create `docker-compose.override.yml`:
```yaml
version: '3.8'
services:
  myapp:
    environment:
      - SENTRY_API_KEY=your-api-key
```

Restart:
```bash
docker-compose up -d myapp
```

---

## 📊 View Logs

1. Go to http://localhost:3000
2. Navigate to **Dashboard**
3. Select your app from sidebar
4. See real-time logs, health metrics, and summaries!

---

## 📚 Documentation

**Getting Started:**
- **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - **30-minute production deployment**
- **[START_HERE.md](START_HERE.md)** - Local development setup
- **[PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)** - Complete production guide

**For Platform Operators:**
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed platform setup
- **[DOCKER.md](DOCKER.md)** - Docker configuration & troubleshooting
- **[PRODUCTION_URLS.md](PRODUCTION_URLS.md)** - Production URL configuration

**For App Developers (Your Users):**
- **[DEVELOPER_JOURNEY.md](DEVELOPER_JOURNEY.md)** - **Main integration guide**
- **[FLOW_DIAGRAM.md](FLOW_DIAGRAM.md)** - End-to-end technical flows
- **[SDK-USAGE.md](SDK-USAGE.md)** - SDK API reference & examples
- **[examples/](examples/)** - Sample applications

**Reference:**
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview & architecture

---

## 🛠️ Development

### Project Structure

```
├── sentry/              # FastAPI backend (Docker)
│   ├── backend/
│   │   └── app/
│   │       ├── main.py
│   │       ├── models/
│   │       └── log_types/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # Next.js app (local)
│   ├── app/
│   ├── components/
│   └── package.json
├── examples/           # Example apps
│   ├── myApp/         # Multi-service FastAPI demo
│   └── README.md
├── sdk/python/         # Python SDK
│   └── sentry_logger/
├── supabase/           # DB migrations
│   └── migrations/
└── docker-compose.yml
```

### Useful Commands

```bash
# View logs
docker-compose logs -f
docker logs sentry-backend -f
docker logs myapp-demo -f

# Restart services
docker-compose restart
docker-compose restart myapp

# Rebuild
docker-compose up --build -d

# Stop all
docker-compose down

# SSH into container
docker exec -it myapp-demo bash
docker exec -it sentry-backend bash
```

---

## 🔧 Customization

### Add Your Own App

1. Create your Python app
2. Add `sentry-logger` to requirements
3. Initialize SDK with your API key
4. Logs automatically flow to dashboard!

### Deploy to Production

1. Use production Supabase instance
2. Set production DSN in SDK
3. Deploy frontend to Vercel/Netlify
4. Deploy backend with Docker on VPS
5. Use environment variables for secrets

---

## 🐛 Troubleshooting

### Backend won't start
- Check `.env.local` has valid Supabase credentials
- Run: `docker-compose logs sentry-backend`

### No logs in dashboard
- Verify API key is set: `docker logs myapp-demo`
- Check SDK initialized: Look for "✅ Sentry SDK initialized"
- Check backend receiving: `docker logs sentry-backend | grep "/ingest"`

### Port conflicts
```powershell
netstat -ano | findstr :3000
taskkill /PID <pid> /F
```

---

## 🌟 Key Differences from Original Sentry

- ✅ **Modular SDK**: Install only when needed (not pre-baked)
- ✅ **Web UI for API keys**: No manual DB queries required
- ✅ **Simpler setup**: One command to start
- ✅ **Docker-first**: Backend runs in containers
- ✅ **Easy customization**: All code is yours to modify

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a PR

---

## 📝 License

MIT License - feel free to use in your own projects!

---

**Questions?** Check the docs or open an issue. Happy logging! 🎉
