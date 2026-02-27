# Requests Module (Build Requests / Intake Pipeline)

## What is this?
The Requests module is where people ask the club to build something:
- A student wants a simple app
- A professor wants a tool
- A club member proposes an internal request

Requests are NOT the same as Ideas:
- **Ideas** = “we might build this”
- **Requests** = “someone wants this built”

## UX
### Requests page (`/requests`)
Two parts:
1) Request submission form
2) Request queue (for members/leads)

### Request detail
- Problem description
- Status
- Comments
- Assigned member

---

## Request lifecycle
- New
- Reviewing
- Accepted
- In Progress
- Shipped
- Rejected

---

## Data model
Request
- id
- title
- problem
- desiredOutcome
- constraints
- requesterName (optional)
- requesterContact (optional)
- status
- priority
- assignedMemberId (optional)
- createdAt

RequestComment
- id
- requestId
- memberId
- body
- createdAt

---

## API endpoints
Public submission (if allowed):
- `POST /requests`

Member views:
- `GET /requests` (members only)
- `GET /requests/{id}`

Lead/admin actions:
- `PATCH /requests/{id}` (status/assignment/priority)
- `POST /requests/{id}/comments`

---

## Security + spam controls
If public requests are allowed:
- CAPTCHA or basic spam filtering (optional)
- Rate limit by IP
- Require email verification if you allow contact fields

---

## Testing checklist
- Public can submit (if enabled)
- Members can view queue
- Only lead/admin can change status
- Comments show correct author + timestamps