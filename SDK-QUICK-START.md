# 🚀 LogSentry SDK - Quick Start

Get your app monitored in **2 minutes**!

---

## 📦 Installation

```bash
pip install logsentry-sdk
```

---

## 🎯 Basic Usage

### 1️⃣ **Get Your API Key**

Go to [logsentry.io/register](https://logsentry.io/register):
1. Sign in with Google
2. Click **"Add App"**
3. Enter your app name
4. **Copy your API key** (starts with `sk_...`)

### 2️⃣ **Initialize in Your App**

```python
# main.py
import sentry_logger as sentry
import logging

# That's it! Just your API key
sentry.init(api_key="sk_your_api_key_here")

# Now use normal Python logging
logging.info("Hello from my app! 🚀")
logging.warning("This is a warning")
logging.error("Something went wrong!")
```

### 3️⃣ **Run Your App**

```bash
python main.py
```

### 4️⃣ **View Logs**

Open [logsentry.io](https://logsentry.io) → Select your app → See logs! ✅

---

## 🔐 Use Environment Variables (Recommended)

**Never hardcode API keys!** Use environment variables:

```python
# main.py
import sentry_logger as sentry
import os
import logging

# Load API key from environment
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

logging.info("App started")
```

**Set the environment variable:**

```bash
# Linux/Mac
export LOGSENTRY_API_KEY=sk_your_api_key

# Windows PowerShell
$env:LOGSENTRY_API_KEY="sk_your_api_key"

# Windows CMD
set LOGSENTRY_API_KEY=sk_your_api_key
```

**Or use a `.env` file:**

```bash
# .env
LOGSENTRY_API_KEY=sk_your_api_key
```

```python
# main.py
from dotenv import load_dotenv
import sentry_logger as sentry
import os

load_dotenv()
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))
```

---

## 🎨 Framework Examples

### FastAPI

```python
# main.py
from fastapi import FastAPI
import sentry_logger as sentry
import logging
import os

# Initialize SDK
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

app = FastAPI()

@app.get("/")
def read_root():
    logging.info("Root endpoint called")
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    logging.info(f"Fetching user {user_id}")
    return {"user_id": user_id}
```

**Run:**
```bash
export LOGSENTRY_API_KEY=sk_...
uvicorn main:app --reload
```

---

### Flask

```python
# app.py
from flask import Flask
import sentry_logger as sentry
import logging
import os

# Initialize SDK
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

app = Flask(__name__)

@app.route('/')
def home():
    logging.info("Home page visited")
    return "Hello, World!"

@app.route('/api/data')
def get_data():
    logging.info("API called")
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(debug=True)
```

**Run:**
```bash
export LOGSENTRY_API_KEY=sk_...
python app.py
```

---

### Django

```python
# your_project/settings.py

import sentry_logger as sentry
import os

# Initialize SDK in settings.py
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

# Rest of your settings...
```

```python
# your_app/views.py
import logging

def my_view(request):
    logging.info("View called")
    return HttpResponse("Hello!")
```

**Run:**
```bash
export LOGSENTRY_API_KEY=sk_...
python manage.py runserver
```

---

## 🌍 Environment Configuration

By default, logs are sent to **https://api.logsentry.io** (production).

### For Local Development

If you're running LogSentry locally:

```bash
# Override the backend URL
export LOGSENTRY_URL=http://localhost:8001
export LOGSENTRY_API_KEY=sk_...

python main.py
```

```python
# main.py - No code changes needed!
import sentry_logger as sentry
import os

sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))
# SDK automatically uses LOGSENTRY_URL if set
```

### Environment Variables Summary

| Variable | Purpose | Default |
|----------|---------|---------|
| `LOGSENTRY_API_KEY` | Your API key (required) | None |
| `LOGSENTRY_URL` | Backend URL (optional) | `https://api.logsentry.io` |

---

## ⚙️ Advanced Configuration

### Custom Batch Size

```python
import sentry_logger as sentry

sentry.init(
    api_key="sk_...",
    batch_size=100,  # Send logs in batches of 100 (default: 50)
    flush_interval_seconds=10.0  # Flush every 10 seconds (default: 5.0)
)
```

### Multiple Environments

```python
import os

# Different API keys for different environments
if os.getenv("ENV") == "production":
    api_key = os.getenv("LOGSENTRY_API_KEY_PROD")
elif os.getenv("ENV") == "staging":
    api_key = os.getenv("LOGSENTRY_API_KEY_STAGING")
else:
    api_key = os.getenv("LOGSENTRY_API_KEY_DEV")

sentry.init(api_key=api_key)
```

---

## 📊 What Gets Logged?

The SDK captures:
- ✅ **Log level** (INFO, WARNING, ERROR, etc.)
- ✅ **Message** (your log message)
- ✅ **Timestamp** (when it happened)
- ✅ **Source** (file, function, line number)
- ✅ **Service name** (your app name from dashboard)

**Example:**

```python
import logging

logging.info("User logged in", extra={"user_id": 123})
logging.error("Payment failed", extra={"amount": 99.99})
```

**In your dashboard:**
```
[INFO] 2026-02-20 10:30:45 - User logged in (user_id=123)
[ERROR] 2026-02-20 10:31:12 - Payment failed (amount=99.99)
```

---

## 🔍 Troubleshooting

### "Logs not appearing in dashboard"

1. **Check API key:**
   ```python
   import os
   print(os.getenv("LOGSENTRY_API_KEY"))  # Should start with sk_
   ```

2. **Check network:**
   ```bash
   curl https://api.logsentry.io/health
   # Should return: {"status": "ok"}
   ```

3. **Check logs are being created:**
   ```python
   import logging
   logging.info("Test log")  # Check your terminal
   ```

### "ValueError: api_key is required"

Make sure you're setting the API key:

```python
# ❌ Wrong
sentry.init()

# ✅ Correct
sentry.init(api_key="sk_...")
```

### "Connection errors"

If you see connection errors, check:
- Internet connection
- Firewall settings (allow HTTPS to api.logsentry.io)
- If using custom URL, check `LOGSENTRY_URL` is correct

---

## 🎯 Best Practices

### ✅ DO

```python
# Use environment variables
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

# Use structured logging
logging.info("Order created", extra={"order_id": 123, "amount": 50.00})

# Different keys per environment
# dev: sk_dev_...
# staging: sk_staging_...
# prod: sk_prod_...
```

### ❌ DON'T

```python
# Don't hardcode API keys
sentry.init(api_key="sk_prod_abc123xyz")  # ❌

# Don't commit .env files
# Add .env to .gitignore! ❌

# Don't use production keys in development
# Use separate keys! ❌
```

---

## 📚 Next Steps

- ✅ Read [ENVIRONMENTS.md](ENVIRONMENTS.md) - Use SDK in any environment
- ✅ Read [DEVELOPER_JOURNEY.md](DEVELOPER_JOURNEY.md) - Complete integration guide
- ✅ Check the [Dashboard](https://logsentry.io) - Monitor your apps

---

## 🆘 Support

- 📖 Docs: [github.com/your-org/logsentry](https://github.com)
- 💬 Issues: [Open an issue](https://github.com/your-org/logsentry/issues)
- 📧 Email: support@logsentry.io

---

## ✨ That's It!

**3 lines of code to get started:**

```python
import sentry_logger as sentry
import os

sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))
```

**Happy logging! 🚀**
