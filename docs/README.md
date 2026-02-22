# AI Club Web App Documentation

Welcome to the AI Club Web App documentation! This directory contains everything you need to understand, build, and deploy the app.

---

## 🚀 Quick Links

### New to the Project?
Start here:
1. **[COMPREHENSIVE-PLAN.md](./COMPREHENSIVE-PLAN.md)** - Complete overview of the project
2. **[ONBOARDING.md](./ONBOARDING.md)** - Get your dev environment set up
3. **[plan.md](./plan.md)** - Original product vision and goals

### Building Features?
Reference these:
- **[api-contract.md](./api-contract.md)** - API standards and endpoints
- **[component-library.md](./component-library.md)** - UI components catalog
- **[frontend-architecture.md](./frontend-architecture.md)** - Frontend patterns
- **[backend-architecture.md](./backend-architecture.md)** - Backend patterns

### Deploying?
Check these:
- **[deployment.md](./deployment.md)** - Deployment guide
- **[testing-strategy.md](./testing-strategy.md)** - Testing approach
- **[performance-budgets.md](./performance-budgets.md)** - Performance targets

---

## 📚 Documentation Structure

### Core Documents
- **COMPREHENSIVE-PLAN.md** - Complete project overview (start here!)
- **ONBOARDING.md** - Developer setup guide
- **plan.md** - Original project plan
- **Architecture.md** - High-level architecture

### Architecture & Design
- **frontend-architecture.md** - Frontend tech stack, patterns, and structure
- **backend-architecture.md** - Backend tech stack, patterns, and structure
- **api-contract.md** - API standards, endpoints, and response formats
- **auth-permissions.md** - Authentication and authorization details
- **component-library.md** - UI component catalog and usage

### Component Modules
Located in `components/`:
- **projects.md** - Projects showcase module
- **ideas.md** - Ideas board module
- **requests.md** - Request intake and pipeline
- **events.md** - Events and RSVP system
- **members.md** - Member directory
- **playground.md** - Playground hub
- **chatbot.md** - AI chatbot assistant
- **whiteboard.md** - Drawing canvas
- **spotify.md** - Music integration
- **prompt-lab.md** - Prompt generator
- **joke-facts.md** - Daily jokes and facts
- **minigames.md** - Browser games
- **Sackbot.md** - Ambient character

### Operations
- **testing-strategy.md** - Testing frameworks, patterns, and coverage
- **deployment.md** - Deployment guide for production
- **performance-budgets.md** - Performance targets and monitoring

### Decisions
Located in `decisions/`:
- **README.md** - ADR index
- **001-nextjs-frontend.md** - Why Next.js
- **002-fastapi-backend.md** - Why FastAPI
- More ADRs as decisions are made

---

## 🎯 Product Overview

### What We're Building
An AI Club web app with three pillars:

**1. Showcase** (Credibility)
- Projects gallery
- Member directory
- Impact stats

**2. Create** (Pipeline)
- Idea board with voting
- Request intake and triage
- Status workflow

**3. Engage** (Retention)
- Events with RSVP
- AI playground tools
- Chatbot assistant

### Tech Stack
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI, PostgreSQL, Redis
- **Deployment**: Vercel (frontend), Railway (backend)

---

## 👥 Team Roles

1. **Tech Lead** - Architecture, reviews, deployment
2. **Frontend Lead** - UI system, pages, components
3. **Backend Lead** - API, database, auth
4. **Full-stack Integrations** - External APIs, realtime
5. **QA / DevOps** - CI/CD, testing, monitoring

---

## 📅 Development Phases

### MVP (Weeks 1-11)
- Sprint 0: Foundations
- Sprint 1: Showcase (projects, members)
- Sprint 2: Create (ideas, requests)
- Sprint 3: Engage (events, chatbot)
- Sprint 4: Hardening
- Sprint 5: Launch

### Phase 2 (Post-Launch)
- Realtime whiteboard
- Spotify integration
- Mini-games
- Sackbot character
- Advanced features

---

## 🔍 Finding Information

### "How do I...?"

**Set up my dev environment?**
→ [ONBOARDING.md](./ONBOARDING.md)

**Understand the architecture?**
→ [Architecture.md](./Architecture.md)
→ [frontend-architecture.md](./frontend-architecture.md)
→ [backend-architecture.md](./backend-architecture.md)

**Create a new API endpoint?**
→ [api-contract.md](./api-contract.md)
→ [backend-architecture.md](./backend-architecture.md)

**Build a new UI component?**
→ [component-library.md](./component-library.md)
→ [frontend-architecture.md](./frontend-architecture.md)

**Add authentication?**
→ [auth-permissions.md](./auth-permissions.md)

**Write tests?**
→ [testing-strategy.md](./testing-strategy.md)

**Deploy to production?**
→ [deployment.md](./deployment.md)

**Understand a feature?**
→ Check `components/[feature].md`

**Know why we made a decision?**
→ Check `decisions/`

---

## 🛠️ Common Tasks

### Starting Development
```bash
# Backend
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend
cd apps/web
npm run dev
```

### Running Tests
```bash
# Backend
cd apps/api
pytest

# Frontend
cd apps/web
npm test
```

### Creating a Migration
```bash
cd apps/api
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Deploying
```bash
# Push to main branch
git push origin main

# Vercel and Railway auto-deploy
```

---

## 📖 Documentation Standards

### When to Update Docs
- Adding a new feature → Update relevant component doc
- Making an architectural decision → Create ADR
- Changing API → Update api-contract.md
- Adding a component → Update component-library.md
- Changing deployment → Update deployment.md

### How to Write Docs
- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep it up to date
- Link to related docs

---

## 🤝 Contributing

### Before Starting
1. Read [ONBOARDING.md](./ONBOARDING.md)
2. Understand the architecture
3. Check the project board for tasks
4. Ask questions in Slack

### Development Workflow
1. Create feature branch
2. Make changes + write tests
3. Update documentation
4. Create PR with description
5. Address review feedback
6. Merge when approved

### PR Checklist
- [ ] Tests pass
- [ ] Linters pass
- [ ] Documentation updated
- [ ] Screenshots (if UI)
- [ ] Reviewed by lead

---

## 📞 Getting Help

### Resources
- **Team Slack**: #ai-club-dev
- **Weekly Standup**: Mondays 10am
- **Code Reviews**: Tag @tech-lead
- **Questions**: Ask in Slack or create GitHub issue

### External Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

## 🎉 Let's Build!

This documentation is a living resource. As the project evolves, so will these docs. If you find something unclear or missing, please update it or ask for clarification.

Welcome to the team! 🚀
