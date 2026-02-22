# Members Module (Showcase)

## What is this?
The Members module displays:
- Club member directory
- Individual member profiles
- Skills and expertise
- Contribution history (projects they've worked on)
- Contact/social links

This is the "team roster" that shows who makes the club work.

## Why it matters
- Helps new members find mentors with specific skills
- Shows external visitors the talent pool
- Recognizes contributions
- Facilitates collaboration

---

## User Experience
### Members Directory (`/members`)
- Grid of member cards
- Filters: role (lead/member), skills, year joined
- Search by name
- Sort: newest / most active / alphabetical

Each card shows:
- Avatar
- Name
- Role badge (Lead, Member, Alumni)
- Top 3 skills
- Project count

### Member Profile Page (`/members/:id`)
- Hero section: avatar + name + role + social links
- Bio (2-3 sentences)
- Skills section (tags with proficiency level optional)
- Projects contributed to (cards with role)
- GitHub/LinkedIn/portfolio links
- Join date

---

## Data Model (conceptual)
Member
- id (FK to users.id)
- userId
- displayName
- bio
- avatarUrl
- skills (array of strings)
- githubUrl
- linkedinUrl
- portfolioUrl
- websiteUrl
- joinedAt
- isAlumni (boolean)
- graduationYear (optional)

MemberSkill (optional, if you want proficiency tracking)
- memberId
- skill
- proficiency (beginner/intermediate/advanced)

---

## API Endpoints
- `GET /members` → list all members
- `GET /members/{id}` → member profile detail
- `PATCH /members/{id}` → update own profile (authenticated)
- `POST /members` → create profile (admin/lead, or auto-create on first login)

---

## Skills Taxonomy (recommended)
To avoid chaos, maintain a predefined skills list:

**Frontend**: React, Vue, Angular, TypeScript, CSS, Tailwind, Next.js
**Backend**: Python, FastAPI, Node.js, Express, Django, Flask
**Database**: PostgreSQL, MongoDB, Redis, SQL
**AI/ML**: PyTorch, TensorFlow, Scikit-learn, LangChain, OpenAI API
**DevOps**: Docker, CI/CD, AWS, Vercel, Railway
**Design**: Figma, UI/UX, Prototyping
**Other**: Git, Testing, Documentation, Project Management

Allow custom skills but suggest from this list.

---

## Common edge cases
- Empty state: "No members yet" (shouldn't happen but handle it)
- Member with no projects: show "No projects yet" + CTA to join one
- Missing avatar: use initials or default avatar
- Alumni members: show "Alumni" badge, optionally filter out by default
- Long bios: clamp to 3 lines in directory, full text on profile

---

## Implementation Notes
### Frontend
- Use avatar component with fallback to initials
- Skills should be clickable to filter directory by that skill
- Show loading skeletons while fetching
- Cache member list (changes infrequently)

### Backend
- Only allow users to edit their own profile (unless admin)
- Validate URLs (GitHub, LinkedIn format)
- Normalize skill names (lowercase, trim whitespace)
- Consider caching member directory (read-heavy)

---

## Testing checklist
- Can view member directory
- Can filter by skills
- Can search by name
- Member can update own profile
- Non-member cannot edit profiles
- Profile shows correct projects
- Alumni badge displays correctly
