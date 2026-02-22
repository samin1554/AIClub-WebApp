# AI Club Web App — Comprehensive Development Plan

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Product Vision](#product-vision)
3. [Architecture Overview](#architecture-overview)
4. [Team Structure](#team-structure)
5. [Development Workflow](#development-workflow)
6. [Implementation Roadmap](#implementation-roadmap)
7. [Quality Standards](#quality-standards)
8. [Documentation Index](#documentation-index)

---

## Quick Start

### For New Developers
1. Read [ONBOARDING.md](./ONBOARDING.md) - Get your dev environment set up
2. Read [Architecture.md](./Architecture.md) - Understand the system
3. Read [api-contract.md](./api-contract.md) - Learn the API patterns
4. Pick a starter task from the backlog
5. Join the team Slack channel

### For Project Managers
1. Read [plan.md](./plan.md) - Understand the product vision
2. Review [Milestone Roadmap](#implementation-roadmap)
3. Set up project tracking (GitHub Projects / Jira)
4. Schedule weekly standups

### For Designers
1. Read [plan.md](./plan.md) - UX/UI direction
2. Read [component-library.md](./component-library.md) - Component inventory
3. Review design system (Tailwind config)
4. Create mockups for priority features

---

## Product Vision

### What We're Building
An AI Club web app that:
1. **Showcases** what the club has built (credibility)
2. **Collects** new ideas and project requests (pipeline)
3. **Engages** members with fun AI tools (retention)

### Success Metrics
- **Showcase**: Visitors understand club's skill level in < 60 seconds
- **Create**: Ideas turn into real projects, nothing gets lost
- **Engage**: Members return weekly because it's alive and fun

### Three Pillars

#### Pillar A — Showcase (Credibility)
- Projects gallery with filters and search
- Member directory with skills and contributions
- Impact stats (projects shipped, members, events)
- Featured projects on home page

#### Pillar B — Create (Pipeline)
- Idea board with voting and comments
- Request intake form and triage queue
- Status workflow (New → Triage → Approved → In Progress → Shipped)
- Promote ideas to requests

#### Pillar C — Engage (Retention)
- Events with RSVP
- Chatbot for club questions
- Playground (whiteboard, prompt lab, jokes, mini-games, Spotify)
- Optional Sackbot character

---

## Architecture Overview

### Tech Stack

**Frontend**:
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- TanStack Query (server state)
- Zustand (client state)

**Backend**:
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Redis (caching, rate limiting)

**Deployment**:
- Frontend: Vercel
- Backend: Railway
- Database: Neon
- Redis: Upstash
- Storage: Cloudflare R2

### Monorepo Structure
```
ai-club-app/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # FastAPI backend
├── packages/
│   ├── ui/           # Shared UI components
│   └── shared/       # Shared types/utils
├── docs/             # Documentation
└── infra/            # Docker, deployment configs
```

### Key Architectural Decisions
See [decisions/](./decisions/) for full ADRs:
- **001**: Next.js for frontend (SEO, routing, deployment)
- **002**: FastAPI for backend (performance, type safety, docs)
- **003**: PostgreSQL for database (relational data, ACID)
- **004**: JWT in HTTP-only cookies (security)
- **005**: Monorepo structure (code sharing)

---

## Team Structure

### Roles (4-5 people)

**1. Tech Lead / Integrator**
- Reviews PRs, enforces architecture
- Owns deployment and environment setup
- Resolves technical blockers
- Mentors team members

**2. Frontend Lead**
- Design system and component library
- Page layouts and routing
- UI consistency and responsiveness
- Frontend testing

**3. Backend Lead**
- API endpoints and business logic
- Database schema and migrations
- Authentication and authorization
- Backend testing

**4. Full-stack Integrations**
- External APIs (OpenAI, Spotify)
- Rate limiting and caching
- WebSocket (Phase 2)
- Background jobs (Phase 2)

**5. QA / DevOps / DX** (part-time)
- CI/CD pipelines
- Testing infrastructure
- Deployment automation
- Developer experience improvements

### Working Rules
1. **One design system** → prevents UI chaos
2. **One API contract** → prevents frontend/backend mismatch
3. **Weekly ship demo** → forces integration
4. **Small PRs** → easier to review
5. **Documentation required** → knowledge sharing

---

## Development Workflow

### Branching Strategy
- `main`: Always deployable, protected
- `dev`: Integration branch (optional)
- Feature branches: `feat/feature-name`
- Bug fixes: `fix/bug-description`

### Commit Convention
Use Conventional Commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

### PR Process
1. Create feature branch
2. Make changes + write tests
3. Run linters and tests locally
4. Push and create PR
5. Add description + screenshots (if UI)
6. Request review from relevant lead
7. Address feedback
8. Merge when approved + CI passes

### PR Requirements
- [ ] Tests pass
- [ ] Linters pass
- [ ] Screenshots for UI changes
- [ ] API docs updated (if backend)
- [ ] No console errors
- [ ] Reviewed by lead

---

## Implementation Roadmap

### Sprint 0: Foundations (Week 1-2)
**Goal**: Get everyone set up and productive

**Tasks**:
- [ ] Monorepo setup with Next.js + FastAPI
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Linting and formatting configured
- [ ] Database connected + first migration
- [ ] Auth skeleton (JWT + roles)
- [ ] Design system basics (Tailwind config, base components)

**Deliverable**: Everyone can run the app locally

---

### Sprint 1: Showcase MVP (Week 3-4)
**Goal**: Visitors can see what the club has built

**Tasks**:
- [ ] Home page shell with bento layout
- [ ] Projects CRUD API endpoints
- [ ] Projects index page (grid + filters)
- [ ] Project detail page
- [ ] Members directory API
- [ ] Members page (grid + search)
- [ ] Basic navigation and layout

**Deliverable**: Projects and members are browsable

---

### Sprint 2: Create MVP (Week 5-6)
**Goal**: Ideas and requests can be submitted and managed

**Tasks**:
- [ ] Ideas board API (CRUD + voting + comments)
- [ ] Ideas board UI (card wall + filters)
- [ ] Idea detail drawer
- [ ] Voting and commenting UI
- [ ] Requests API (CRUD + status workflow)
- [ ] Request submission form
- [ ] Request queue (members only)
- [ ] Request detail page

**Deliverable**: Ideas and requests flow works end-to-end

---

### Sprint 3: Engage MVP (Week 7-8)
**Goal**: Members can RSVP to events and use basic playground

**Tasks**:
- [ ] Events API (CRUD + RSVP)
- [ ] Events list page
- [ ] Event detail page with RSVP
- [ ] Calendar export (.ics)
- [ ] Chatbot API (OpenAI integration)
- [ ] Chatbot drawer UI
- [ ] Playground hub page
- [ ] Basic prompt lab

**Deliverable**: Events and chatbot are functional

---

### Sprint 4: Hardening (Week 9-10)
**Goal**: App is production-ready

**Tasks**:
- [ ] Security audit (auth, permissions, input validation)
- [ ] Rate limiting on all endpoints
- [ ] Error handling and logging (Sentry)
- [ ] Responsive polish (mobile, tablet)
- [ ] Loading and error states everywhere
- [ ] Content moderation tools (admin)
- [ ] Performance optimization
- [ ] Documentation complete

**Deliverable**: App is ready to launch

---

### Sprint 5: Launch (Week 11)
**Goal**: App is live and stable

**Tasks**:
- [ ] Deploy to production
- [ ] Seed initial content (projects, members, events)
- [ ] Announce to club
- [ ] Monitor for issues
- [ ] Gather feedback
- [ ] Fix critical bugs

**Deliverable**: App is live and being used

---

### Phase 2: Advanced Features (Post-Launch)
**Goal**: Add realtime and advanced playground features

**Features**:
- Whiteboard (single-user → multi-user)
- Spotify integration (embeds → OAuth → playback)
- Mini-games
- Sackbot roaming character
- Advanced chatbot (RAG, club knowledge)
- Prompt lab upgrades
- Analytics dashboard
- Notifications (email, push)

**Timeline**: 4-6 weeks after launch

---

## Quality Standards

### Definition of Done
A feature is "done" when:
- [ ] Works on desktop + mobile
- [ ] Has loading, error, and empty states
- [ ] Has test coverage (80% backend, 70% frontend)
- [ ] Doesn't break existing features
- [ ] Is documented (component README updated)
- [ ] Passes code review
- [ ] Deployed to staging and tested

### Code Quality
- **Backend**: Follow PEP 8, use type hints, max line 100 chars
- **Frontend**: Use Prettier, ESLint, TypeScript strict mode
- **Tests**: Unit tests for logic, integration tests for APIs, E2E for critical flows
- **Documentation**: Update docs with every feature

### Performance Budgets
- **Page load**: < 2s
- **API response**: < 300ms
- **Bundle size**: < 200 KB (gzipped)
- **Lighthouse score**: > 90

See [performance-budgets.md](./performance-budgets.md) for details.

### Security Checklist
- [ ] All secrets in environment variables
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitize input)
- [ ] CSRF protection enabled
- [ ] Secure password hashing (bcrypt)
- [ ] JWT in HTTP-only cookies
- [ ] HTTPS enforced

See [auth-permissions.md](./auth-permissions.md) for details.

---

## Documentation Index

### Getting Started
- [ONBOARDING.md](./ONBOARDING.md) - Developer setup guide
- [plan.md](./plan.md) - Original project plan
- [Architecture.md](./Architecture.md) - High-level architecture

### Architecture & Design
- [frontend-architecture.md](./frontend-architecture.md) - Frontend tech stack and patterns
- [backend-architecture.md](./backend-architecture.md) - Backend tech stack and patterns
- [api-contract.md](./api-contract.md) - API standards and endpoints
- [auth-permissions.md](./auth-permissions.md) - Authentication and authorization

### Component Documentation
- [component-library.md](./component-library.md) - UI component catalog
- [components/projects.md](./components/projects.md) - Projects module
- [components/ideas.md](./components/ideas.md) - Ideas board module
- [components/requests.md](./components/requests.md) - Requests module
- [components/events.md](./components/events.md) - Events module
- [components/members.md](./components/members.md) - Members module
- [components/playground.md](./components/playground.md) - Playground hub
- [components/chatbot.md](./components/chatbot.md) - Chatbot module
- [components/whiteboard.md](./components/whiteboard.md) - Whiteboard module
- [components/spotify.md](./components/spotify.md) - Spotify integration
- [components/prompt-lab.md](./components/prompt-lab.md) - Prompt lab
- [components/joke-facts.md](./components/joke-facts.md) - Jokes and facts
- [components/minigames.md](./components/minigames.md) - Mini-games
- [components/Sackbot.md](./components/Sackbot.md) - Sackbot character

### Operations
- [testing-strategy.md](./testing-strategy.md) - Testing approach and tools
- [deployment.md](./deployment.md) - Deployment guide
- [performance-budgets.md](./performance-budgets.md) - Performance targets

### Decisions
- [decisions/](./decisions/) - Architecture Decision Records (ADRs)
- [decisions/001-nextjs-frontend.md](./decisions/001-nextjs-frontend.md)
- [decisions/002-fastapi-backend.md](./decisions/002-fastapi-backend.md)

---

## Success Criteria

### MVP Launch (Week 11)
- [ ] All core features working (Showcase, Create, Engage)
- [ ] 20+ projects showcased
- [ ] 30+ club members registered
- [ ] 5+ upcoming events
- [ ] 50+ ideas submitted
- [ ] Zero critical bugs
- [ ] Lighthouse score > 85

### 1 Month Post-Launch
- [ ] 100+ active users
- [ ] 10+ new ideas per week
- [ ] 5+ new requests submitted
- [ ] 80%+ event RSVP rate
- [ ] < 1% error rate
- [ ] < 2s average page load

### 3 Months Post-Launch
- [ ] 200+ active users
- [ ] 50+ projects showcased
- [ ] 20+ requests completed
- [ ] Phase 2 features launched
- [ ] 90+ Lighthouse score
- [ ] Community feedback positive

---

## Risk Mitigation

### Technical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Scope creep | High | Enforce MVP/Phase 2 boundary strictly |
| Auth complexity | Medium | Start simple, iterate based on needs |
| Realtime features | Medium | Phase 2 only, ship single-user first |
| External API failures | Medium | Implement fallbacks and error handling |
| Performance issues | Medium | Set budgets early, monitor continuously |

### Team Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Team member leaves | High | Document everything, pair programming |
| Skill gaps | Medium | Provide learning resources, mentorship |
| Communication issues | Medium | Weekly standups, clear documentation |
| Burnout | Medium | Realistic timelines, celebrate wins |

---

## Next Steps

### Immediate (This Week)
1. [ ] Set up monorepo structure
2. [ ] Configure CI/CD pipeline
3. [ ] Create project board (GitHub Projects)
4. [ ] Assign roles to team members
5. [ ] Schedule weekly standup
6. [ ] Set up team communication (Slack)

### Short-term (Next 2 Weeks)
1. [ ] Complete Sprint 0 (Foundations)
2. [ ] Start Sprint 1 (Showcase MVP)
3. [ ] Create design mockups for key pages
4. [ ] Set up staging environment
5. [ ] Begin writing tests

### Long-term (Next 3 Months)
1. [ ] Complete MVP (Sprints 1-4)
2. [ ] Launch to club members
3. [ ] Gather feedback and iterate
4. [ ] Plan Phase 2 features
5. [ ] Grow user base

---

## Resources

### Learning Materials
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Next.js Learn](https://nextjs.org/learn)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [React Query Docs](https://tanstack.com/query/latest)

### Design Inspiration
- [Awwwards](https://www.awwwards.com/)
- [Dribbble](https://dribbble.com/)
- [Vercel Design](https://vercel.com/design)

### Community
- Team Slack: #ai-club-dev
- Weekly standup: Mondays 10am
- Code reviews: Tag @tech-lead
- Questions: Ask in Slack or create GitHub issue

---

## Conclusion

This is an ambitious but achievable project. The key to success:
1. **Start small**: Ship MVP first, add features later
2. **Stay organized**: Use project board, document decisions
3. **Communicate**: Weekly standups, clear PRs, ask questions
4. **Test everything**: Write tests, review code, test on staging
5. **Have fun**: This is a learning experience, celebrate wins!

Let's build something amazing! 🚀
