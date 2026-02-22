# Authentication & Authorization

## Overview
The app uses role-based access control (RBAC) with 4 roles:
- **Guest**: unauthenticated visitors
- **Member**: authenticated club members
- **Lead**: club leadership (project leads, officers)
- **Admin**: full system access

---

## Authentication Strategy

### Session Management
**Recommended approach**: JWT tokens + HTTP-only cookies

**Flow**:
1. User logs in with email/password
2. Backend validates credentials
3. Backend generates JWT with user ID + roles
4. JWT stored in HTTP-only cookie (secure, sameSite=strict)
5. Frontend includes cookie automatically on requests
6. Backend validates JWT on protected endpoints

**Token expiry**: 7 days (configurable)
**Refresh strategy**: Issue new token when < 1 day remaining

### Alternative: Session-based
- Store session ID in cookie
- Session data in Redis
- Simpler but requires Redis

---

## User Registration Flow

### For Club Members (Recommended)
**Option A: Invite-only**
1. Admin creates member account with email
2. System sends invite email with setup link
3. User clicks link, sets password
4. Account activated

**Option B: GitHub OAuth**
1. User clicks "Login with GitHub"
2. OAuth flow redirects to GitHub
3. User authorizes app
4. Backend creates/updates user record
5. User logged in

**Option C: Email/Password Signup**
1. User fills signup form
2. System sends verification email
3. User clicks verification link
4. Admin approves new member (optional)
5. Account activated

### For Public (Guests)
- No registration required to browse
- Must register to vote, comment, RSVP

---

## Password Requirements
- Minimum 8 characters
- At least 1 uppercase, 1 lowercase, 1 number
- No common passwords (check against list)
- Hashed with bcrypt (cost factor 12)

---

## Password Reset Flow
1. User clicks "Forgot Password"
2. Enters email
3. Backend generates reset token (expires in 1 hour)
4. Email sent with reset link
5. User clicks link, enters new password
6. Token validated and consumed
7. Password updated, user logged in

---

## Permissions Matrix

| Action | Guest | Member | Lead | Admin |
|--------|-------|--------|------|-------|
| **Projects** |
| View published projects | ✅ | ✅ | ✅ | ✅ |
| View draft projects | ❌ | ❌ | ✅ | ✅ |
| Create project | ❌ | ❌ | ✅ | ✅ |
| Edit project | ❌ | ❌ | ✅ (own) | ✅ |
| Delete project | ❌ | ❌ | ❌ | ✅ |
| **Ideas** |
| View ideas | ✅ | ✅ | ✅ | ✅ |
| Submit idea | ❌ | ✅ | ✅ | ✅ |
| Vote on idea | ❌ | ✅ | ✅ | ✅ |
| Comment on idea | ❌ | ✅ | ✅ | ✅ |
| Edit idea | ❌ | ✅ (own) | ✅ | ✅ |
| Delete idea | ❌ | ✅ (own) | ✅ | ✅ |
| Change idea status | ❌ | ❌ | ✅ | ✅ |
| Promote to request | ❌ | ❌ | ✅ | ✅ |
| **Requests** |
| Submit request | ✅ | ✅ | ✅ | ✅ |
| View request queue | ❌ | ✅ | ✅ | ✅ |
| Comment on request | ❌ | ✅ | ✅ | ✅ |
| Change request status | ❌ | ❌ | ✅ | ✅ |
| Assign request | ❌ | ❌ | ✅ | ✅ |
| Delete request | ❌ | ❌ | ❌ | ✅ |
| **Events** |
| View events | ✅ | ✅ | ✅ | ✅ |
| RSVP to event | ❌ | ✅ | ✅ | ✅ |
| Create event | ❌ | ❌ | ✅ | ✅ |
| Edit event | ❌ | ❌ | ✅ (own) | ✅ |
| Delete event | ❌ | ❌ | ❌ | ✅ |
| View attendee list | ❌ | ✅ | ✅ | ✅ |
| **Members** |
| View member directory | ✅ | ✅ | ✅ | ✅ |
| Edit own profile | ❌ | ✅ | ✅ | ✅ |
| Edit other profiles | ❌ | ❌ | ❌ | ✅ |
| **Playground** |
| Use chatbot | ✅ | ✅ | ✅ | ✅ |
| Use whiteboard | ❌ | ✅ | ✅ | ✅ |
| Use prompt lab | ✅ | ✅ | ✅ | ✅ |
| View jokes/facts | ✅ | ✅ | ✅ | ✅ |
| Play mini-games | ✅ | ✅ | ✅ | ✅ |
| **Admin** |
| Access admin panel | ❌ | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ❌ | ✅ |
| Moderate content | ❌ | ❌ | ✅ | ✅ |
| View analytics | ❌ | ❌ | ✅ | ✅ |

---

## Implementation Pattern

### Backend (FastAPI)
```python
# Dependency for auth
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate JWT, return user
    pass

def require_role(required_role: str):
    def role_checker(user = Depends(get_current_user)):
        if not user.has_role(required_role):
            raise HTTPException(403, "Insufficient permissions")
        return user
    return role_checker

# Usage in endpoints
@app.post("/projects")
def create_project(
    project: ProjectCreate,
    user = Depends(require_role("lead"))
):
    # Only leads and admins can create projects
    pass
```

### Frontend (React)
```typescript
// Hook for checking permissions
function usePermission(action: string, resource: string) {
  const { user } = useAuth();
  return checkPermission(user.role, action, resource);
}

// Usage in components
function ProjectCard({ project }) {
  const canEdit = usePermission('edit', 'project');
  
  return (
    <div>
      {canEdit && <EditButton />}
    </div>
  );
}
```

---

## Security Best Practices

### Token Security
- Store JWT in HTTP-only cookies (not localStorage)
- Use secure flag in production
- Set sameSite=strict to prevent CSRF
- Short expiry (7 days max)
- Rotate tokens on sensitive actions

### Password Security
- Hash with bcrypt (cost 12)
- Never log passwords
- Rate limit login attempts (5 per 15 min)
- Lock account after 10 failed attempts
- Require password change after reset

### API Security
- Validate all inputs
- Use parameterized queries (prevent SQL injection)
- Rate limit all endpoints
- Log authentication events
- Monitor for suspicious activity

---

## Rate Limiting

### Login Attempts
- 5 attempts per 15 minutes per IP
- 10 attempts per hour per email
- Exponential backoff after failures

### API Endpoints
- Guest: 100 requests/hour
- Member: 1000 requests/hour
- Lead/Admin: 5000 requests/hour

### Specific Actions
- Vote: 50 per hour per user
- Comment: 20 per hour per user
- Submit idea: 5 per day per user
- Submit request: 3 per day per user
- AI requests (chatbot, prompt lab): 20 per hour per user

---

## Testing Checklist
- Guest cannot access member-only features
- Member cannot access lead-only features
- JWT validation works correctly
- Expired tokens are rejected
- Password reset flow works
- Rate limiting prevents abuse
- Login attempts are rate limited
- Permissions are enforced on backend (not just frontend)
