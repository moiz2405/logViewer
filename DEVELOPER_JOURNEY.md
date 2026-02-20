# 🚀 Developer Journey - Using Sentry SDK

This guide walks through the **complete flow** for any developer who wants to use your Sentry clone to monitor their application.

---

## 📋 Overview

```
Developer's App → Install SDK → Get API Key → Initialize → Logs Flow to Dashboard
```

---

## 🎯 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Developer discovers your Sentry clone          │
│ - Visits your hosted instance (e.g., logs.yourapp.com) │
│ - Or runs it locally for testing                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: Sign Up / Login                                │
│ - Click "Login with Google"                            │
│ - OAuth flow completes                                 │
│ - Lands on Dashboard                                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: Register Their App                             │
│ - Click "Add App" button                               │
│ - Enter app name (e.g., "my-ecommerce-api")           │
│ - Enter description (optional)                         │
│ - Click "Register App"                                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: Copy API Key                                   │
│ ⚠️  API key shown ONLY ONCE                            │
│ - Copy to clipboard                                    │
│ - Save in password manager / .env file                 │
│ - SDK installation instructions shown                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 5: Install SDK in Their App                       │
│                                                         │
│ Option A: From PyPI (if published)                     │
│   pip install sentry-logger                            │
│                                                         │
│ Option B: From GitHub                                  │
│   pip install git+https://github.com/you/sentry.git    │
│                                                         │
│ Option C: Local development                            │
│   pip install -e /path/to/sdk/python                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 6: Initialize SDK in Code                         │
│                                                         │
│ # main.py or app.py                                    │
│ from sentry_logger import init                         │
│ import os                                              │
│                                                         │
│ init(                                                   │
│     api_key=os.getenv("SENTRY_API_KEY"),              │
│     dsn=os.getenv("SENTRY_DSN",                        │
│         "https://logs.yourapp.com")                    │
│ )                                                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 7: Set Environment Variables                      │
│                                                         │
│ # .env file                                            │
│ SENTRY_API_KEY=sk_abc123xyz...                        │
│ SENTRY_DSN=https://logs.yourapp.com                    │
│                                                         │
│ # or export in shell                                   │
│ export SENTRY_API_KEY=sk_abc123xyz...                  │
│ export SENTRY_DSN=https://logs.yourapp.com             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 8: Run Their App                                  │
│ - App starts                                           │
│ - SDK initializes                                      │
│ - Logs start flowing to your backend                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 9: View Logs in Dashboard                         │
│ - Go back to https://logs.yourapp.com                  │
│ - Click on their app in sidebar                        │
│ - See real-time logs                                   │
│ - View health metrics                                  │
│ - Check log summaries                                  │
│ - Set up alerts (optional)                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Two Authentication Methods

### Method 1: Web UI (Recommended)

**Best for:** Most users, simple setup

```bash
# 1. Visit dashboard
https://logs.yourapp.com

# 2. Login with Google

# 3. Click "Add App" → Copy API key

# 4. In your app:
pip install sentry-logger

# 5. Initialize in code:
from sentry_logger import init
init(api_key="your-api-key", dsn="https://logs.yourapp.com")
```

**Pros:**
- ✅ Simple and visual
- ✅ No CLI tools needed
- ✅ Works everywhere (local, Docker, cloud)
- ✅ Easy to share keys with team

**Cons:**
- ⚠️ Need to manually copy/paste API key

---

### Method 2: CLI Device Flow (Advanced)

**Best for:** Power users, automated workflows

```bash
# 1. Install SDK with CLI
pip install sentry-logger

# 2. Run interactive setup
sentry-logger init --app-name "my-app" --dsn "https://logs.yourapp.com"

# 3. Browser opens → Login with Google → Authorize

# 4. API key saved to ~/.sentry_logger/config.json

# 5. In your app code (SDK auto-reads config):
from sentry_logger import init
init()  # Reads from ~/.sentry_logger/config.json
```

**Backend Flow:**
1. CLI calls `POST /sdk/device/start` → gets `device_code` + `user_code`
2. CLI opens browser to `/sdk/link?code={user_code}`
3. User logs in and authorizes
4. Frontend calls `POST /sdk/device/complete`
5. Backend creates app + API key in DB
6. CLI polls `GET /sdk/device/poll?device_code={device_code}`
7. Backend returns API key
8. CLI saves to `~/.sentry_logger/config.json`

**Pros:**
- ✅ One command setup
- ✅ API key stored securely in config file
- ✅ Great for CI/CD pipelines
- ✅ No need to copy/paste

**Cons:**
- ⚠️ Requires browser access
- ⚠️ More complex for beginners

---

## 📝 Example: Integrating with FastAPI

### Step-by-Step Integration

**1. Create your FastAPI app**
```python
# my_app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Your logic here
    return {"user_id": user_id}
```

**2. Install Sentry SDK**
```bash
pip install sentry-logger
```

