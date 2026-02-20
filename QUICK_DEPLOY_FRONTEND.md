# 🎯 Quick Deploy - Frontend to Vercel

**Time: 10 minutes** | **Difficulty: Easy** ⭐

---

## 🚀 5-Step Deployment

### 1️⃣ **Prepare Secrets**

```powershell
# Generate NextAuth secret
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

Copy this output - you'll need it!

---

### 2️⃣ **Update Google OAuth**

Go to: https://console.cloud.google.com/apis/credentials

Add redirect URI:
```
https://logsentry.vercel.app/api/auth/callback/google
```

---

### 3️⃣ **Push to GitHub**

```powershell
cd d:\projects\sentry
git add .
git commit -m "Deploy to Vercel"
git push origin main
```

---

### 4️⃣ **Deploy on Vercel**

1. Visit: https://vercel.com
2. Click "Add New Project"
3. Import your `logsentry` repo
4. **Root Directory:** `frontend`
5. Add environment variables:

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
NEXTAUTH_SECRET=<paste generated secret>
NEXTAUTH_URL=https://logsentry.vercel.app
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

6. Click **Deploy**

---

### 5️⃣ **Test It!**

Visit: `https://logsentry.vercel.app`
- ✅ Sign in with Google
- ✅ Dashboard loads
- ✅ No errors

---

## 📋 Environment Variables Quick Copy

| Variable | Get From |
|----------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase dashboard |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase dashboard → API |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase dashboard → API (secret) |
| `GOOGLE_CLIENT_ID` | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Google Cloud Console |
| `NEXTAUTH_SECRET` | Generate with command above |
| `NEXTAUTH_URL` | `https://logsentry.vercel.app` |
| `NEXT_PUBLIC_BACKEND_URL` | `https://api.logsentry.io` |

---

## 🆘 Need Help?

**Full guide:** See `DEPLOY_FRONTEND_VERCEL.md`

**Troubleshooting:**
- Build fails → Run `cd frontend && npm run build` locally
- OAuth fails → Check Google Console redirect URIs
- Env vars missing → Add in Vercel Dashboard → Redeploy

---

**That's it! Frontend deployed! 🎉**

**Next:** Deploy backend to VPS (see `PRODUCTION_DEPLOYMENT.md`)
