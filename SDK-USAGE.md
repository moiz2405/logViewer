# 📦 Using the SDK in Your Own Apps

Once you have the Sentry backend running, you can send logs from **any Python application**.

---

## 🚀 Quick Setup

### 1. Generate API Key

1. Go to http://localhost:3000
2. Login with Google
3. Click **"Add App"** or navigate to `/register`
4. Enter your app name (e.g., "my-flask-app")
5. Click **"Register App"**
6. **Copy the API key** (shown only once - save it!)

---

### 2. Install SDK

#### Option A: From Local Repository
```bash
pip install /path/to/sentry/sdk/python
```

#### Option B: From PyPI (if published)
```bash
pip install sentry-logger
```

#### Option C: In requirements.txt
```txt
sentry-logger
# or for local dev:
# -e ./sdk/python
```

---

### 3. Initialize in Your App

**FastAPI Example:**
```python
from fastapi import FastAPI
from sentry_logger import init

# Initialize Sentry SDK
init(
    api_key="your-api-key-from-dashboard",
    dsn="http://localhost:8001"  # or your production URL
)

app = FastAPI()

@app.get("/")
def read_root():
    import logging
    logging.info("Hello from my app!")
    return {"message": "Hello World"}
```

**Flask Example:**
```python
from flask import Flask
from sentry_logger import init
import logging

init(api_key="your-api-key", dsn="http://localhost:8001")

app = Flask(__name__)

@app.route("/")
def hello():
    logging.info("Request received")
    return "Hello World!"
```

**Django Example:**
```python
# In settings.py or manage.py
from sentry_logger import init

init(
    api_key="your-api-key",
    dsn="http://localhost:8001"
)

# Your logs will now flow to Sentry dashboard
import logging
logging.info("Django app started")
```

**Any Python Script:**
```python
from sentry_logger import init
import logging

init(api_key="your-api-key", dsn="http://localhost:8001")

logging.info("Script started")
logging.warning("This is a warning")
logging.error("This is an error")
```

---

### 4. Use Environment Variables (Recommended)

Instead of hardcoding the API key:

```python
import os
from sentry_logger import init

init(
    api_key=os.environ.get("SENTRY_API_KEY"),
    dsn=os.environ.get("SENTRY_DSN", "http://localhost:8001")
)
```

Then set in your environment:
```bash
export SENTRY_API_KEY=your-api-key
export SENTRY_DSN=http://localhost:8001
```

Or in `.env` file:
```bash
SENTRY_API_KEY=your-api-key
SENTRY_DSN=http://localhost:8001
```

---

## 🐳 Docker Setup

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install SDK
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  my-app:
    build: .
    environment:
      - SENTRY_API_KEY=${SENTRY_API_KEY}
      - SENTRY_DSN=http://sentry-backend:8001
    networks:
      - sentry-network

networks:
  sentry-network:
    external: true
```

---

## 📊 View Logs in Dashboard

1. Go to http://localhost:3000
2. Login
3. Navigate to **Dashboard**
4. Select your app from the sidebar
5. See real-time logs, summaries, and health metrics

---

## 🎯 What Gets Sent?

The SDK automatically captures:
- ✅ All log levels (INFO, WARNING, ERROR, CRITICAL)
- ✅ Log timestamps
- ✅ Service names (if using multiple services)
- ✅ Log context and metadata
- ✅ Error stack traces

---

## 🔧 Advanced Configuration

### Custom Service Names
```python
init(
    api_key="your-api-key",
    dsn="http://localhost:8001",
    service_name="payment-service"  # Optional
)
```

### Batch Settings
```python
init(
    api_key="your-api-key",
    dsn="http://localhost:8001",
    batch_size=100,      # Send logs in batches of 100
    flush_interval=5.0   # Flush every 5 seconds
)
```

---

## 🐛 Troubleshooting

### Logs Not Appearing?

1. **Check SDK initialization:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   # You should see SDK debug output
   ```

2. **Verify API key is valid:**
   - Go to Supabase → `app_api_keys` table
   - Check your key exists

3. **Check network connectivity:**
   ```bash
   curl http://localhost:8001/health
   ```

4. **View SDK logs:**
   The SDK will log any errors to console

### Common Issues

**"API key not found"**
- Regenerate API key from dashboard
- Make sure you copied it correctly

**"Connection refused"**
- Make sure backend is running: `docker ps`
- Check DSN URL is correct

**"No logs in dashboard"**
- Verify you're logged in with the same Google account
- Check the app is linked to your user

---

## 📚 Next Steps

- Add multiple apps from dashboard
- Configure alert rules in Supabase
- Deploy to production
- Explore the dashboard features

---

**That's it!** Your app is now sending logs to your Sentry dashboard. 🎉
