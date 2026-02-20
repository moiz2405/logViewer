# ✅ Frontend Deployment Checklist

Quick checklist before deploying to Vercel.

---

## 📋 Pre-Deployment Checks

### 1. Environment Variables Ready

Create `frontend/.env.production.local` (for your reference - DON'T commit):

```bash
# Google OAuth (from console.cloud.google.com)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# NextAuth
NEXTAUTH_SECRET=  # Generate with: openssl rand -base64 32
NEXTAUTH_URL=https://logsentry.vercel.app

# Backend (update after backend deployed)
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

> **No Supabase creds needed!** Backend handles database access.

**PowerShell command to generate NEXTAUTH_SECRET:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

---

### 2. Code Quality Checks

```powershell
cd frontend

# Install dependencies
npm install

# Type check
npm run build

# Should complete without errors ✅
```

---

### 3. Google OAuth Configuration

Before deploying, add Vercel URLs to Google OAuth:

1. Go to: https://console.cloud.google.com/apis/credentials
2. Select your OAuth 2.0 Client ID
3. Add Authorized redirect URIs:
   ```
   https://logsentry.vercel.app/api/auth/callback/google
   ```
4. Add Authorized JavaScript origins:
   ```
   https://logsentry.vercel.app
   ```
5. Click Save

---

### 4. GitHub Repository

```powershell
# Make sure code is pushed
cd d:\projects\sentry

git status
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

---

## 🚀 Quick Deploy Commands

### Option 1: Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import GitHub repo
4. Set Root Directory: `frontend`
5. Add environment variables
6. Click Deploy

---

### Option 2: Vercel CLI

```powershell
# Install CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Login
vercel login

# Deploy
vercel --prod
```

---

## 🔍 Post-Deployment Verification

After deployment, test these:

```
✅ Visit: https://logsentry.vercel.app
✅ Click "Sign In" → Google OAuth works
✅ Dashboard loads
✅ No console errors (F12)
✅ Profile menu works
```

---

## 📝 Save These URLs

After deployment:

```
Frontend URL: https://logsentry.vercel.app
Vercel Dashboard: https://vercel.com/YOUR_USERNAME/logsentry
```

---

## ⚠️ Common Issues

**Build Fails:**
- Check: `cd frontend && npm run build` locally first
- Fix TypeScript errors before deploying

**OAuth Not Working:**
- Verify redirect URIs in Google Console
- Check NEXTAUTH_URL matches deployment URL
- Ensure all OAuth env vars are set in Vercel

**Environment Variables Missing:**
- Add them in Vercel Dashboard → Settings → Environment Variables
- Select "Production" environment
- Redeploy after adding

---

## 🎯 Next Step

After frontend is deployed:
→ Deploy backend following `PRODUCTION_DEPLOYMENT.md`
→ Update `NEXT_PUBLIC_BACKEND_URL` in Vercel
→ Redeploy frontend

---

**Ready to deploy? Follow `DEPLOY_FRONTEND_VERCEL.md`!** 🚀
