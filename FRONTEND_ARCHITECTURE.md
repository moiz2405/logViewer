# 🎯 Frontend Architecture - Direct Backend API Calls

## ✅ Clean Architecture Achieved!

**Frontend DOES NOT:**
- ❌ Access Supabase directly
- ❌ Use Next.js API routes as middleware
- ❌ Expose database credentials

**Frontend DOES:**
- ✅ Call backend API directly via utility
- ✅ Keep all secrets in backend
- ✅ Use simple, clean API client

---

## 📁 Structure

```
frontend/
├── lib/
│   └── api/
│       └── backend-api.ts          ← Single source of truth for API calls
│
├── components/
│   ├── dashboard/
│   │   └── section-cards.tsx       ← Uses backendAPI.getApps()
│   ├── register/
│   │   └── AddAppContent.tsx       ← Uses backendAPI.createApp()
│   └── appscreen/
│       └── LogRatiosPopover.tsx    ← Uses backendAPI.updateDemoLogRatios()
│
└── app/
    └── api/                        ← DELETED (not needed!)
        ├── project/                ← REMOVED
        └── summarize/              ← REMOVED
```

---

## 🔧 Backend API Client (`lib/api/backend-api.ts`)

### Configuration

```typescript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8001';
```

**Environment Variable:**
- `NEXT_PUBLIC_BACKEND_URL` - Your backend URL (default: http://localhost:8001)

---

### Available Methods

#### Apps Management

```typescript
// Get all apps for a user
await backendAPI.getApps(userId)

// Get specific app
await backendAPI.getApp(appId)

// Create new app
await backendAPI.createApp({
  user_id: userId,
  name: "My App",
  description: "Optional description"
})

// Delete app
await backendAPI.deleteApp(appId)
```

#### Logs

```typescript
// Get logs for an app
await backendAPI.getLogs(appId, {
  level: 'ERROR',
  limit: 100,
  offset: 0,
  start_time: '2026-01-01T00:00:00Z',
  end_time: '2026-02-20T23:59:59Z'
})

// Ingest logs (used by SDK, included for completeness)
await backendAPI.ingestLogs({
  api_key: "sk_...",
  logs: [{ level: "INFO", message: "Test", timestamp: "..." }]
})
```

#### Analytics

```typescript
// Get app health metrics
await backendAPI.getAppHealth(appId)

// Get log statistics
await backendAPI.getLogStats(appId, "7d")
```

#### Summary

```typescript
// Get AI-generated log summary
await backendAPI.getSummary(appId, {
  start_time: '2026-02-01T00:00:00Z',
  end_time: '2026-02-20T23:59:59Z',
  level: 'ERROR'
})
```

#### Health Check

```typescript
// Check backend health
await backendAPI.healthCheck()
```

---

## 📝 Usage Examples

### Example 1: Load Apps in Dashboard

**Before (Bad - Using Next.js API route):**
```typescript
// ❌ frontend/components/dashboard/section-cards.tsx
fetch(`/api/project?user_id=${session.user.id}`)
  .then(res => res.json())
  .then(data => setApps(data))
```

**After (Good - Direct backend call):**
```typescript
// ✅ frontend/components/dashboard/section-cards.tsx
import { backendAPI } from "@/lib/api/backend-api"

backendAPI.getApps(session.user.id)
  .then(data => setApps(data))
  .catch(error => console.error('Failed to load apps:', error))
```

---

### Example 2: Create New App

**Before (Bad - Using Next.js API route):**
```typescript
// ❌ frontend/components/register/AddAppContent.tsx
const res = await fetch("/api/project", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ user_id, name, description })
})
const data = await res.json()
if (!res.ok) throw new Error(data.error)
```

**After (Good - Direct backend call):**
```typescript
// ✅ frontend/components/register/AddAppContent.tsx
import { backendAPI } from "@/lib/api/backend-api"

const data = await backendAPI.createApp({
  user_id,
  name,
  description
})
// Done! Error handling built into backendAPI
```

---

### Example 3: Delete App

**Before (Bad - Using Next.js API route):**
```typescript
// ❌
const res = await fetch('/api/project', {
  method: 'DELETE',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ app_id: appId })
})
if (!res.ok) throw new Error('Failed to delete')
```

**After (Good - Direct backend call):**
```typescript
// ✅
await backendAPI.deleteApp(appId)
```

---

## 🔒 Security Benefits

### 1. No Database Credentials in Frontend

**Before:**
```env
# ❌ Bad - Frontend had these
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...  # DANGEROUS!
```

**After:**
```env
# ✅ Good - Only backend URL
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

### 2. Backend Controls Access

- Frontend can't bypass permissions
- All validation in backend
- Rate limiting in backend
- API keys validated server-side

### 3. Single Point of Control

- Change database? Update backend only
- Add caching? Backend only
- Add rate limiting? Backend only
- Frontend stays simple

---

## 🚀 Deployment

### Environment Variables (Frontend)

**Development:**
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8001
```

**Production:**
```env
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

### Vercel Deployment

Only need these env vars:
```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
NEXTAUTH_SECRET=...
NEXTAUTH_URL=https://logsentry.vercel.app
NEXT_PUBLIC_BACKEND_URL=https://api.logsentry.io
```

**No Supabase credentials needed!** ✅

---

## 📊 Comparison

| Aspect | Before (Bad) | After (Good) |
|--------|-------------|--------------|
| **API Calls** | Next.js API routes → Backend | Direct backend calls |
| **Database Access** | Frontend had Supabase creds | Backend only |
| **Code Complexity** | 3 API route files + fetch calls | 1 utility file |
| **Security** | Credentials in frontend | Credentials in backend only |
| **Type Safety** | Manual typing | TypeScript types exported |
| **Error Handling** | Scattered in components | Centralized in utility |
| **Maintenance** | Update multiple files | Update one file |

---

## ✅ Benefits Summary

1. **Simpler Frontend**
   - One import: `import { backendAPI } from "@/lib/api/backend-api"`
   - Clean method calls: `backendAPI.getApps(userId)`
   - No manual fetch, JSON parsing, error handling

2. **Better Security**
   - No database credentials in frontend
   - Backend controls all access
   - Can't bypass permissions

3. **Easier Maintenance**
   - Update API client once
   - All components automatically updated
   - TypeScript catches errors

4. **Faster Development**
   - No need to create API routes
   - Copy-paste from examples
   - IntelliSense shows available methods

5. **Better Architecture**
   - Clear separation of concerns
   - Frontend = UI only
   - Backend = Data + Business logic

---

## 🎯 Migration Checklist

- ✅ Created `lib/api/backend-api.ts`
- ✅ Updated `section-cards.tsx` to use backendAPI
- ✅ Updated `AddAppContent.tsx` to use backendAPI
- ✅ Updated `LogRatiosPopover.tsx` to use backendAPI
- ✅ Removed `/api/project/route.ts`
- ✅ Removed `/api/project/[appId]/route.ts`
- ✅ Removed `/api/summarize/route.ts`
- ✅ Removed `lib/db/supabaseClient.ts`
- ✅ Updated deployment docs (no Supabase creds)
- ✅ Simplified environment variables

---

## 📖 For Future Development

**Adding a new backend endpoint?**

1. Add method to `lib/api/backend-api.ts`:
```typescript
async getNewFeature(id: string) {
  return this.request(`/new-feature/${id}`);
}
```

2. Use in component:
```typescript
import { backendAPI } from "@/lib/api/backend-api";
const data = await backendAPI.getNewFeature(id);
```

**That's it!** No Next.js API routes needed!

---

**Clean, simple, secure architecture!** 🎉