**3. Initialize at app startup**
```python
# my_app/main.py
from fastapi import FastAPI
from sentry_logger import init
import os
import logging

# Initialize Sentry BEFORE creating FastAPI app
init(
    api_key=os.getenv("SENTRY_API_KEY"),
    dsn=os.getenv("SENTRY_DSN", "https://logs.yourapp.com")
)

app = FastAPI()

@app.get("/")
def read_root():
    logging.info("Root endpoint called")
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    logging.info(f"Fetching user {user_id}")
    try:
        # Your logic here
        return {"user_id": user_id}
    except Exception as e:
        logging.error(f"Error fetching user: {e}")
        raise
```

**4. Create .env file**
```bash
# .env
SENTRY_API_KEY=sk_abc123xyz...
SENTRY_DSN=https://logs.yourapp.com
```

**5. Run your app**
```bash
# Load .env and run
python -m uvicorn main:app --reload
```

**6. View logs in dashboard**
- Visit https://logs.yourapp.com
- Select "my-app" from sidebar
- See all your logs in real-time!

---

## 🐳 Example: Using in Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt
```txt
fastapi
uvicorn
sentry-logger  # Your SDK
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  my-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SENTRY_API_KEY=${SENTRY_API_KEY}
      - SENTRY_DSN=https://logs.yourapp.com
    env_file:
      - .env
```

### .env
```bash
SENTRY_API_KEY=sk_abc123xyz...
```

### Run
```bash
docker-compose up -d
```

---

## 🔄 What Happens Behind the Scenes

### When SDK Initializes

```python
init(api_key="sk_123", dsn="https://logs.yourapp.com")
```

1. ✅ SDK validates API key format
2. ✅ SDK connects to DSN endpoint
3. ✅ SDK intercepts Python's logging module
4. ✅ SDK starts background thread for batching logs
5. ✅ Ready to send logs!

### When You Log Something

```python
logging.info("User logged in", extra={"user_id": 123})
```

1. ✅ SDK captures log record
2. ✅ Adds metadata (timestamp, level, service name)
3. ✅ Adds to batch queue
4. ✅ When batch is full OR 5 seconds pass:
   - Sends `POST /ingest` to backend
   - Payload: `{"api_key": "...", "logs": [...]}`
5. ✅ Backend validates API key
6. ✅ Backend resolves app_id from API key
7. ✅ Backend stores logs in Supabase
8. ✅ Backend triggers AI summary (if configured)
9. ✅ Backend checks alert rules
10. ✅ Dashboard updates in real-time

---

## 🎨 Dashboard Features

Once integrated, developers get:

### Real-Time Logs
- Live tail of all logs
- Filter by level (INFO, WARNING, ERROR)
- Search by keywords
- Time-range filtering

### Health Metrics
- Error rate per service
- Log volume over time
- Response time trends
- Service health cards

### AI Summaries
- Automatic daily summaries
- Anomaly detection
- Error pattern recognition
- Recommendations

### Alerts
- Configure thresholds (e.g., >10 errors/min)
- Email/Slack notifications
- Custom alert rules

---

## 🔒 Security Best Practices

### For Developers Using Your SDK

1. **Never commit API keys**
   ```bash
   # .gitignore
   .env
   .env.local
   config.json
   ```

2. **Use environment variables**
   ```python
   # ✅ Good
   init(api_key=os.getenv("SENTRY_API_KEY"))
   
   # ❌ Bad
   init(api_key="sk_abc123...")
   ```

3. **Rotate keys regularly**
   - Dashboard should have "Regenerate API Key" button
   - Old key invalidated immediately

4. **Use different keys per environment**
   ```bash
   # .env.dev
   SENTRY_API_KEY=sk_dev_123...
   
   # .env.prod
   SENTRY_API_KEY=sk_prod_456...
   ```

---

## 📊 Verification Checklist

After integration, developers should verify:

- [ ] SDK installed: `pip list | grep sentry-logger`
- [ ] App created in dashboard
- [ ] API key copied and set in .env
- [ ] App runs without errors
- [ ] Dashboard shows logs appearing
- [ ] Can filter/search logs
- [ ] Health metrics displaying
- [ ] Alerts working (if configured)

---

## 🆘 Common Issues & Solutions

### "API key not found"
**Cause:** Invalid or expired API key  
**Solution:** Regenerate key from dashboard

### "Connection refused"
**Cause:** Wrong DSN URL or backend down  
**Solution:** Check DSN matches your backend URL

### "No logs appearing"
**Cause:** API key not set in environment  
**Solution:** Verify `echo $SENTRY_API_KEY` returns your key

### "SDK not initializing"
**Cause:** SDK not installed  
**Solution:** Run `pip install sentry-logger`

---

## 🚀 Next Steps

- Check out the [examples/](examples/) directory for sample apps
- Read [SDK-USAGE.md](SDK-USAGE.md) for advanced features
- Join our Discord for support
- Star the repo if you find it useful!

---

**Questions?** Open an issue or check the docs! 🎉
