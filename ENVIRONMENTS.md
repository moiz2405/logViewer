# 🌍 Using LogSentry in Any Environment

Your LogSentry platform works with apps running **anywhere** - from your laptop to production servers!

---

## ✅ Supported Environments

### 1️⃣ **Local Development (Recommended for Testing)**

**Perfect for:**
- Testing integration before deploying
- Development workflow
- Debugging

**Setup:**
```python
# Your app running on localhost
# myapp/main.py

import sentry_logger as sentry
import os

# Simple! Just pass your API key
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

# Now run your app locally
# uvicorn main:app --reload
```

**Flow:**
```
Your Laptop                        Cloud
┌─────────────────┐               ┌──────────────────┐
│  Your App       │               │  LogSentry       │
│  localhost:8000 │─── Logs ─────>│  api.logsentry.io│
│                 │               │                  │
│  ✅ Logs sent   │               │  ✅ Logs received│
└─────────────────┘               └──────────────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │  Dashboard       │
                                  │  logsentry.io    │
                                  │  ✅ View logs    │
                                  └──────────────────┘
```

**Benefits:**
- ✅ See logs in real-time while developing
- ✅ No need to deploy to test
- ✅ Faster development cycle
- ✅ Debug locally, monitor remotely

---

### 2️⃣ **Docker Containers (Local)**

**Your app in Docker, LogSentry in cloud:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  my-app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOGSENTRY_API_KEY=sk_dev_abc123...
      # Optional: Override backend URL for local testing
      # - LOGSENTRY_URL=http://localhost:8001
```

**Run:**
```bash
docker-compose up
# Logs from container → Cloud dashboard ✅
```

---

### 3️⃣ **Staging/Test Servers**

**Your app on staging server, LogSentry in cloud:**

```bash
# On your staging server (staging.yourapp.com)
export LOGSENTRY_API_KEY=sk_staging_xyz...

python main.py
# Staging logs → Cloud dashboard ✅
```

**Best Practice:**
Use different API keys for different environments:

```python
# .env.dev
LOGSENTRY_API_KEY=sk_dev_abc123...

# .env.staging  
LOGSENTRY_API_KEY=sk_staging_xyz456...

# .env.production
LOGSENTRY_API_KEY=sk_prod_def789...
```

In your LogSentry dashboard, you'll see separate apps:
- "my-app-dev"
- "my-app-staging"
- "my-app-production"

---

### 4️⃣ **Production Servers**

**Your app in production, LogSentry monitoring:**

```bash
# On production server (api.yourapp.com)
export LOGSENTRY_API_KEY=sk_prod_...

gunicorn main:app
# Production logs → Cloud dashboard ✅
```

---

### 5️⃣ **Serverless (AWS Lambda, Google Cloud Functions)**

**Your function running serverless:**

```python
# lambda_function.py
import sentry_logger as sentry
import logging
import os

# Initialize once (outside handler for reuse)
sentry.init(api_key=os.environ["LOGSENTRY_API_KEY"])

def handler(event, context):
    logging.info("Lambda invoked")
    # Your code
    return {"statusCode": 200}
```

**Set environment variable in AWS Console:**
```
LOGSENTRY_API_KEY=sk_lambda_...
```

---

### 6️⃣ **CI/CD Pipelines**

**Monitor your tests and builds:**

```yaml
# .github/workflows/test.yml
name: Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        env:
          LOGSENTRY_API_KEY: ${{ secrets.LOGSENTRY_API_KEY }}
        run: |
          pytest --log-level=INFO
          # Test logs → Dashboard ✅
```

---

## 🎯 Common Use Cases

### Use Case 1: Developer Testing Locally

```
Scenario: Sarah is building a new feature locally
Goal: See logs in LogSentry dashboard while coding

Setup:
1. Sarah creates app in dashboard: "ecommerce-dev"
2. Gets API key: sk_dev_abc123...
3. In her laptop terminal:
   export LOGSENTRY_API_KEY=sk_dev_abc123...
4. Runs: uvicorn main:app --reload
5. Hits http://localhost:8000/orders
6. Opens https://logsentry.io → sees logs in real-time ✅

Result: Logs from her laptop → Cloud dashboard
```

---

### Use Case 2: Team with Multiple Environments

```
Scenario: Startup with dev, staging, production
Goal: Monitor all environments separately

Setup:
1. Create 3 apps in dashboard:
   - "app-dev"     → sk_dev_...
   - "app-staging" → sk_staging_...
   - "app-prod"    → sk_prod_...

2. Each environment uses different key:
   Dev server:     export LOGSENTRY_API_KEY=sk_dev_...
   Staging server: export LOGSENTRY_API_KEY=sk_staging_...
   Prod server:    export LOGSENTRY_API_KEY=sk_prod_...

3. Dashboard shows all 3 apps separately

Result: One LogSentry instance monitoring everything ✅
```

---

### Use Case 3: Debugging Production Issues Locally

```
Scenario: Bug in production, need to reproduce locally
Goal: Test fix locally before deploying

Setup:
1. Developer runs app locally with production API key
2. Reproduces issue on localhost
3. Sees logs in same dashboard as production
4. Fixes bug
5. Verifies fix locally
6. Deploys to production

