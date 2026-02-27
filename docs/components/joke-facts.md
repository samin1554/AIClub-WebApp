# Joke of the Day + Fun Fact Module

## What is this?
A lightweight daily content feature.

## Approaches
### Simple (manual)
Admins add jokes/facts via admin panel.

### Automated (later)
Backend scheduled job updates daily content.
(If using AI generation, must moderate and rate limit.)

## UX
- Small card on home page
- Dedicated `/playground/jokes` page with archive

## Testing checklist
- Empty state handled
- Doesn’t block page load