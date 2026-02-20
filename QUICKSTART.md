# 🚀 Quick Start Guide

This project has 3 components that run together:

1. **Sentry Backend** (Docker) - Port 8001
2. **Frontend** (npm dev server) - Port 3000  
3. **myApp Demo** (Docker) - Port 8000

---

## Prerequisites

- Docker & Docker Compose
- Node.js 18+ & npm
- Supabase account (for DB)

---

## Setup Steps

### 1️⃣ Configure Environment

Create/edit `.env.local` in the root:

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SDK_VERIFICATION_BASE_URL=http://localhost:3000
SDK_DEFAULT_DSN=http://localhost:8001
SDK_SCHEMA_STRICT_STARTUP=false
```

> **Note:** The containers will automatically pick this up.

---

### 2️⃣ Run Database Migrations

Go to your Supabase SQL Editor and run:

1. `supabase/migrations/20250218000000_add_api_key_to_apps.sql`
2. `supabase/migrations/20260218000000_add_sdk_device_sessions.sql`

---

### 3️⃣ Start Backend Services (Docker)

```powershell
docker-compose up --build
```

This starts:
- **sentry** on `localhost:8001`
- **myapp** on `localhost:8000`

---

### 4️⃣ Start Frontend (Local)

In a separate terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `localhost:3000`

---

## 🧪 Test the Flow

### Validate Backend is Running

```powershell
curl http://localhost:8001/sdk/schema/validate
```

Expected: `{"ok": true, ...}`

---

### Connect myApp to Send Logs

**By default, myApp runs WITHOUT the SDK** - logs only go to console.

To send logs to your dashboard:

#### 1. Create an App in Dashboard

1. Go to http://localhost:3000
2. Login with Google
3. Click **"Add App"** → Enter "myApp" → Click **"Register App"**
4. **Copy the API key** (shown only once!)

#### 2. Install SDK in Container

```powershell
docker exec -it myapp-demo pip install /sdk/python
```

#### 3. Set API Key

Create `docker-compose.override.yml`:
```yaml
version: '3.8'
services:
  myapp:
    environment:
      - SENTRY_API_KEY=your-api-key-from-step-1
```

#### 4. Restart myApp

```powershell
docker-compose up -d myapp
```

#### 5. Verify Logs are Flowing

```powershell
# Check myApp initialized SDK
docker logs myapp-demo
# Should see: "✅ Sentry SDK initialized - logs will be sent to dashboard"

# Check backend is receiving
docker logs sentry-backend | grep "/ingest"
# Should see POST requests
```

Go to dashboard → myApp → see live logs!

---

## 📊 View Logs

1. Go to `http://localhost:3000`
2. Login with Google
3. Navigate to **Dashboard** → select **myApp**
4. See live logs, summaries, health metrics

---

## 🛑 Stop Everything

```powershell
# Stop containers
docker-compose down

# Stop frontend (Ctrl+C in terminal)
```

---

## Troubleshooting

### Container can't reach frontend
- Make sure `.env.local` has `SDK_VERIFICATION_BASE_URL=http://host.docker.internal:3000` for Windows Docker

### Logs not appearing
- Check myApp logs: `docker logs myapp-demo`
- Verify API key is set in `/root/.sentry_logger/config.json` inside container
- Check sentry backend logs: `docker logs sentry-backend`

### Port conflicts
- Stop services using 3000, 8000, 8001:
  ```powershell
  netstat -ano | findstr :3000
  taskkill /PID <pid> /F
  ```

---

## Architecture

```
┌─────────────────┐
│  Frontend :3000 │ (npm run dev)
│  Next.js + Auth │
└────────┬────────┘
         │
         │ API calls
         ▼
┌─────────────────┐
│ Sentry :8001    │ (Docker)
│ FastAPI Backend │◄──── Logs from myApp
└────────┬────────┘
         │
         │ Supabase
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   (Supabase)    │
└─────────────────┘

┌─────────────────┐
│  myApp :8000    │ (Docker)
│  Demo App       │
│  + SDK          │
└─────────────────┘
```

---

## Next Steps

- Customize `myApp/main.py` to emit your own logs
- Add more apps via the frontend "Add App" button
- Configure alert rules in Supabase `alert_rules` table
- Deploy to production using Docker Compose on a VPS
