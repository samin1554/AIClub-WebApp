# API Contract & Standards

## Overview
This document defines the API contract between frontend and backend.
All endpoints follow consistent patterns for requests, responses, errors, and data formats.

---

## API Versioning
All endpoints are prefixed with `/api/v1/`

Example: `https://aiclub.app/api/v1/projects`

---

## Request Format

### Headers
```
Content-Type: application/json
Authorization: Bearer <token> (for authenticated requests)
```

### Query Parameters
Use for filtering, sorting, pagination:
```
GET /api/v1/projects?tag=ai&sort=newest&page=1&limit=20
```

### Body (POST/PATCH)
Always JSON:
```json
{
  "title": "My Project",
  "description": "A cool project"
}
```

---

## Response Format

### Success Response
```json
{
  "data": {
    // The actual response data
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

### Success Response (List)
```json
{
  "data": [
    { "id": 1, "title": "Project 1" },
    { "id": 2, "title": "Project 2" }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

---

## Error Codes

### Client Errors (4xx)
- `VALIDATION_ERROR` (400): Invalid input data
- `UNAUTHORIZED` (401): Not authenticated
- `FORBIDDEN` (403): Insufficient permissions
- `NOT_FOUND` (404): Resource not found
- `CONFLICT` (409): Resource already exists
- `RATE_LIMITED` (429): Too many requests

### Server Errors (5xx)
- `INTERNAL_ERROR` (500): Unexpected server error
- `SERVICE_UNAVAILABLE` (503): Service temporarily down

---

## Pagination

### Request
```
GET /api/v1/projects?page=2&limit=20
```

### Response
```json
{
  "data": [...],
  "meta": {
    "pagination": {
      "page": 2,
      "limit": 20,
      "total": 45,
      "totalPages": 3,
      "hasNext": true,
      "hasPrev": true
    }
  }
}
```

### Defaults
- Default page: 1
- Default limit: 20
- Max limit: 100

---

## Filtering & Sorting

### Filtering
```
GET /api/v1/projects?tag=ai&status=published
```

### Sorting
```
GET /api/v1/projects?sort=newest
GET /api/v1/projects?sort=-createdAt (descending)
```

### Search
```
GET /api/v1/projects?search=machine+learning
```

---

## Date/Time Format
All timestamps use ISO 8601 format in UTC:
```
2024-01-15T10:30:00Z
```

Frontend should convert to user's local timezone for display.

---

## Endpoint Patterns

### Resource CRUD
```
GET    /api/v1/resources          List resources
POST   /api/v1/resources          Create resource
GET    /api/v1/resources/{id}     Get resource detail
PATCH  /api/v1/resources/{id}     Update resource
DELETE /api/v1/resources/{id}     Delete resource
```

### Nested Resources
```
GET    /api/v1/projects/{id}/contributors
POST   /api/v1/projects/{id}/contributors
DELETE /api/v1/projects/{id}/contributors/{userId}
```

### Actions
```
POST   /api/v1/ideas/{id}/vote
DELETE /api/v1/ideas/{id}/vote
POST   /api/v1/events/{id}/rsvp
```

---

## Complete Endpoint List

### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/me
```

### Projects
```
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{slug}
PATCH  /api/v1/projects/{id}
DELETE /api/v1/projects/{id}
GET    /api/v1/projects/{id}/contributors
POST   /api/v1/projects/{id}/contributors
DELETE /api/v1/projects/{id}/contributors/{userId}
```

### Ideas
```
GET    /api/v1/ideas
POST   /api/v1/ideas
GET    /api/v1/ideas/{id}
PATCH  /api/v1/ideas/{id}
DELETE /api/v1/ideas/{id}
POST   /api/v1/ideas/{id}/vote
DELETE /api/v1/ideas/{id}/vote
GET    /api/v1/ideas/{id}/comments
POST   /api/v1/ideas/{id}/comments
DELETE /api/v1/ideas/{id}/comments/{commentId}
POST   /api/v1/ideas/{id}/promote (lead/admin only)
```

### Requests
```
GET    /api/v1/requests
POST   /api/v1/requests
GET    /api/v1/requests/{id}
PATCH  /api/v1/requests/{id}
DELETE /api/v1/requests/{id}
GET    /api/v1/requests/{id}/comments
POST   /api/v1/requests/{id}/comments
```

### Events
```
GET    /api/v1/events
POST   /api/v1/events
GET    /api/v1/events/{id}
PATCH  /api/v1/events/{id}
DELETE /api/v1/events/{id}
POST   /api/v1/events/{id}/rsvp
DELETE /api/v1/events/{id}/rsvp
GET    /api/v1/events/{id}/attendees
GET    /api/v1/events/{id}/calendar.ics
```

### Members
```
GET    /api/v1/members
GET    /api/v1/members/{id}
PATCH  /api/v1/members/{id}
```

### Playground
```
POST   /api/v1/chat
GET    /api/v1/chat/sessions
GET    /api/v1/chat/sessions/{id}
POST   /api/v1/prompt-lab/generate
GET    /api/v1/jokes/daily
GET    /api/v1/facts/daily
GET    /api/v1/whiteboard/{id}
POST   /api/v1/whiteboard
WS     /api/v1/whiteboard/{id}/live
```

### Admin
```
GET    /api/v1/admin/stats
GET    /api/v1/admin/users
PATCH  /api/v1/admin/users/{id}
DELETE /api/v1/admin/users/{id}
POST   /api/v1/admin/moderate/{resourceType}/{id}
```

---

## Type Generation

### Backend (Python)
Use Pydantic models for request/response schemas:
```python
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title: str
    description: str
    tags: list[str]

class ProjectResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    tags: list[str]
    createdAt: datetime
```

### Frontend (TypeScript)
Generate types from OpenAPI spec or manually maintain:
```typescript
interface Project {
  id: number;
  slug: string;
  title: string;
  description: string;
  tags: string[];
  createdAt: string;
}

interface ApiResponse<T> {
  data: T;
  meta: {
    timestamp: string;
    requestId: string;
  };
}
```

### Recommended: OpenAPI/Swagger
1. Backend generates OpenAPI spec
2. Use `openapi-typescript` to generate frontend types
3. Keep types in sync automatically

---

## API Client Pattern (Frontend)

### Base Client
```typescript
class ApiClient {
  private baseUrl = '/api/v1';

  async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      credentials: 'include', // Include cookies
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(error);
    }

    return response.json();
  }

  get<T>(endpoint: string) {
    return this.request<T>(endpoint);
  }

  post<T>(endpoint: string, data: any) {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // ... patch, delete methods
}

export const api = new ApiClient();
```

### Usage
```typescript
// Get projects
const { data: projects } = await api.get<Project[]>('/projects');

// Create project
const { data: newProject } = await api.post<Project>('/projects', {
  title: 'My Project',
  description: 'Cool project',
});
```

---

## Testing Checklist
- All endpoints follow consistent patterns
- Error responses include helpful messages
- Pagination works correctly
- Filtering and sorting work
- Rate limiting is enforced
- Authentication is required where needed
- Types are generated and in sync
