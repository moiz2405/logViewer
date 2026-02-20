# 🎯 Quick Production Setup Guide

Follow these steps to deploy LogSentry to production:

---

## ⚡ Fast Track (30 minutes)

### 1. Setup VPS (5 min)
```bash
# Get a VPS (DigitalOcean, Hetzner, AWS, etc.)
# Ubuntu 22.04, 2GB RAM minimum
# Note your IP address
```

### 2. Configure DNS (2 min)
```
# Add A records:
api.logsentry.io  →  YOUR_VPS_IP
```

### 3. Deploy Backend (10 min)
```bash
# SSH into VPS
ssh root@YOUR_VPS_IP

# Download and run deployment script
curl -fsSL https://raw.githubusercontent.com/yourname/sentry/main/deploy-production.sh -o deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh

# Follow prompts to:
# - Enter repository URL
# - Configure .env.production
# - Get SSL certificate
```

### 4. Setup Supabase (5 min)
```bash
# 1. Create project at supabase.com
# 2. Run migrations from supabase/migrations/
# 3. Note your connection details
# 4. Update .env.production on VPS
```

### 5. Deploy Frontend (5 min)
```bash
# In your local terminal:
cd frontend
vercel login
vercel --prod

# Or push to GitHub and deploy via Vercel dashboard
```

### 6. Configure OAuth (3 min)
```
# Google Cloud Console:
Authorized origins:     https://logsentry.io
Authorized redirects:   https://logsentry.io/api/auth/callback/google
```

### 7. Test (5 min)
```bash
# Test backend
curl https://api.logsentry.io/health

# Test frontend  
# Visit https://logsentry.io
# Login with Google
# Create test app
# Get API key

# Test SDK
pip install logsentry-sdk
python -c "from logsentry_sdk import init; init(api_key='your-key', dsn='https://api.logsentry.io')"
```

---

## 🎯 That's it!

Your production Sentry clone is live at:
- Frontend: https://logsentry.io
- Backend: https://api.logsentry.io

Users can now:
1. Visit https://logsentry.io
2. Login
3. Create apps
4. Get API keys
5. Install SDK: `pip install logsentry-sdk`
6. Start monitoring!

---

## 📚 Detailed Guides

- [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) - Full deployment guide
- [PRODUCTION_URLS.md](PRODUCTION_URLS.md) - URL configuration
- [DEVELOPER_JOURNEY.md](DEVELOPER_JOURNEY.md) - For your users
