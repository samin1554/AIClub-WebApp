# Architecture Decision Records (ADRs)

This directory contains records of architectural decisions made for the AI Club Web App.

## Format

Each decision is documented in a separate markdown file with the following structure:

```markdown
# [Number]. [Title]

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded
**Deciders**: [Names]

## Context
What is the issue we're trying to solve?

## Decision
What did we decide to do?

## Consequences
What are the trade-offs and implications?

## Alternatives Considered
What other options did we evaluate?
```

## Index

### 001. Use Next.js for Frontend
**Status**: Accepted
**Summary**: Chose Next.js over Vite + React SPA for better SEO, routing, and deployment ergonomics.

### 002. Use FastAPI for Backend
**Status**: Accepted
**Summary**: Chose FastAPI over Express/Django for Python ecosystem, type safety, and automatic API docs.

### 003. Use PostgreSQL for Database
**Status**: Accepted
**Summary**: Chose PostgreSQL over MongoDB for relational data, ACID compliance, and mature ecosystem.

### 004. Use JWT in HTTP-only Cookies
**Status**: Accepted
**Summary**: Chose JWT in HTTP-only cookies over localStorage for better security against XSS.

### 005. Use Monorepo Structure
**Status**: Accepted
**Summary**: Chose monorepo over separate repos for easier code sharing and coordinated changes.

### 006. Use shadcn/ui for Components
**Status**: Accepted
**Summary**: Chose shadcn/ui over Material-UI for customization, bundle size, and modern design.

### 007. Use TanStack Query for Server State
**Status**: Accepted
**Summary**: Chose TanStack Query over Redux for simpler server state management and caching.

### 008. Use Vercel for Frontend Hosting
**Status**: Accepted
**Summary**: Chose Vercel over Netlify/AWS for Next.js optimization and preview deployments.

### 009. Use Railway for Backend Hosting
**Status**: Accepted
**Summary**: Chose Railway over Heroku/AWS for simplicity, pricing, and PostgreSQL integration.

### 010. Defer Realtime Features to Phase 2
**Status**: Accepted
**Summary**: Decided to ship MVP without WebSocket features to reduce complexity and ship faster.
