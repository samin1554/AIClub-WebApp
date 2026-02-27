# Whiteboard Module (Drawing Canvas)

## What is this?
A simple “empty whiteboard” where users can draw freely.
This is primarily a fun/creative feature.

## Phase strategy
### MVP (single-user)
- Draw on canvas locally
- Clear button
- Export PNG (optional)

### Phase 2 (multiplayer realtime)
- Users join a session
- Strokes broadcast via WebSocket
- Optional: store strokes to DB for replay

## UX
- Tool controls: pen size, color, eraser, clear
- Canvas fills most of the page
- Works with mouse + touch + stylus

## Data model (Phase 2)
WhiteboardSession
- id
- title
- createdByMemberId
- createdAt
- isPublic

WhiteboardStroke
- id
- sessionId
- memberId
- points (JSON array)
- color
- width
- createdAt

## API endpoints (Phase 2)
- `GET /whiteboard/{id}` (history)
- `WS /whiteboard/{id}/live` (realtime strokes)

## Testing checklist
- Drawing works on mobile
- Resize doesn’t break coordinate mapping
- Multiplayer doesn’t lag with many strokes (later)