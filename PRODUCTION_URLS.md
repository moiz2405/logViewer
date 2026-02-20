# 🔗 Production URLs Configuration

Configure these in your deployment:

---

## 📍 URL Structure

### Frontend (Vercel)
```
Production:  https://logsentry.io
Staging:     https://staging.logsentry.io (optional)
```

### Backend (VPS)
```
Production:  https://api.logsentry.io
Staging:     https://api-staging.logsentry.io (optional)
```

---

## 🔧 Environment Variables

### Frontend (.env.production)
```bash
NEXTAUTH_URL=https://logsentry.io
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
# ... other vars
```

### Backend (.env.production)
```bash
SDK_VERIFICATION_BASE_URL=https://logsentry.io
SDK_DEFAULT_DSN=https://api.logsentry.io
# ... other vars
```

---

## 📝 SDK Usage (Production)

Users will install and use like this:

```python
# Install
pip install logsentry-sdk

# Use in their app
from logsentry_sdk import init

init(
    api_key=os.getenv("LOGSENTRY_API_KEY"),
    dsn="https://api.logsentry.io"  # Your production backend
)
```

---

## 🌐 DNS Configuration

```
# A Records
api.logsentry.io  → VPS_IP_ADDRESS

# Vercel handles
logsentry.io      → Vercel (configured in Vercel dashboard)
www.logsentry.io  → Vercel (configured in Vercel dashboard)
```

---

## ✅ Checklist

- [ ] Domain purchased
- [ ] DNS configured
- [ ] SSL certificates obtained
- [ ] Environment variables set
- [ ] CORS allows production domains
- [ ] Google OAuth configured for production URLs
- [ ] SDK published with production DSN in docs
