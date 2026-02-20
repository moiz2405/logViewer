# 🔄 Complete Integration Flow

This document describes the **complete end-to-end flow** from a developer discovering your Sentry clone to seeing their logs in the dashboard.

---

## 📊 Flow Overview

```
┌─────────────┐
│  Developer  │
└──────┬──────┘
       │
       ▼
[Discovers Platform] → [Creates Account] → [Registers App] → [Gets API Key]
       │                      │                  │                  │
       ▼                      ▼                  ▼                  ▼
[Installs SDK] → [Initializes in Code] → [Deploys App] → [Views Logs]
```

---

## 🎬 Detailed Flow

### Phase 1: Discovery & Setup (5 minutes)

#### Step 1: Developer Visits Platform

**What happens:**
- Developer visits `https://logs.yourapp.com` (or `localhost:3000` for local)
- Sees landing page with features
- Clicks "Get Started" or "Login"

**User sees:**
```
┌────────────────────────────────────┐
│  Sentry Clone - Log Monitoring     │
│  ────────────────────────────────  │
│  • Real-time log streaming         │
│  • AI-powered summaries            │
│  • Smart alerting                  │
│                                    │
│  [ Login with Google ]             │
└────────────────────────────────────┘
```

#### Step 2: Google OAuth Login

**What happens:**
1. User clicks "Login with Google"
2. Redirects to Google OAuth consent screen
3. User authorizes app
4. Google redirects back with auth code
5. NextAuth exchanges code for user info
6. User record created/updated in Supabase `users` table
7. Session created, user lands on dashboard

**Backend flow:**
```
Frontend → Google OAuth → NextAuth → Supabase
  │                          │            │
  └─────────────────────────┴────────────┘
              User Session Created
```

**User sees:**
```
┌────────────────────────────────────┐
│  Dashboard                     [👤] │
│  ────────────────────────────────  │
│  Welcome, John!                    │
│                                    │
│  No apps yet. Get started:         │
│  [ + Add Your First App ]          │
└────────────────────────────────────┘
```

---

### Phase 2: App Registration (2 minutes)

#### Step 3: Register Application

**What happens:**
1. User clicks "Add App" button
2. Modal/page opens with registration form
3. User enters:
   - App name: `"my-ecommerce-api"`
   - Description: `"Production e-commerce backend"`
4. Clicks "Register App"

**Frontend code:**
```typescript
// POST /api/project
{
  user_id: session.user.id,
  name: "my-ecommerce-api",
  description: "Production e-commerce backend"
}
```

**Backend flow:**
```
Frontend                Backend                 Database
   │                       │                       │
   ├─POST /api/project────>│                       │
   │                       ├─Generate UUID────────>│
   │                       │                       │
   │                       ├─Generate API Key      │
   │                       │  (sk_RANDOM_STRING)   │
   │                       │                       │
   │                       ├─Hash API key          │
   │                       │  (bcrypt)             │
   │                       │                       │
   │                       ├─INSERT INTO apps─────>│
   │                       │  (id, name, user_id)  │
   │                       │                       │
   │                       ├─INSERT api_key───────>│
   │                       │  (app_id, key_hash)   │
   │                       │                       │
   │<──Returns {           │                       │
   │     id,               │                       │
   │     name,             │                       │
   │     api_key (plain)   │                       │
   │   }────────────────────┘                      │
```

**Database changes:**
```sql
-- apps table
INSERT INTO apps (id, name, description, user_id, created_at)
VALUES (
  'app_abc123',
  'my-ecommerce-api',
  'Production e-commerce backend',
  'user_xyz789',
  NOW()
);

-- app_api_keys table
INSERT INTO app_api_keys (app_id, key_hash, created_at)
VALUES (
  'app_abc123',
  '$2b$12$hash...', -- bcrypt hash
  NOW()
);
```

#### Step 4: API Key Display (⚠️ Critical)

**What happens:**
- Frontend displays API key **ONLY ONCE**
- User must copy it now or lose it forever
- Instructions shown for SDK installation

**User sees:**
```
┌────────────────────────────────────────────┐
│  App Registered Successfully! ✅           │
│  ──────────────────────────────────────── │
│                                            │
│  ⚠️  Save this API key - shown only once!  │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ sk_1a2b3c4d5e6f7g8h9i0j...        [📋]│ │
│  └──────────────────────────────────────┘ │
│                                            │
│  Quick Start:                              │
│  ```bash                                   │
│  pip install sentry-logger                 │
│                                            │
│  # In your app:                            │
│  from sentry_logger import init            │
│  init(api_key="sk_1a2b...",                │
│       dsn="https://logs.yourapp.com")      │
│  ```                                       │
│                                            │
│  [ Add Another App ]  [ Go to Dashboard ]  │
└────────────────────────────────────────────┘
```

---

### Phase 3: SDK Integration (10 minutes)

#### Step 5: Developer Installs SDK

