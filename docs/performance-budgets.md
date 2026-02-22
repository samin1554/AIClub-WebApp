# Performance Budgets

## Overview
Performance budgets ensure the app stays fast as we add features.
These are targets, not hard limits, but we should investigate if we exceed them.

---

## Page Load Performance

### Targets (Lighthouse Scores)
- **Performance**: ≥ 90
- **Accessibility**: ≥ 95
- **Best Practices**: ≥ 95
- **SEO**: ≥ 95

### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

### Page Load Times
- **Home page**: < 2s (first load), < 1s (cached)
- **Projects list**: < 2s
- **Project detail**: < 2.5s
- **Ideas board**: < 2s
- **Playground**: < 2s

---

## Bundle Size

### JavaScript Bundles
- **Initial bundle**: < 200 KB (gzipped)
- **Total JS**: < 500 KB (gzipped)
- **Per route**: < 100 KB (gzipped)

### CSS
- **Total CSS**: < 50 KB (gzipped)

### Images
- **Hero images**: < 200 KB (optimized)
- **Thumbnails**: < 50 KB
- **Icons**: Use SVG or icon fonts

### Fonts
- **Total fonts**: < 100 KB
- Use `next/font` for optimization
- Subset fonts to needed characters

---

## API Performance

### Response Times (95th percentile)
- **GET requests**: < 200ms
- **POST requests**: < 300ms
- **Complex queries**: < 500ms
- **AI requests** (chatbot, prompt lab): < 3s

### Database Queries
- **Simple queries**: < 50ms
- **Complex queries**: < 200ms
- **N+1 queries**: 0 (use eager loading)

### Rate Limits
- **Guest**: 100 requests/hour
- **Member**: 1000 requests/hour
- **Lead/Admin**: 5000 requests/hour
- **AI requests**: 20/hour per user

---

## Resource Limits

### Database
- **Connection pool**: 20 connections
- **Query timeout**: 30s
- **Max query size**: 10 MB

### Redis
- **Memory**: 256 MB (MVP), 1 GB (Phase 2)
- **Key expiry**: Set for all cached data
- **Max key size**: 1 MB

### Object Storage
- **Max file size**: 10 MB per file
- **Total storage**: 10 GB (MVP), 100 GB (Phase 2)
- **Allowed types**: images (jpg, png, webp), videos (mp4)

---

## Monitoring Thresholds

### Alerts
Trigger alerts when:
- **Error rate** > 1%
- **Response time** > 1s (95th percentile)
- **Database connections** > 80% of pool
- **Redis memory** > 80% of limit
- **Disk space** > 80% used

### Performance Degradation
Investigate when:
- **Page load time** increases by > 20%
- **API response time** increases by > 50%
- **Bundle size** increases by > 10%

---

## Optimization Strategies

### Frontend
1. **Code Splitting**
   - Lazy load routes
   - Lazy load heavy components (whiteboard, mini-games)
   - Use dynamic imports

2. **Image Optimization**
   - Use `next/image` for all images
   - Serve WebP format
   - Use appropriate sizes (srcset)
   - Lazy load below-the-fold images

3. **Caching**
   - Cache static assets (1 year)
   - Cache API responses (TanStack Query)
   - Use service worker (Phase 2)

4. **Reduce JavaScript**
   - Remove unused dependencies
   - Use tree-shaking
   - Minimize third-party scripts

### Backend
1. **Database Optimization**
   - Add indexes for common queries
   - Use connection pooling
   - Eager load relationships (avoid N+1)
   - Use database-level pagination

2. **Caching**
   - Cache frequently accessed data (Redis)
   - Cache API responses (short TTL)
   - Use ETags for conditional requests

3. **Query Optimization**
   - Use `EXPLAIN ANALYZE` to find slow queries
   - Add indexes where needed
   - Denormalize if necessary
   - Use database views for complex queries

4. **Response Optimization**
   - Enable gzip compression
   - Paginate large lists
   - Return only needed fields
   - Use streaming for large responses

---

## Testing Performance

### Tools
- **Lighthouse**: Page performance
- **WebPageTest**: Detailed analysis
- **Chrome DevTools**: Network, Performance tabs
- **k6 / Artillery**: Load testing
- **pgAdmin**: Database query analysis

### Load Testing
Run before major releases:
```bash
# Backend load test
k6 run load-test.js

# Expected results:
# - 100 concurrent users
# - < 200ms average response time
# - < 1% error rate
```

### Lighthouse CI
Run on every PR:
```yaml
# .github/workflows/lighthouse.yml
- name: Lighthouse CI
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: |
      https://preview.aiclub.app
    budgetPath: ./lighthouse-budget.json
```

---

## Budget Enforcement

### Pre-commit
- Run bundle size check
- Warn if bundle increases by > 5%

### CI/CD
- Fail build if bundle > 10% over budget
- Fail build if Lighthouse score < 80
- Warn if API response time > 500ms

### Code Review
- Review performance impact of changes
- Require justification for large dependencies
- Check for N+1 queries
- Verify images are optimized

---

## Performance Checklist

### Before Merging PR
- [ ] Bundle size within budget
- [ ] No new N+1 queries
- [ ] Images optimized
- [ ] API responses < 300ms
- [ ] No console errors/warnings
- [ ] Lighthouse score > 90

### Before Deploying
- [ ] Load test passes
- [ ] Database queries optimized
- [ ] Cache strategy in place
- [ ] CDN configured
- [ ] Monitoring set up

### Monthly Review
- [ ] Check bundle size trends
- [ ] Review slow API endpoints
- [ ] Analyze database query performance
- [ ] Check cache hit rates
- [ ] Review error rates

---

## Performance Goals by Phase

### MVP
- Home page loads in < 2s
- API responses < 300ms
- Lighthouse score > 85
- No major performance issues

### Phase 2
- Home page loads in < 1.5s
- API responses < 200ms
- Lighthouse score > 90
- Implement service worker
- Add performance monitoring dashboard

### Long-term
- Home page loads in < 1s
- API responses < 150ms
- Lighthouse score > 95
- Edge caching (Cloudflare)
- Real-time performance monitoring
