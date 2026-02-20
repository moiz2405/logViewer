# 🐳 Docker Setup Complete!

Your project is now fully containerized. Here's what changed:

## What You Get

```
┌─────────────────────────────────────────┐
│  YOUR MACHINE                           │
│  ┌────────────────┐                     │
│  │ Frontend :3000 │                     │
│  │ (npm run dev)  │                     │
│  └───────┬────────┘                     │
│          │                              │
│          │ HTTP requests                │
│          ▼                              │
│  ┌─────────────────────────────┐       │
│  │  DOCKER NETWORK             │       │
│  │  ┌──────────────────────┐   │       │
│  │  │ sentry-backend :8001 │   │       │
│  │  │ - FastAPI            │   │       │
│  │  │ - Log ingestion      │   │       │
│  │  │ - SDK endpoints      │◄──┼───┐   │
│  │  └──────────────────────┘   │   │   │
│  │                              │   │   │
│  │  ┌──────────────────────┐   │   │   │
│  │  │ myapp-demo :8000     │   │   │   │
│  │  │ - Demo FastAPI app   │   │   │   │
│  │  │ - SDK installed      │───┼───┘   │
│  │  │ - Emits logs         │   │       │
│  │  └──────────────────────┘   │       │
│  └─────────────────────────────┘       │
└─────────────────────────────────────────┘
```

## 🚀 How to Run

### Simple Way (Just One Command)

```powershell
.\start.ps1
```

This:
1. ✅ Checks your `.env.local` exists
2. ✅ Verifies Docker is running
3. ✅ Builds and starts both containers
4. ✅ Tests backend health

Then in **another terminal**:

```powershell
cd frontend
npm install    # First time only
npm run dev
```

Visit: **http://localhost:3000**

---

### Manual Way

```powershell
# 1. Start containers
docker-compose up --build

# 2. In another terminal - start frontend
cd frontend
npm run dev
```

---

## 🔧 How It Works

### Container: `sentry-backend`
- Runs your FastAPI backend on port **8001**
- Reads `.env.local` for Supabase credentials
- Handles:
  - `/ingest` - receives logs from SDK
  - `/sdk/device/*` - OAuth device flow endpoints
  - `/sdk/schema/validate` - schema validation

### Container: `myapp-demo`
- Runs your demo app on port **8000**
- **SDK is pre-installed** via Dockerfile
- Emits sample logs every few seconds
- Sends logs to `http://sentry:8001/ingest`

### Frontend (Local)
- Runs on **localhost:3000**
- Dashboard to view logs
- Login page for SDK OAuth flow

---

## 🔑 Linking myApp with Sentry (First Time)

The myApp container needs an API key to send logs. Two options:

### Option 1: Quick Test (Manual API Key)

1. Go to your Supabase dashboard
2. Run this SQL to create an app + API key:
   ```sql
   INSERT INTO apps (name, user_id) 
   VALUES ('myApp', 'your-user-id') 
   RETURNING id;
   
   -- Use the returned id
   INSERT INTO app_api_keys (app_id, key_hash) 
   VALUES ('app-id-here', crypt('test-key-123', gen_salt('bf'))) 
   RETURNING *;
   ```

3. Set it in the container:
   ```powershell
   docker exec -it myapp-demo bash
   mkdir -p /root/.sentry_logger
   echo '{"api_key": "test-key-123", "dsn": "http://sentry:8001"}' > /root/.sentry_logger/config.json
   exit
   ```

4. Restart:
   ```powershell
   docker-compose restart myapp
   ```

### Option 2: Full OAuth Flow (Recommended)

1. Install SDK locally:
   ```powershell
   pip install -e ./sdk/python
   ```

2. Run onboarding:
   ```powershell
   sentry-logger init --app-name "myApp" --dsn "http://localhost:8001"
   ```

3. Browser opens → login → API key saved to `~/.sentry_logger/config.json`

4. Copy into container:
   ```powershell
   docker cp ~/.sentry_logger/config.json myapp-demo:/root/.sentry_logger/config.json
   docker-compose restart myapp
   ```

---

## 📊 Verify It's Working

### Check Backend Health
```powershell
curl http://localhost:8001/sdk/schema/validate
```
Should return: `{"ok": true, ...}`

### Check myApp Logs
```powershell
docker logs myapp-demo -f
```
You should see:
- `✅ Sentry SDK initialized successfully`
- Log entries being generated

### Check Sentry Received Logs
```powershell
docker logs sentry-backend -f
```
Look for: `POST /ingest` requests

---

## 🛠️ Development Tips

### Restart Services
```powershell
docker-compose restart           # Restart all
docker-compose restart sentry    # Just backend
docker-compose restart myapp     # Just demo app
```

### View Logs
```powershell
docker-compose logs -f           # All services
docker logs sentry-backend -f    # Just backend
docker logs myapp-demo -f        # Just demo app
```

### Rebuild After Code Changes
```powershell
docker-compose up --build -d
```

### Stop Everything
```powershell
docker-compose down              # Stop containers
# Frontend: Ctrl+C in terminal
```

### SSH into Containers
```powershell
docker exec -it sentry-backend bash
docker exec -it myapp-demo bash
```

---

## 📁 File Changes Made

### Updated Files:
- `docker-compose.yml` - Added networking, volumes, env handling
- `sentry/Dockerfile` - Optimized build, added reload
- `myApp/Dockerfile` - **Auto-installs SDK** from `./sdk/python`
- `myApp/main.py` - Updated to use config file or env vars

### New Files:
- `QUICKSTART.md` - Detailed setup guide
- `DOCKER.md` - This file!
- `start.ps1` - Windows startup script
- `start.sh` - Linux/Mac startup script
- `.env.example` - Template for root env
- `frontend/.env.local` - Template for frontend env

---

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Find process using port 8001
netstat -ano | findstr :8001
# Kill it
taskkill /PID <pid> /F
```

### Container Won't Start
```powershell
# Check logs
docker-compose logs sentry
docker-compose logs myapp

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

### Logs Not Appearing in Dashboard
1. Check myApp has API key:
   ```powershell
   docker exec myapp-demo cat /root/.sentry_logger/config.json
   ```
2. Check backend is receiving logs:
   ```powershell
   docker logs sentry-backend | grep "/ingest"
   ```
3. Verify Supabase credentials in `.env.local`

### Frontend Can't Connect to Backend
- Make sure backend is on `http://localhost:8001`
- Check `frontend/.env.local` has `NEXT_PUBLIC_BACKEND_URL=http://localhost:8001`

---

## 🎯 Next Steps

1. ✅ Run `.\start.ps1`
2. ✅ Start frontend with `npm run dev`
3. ✅ Link myApp using one of the methods above
4. ✅ Visit dashboard at `http://localhost:3000`
5. 🎉 See your logs in real-time!

---

**Questions?** Check `QUICKSTART.md` for more details or raise an issue.
