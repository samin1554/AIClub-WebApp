# Spotify Module

## What is this?
A music feature for fun / atmosphere.
Options:
- MVP: Spotify embed widgets (simple)
- Later: OAuth login + now-playing + playlist control
- Later: in-app playback (harder)

## MVP approach (recommended first)
Use Spotify Embeds:
- No authentication needed
- Minimal failure points

## Phase 2 approach
OAuth authorization:
- Store tokens securely in backend
- Provide “Now Playing” widget per user (optional)

## UX ideas
- Small “Now Playing” card on Playground or Home
- “Study playlist” embed for club sessions

## Testing checklist
- Embed loads on mobile
- If blocked by browser, show fallback message