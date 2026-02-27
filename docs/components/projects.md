# Projects Module (Showcase)

## What is this?
The Projects module displays:
- Previous club projects
- Project details (what it is, what we learned)
- Links (GitHub, demo)
- Contributors (members who built it)

This is the “portfolio” of the club.

## Why it matters
Most visitors decide if a club is “serious” by:
1) Do they ship real things?
2) Can I see proof?

Projects provides that proof.

---

## User Experience
### Projects Index Page (`/projects`)
- Grid of project cards
- Filters: category, tech tags, year
- Search box
- Sort: newest / featured / most viewed (optional)

### Project Detail Page (`/projects/:slug`)
- Hero section: cover image/video + title
- Summary: 2–4 sentences
- Sections:
  - Problem
  - Solution
  - Tech stack
  - What we learned
- Contributors module
- Related projects/ideas (optional)

---

## Data Model (conceptual)
Project
- id
- slug
- title
- summary
- content (markdown or rich text)
- tags (array)
- coverMediaUrl
- repoUrl
- demoUrl
- status (draft/published)
- createdAt, updatedAt

ProjectContributor
- projectId
- memberId
- role (frontend/backend/design/pm)
- order

---

## API Endpoints (example)
- `GET /projects` → list projects
- `GET /projects/{slug}` → project detail
- `POST /projects` → create (admin/lead)
- `PATCH /projects/{id}` → update (admin/lead)
- `DELETE /projects/{id}` → delete (admin)

---

## Common edge cases
- Empty state: “No projects yet” + CTA (submit)
- Missing demoUrl: hide demo button
- Long titles: clamp text
- Unpublished projects: only visible to admin/lead

---

## Implementation Notes (beginner-friendly)
### Frontend
- Use a card component for each project
- Fetch projects list on page load
- Show loading skeletons
- Use stable keys for rendering lists

### Backend
- Validate slugs are unique
- Only allow admin/lead to publish
- Consider caching project list (read-heavy)

---

## Testing checklist
- Can open project detail from index
- Filters/search work
- Unauthorized users cannot create/update/delete
- Project detail renders without repo/demo links