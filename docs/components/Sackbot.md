# Sackbot Module (Ambient Character)

## What is this?
Sackbot is an optional, playful ambient character that:
- Appears as a small animated mascot on screen
- Provides helpful hints and encouragement
- Adds personality to the app
- Can be dismissed and won't interrupt workflows

Think of it like Clippy, but actually helpful and not annoying.

## Why it matters
- Adds warmth and personality
- Provides contextual help without being intrusive
- Makes the app feel more alive
- Reinforces club brand/identity

---

## Design Principles (Critical)
Sackbot MUST be:
1. **Dismissible**: User can hide it permanently or temporarily
2. **Non-blocking**: Never covers important UI or blocks clicks
3. **Rate-limited**: Messages appear sparingly (max 1 per 5 minutes)
4. **Contextual**: Messages are relevant to what user is doing
5. **Optional**: First-time users see it, but can opt out

---

## User Experience
### Visual Design
- Small character (100-150px) in corner of screen
- Animated idle state (subtle breathing/bobbing)
- Speech bubble appears above/beside character
- Smooth entrance/exit animations

### Positioning
- Default: bottom-left corner
- Must not overlap with:
  - Chatbot button (bottom-right)
  - Navigation
  - Important CTAs
- User can drag to reposition (optional)

### Interaction States
1. **Idle**: Character visible, no message
2. **Speaking**: Speech bubble appears with message
3. **Dismissed**: Character hidden, small "Show Sackbot" button remains
4. **Hidden**: Completely hidden (user preference)

---

## Message Triggers (Contextual Help)
### Welcome Message
- First visit: "Hey! Welcome to AI Club. I'm Sackbot, here to help!"
- Returning user: "Welcome back! Check out the new projects."

### Contextual Hints
- On `/projects` with no filters: "Try filtering by tech stack to find specific projects"
- On `/ideas` after 30 seconds: "Don't forget to vote on ideas you like!"
- On empty `/playground`: "Try the Prompt Lab to generate creative prompts"
- After submitting idea: "Great idea! Share it with the club to get votes"
- On `/events` with upcoming event: "Don't forget to RSVP for tomorrow's workshop!"

### Encouragement
- After user creates first project: "Awesome! Your first project is live 🎉"
- After user votes on 5 ideas: "You're an active member! Keep it up"
- Random positive messages (rare): "You're doing great!", "Keep building cool stuff!"

---

## Message Rules (Anti-Annoyance)
1. **Rate Limiting**:
   - Max 1 message per 5 minutes
   - Max 3 messages per session
   - No messages on first 10 seconds of page load

2. **Priority System**:
   - High: Welcome message, important announcements
   - Medium: Contextual hints
   - Low: Encouragement, random messages

3. **Dismissal Behavior**:
   - Click "X" on speech bubble: hide current message
   - Click "Hide Sackbot": hide character for session
   - Settings toggle: hide permanently (stored in user preferences)

4. **No Interruptions**:
   - Never show during form submission
   - Never show during video/demo playback
   - Never show in modals or drawers

---

## Data Model
SackbotMessage (predefined messages)
- id
- trigger (welcome/contextual/encouragement)
- context (page or action that triggers it)
- message (text)
- priority (high/medium/low)
- isEnabled

UserSackbotPreference
- userId
- isEnabled (boolean)
- lastMessageAt (timestamp)
- messageCount (session counter)

---

## API Endpoints
- `GET /sackbot/message` → get next message based on context
- `POST /sackbot/dismiss` → log dismissal (for analytics)
- `PATCH /users/me/preferences` → update Sackbot enabled/disabled

---

## Implementation Notes
### Frontend
- Use React state to manage visibility
- Store dismissal preference in localStorage + backend
- Animate with CSS transitions or Framer Motion
- Use absolute positioning with z-index management
- Respect `prefers-reduced-motion`

### Backend
- Message selection logic:
  - Check user's last message timestamp
  - Check session message count
  - Filter by context (current page)
  - Select highest priority message
  - Return null if rate limited

### Animation Guidelines
- Entrance: fade + slide from bottom (300ms)
- Exit: fade out (200ms)
- Idle: subtle scale/rotate animation (2s loop)
- Speech bubble: fade + scale from character (250ms)

---

## Phase 1 (MVP)
- Static character image (no complex animation)
- 5-10 predefined messages
- Basic show/hide functionality
- localStorage persistence

## Phase 2 (Enhanced)
- Animated sprite or Lottie animation
- More contextual messages (20+)
- Personality variations (helpful/funny/encouraging)
- User can choose character style
- Integration with chatbot (click Sackbot to open chat)

---

## Common edge cases
- User dismisses immediately: respect preference, don't show again
- Multiple tabs open: sync dismissal state across tabs
- Mobile: smaller character, position carefully to avoid blocking
- Accessibility: ensure speech bubble text is readable, keyboard accessible
- Slow connection: don't block page load waiting for Sackbot assets

---

## Accessibility Considerations
- Speech bubble text must have sufficient contrast
- Provide keyboard shortcut to dismiss (Escape key)
- Screen reader announcement for messages (use aria-live)
- Option to disable animations
- Don't rely solely on Sackbot for critical information

---

## Testing checklist
- Character appears on first visit
- Can dismiss individual messages
- Can hide character for session
- Can disable permanently in settings
- Rate limiting works (max 1 per 5 minutes)
- Doesn't block important UI elements
- Animations respect prefers-reduced-motion
- Works on mobile without blocking content
- Keyboard accessible (Tab to focus, Escape to dismiss)
