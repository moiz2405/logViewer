# 🎯 SDK API Design - Clean & Simple

## ✨ New Simplified API

### Before (Old API)
```python
from logsentry_sdk import init

init(
    api_key="sk_...",
    dsn="https://api.logsentry.io"  # User had to provide this
)
```

**Problems:**
- ❌ Confusing - why do I need both API key AND URL?
- ❌ Error-prone - users might use wrong URL
- ❌ Inconsistent - some services call it "DSN", others "URL"
- ❌ Not beginner-friendly

---

### After (New API) ✅
```python
import sentry_logger as sentry

sentry.init(api_key="sk_...")
```

**Benefits:**
- ✅ **Simple** - Only API key required
- ✅ **Secure** - Backend URL controlled by platform owner (you!)
- ✅ **Flexible** - URL can be overridden via env var if needed
- ✅ **Beginner-friendly** - Minimal configuration
- ✅ **Pythonic** - Import as `sentry`, use `sentry.init()`

---

## 🔧 How It Works

### 1. Default Behavior (Production)

```python
import sentry_logger as sentry

sentry.init(api_key="sk_...")
# Automatically uses: https://api.logsentry.io
```

The SDK **automatically** sends logs to your production backend.

### 2. Override for Local Testing (Optional)

If someone wants to test against a local LogSentry instance:

```bash
export LOGSENTRY_URL=http://localhost:8001
export LOGSENTRY_API_KEY=sk_dev_...
```

```python
import sentry_logger as sentry
import os

sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))
# Now uses: http://localhost:8001
```

### 3. Inside Docker Containers

```yaml
# docker-compose.yml
environment:
  - LOGSENTRY_API_KEY=sk_...
  - LOGSENTRY_URL=http://sentry:8001  # Optional override
```

---

## 🎯 Design Principles

### 1. **Sensible Defaults**
- Default URL: `https://api.logsentry.io`
- Users don't need to know/care about URLs
- "It just works" out of the box

### 2. **Environment-Driven Configuration**
```python
# All config via environment variables
LOGSENTRY_API_KEY=sk_...       # Required
LOGSENTRY_URL=...              # Optional
```

### 3. **Zero Hardcoding**
```python
# ✅ Good - No hardcoded URLs
sentry.init(api_key=os.getenv("LOGSENTRY_API_KEY"))

# ❌ Bad - Don't do this
sentry.init(api_key="sk_...", url="https://...")
```

### 4. **Platform Control**
- **You** (platform owner) control the default URL
- Update it in the SDK package
- All users automatically use the right URL
- No need to communicate URL changes to users

---

## 📦 SDK Configuration Hierarchy

```
1. Default (hardcoded in SDK)
   └─> https://api.logsentry.io

2. Environment Variable (override)
   └─> LOGSENTRY_URL

3. User's API Key
   └─> LOGSENTRY_API_KEY
```

---

## 🚀 User Experience Comparison

### Old Way (Confusing)
```python
# User thinks: "What's a DSN? Where do I get it?"
from logsentry_sdk import init

init(
    api_key="sk_...",  # From dashboard
    dsn="???"          # From where???
)
```

### New Way (Simple) ✅
```python
# User thinks: "Just need my API key!"
import sentry_logger as sentry

sentry.init(api_key="sk_...")  # Done! 🎉
```

---

## 🔐 Security Benefits

### 1. **Controlled Backend**
- Users can't accidentally send logs to wrong server
- You control where logs go
- Easier to migrate backends if needed

### 2. **API Key Only**
- Single secret to manage
- No URL leakage
- Simpler secrets management

### 3. **Production by Default**
- Users don't accidentally point to dev servers
- No risk of "oops, I used localhost in production"

---

## 📚 Documentation Impact

### What Users See in Docs

**Step 1: Install**
```bash
pip install logsentry-sdk
```

**Step 2: Get API Key**
- Go to dashboard
- Create app
- Copy API key

**Step 3: Initialize**
```python
import sentry_logger as sentry
sentry.init(api_key="sk_...")
```

**That's it!** ← 3 simple steps

---

## 🎨 Marketing Angles

### "One Line to Monitor"
```python
sentry.init(api_key="sk_...")
```

### "No Configuration, Just Works"
> Install, initialize, done. No YAML files, no config management, no DevOps needed.

### "Secure by Default"
> Your API key is all you need. We handle the rest.

---

## 🔄 Migration Guide (for existing users)

If anyone is already using the old API:

### Old Code
```python
from logsentry_sdk import init

init(api_key="sk_...", dsn="https://api.logsentry.io")
```

### New Code
```python
import sentry_logger as sentry

sentry.init(api_key="sk_...")
```

**Changes:**
1. Import as `sentry` instead of importing `init`
2. Remove `dsn` parameter
3. (Optional) Set `LOGSENTRY_URL` env var if not using default

---

## ✅ Implementation Checklist

- ✅ Updated `sdk/python/sentry_logger/__init__.py`
  - Remove `dsn` parameter
  - Use `LOGSENTRY_URL` env var
  - Default to `https://api.logsentry.io`

- ✅ Updated `sdk/python/sentry_logger/config.py`
  - Removed `dsn` field
  - Added `_backend_url` with env var fallback

- ✅ Updated all documentation
  - README.md
  - ENVIRONMENTS.md
  - SDK-QUICK-START.md
  - DEVELOPER_JOURNEY.md

- ✅ Updated example app
  - examples/myApp/main.py
  - Uses new `sentry.init()` API
  - Uses `LOGSENTRY_API_KEY` env var

- ✅ Updated docker-compose.yml
  - Changed `SENTRY_DSN` → `LOGSENTRY_URL`
  - Changed `SENTRY_API_KEY` → `LOGSENTRY_API_KEY`

---

## 🎯 Result

**Developers love simple APIs!**

Before: 😕 "Wait, what's a DSN?"
After: 😍 "Just my API key? Perfect!"

---

**Clean, simple, production-ready!** 🚀
