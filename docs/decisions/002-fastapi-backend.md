# 002. Use FastAPI for Backend

**Date**: 2024-01-15
**Status**: Accepted
**Deciders**: Tech Lead, Backend Lead

## Context

We need to choose a backend framework. Requirements:
- Python ecosystem (team familiar with Python)
- Type safety and validation
- Good API documentation
- Easy to learn for students
- Good performance
- WebSocket support (Phase 2)

## Decision

We will use FastAPI with Python 3.11+.

## Consequences

### Positive
- Automatic API documentation (Swagger/OpenAPI)
- Type hints with Pydantic for validation
- Excellent performance (comparable to Node.js)
- Async support built-in
- Easy to learn and use
- Great documentation
- WebSocket support for Phase 2
- Large and growing community

### Negative
- Async can be confusing for beginners
- Smaller ecosystem than Django
- Need to choose ORM separately (SQLAlchemy)
- Less "batteries included" than Django

### Neutral
- Requires Python 3.7+ (we're using 3.11+)
- Need to set up database migrations separately (Alembic)

## Alternatives Considered

### Django + Django REST Framework
**Pros**:
- Batteries included (admin panel, ORM, migrations)
- Huge ecosystem
- Very mature
- Built-in auth

**Cons**:
- Heavier and slower
- More opinionated
- Synchronous by default
- More boilerplate for simple APIs
- Admin panel not needed for our use case

**Why rejected**: Too heavy for our needs, slower performance, and we don't need the admin panel.

### Express.js (Node.js)
**Pros**:
- JavaScript everywhere (same language as frontend)
- Huge ecosystem
- Very flexible

**Cons**:
- No built-in validation
- No automatic API docs
- Type safety requires extra setup (TypeScript)
- Team more familiar with Python
- Less structured (can lead to inconsistency)

**Why rejected**: Team is more comfortable with Python, and FastAPI provides better structure and validation.

### Flask
**Pros**:
- Simple and lightweight
- Flexible
- Large ecosystem

**Cons**:
- No built-in validation
- No automatic API docs
- No async support (without extensions)
- More manual setup required
- Less modern than FastAPI

**Why rejected**: FastAPI provides more features out of the box with better performance.

## Implementation Notes

- Use Pydantic v2 for schemas
- Use SQLAlchemy 2.0 for ORM
- Use Alembic for migrations
- Enable CORS for frontend
- Use dependency injection for database sessions
- Follow REST conventions
- Use async endpoints where beneficial

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
