# Backend Architecture

## Tech Stack

### Core
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Cache**: Redis (optional, for rate limiting + sessions)

### Additional Libraries
- **Auth**: python-jose (JWT), passlib (password hashing)
- **Validation**: Pydantic v2
- **HTTP Client**: httpx (for external APIs)
- **Task Queue**: Celery + Redis (Phase 2, for background jobs)
- **WebSocket**: FastAPI WebSocket support

---

## Project Structure

```
apps/api/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── dependencies.py      # Shared dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── idea.py
│   │   └── ...
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── ...
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── ideas.py
│   │   │   └── ...
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   └── ...
│   ├── core/                # Core utilities
│   │   ├── security.py      # Auth helpers
│   │   ├── permissions.py   # RBAC logic
│   │   └── rate_limit.py    # Rate limiting
│   └── integrations/        # External APIs
│       ├── openai_client.py
│       ├── spotify_client.py
│       └── ...
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── ...
├── requirements.txt
└── .env.example
```

---

## Database Models

### User & Auth
```python
# app/models/user.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    roles = relationship("UserRole", back_populates="user")
    member_profile = relationship("Member", back_populates="user", uselist=False)
```


### Projects
```python
# app/models/project.py
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    content_md = Column(Text, nullable=True)
    tags = Column(ARRAY(String), default=[])
    cover_url = Column(String, nullable=True)
    repo_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    status = Column(String, default="draft")  # draft, published
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    contributors = relationship("ProjectContributor", back_populates="project")
```

---

## API Layer Pattern

### Route Structure
```python
# app/api/v1/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    skip: int = 0,
    limit: int = 20,
    tag: str | None = None,
    db: Session = Depends(get_db),
):
    return project_service.get_all(db, skip=skip, limit=limit, tag=tag)

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("lead")),
):
    return project_service.create(db, project, current_user)
```

### Service Layer
```python
# app/services/project_service.py
class ProjectService:
    def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        tag: str | None = None
    ) -> list[Project]:
        query = db.query(Project).filter(Project.status == "published")
        if tag:
            query = query.filter(Project.tags.contains([tag]))
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, data: ProjectCreate, user: User) -> Project:
        # Generate slug from title
        slug = slugify(data.title)
        
        # Check if slug exists
        if db.query(Project).filter(Project.slug == slug).first():
            raise ValueError("Project with this title already exists")
        
        project = Project(
            slug=slug,
            title=data.title,
            summary=data.summary,
            tags=data.tags,
            status="draft",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

project_service = ProjectService()
```

---

## Authentication & Authorization

### JWT Token Generation
```python
# app/core/security.py
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### Permission Checking
```python
# app/core/permissions.py
def require_role(required_role: str):
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        user_roles = [r.role.name for r in current_user.roles]
        
        # Admin has all permissions
        if "admin" in user_roles:
            return current_user
        
        # Check specific role
        if required_role not in user_roles:
            raise HTTPException(403, "Insufficient permissions")
        
        return current_user
    return role_checker
```

---

## Rate Limiting

### Redis-based Rate Limiter
```python
# app/core/rate_limit.py
from redis import Redis
from fastapi import HTTPException

redis_client = Redis.from_url(settings.REDIS_URL)

def rate_limit(key: str, limit: int, window: int):
    """
    Rate limit based on key (e.g., user_id, ip_address)
    limit: max requests
    window: time window in seconds
    """
    current = redis_client.get(key)
    
    if current is None:
        redis_client.setex(key, window, 1)
        return
    
    if int(current) >= limit:
        raise HTTPException(429, "Rate limit exceeded")
    
    redis_client.incr(key)

# Usage in endpoint
@router.post("/ideas/{id}/vote")
def vote_on_idea(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rate_limit(f"vote:{current_user.id}", limit=50, window=3600)
    return idea_service.vote(db, id, current_user)
```

---

## External Integrations

### OpenAI Client
```python
# app/integrations/openai_client.py
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatService:
    def generate_response(self, message: str, context: str = "") -> str:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content
```

### Spotify Client
```python
# app/integrations/spotify_client.py
import httpx

class SpotifyClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1"
    
    async def get_now_playing(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/me/player/currently-playing",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            return response.json()
```

---

## WebSocket Support (Whiteboard)

```python
# app/api/v1/whiteboard.py
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: int):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: int):
        self.active_connections[session_id].remove(websocket)
    
    async def broadcast(self, message: dict, session_id: int):
        for connection in self.active_connections.get(session_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/whiteboard/{session_id}/live")
async def whiteboard_websocket(
    websocket: WebSocket,
    session_id: int,
):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast stroke to all connected clients
            await manager.broadcast(data, session_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
```

---

## Database Migrations

### Creating a Migration
```bash
alembic revision --autogenerate -m "Add projects table"
```

### Migration File Example
```python
# alembic/versions/001_add_projects.py
def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_projects_slug', 'projects', ['slug'])

def downgrade():
    op.drop_index('ix_projects_slug')
    op.drop_table('projects')
```

---

## Testing

### Unit Tests (pytest)
```python
# tests/test_projects.py
def test_create_project(client, auth_headers):
    response = client.post(
        "/api/v1/projects",
        json={
            "title": "Test Project",
            "summary": "A test project",
            "tags": ["ai", "ml"]
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Test Project"

def test_list_projects(client):
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
```

---

## Configuration Management

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Club API"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # External APIs
    OPENAI_API_KEY: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Error Handling

```python
# app/main.py
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.detail,
                "message": str(exc.detail),
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url),
            }
        }
    )
```

---

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/aiclub
SECRET_KEY=your-secret-key
OPENAI_API_KEY=sk-...
REDIS_URL=redis://localhost:6379
```

---

## Testing Checklist
- All endpoints return correct status codes
- Authentication required where needed
- Permissions enforced correctly
- Rate limiting works
- Database transactions rollback on error
- Migrations run successfully
- External API errors handled gracefully
