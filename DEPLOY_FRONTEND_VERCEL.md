# 🚀 Deploy Frontend to Vercel - Step by Step

Deploy your LogSentry frontend to Vercel in **10 minutes**!

---

## ✅ Prerequisites

- GitHub account
- Vercel account (free at [vercel.com](https://vercel.com))
- Your code pushed to GitHub

---

## 📋 Step-by-Step Deployment

### Step 1: Push to GitHub

```powershell
# Navigate to your project
cd d:\projects\sentry

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - LogSentry platform"

# Create a new repository on GitHub (github.com/new)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/logsentry.git
git branch -M main
git push -u origin main
```

---

### Step 2: Prepare Environment Variables

**Create a file to track your production secrets** (don't commit this!):

```powershell
# Create .env.production.local (for your reference only)
New-Item -Path "frontend\.env.production.local" -ItemType File -Force
```

**Add these values:**

```bash
# frontend/.env.production.local

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Google OAuth
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx

# NextAuth
NEXTAUTH_SECRET=your-random-secret-here
NEXTAUTH_URL=https://logsentry.vercel.app

# Backend API (update after backend is deployed)
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

**Generate NEXTAUTH_SECRET:**
```powershell
# PowerShell - Generate random secret
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

---

### Step 3: Update Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Select your OAuth 2.0 Client ID
3. Add **Authorized redirect URIs**:
   ```
   https://logsentry.vercel.app/api/auth/callback/google
   https://your-custom-domain.com/api/auth/callback/google
   ```
4. Add **Authorized JavaScript origins**:
   ```
   https://logsentry.vercel.app
   https://your-custom-domain.com
   ```
5. Click **Save**

---

### Step 4: Deploy to Vercel

#### Option A: Via Vercel Dashboard (Easiest)

1. **Go to [vercel.com](https://vercel.com) and sign in**

2. **Click "Add New Project"**

3. **Import your GitHub repository:**
   - Click "Import" next to your `logsentry` repo
   - If not visible, click "Adjust GitHub App Permissions"

4. **Configure Project:**
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build (auto-detected)
   Output Directory: .next (auto-detected)
   Install Command: npm install (auto-detected)
   ```

5. **Add Environment Variables:**
   Click "Environment Variables" and add each variable from `.env.production.local`:
   
   | Name | Value |
   |------|-------|
   | `NEXT_PUBLIC_SUPABASE_URL` | `https://xxxxx.supabase.co` |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJhbGci...` |
   | `SUPABASE_SERVICE_ROLE_KEY` | `eyJhbGci...` |
   | `GOOGLE_CLIENT_ID` | `xxxxx.apps.googleusercontent.com` |
   | `GOOGLE_CLIENT_SECRET` | `GOCSPX-xxxxx` |
   | `NEXTAUTH_SECRET` | `your-generated-secret` |
   | `NEXTAUTH_URL` | `https://logsentry.vercel.app` |
   | `NEXT_PUBLIC_BACKEND_URL` | `https://api.logsentry.io` |

6. **Click "Deploy"**

7. **Wait 2-3 minutes** ⏳

8. **Done!** 🎉 Your app is live at `https://logsentry.vercel.app`

---

#### Option B: Via Vercel CLI (Advanced)

```powershell
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Login to Vercel
vercel login

# Deploy (it will ask questions)
vercel

# Follow prompts:
# Set up and deploy? Yes
# Which scope? Your account
# Link to existing project? No
# Project name? logsentry
# Directory? ./ (current directory)

# Add environment variables
vercel env add NEXT_PUBLIC_SUPABASE_URL
# Paste value, press Enter
# Which environments? Production
# Repeat for all variables...

# Deploy to production
vercel --prod
```

---

### Step 5: Verify Deployment

1. **Open your Vercel URL:** `https://logsentry.vercel.app`

2. **Test Login:**
   - Click "Sign In"
   - Login with Google
   - Should redirect successfully ✅

3. **Test Dashboard:**
   - Should see empty dashboard (no apps yet)
   - No console errors ✅

4. **Check API Connection:**
   - Open DevTools Console (F12)
   - Look for errors
   - Backend calls will fail (expected - backend not deployed yet)

---

### Step 6: Add Custom Domain (Optional)

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Click "Add"

2. **Add your domain:**
   ```
   logsentry.io
   www.logsentry.io
   ```

3. **Update DNS:**
   Add these records in your domain registrar:
   
   ```
   Type    Name    Value
   A       @       76.76.21.21
   CNAME   www     cname.vercel-dns.com
   ```

4. **Wait for DNS propagation** (5-60 minutes)

5. **Update Environment Variables:**
   - In Vercel Dashboard → Settings → Environment Variables
   - Update `NEXTAUTH_URL` to `https://logsentry.io`
   - Redeploy

6. **Update Google OAuth:**
   - Add `https://logsentry.io/api/auth/callback/google` to Authorized redirect URIs

---

### Step 7: Update Backend URL (After Backend Deployed)

Once you deploy the backend to VPS:

1. **In Vercel Dashboard:**
   - Settings → Environment Variables
   - Edit `NEXT_PUBLIC_BACKEND_URL`
   - Change to: `https://api.logsentry.io` (your backend URL)

2. **Redeploy:**
   ```powershell
   # Trigger redeploy
   vercel --prod
   ```

---

## 🔧 Troubleshooting

### Issue: "Google OAuth Error"

**Solution:**
```
1. Check Google Cloud Console redirect URIs match Vercel URL exactly
2. Make sure GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are set in Vercel
3. Verify NEXTAUTH_URL matches your deployment URL
```

### Issue: "Environment Variables Not Working"

**Solution:**
```
1. Go to Vercel Dashboard → Settings → Environment Variables
2. Verify all variables are set for "Production"
3. Redeploy the project (Deployments → ... → Redeploy)
```

### Issue: "API Calls Failing"

**Expected if backend not deployed yet!**
```
1. Frontend works independently for auth/UI
2. Backend calls will fail until you deploy backend
3. This is normal - deploy backend next
```

### Issue: "Build Failed"

**Check logs:**
```powershell
# In Vercel Dashboard
Deployments → Click failed deployment → View Build Logs
```

**Common fixes:**
```
1. Missing environment variables
2. TypeScript errors (check locally: npm run build)
3. Missing dependencies (check package.json)
```

---

## 📊 Expected Results

### ✅ After Frontend Deployment

**Working:**
- ✅ Landing page
- ✅ Google OAuth login
- ✅ Dashboard UI
- ✅ User profile
- ✅ "Add App" form (UI only)

**Not Working (Expected):**
- ❌ Creating apps (backend not deployed)
- ❌ Viewing logs (backend not deployed)
- ❌ API key generation (backend not deployed)

**This is normal!** These will work once you deploy the backend.

---

## 🎯 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Environment variables configured
- [ ] Google OAuth redirect URIs updated
- [ ] Deployment successful
- [ ] Can access frontend URL
- [ ] Google login works
- [ ] Dashboard UI loads
- [ ] (Optional) Custom domain configured

---

## 🔄 Next Steps

### 1. Test Frontend ✅
```
Visit: https://logsentry.vercel.app
Login with Google
Verify dashboard loads
```

### 2. Deploy Backend 🚀
```
Follow: PRODUCTION_DEPLOYMENT.md
Deploy backend to VPS
Get backend URL: https://api.logsentry.io
```

### 3. Connect Frontend to Backend 🔗
```
Update NEXT_PUBLIC_BACKEND_URL in Vercel
Redeploy frontend
Test full flow: Create app → Generate API key → View logs
```

---

## 📝 Important URLs to Save

```bash
# Frontend
Production URL: https://logsentry.vercel.app
Custom Domain: https://logsentry.io (if configured)

# Vercel Dashboard
https://vercel.com/your-username/logsentry

# GitHub Repo
https://github.com/YOUR_USERNAME/logsentry
```

---

## 🎉 Congratulations!

Your frontend is now live on Vercel! 🚀

**Next:** Deploy the backend to VPS following `PRODUCTION_DEPLOYMENT.md`

---

## 💡 Pro Tips

### Automatic Deployments
- Vercel auto-deploys on every `git push` to main
- Preview deployments for every PR
- No need to manually redeploy

### Environment Variables
- Store secrets in Vercel Dashboard, not in code
- Different values for Preview vs Production
- Can update without redeploying

### Monitoring
- Check Vercel Dashboard for deployment status
- View logs in real-time
- Analytics available (page views, performance)

### Free Tier Limits
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- Global CDN

---

**Happy deploying! 🎊**