**In their terminal:**
```bash
# Option 1: From PyPI (if published)
pip install sentry-logger

# Option 2: From GitHub
pip install git+https://github.com/yourname/sentry.git#subdirectory=sdk/python

# Option 3: Local development
pip install -e /path/to/sentry/sdk/python
```

**What happens:**
- SDK package downloaded
- Dependencies installed (requests, etc.)
- CLI tool `sentry-logger` available

#### Step 6: Initialize SDK in Code

**Developer's app code:**
```python
# my_app/main.py
from fastapi import FastAPI
from sentry_logger import init
import os
import logging

# 🔑 Initialize SDK (BEFORE app creation)
init(
    api_key=os.getenv("SENTRY_API_KEY"),
    dsn=os.getenv("SENTRY_DSN", "https://logs.yourapp.com")
)

app = FastAPI()

@app.get("/")
def read_root():
    logging.info("Root endpoint accessed")
    return {"status": "ok"}

@app.post("/orders")
def create_order(order: dict):
    logging.info(f"Creating order: {order}")
    try:
        # Process order
        logging.info("Order created successfully")
        return {"id": "order_123"}
    except Exception as e:
        logging.error(f"Order creation failed: {e}")
        raise
```

**SDK initialization flow:**
```
init(api_key, dsn)
  │
  ├─1. Validate API key format
  │   └─ Check starts with "sk_"
  │
  ├─2. Store config
  │   ├─ API key (in memory)
  │   └─ DSN URL
  │
  ├─3. Setup logging handler
  │   ├─ Intercept logging.info/warning/error
  │   └─ Add custom handler
  │
  ├─4. Start background thread
  │   ├─ Batch queue for logs
  │   └─ Flush every 5 seconds OR when batch full
  │
  └─5. Test connection
      └─ Send ping to DSN /health (optional)
```

#### Step 7: Set Environment Variables

**Developer creates `.env`:**
```bash
# .env
SENTRY_API_KEY=sk_1a2b3c4d5e6f7g8h9i0j...
SENTRY_DSN=https://logs.yourapp.com
```

**Or exports in shell:**
```bash
export SENTRY_API_KEY=sk_1a2b3c4d5e6f7g8h9i0j...
export SENTRY_DSN=https://logs.yourapp.com
```

---

### Phase 4: Runtime & Log Flow (Continuous)

#### Step 8: Application Starts

**What happens:**
```
Developer runs: python main.py
  │
  ├─1. Python imports sentry_logger
  │
  ├─2. init() called
  │   ├─ Reads SENTRY_API_KEY from env
  │   ├─ Reads SENTRY_DSN from env
  │   ├─ Validates API key
  │   ├─ Sets up logging handler
  │   └─ Starts background thread
  │
  ├─3. FastAPI app starts
  │
  └─4. App ready to handle requests
```

**Console output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Sentry SDK initialized - logs will be sent to dashboard
INFO:     Application startup complete.
```

#### Step 9: Logs Generated & Sent

**When user hits endpoint:**
```
User Request → FastAPI → logging.info() → SDK captures
```

**SDK batching logic:**
```python
# Pseudocode
class SentryHandler:
    def __init__(self):
        self.batch = []
        self.batch_size = 100
        self.last_flush = time.time()
    
    def emit(self, record):
        log_entry = {
            "timestamp": record.created,
            "level": record.levelname,
            "message": record.getMessage(),
            "service": "api",
            "extra": record.__dict__
        }
        
        self.batch.append(log_entry)
        
        # Flush if batch full OR 5 seconds passed
        if len(self.batch) >= self.batch_size or \
           time.time() - self.last_flush > 5.0:
            self.flush()
    
    def flush(self):
        if not self.batch:
            return
            
        # Send to backend
        requests.post(
            f"{self.dsn}/ingest",
            json={
                "api_key": self.api_key,
                "logs": self.batch
            }
        )
        
        self.batch = []
        self.last_flush = time.time()
```

**HTTP request to backend:**
```http
POST /ingest HTTP/1.1
Host: logs.yourapp.com
Content-Type: application/json

{
  "api_key": "sk_1a2b3c4d5e6f7g8h9i0j...",
  "logs": [
    {
      "timestamp": 1708473600.123,
      "level": "INFO",
      "message": "Root endpoint accessed",
      "service": "api"
    },
    {
      "timestamp": 1708473601.456,
      "level": "INFO",
      "message": "Creating order: {...}",
      "service": "api"
    }
  ]
}
```

---

### Phase 5: Backend Processing (Milliseconds)

#### Step 10: Backend Receives Logs

**Backend flow:**
```
POST /ingest
  │
  ├─1. Extract API key from payload
  │
  ├─2. Validate API key
  │   ├─ Query: SELECT app_id FROM app_api_keys WHERE key_hash = bcrypt(api_key)
  │   └─ If not found: Return 401 Unauthorized
  │
  ├─3. Resolve app_id
  │   └─ app_id = "app_abc123"
  │
  ├─4. Store logs in database
  │   └─ INSERT INTO logs (app_id, timestamp, level, message, ...)
  │
  ├─5. Update metrics
  │   └─ UPDATE app_metrics SET log_count = log_count + N
  │
  ├─6. Check alert rules (async)
  │   └─ If error_rate > threshold: Send notification
  │
  ├─7. Trigger AI summary (async, batched)
  │   └─ Queue for GPT analysis
  │
  └─8. Return 200 OK
