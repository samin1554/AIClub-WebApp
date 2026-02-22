# Deployment Guide

## Overview
This guide covers deploying the AI Club app to production.

**Recommended Stack**:
- Frontend: Vercel
- Backend: Railway / Render
- Database: Neon / Supabase
- Redis: Upstash
- Object Storage: Cloudflare R2 / AWS S3

---

## Environment Setup

### Development
- Local PostgreSQL
- Local Redis (optional)
- `.env` files with dev credentials

### Staging
- Staging database (separate from prod)
- Staging API URL
- Test API keys (OpenAI, Spotify)

### Production
- Production database with backups
- Production API URL
- Production API keys
- SSL/TLS enabled
- Rate limiting enabled

---

## Frontend Deployment (Vercel)

### Initial Setup

1. **Connect Repository**
   - Go to vercel.com
   - Import GitHub repository
   - Select `apps/web` as root directory

2. **Configure Build Settings**
   ```
   Framework Preset: Next.js
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://api.aiclub.app/api/v1
   NEXT_PUBLIC_APP_URL=https://aiclub.app
   NEXT_PUBLIC_SENTRY_DSN=...
   ```

4. **Deploy**
   - Push to `main` branch
   - Vercel auto-deploys

### Custom Domain
1. Add domain in Vercel dashboard
2. Update DNS records:
   ```
   A     @     76.76.21.21
   CNAME www   cname.vercel-dns.com
   ```
3. SSL certificate auto-provisioned

### Preview Deployments
- Every PR gets a preview URL
- Test changes before merging
- Share with team for review

---

## Backend Deployment (Railway)

### Initial Setup

1. **Create Project**
   - Go to railway.app
   - New Project → Deploy from GitHub
   - Select repository

2. **Add Services**
   - **API Service**: Python app
   - **PostgreSQL**: Database
   - **Redis**: Cache (optional)

3. **Configure API Service**
   ```
   Root Directory: apps/api
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables**
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   SECRET_KEY=<generate-secure-key>
   OPENAI_API_KEY=<your-key>
   SPOTIFY_CLIENT_ID=<your-id>
   SPOTIFY_CLIENT_SECRET=<your-secret>
   CORS_ORIGINS=https://aiclub.app,https://www.aiclub.app
   ```

5. **Run Migrations**
   ```bash
   railway run alembic upgrade head
   ```

### Custom Domain
1. Add domain in Railway dashboard
2. Update DNS:
   ```
   CNAME api railway.app
   ```

---

## Database Setup (Neon)

### Create Database

1. **Sign up at neon.tech**
2. **Create Project**: "AI Club Production"
3. **Get Connection String**:
   ```
   postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/aiclub?sslmode=require
   ```

### Configure Backups
- Neon auto-backups daily
- Point-in-time recovery available
- Test restore process monthly

### Connection Pooling
- Use Neon's built-in pooler
- Max connections: 100
- Idle timeout: 10 minutes

---

## Redis Setup (Upstash)

### Create Database

1. **Sign up at upstash.com**
2. **Create Database**: "AI Club Redis"
3. **Get Connection String**:
   ```
   redis://default:xxx@us1-xxx.upstash.io:6379
   ```

### Configure
- Enable TLS
- Set eviction policy: `allkeys-lru`
- Max memory: 256MB (adjust based on usage)

---

## Object Storage (Cloudflare R2)

### Setup

1. **Create R2 Bucket**: "aiclub-media"
2. **Configure CORS**:
   ```json
   {
     "AllowedOrigins": ["https://aiclub.app"],
     "AllowedMethods": ["GET", "PUT", "POST"],
     "AllowedHeaders": ["*"],
     "MaxAgeSeconds": 3600
   }
   ```

3. **Create API Token**
   - Permissions: Read & Write
   - Add to backend env vars

### Usage
```python
# Backend: Upload file
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='https://xxx.r2.cloudflarestorage.com',
    aws_access_key_id=settings.R2_ACCESS_KEY,
    aws_secret_access_key=settings.R2_SECRET_KEY,
)

s3.upload_file('local.jpg', 'aiclub-media', 'projects/cover.jpg')
```

---

## SSL/TLS Configuration

### Frontend (Vercel)
- Auto-provisioned
- Renews automatically
- Force HTTPS enabled by default

### Backend (Railway)
- Auto-provisioned for custom domains
- Use HTTPS URLs in frontend

### Database (Neon)
- SSL required by default
- Connection string includes `sslmode=require`

---

## Monitoring & Logging

### Application Monitoring (Sentry)

1. **Setup Sentry**
   ```bash
   npm install @sentry/nextjs
   pip install sentry-sdk[fastapi]
   ```

2. **Configure Frontend**
   ```typescript
   // sentry.client.config.ts
   Sentry.init({
     dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
     environment: process.env.NODE_ENV,
     tracesSampleRate: 0.1,
   });
   ```

