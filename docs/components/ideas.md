# Ideas Board Module

## What is this?
The Ideas board is a place to submit and discuss new project ideas.
Ideas are displayed as **portrait cards** (like a modern “idea wall”).

## Why it matters
This is how the club stays alive:
- new ideas continuously enter the system
- members vote/comment
- leads pick ideas to build

---

## UX
### Ideas Board (`/ideas`)
- Card wall (grid or masonry)
- Each card shows:
  - Title
  - Short pitch
  - Tags
  - Vote count
- Clicking a card opens detail (page or drawer)

### Idea Detail (`/ideas/:id`)
- Full description
- Comments thread
- Vote button
- “Promote to Project” (lead/admin only)

---

## Data model
Idea
- id
- title
- pitch (short)
- description (long)
- tags[]
- createdByMemberId
- status (new/needs-work/accepted/rejected)
- createdAt

IdeaVote
- ideaId
- memberId
- value (+1 or 0/1)
- createdAt

IdeaComment
- id
- ideaId
- memberId
- body
- createdAt

---

## API endpoints
- `GET /ideas`
- `POST /ideas` (member)
- `GET /ideas/{id}`
- `POST /ideas/{id}/vote` (member)
- `POST /ideas/{id}/comments` (member)
- `PATCH /ideas/{id}` (lead/admin, e.g. status)

---

## Anti-spam / quality
- Rate limit votes per user
- Only authenticated members can vote/comment
- Basic moderation: report flag, admin hide

---

## Common edge cases
- A user tries to vote twice → backend must prevent duplicates
- Empty board → show CTA “Submit the first idea”
- Overly long descriptions → clamp in card view

---

## Testing checklist
- Submit idea works
- Vote increments/decrements correctly
- Only members can vote/comment
- Admin can change status