Result: Same monitoring for local debugging ✅
```

---

## 🔒 Security Considerations

### ✅ **Safe for Local Development**

Your SDK sends logs over **HTTPS** regardless of where your app runs:

```
Local App (HTTP)               LogSentry (HTTPS)
┌──────────────┐              ┌─────────────────┐
│ localhost    │──HTTPS────>  │ api.logsentry.io│
│ :8000        │              │ (SSL encrypted) │
└──────────────┘              └─────────────────┘
```

### ✅ **API Keys are Safe**

- Never exposed in logs
- Sent in request headers only
- Validated server-side
- Can be rotated anytime

### ⚠️ **Best Practices**

1. **Different keys per environment:**
   ```bash
   # Don't use production keys in development!
   Dev:     sk_dev_...
   Staging: sk_staging_...
   Prod:    sk_prod_...
   ```

2. **Use environment variables:**
   ```python
   # ✅ Good
   api_key=os.getenv("LOGSENTRY_API_KEY")
   
   # ❌ Bad
   api_key="sk_prod_hardcoded123"
   ```

3. **Add to .gitignore:**
   ```bash
   # .gitignore
   .env
   .env.local
   .env.production
   ```

---

## 📊 Example: Full Development Workflow

### Step 1: Local Development

```bash
# Developer's laptop
cd my-fastapi-app

# Install SDK
pip install logsentry-sdk

# Set dev API key
export LOGSENTRY_API_KEY=sk_dev_abc123

# Run locally
uvicorn main:app --reload

# Open dashboard
# Visit: https://logsentry.io
# Select: "my-app-dev"
# See: Real-time logs from localhost ✅
```

### Step 2: Commit & Push

```bash
git add .
git commit -m "Add feature X"
git push origin feature-x
```

### Step 3: CI/CD Runs Tests

```yaml
# GitHub Actions automatically:
# 1. Checks out code
# 2. Runs tests with LOGSENTRY_API_KEY
# 3. Sends test logs to dashboard
# 4. You see test results in LogSentry ✅
```

### Step 4: Deploy to Staging

```bash
# SSH to staging server
ssh user@staging.myapp.com

# Pull latest code
git pull

# Restart with staging key
export LOGSENTRY_API_KEY=sk_staging_xyz456
systemctl restart myapp

# Check dashboard
# Visit: https://logsentry.io
# Select: "my-app-staging"
# See: Staging logs ✅
```

### Step 5: Deploy to Production

```bash
# SSH to production
ssh user@production.myapp.com

# Deploy
git pull
export LOGSENTRY_API_KEY=sk_prod_def789
systemctl restart myapp

# Monitor dashboard
# Visit: https://logsentry.io
# Select: "my-app-production"
# See: Production logs ✅
```

---

## 🎯 Key Takeaways

### ✅ **Your app can be ANYWHERE**
- Laptop
- Docker container
- VPS
- Cloud (AWS, GCP, Azure)
- Serverless
- CI/CD pipeline

### ✅ **LogSentry is always in the cloud**
- Users don't deploy LogSentry
- You host it once at `https://api.logsentry.io`
- Everyone connects to your instance

### ✅ **Network requirements**
- Your app just needs **internet access**
- Outbound HTTPS to `https://api.logsentry.io`
- No inbound connections needed
- Works behind firewalls (outbound only)

### ✅ **Perfect for testing**
- Developers test locally first
- See logs immediately in dashboard
- No deployment needed to test integration

---

## 🚀 Marketing This Feature

### Tagline Ideas

> **"Monitor locally, debug globally"**

> **"From localhost to production, we've got you covered"**

> **"Works anywhere Python runs"**

### Features to Highlight

**✅ Zero Deployment Friction**
- Test integration in 5 minutes
- No need to deploy to try it
- Works on your laptop

**✅ Universal Compatibility**
- Any environment
- Any platform
- Any hosting provider

**✅ Developer-Friendly**
- Install SDK: 1 line
- Initialize: 2 lines
- See logs: Instantly

---

## 📝 Update Your Docs

Add this to your landing page:

```markdown
## Works Everywhere Python Runs

✅ Local development (localhost)
✅ Docker containers
✅ VPS & Cloud servers
✅ Serverless functions
✅ CI/CD pipelines

No matter where your app runs, LogSentry monitors it.
```

---

## ✅ Answer to Your Question

**Q: Should the app which will install the SDK be deployed as well?**

**A: NO!** The app can be:
- ✅ **Local** (running on developer's laptop)
- ✅ **Staging** (test server)
- ✅ **Production** (live server)
- ✅ **Docker** (containerized locally or in cloud)
- ✅ **Serverless** (Lambda, Cloud Functions)
- ✅ **CI/CD** (GitHub Actions, Jenkins)

**Q: Can we do it in dev/local too?**

**A: YES!** In fact, **most developers will test locally first!**

**Typical flow:**
1. Developer installs SDK
2. Tests on **localhost** ← Works perfectly!
3. Sees logs in your cloud dashboard
4. Happy with integration
5. Then deploys to production

**This is a HUGE selling point** - developers can try it risk-free on their laptop before committing!

---

**The magic:** Your LogSentry is in the cloud. Their app can be anywhere with internet! 🌍
