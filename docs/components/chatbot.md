# Chatbot / Q&A Module

## What is this?
A chatbot that helps users:
- learn about the club
- find projects
- get onboarding help
- answer FAQ
- (optional) assist with idea creation

It appears as:
- a floating button
- a right-side drawer with conversation history

## Key principle
**Frontend never calls the AI provider directly.**
Frontend calls our backend `/chat`.
Backend calls the AI provider securely.

## UX
- Floating icon bottom-right
- Drawer opens with:
  - message list
  - input box
  - “clear chat” (optional)
- Must be dismissible and not block navigation

## Data model
ChatSession (optional storage)
- id
- memberId (optional)
- createdAt
- sourcePage

ChatMessage
- id
- sessionId
- role (user/assistant/system)
- content
- createdAt

## API endpoints
- `POST /chat` → sends user message, returns assistant response
Optional:
- `GET /chat/sessions`
- `GET /chat/sessions/{id}`

## Safety + cost controls
- Rate limit per user/IP
- Input length limit
- Basic moderation (block obvious abuse)
- Timeout + fallback message on provider failure

## Testing checklist
- Drawer opens/closes
- Backend rate limiting works
- Errors show user-friendly message