# AI Club Web App — Architecture Document

## 1) Architecture Overview
We use a monorepo with:
- **Web app (React)**: UI pages + client-side interactions
- **API (FastAPI)**: authentication, CRUD, business logic, integrations
- **Database (Postgres)**: persistent data
- **Redis**: caching + rate limiting + realtime pub/sub (optional)
- **Object storage (optional)**: images, project media (S3-compatible)

### High-level diagram
```mermaid
flowchart LR
  U[User Browser] --> W[Web Frontend (React)]
  W -->|HTTPS JSON| A[FastAPI Backend]
  A --> DB[(Postgres)]
  A --> R[(Redis)]
  A --> S[(Object Storage)]
  A --> OAI[LLM Provider API]
  A --> SP[Spotify API]
  W <-->|WebSocket (Phase 2)| A