3. **Configure Backend**
   ```python
   # app/main.py
   import sentry_sdk
   
   sentry_sdk.init(
       dsn=settings.SENTRY_DSN,
       environment="production",
       traces_sample_rate=0.1,
   )
   ```

### Logging

**Backend**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("User logged in", extra={"user_id": user.id})
```

**Frontend**:
```typescript
// Use console in dev, Sentry in prod
const log = {
  info: (message: string, data?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(message, data);
    }
    // Send to analytics in production
  },
  error: (message: string, error?: Error) => {
    console.error(message, error);
    Sentry.captureException(error);
  },
};
```

---

## Performance Optimization

### Frontend
- Enable Next.js Image Optimization
- Use `next/font` for font optimization
- Enable compression in Vercel
- Set cache headers for static assets

### Backend
- Enable response compression (gzip)
- Use database connection pooling
- Cache frequently accessed data in Redis
- Add database indexes for common queries

### Database
```sql
-- Add indexes for common queries
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_tags ON projects USING GIN(tags);
CREATE INDEX idx_ideas_created_by ON ideas(created_by_member_id);
```

---

## Security Checklist

### Pre-Deployment
- [ ] All secrets in environment variables (not in code)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] SQL injection prevention (use parameterized queries)
- [ ] XSS prevention (sanitize user input)
- [ ] CSRF protection enabled
- [ ] Secure password hashing (bcrypt)
- [ ] JWT tokens in HTTP-only cookies
- [ ] HTTPS enforced
- [ ] Security headers configured

### Security Headers
```python
# Backend: Add security headers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

---

## Backup Strategy

### Database Backups
- **Automated**: Daily backups by Neon
- **Manual**: Weekly manual backup before major changes
- **Retention**: 30 days
- **Test restores**: Monthly

### Backup Command
```bash
# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20240115.sql
```

### Code Backups
- Git repository (GitHub)
- Multiple team members with access
- Protected main branch

---

## Rollback Procedure

### Frontend (Vercel)
1. Go to Vercel dashboard
2. Select deployment to rollback to
3. Click "Promote to Production"
4. Verify site works

### Backend (Railway)
1. Go to Railway dashboard
2. Select previous deployment
3. Click "Redeploy"
4. Run migrations if needed:
   ```bash
   railway run alembic downgrade -1
   ```

### Database
1. Stop backend service
2. Restore from backup:
   ```bash
   psql $DATABASE_URL < backup_20240115.sql
   ```
3. Restart backend service

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Code reviewed and approved
- [ ] Staging tested
- [ ] Database migrations ready
- [ ] Environment variables configured
- [ ] Backup created
- [ ] Team notified

### Deployment Steps
1. [ ] Merge PR to main
2. [ ] Verify CI/CD passes
3. [ ] Run database migrations
4. [ ] Deploy backend (Railway auto-deploys)
5. [ ] Deploy frontend (Vercel auto-deploys)
6. [ ] Verify deployment
7. [ ] Monitor for errors (Sentry)
8. [ ] Test critical flows

### Post-Deployment
- [ ] Verify site loads
- [ ] Test login/auth
- [ ] Check API health endpoint
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Update team

---

## Monitoring Dashboard

### Key Metrics to Track
- **Uptime**: 99.9% target
- **Response time**: < 200ms API, < 2s page load
- **Error rate**: < 0.1%
- **Database connections**: < 80% of max
- **Redis memory**: < 80% of max

### Tools
- **Vercel Analytics**: Frontend performance
- **Railway Metrics**: Backend CPU/memory
- **Sentry**: Error tracking
- **Uptime Robot**: Uptime monitoring

---

## Troubleshooting

### Site Down
1. Check Vercel/Railway status pages
2. Check error logs in Sentry
3. Verify database connection
4. Check recent deployments
5. Rollback if needed

### Slow Performance
1. Check database query performance
2. Check Redis hit rate
3. Review Sentry performance traces
4. Check for N+1 queries
5. Add database indexes if needed

### Database Connection Errors
1. Check connection pool settings
2. Verify DATABASE_URL is correct
3. Check database is running
4. Increase max connections if needed

---

## Cost Estimation

### Monthly Costs (Estimated)
- **Vercel**: $0 (Hobby) or $20 (Pro)
- **Railway**: $5-20 (usage-based)
- **Neon**: $0 (Free tier) or $19 (Pro)
- **Upstash**: $0 (Free tier) or $10 (Pro)
- **Cloudflare R2**: $0.015/GB storage
- **OpenAI API**: Variable (usage-based)
- **Total**: ~$50-100/month for small scale

### Scaling Costs
- Add more Railway instances: +$5-10 each
- Upgrade database: +$19-99/month
- More Redis memory: +$10-50/month
