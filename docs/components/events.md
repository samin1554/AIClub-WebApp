# Events Module (Engage)

## What is this?
The Events module displays:
- Upcoming club events (meetings, workshops, hackathons)
- Event details (time, location, agenda)
- RSVP functionality
- Past events archive

This keeps members engaged and informed about club activities.

## Why it matters
- Drives attendance
- Keeps members in the loop
- Shows activity to prospective members
- Provides event history for the club

---

## User Experience
### Events List (`/events`)
- Timeline or card layout
- Upcoming events section (prominent)
- Past events section (collapsed or separate tab)
- Each event card shows:
  - Title
  - Date/time
  - Location (physical or virtual)
  - RSVP count
  - Quick RSVP button

### Event Detail Page (`/events/:id`)
- Hero section: title + date/time + location
- Description (markdown)
- Agenda (optional)
- RSVP button (changes to "Cancel RSVP" if already registered)
- RSVP list (names + avatars of attendees)
- Meeting link (Zoom/Google Meet) - only visible to RSVPed members
- Calendar export button (.ics file)
- Related projects/ideas (optional)

---

## Data Model
Event
- id
- title
- description (markdown)
- startsAt (timestamp)
- endsAt (timestamp)
- location (string, e.g., "Room 301" or "Virtual")
- meetingUrl (optional, for virtual events)
- meetingPassword (optional)
- maxAttendees (optional, null = unlimited)
- isPublic (boolean, can non-members see it?)
- createdByMemberId
- createdAt
- updatedAt

EventRSVP
- id
- eventId
- userId
- status (going/maybe/not_going)
- createdAt
- updatedAt

---

## API Endpoints
- `GET /events` → list events (query params: upcoming=true, past=true)
- `GET /events/{id}` → event detail
- `POST /events` → create event (lead/admin)
- `PATCH /events/{id}` → update event (lead/admin)
- `DELETE /events/{id}` → delete event (admin)
- `POST /events/{id}/rsvp` → RSVP to event (member)
- `DELETE /events/{id}/rsvp` → cancel RSVP (member)
- `GET /events/{id}/attendees` → list RSVPs

---

## RSVP Workflow
1. Member clicks "RSVP" on event
2. Backend creates EventRSVP record with status="going"
3. Frontend updates button to "Cancel RSVP" and increments count
4. If event has maxAttendees, check capacity before allowing RSVP
5. If full, show "Event Full" or "Join Waitlist" option

### RSVP Status Options
- **going**: confirmed attendance
- **maybe**: interested but not confirmed (optional)
- **not_going**: explicitly declined (optional, or just delete RSVP)

---

## Calendar Integration
Generate .ics file with:
- Event title
- Start/end time
- Location
- Description
- Meeting URL in description

Users can download and add to Google Calendar, Apple Calendar, Outlook.

---

## Notifications (Phase 2)
- Email reminder 24 hours before event (to RSVPed members)
- Email with meeting link 1 hour before virtual events
- Push notification option (if you add PWA support)

---

## Common edge cases
- Event in the past: disable RSVP, show "Event Ended"
- Event at capacity: show "Full" or waitlist option
- Missing meeting URL: hide meeting link section
- Event cancelled: show banner, send notification to RSVPed members
- User not logged in: show "Login to RSVP"
- Timezone handling: store in UTC, display in user's local timezone

---

## Implementation Notes
### Frontend
- Use date library (date-fns or dayjs) for formatting
- Show relative time ("in 2 days", "tomorrow at 3pm")
- Highlight upcoming events (within 7 days)
- Show timezone clearly
- Countdown timer for events starting soon (optional)

### Backend
- Store all timestamps in UTC
- Validate startsAt < endsAt
- Only allow lead/admin to create/edit events
- Rate limit RSVP changes (prevent spam)
- Send email notifications (use background job queue)

---

## Testing checklist
- Can view upcoming events
- Can RSVP to event
- Can cancel RSVP
- RSVP count updates correctly
- Cannot RSVP to full event
- Cannot RSVP to past event
- Meeting URL only visible to RSVPed members
- Calendar export works
- Past events show in archive
