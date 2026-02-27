# AI Club Web App — Project Plan

## 0) Purpose (What are we building?)
We are building an AI Club web app that:
1) **Showcases** what the club has built (projects, contributors, demos)
2) **Collects** new ideas + project requests in an organized pipeline
3) **Engages** members with fun + lightweight “AI playground” tools (chatbot, prompt lab, whiteboard, mini-games, Spotify, jokes/facts)
4) Feels modern and “premium” (Awwwards/Dribbble inspiration), but is still maintainable by a student team

---

## 1) Product Pillars (The app must do these well)
### Pillar A — Showcase
- Projects gallery (cards, filters, project pages)
- Contributors/members page (who built what)
- “Featured” projects section on home

**Success looks like:** someone can understand the club’s skill level in <60 seconds.

### Pillar B — Create (intake + pipeline)
- Idea board (portraits/cards with tags, votes, comments)
- Request tab (external people request software; internal members triage)
- Status workflow (“New → Reviewing → Accepted → In Progress → Shipped”)

**Success looks like:** ideas turn into real projects, and nothing gets lost.

### Pillar C — Engage
- Events section (upcoming + RSVP)
- Chatbot/Q&A (club assistant)
- Playground zone: prompt generator, jokes/facts, mini-games, drawing board, Spotify widget
- Ambient “Sackbot” character (optional, dismissible)

**Success looks like:** users return weekly because it’s alive and fun.

---

## 2) MVP vs Phase 2 (avoid scope explosion)

### MVP (Ship this first)
**Pages**
- Home (bento highlights + featured + upcoming event + latest projects/ideas)
- Projects (index + detail)
- Members (directory)
- Ideas (board + submit + vote + comments)
- Requests (submit + request list)
- Events (list + details)

**Core features**
- Auth (club members can create/edit; public can browse)
- Admin role (approve content, moderate)
- Basic chatbot drawer (simple Q&A)

### Phase 2 (after MVP is stable)
- Whiteboard (drawing) + realtime collaboration
- Spotify integration (start with embeds)
- Mini-games window
- Prompt lab upgrades
- Sackbot roaming character + speech bubbles
- “Fun Fact / Joke of the Day” automation
- More advanced analytics + notifications

**Rule:** if it doesn’t strengthen Showcase/Create/Engage, it’s Phase 2.

---

## 3) UX / Design Direction (Awwwards/Dribbble style, but practical)
We want:
- Card-first layout, bento grids, clean typography
- Sticky nav with subtle blur
- Smooth micro-interactions (hover, drawer, modal)
- Dark mode support (optional but recommended)
- Accessibility baseline (keyboard navigation, readable contrast, reduced motion)

**Design guardrails**
- Do not hide important actions only on hover (mobile users)
- Keep animations subtle and optional (prefers-reduced-motion)
- Maintain consistent spacing and a small set of UI primitives

---

## 4) Information Architecture (site map)
- `/` Home
- `/projects` Projects grid
- `/projects/:slug` Project detail
- `/members` Members + contributors
- `/ideas` Idea board
- `/ideas/:id` Idea detail
- `/requests` Request form + request queue
- `/events` Upcoming events
- `/events/:id` Event detail
- `/playground` Tools hub
  - `/playground/chat`
  - `/playground/whiteboard`
  - `/playground/prompt-lab`
  - `/playground/jokes`
  - `/playground/minigames`
  - `/playground/spotify`
- `/admin` Admin dashboard (role-gated)

---

## 5) Team Roles (4–5 people)
### Recommended breakdown
1) **Tech Lead / Integrator**
   - Reviews PRs, enforces architecture, merges safely
   - Owns deployment + env setup
2) **Frontend Lead**
   - Design system + pages + UI consistency
3) **Backend Lead**
   - FastAPI endpoints + auth + DB schema + migrations
4) **Feature Engineer A**
   - Ideas + requests workflows
5) **Feature Engineer B (optional)**
   - Playground tools + chatbot + whiteboard

---

## 6) Development Workflow (how we avoid chaos)
### Repo conventions
- Monorepo with clear folders (`apps/web`, `apps/api`, `packages/shared`)
- Shared types (OpenAPI generated client OR shared schema definitions)
- One PR = one feature, small and reviewable

### Branching
- `main` = always deployable
- `dev` = integration branch (optional)
- feature branches: `feat/ideas-voting`, `fix/request-validation`

### PR rules (simple)
- Must include screenshot/video for UI changes
- Must include endpoint docs for API changes
- Must pass lint + tests

---

## 7) Milestone Roadmap (example)
### Milestone 1 — Foundations
- Repo setup, CI, linting
- Auth skeleton + roles
- DB connected + migrations working

### Milestone 2 — Showcase MVP
- Projects index + detail
- Members directory

### Milestone 3 — Create MVP
- Ideas board + submit + vote + comments
- Requests submit + request list + status

### Milestone 4 — Engage MVP
- Events + RSVP
- Chatbot drawer basic

### Milestone 5 — Hardening + Launch
- Security pass
- Rate limiting
- Responsive polish
- Content moderation tools

---

## 8) Definition of Done (DoD)
A feature is “done” when:
- Works on desktop + mobile
- Has loading + error + empty states
- Has basic test coverage (at least critical logic)
- Doesn’t break existing pages
- Is documented (component README updated)

---

## 9) Risks + Mitigations
- **Scope creep** → enforce MVP/Phase 2 boundary
- **Auth complexity** → start with a simple roles table and server-side checks
- **Realtime features** → phase 2; ship single-user whiteboard first
- **Spotify playback complexity** → start with embeds; playback SDK later