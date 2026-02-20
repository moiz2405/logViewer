# ✨ You're All Set! Here's How to Get Started

## 📦 What You Have Now

Your project is **fully containerized**:

- ✅ **Sentry backend** runs in Docker (port 8001)
- ✅ **myApp demo** runs in Docker (port 8000) with SDK pre-installed
- ✅ **Frontend** runs locally with npm (port 3000)
- ✅ All services talk to each other via Docker network

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Fill in Environment Variables

Edit `.env.local` in the root folder:

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

(Keep the other values as-is)

### 2️⃣ Run Database Migrations

Go to Supabase SQL Editor and run:
- `supabase/migrations/20250218000000_add_api_key_to_apps.sql`
- `supabase/migrations/20260218000000_add_sdk_device_sessions.sql`

### 3️⃣ Start Everything

**Terminal 1 (Backend + Demo):**
```powershell
.\start.ps1
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm install      # First time only
npm run dev
```

**Visit:** http://localhost:3000

---

## 🔑 First-Time Setup: Connect myApp to Sentry

The demo app (myApp) runs **without the SDK by default**. To send logs to your dashboard:

### Step 1: Generate API Key from Dashboard

1. Go to http://localhost:3000
2. Login with Google
3. Click **"Add App"** or go to `/register`
4. Enter app name: **"myApp"**
5. Click **"Register App"**
6. **Copy the API key** (shown only once!)

### Step 2: Install SDK in myApp Container

```powershell
# SSH into the container
docker exec -it myapp-demo bash

# Install SDK from your local repository
pip install /sdk/python

# Or install from PyPI (if published)
pip install sentry-logger

# Exit container
exit
```

### Step 3: Set API Key and Restart

```powershell
# Edit docker-compose.yml and add under myapp > environment:
# - SENTRY_API_KEY=your-api-key-here

# Or use .env file:
echo "SENTRY_API_KEY=your-api-key-here" >> .env.local

# Restart myApp
docker-compose restart myapp
```

**Alternative: Use docker-compose override**

Create `docker-compose.override.yml`:
```yaml
version: '3.8'
services:
  myapp:
    environment:
      - SENTRY_API_KEY=your-api-key-from-dashboard
```

Then restart:
```powershell
docker-compose up -d myapp
```

---

## ✅ Verify It's Working

```powershell
# 1. Backend is healthy
curl http://localhost:8001/sdk/schema/validate
# Should return: {"ok": true}

# 2. Check myApp logs (before SDK install)
docker logs myapp-demo -f
# Look for: "ℹ️ Sentry SDK not installed - logs will only go to console"

# 3. After installing SDK and setting API key:
docker logs myapp-demo -f
# Look for: "✅ Sentry SDK initialized - logs will be sent to dashboard"

# 4. Backend receiving logs
docker logs sentry-backend -f
# Look for: "POST /ingest" requests
```

Then go to http://localhost:3000 → Dashboard → myApp to see live logs!

---

## 📚 More Info

- **[DEVELOPER_JOURNEY.md](DEVELOPER_JOURNEY.md)** - **For app developers:** Complete guide to integrating SDK
- **[FLOW_DIAGRAM.md](FLOW_DIAGRAM.md)** - Detailed flow diagrams & architecture
- **[SDK-USAGE.md](SDK-USAGE.md)** - SDK API reference & advanced features
- **[DOCKER.md](DOCKER.md)** - Docker setup & troubleshooting
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed platform setup
- **[examples/](examples/)** - Sample applications with SDK integration

---

## 🛑 Stop Everything

```powershell
docker-compose down    # Stop containers
# Frontend: Ctrl+C
```

---

**That's it!** You now have:
- 🐳 Backend running in Docker
- 🐳 Demo app running in Docker (SDK optional, installed when needed)
- 🌐 Frontend running locally
- 🔗 All services connected and talking
- 🎯 **Modular setup**: Install SDK only when you need it!

Enjoy your Sentry clone! 🎉