```

**Database insert:**
```sql
INSERT INTO logs (
  id,
  app_id,
  timestamp,
  level,
  message,
  service,
  created_at
)
VALUES
  ('log_1', 'app_abc123', '2024-02-20 10:30:00', 'INFO', 'Root endpoint accessed', 'api', NOW()),
  ('log_2', 'app_abc123', '2024-02-20 10:30:01', 'INFO', 'Creating order: {...}', 'api', NOW());
```

---

### Phase 6: Dashboard Display (Real-time)

#### Step 11: Developer Views Logs

**What happens:**
1. Developer goes to `https://logs.yourapp.com`
2. Clicks on "my-ecommerce-api" in sidebar
3. Frontend calls `GET /api/logs?app_id=app_abc123`
4. Backend queries Supabase
5. Returns logs
6. Frontend displays in real-time table

**Frontend polling (or WebSocket):**
```typescript
// Auto-refresh every 5 seconds
useEffect(() => {
  const interval = setInterval(() => {
    fetchLogs(appId);
  }, 5000);
  
  return () => clearInterval(interval);
}, [appId]);
```

**User sees:**
```
┌──────────────────────────────────────────────────────┐
│  my-ecommerce-api                            [🔴 LIVE]│
│  ────────────────────────────────────────────────────│
│  📊 Health: ✅ Good    Errors: 2    Logs/min: 45     │
│  ────────────────────────────────────────────────────│
│  Timestamp          Level    Service  Message        │
│  ────────────────────────────────────────────────────│
│  10:30:01  INFO     api      Creating order: {...}   │
│  10:30:00  INFO     api      Root endpoint accessed  │
│  10:29:58  ERROR    payment  Transaction failed      │
│  10:29:55  INFO     auth     User logged in          │
│  ...                                                  │
│  ────────────────────────────────────────────────────│
│  [Filter] [Export] [Set Alert]                       │
└──────────────────────────────────────────────────────┘
```

---

## 🔐 Alternative: CLI Device Flow

For power users, there's also a CLI-based OAuth flow:

### CLI Flow Diagram

```
Developer Terminal          Frontend                Backend                Database
       │                       │                       │                       │
       ├─sentry-logger init──>│                       │                       │
       │                       │                       │                       │
       │                       │<─POST /sdk/device/start                       │
       │                       │                       │                       │
       │                       │                       ├─Generate device_code─>│
       │                       │                       ├─Generate user_code   │
       │                       │                       ├─INSERT session───────>│
       │                       │                       │                       │
       │<─────────────────────┴─Returns {              │                       │
       │                         device_code,          │                       │
       │                         user_code,            │                       │
       │                         verification_url      │                       │
       │                       }                       │                       │
       │                                               │                       │
       ├─Opens browser to:                            │                       │
       │  /sdk/link?code=ABC123                       │                       │
       │                       │                       │                       │
       │                    [User logs in with Google] │                       │
       │                       │                       │                       │
       │                       ├─POST /sdk/device/complete                     │
       │                       │  {user_code, app_name}│                       │
       │                       │                       │                       │
       │                       │                       ├─Verify user_code────>│
       │                       │                       ├─Create app──────────>│
       │                       │                       ├─Generate API key     │
       │                       │                       ├─Update session──────>│
       │                       │                       │  with api_key         │
       │                       │                       │                       │
       │                       │<─Returns success─────┘                       │
       │                                                                       │
       ├─Polls GET /sdk/device/poll?device_code=...                           │
       │  (every 2 seconds)    │                       │                       │
       │                       │                       │<─Query session───────┤
       │                       │                       │                       │
       │<──────────────────────┴─Returns {             │                       │
       │                         status: "complete",   │                       │
       │                         api_key: "sk_..."     │                       │
       │                       }                       │                       │
       │                                                                       │
       ├─Save to ~/.sentry_logger/config.json                                 │
       │                                                                       │
       └─✅ Setup complete!                                                     │
```

---

## 📊 Summary

**Total time:** ~15 minutes from discovery to seeing logs

**Steps:**
1. ✅ Visit platform (1 min)
2. ✅ Login with Google (1 min)
3. ✅ Register app (2 min)
4. ✅ Copy API key (1 min)
5. ✅ Install SDK (2 min)
6. ✅ Initialize in code (5 min)
7. ✅ Set env vars (1 min)
8. ✅ Run app (1 min)
9. ✅ View logs (1 min)

**Developer gets:**
- 📊 Real-time log streaming
- 🎯 Health metrics
- 🤖 AI summaries
- 🔔 Smart alerts
- 🔍 Searchable logs

---

**This is the complete flow!** 🎉
