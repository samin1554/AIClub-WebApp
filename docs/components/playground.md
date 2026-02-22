# Playground Module (Engage)

## What is this?
The Playground is a hub for fun, experimental AI tools and interactive features:
- Chatbot
- Whiteboard
- Prompt Lab
- Jokes/Facts
- Mini-games
- Spotify widget

It's the "fun zone" that keeps members engaged between projects.

## Why it matters
- Provides low-stakes ways to interact with AI
- Keeps members coming back
- Showcases club's technical creativity
- Offers learning opportunities in a playful context

---

## User Experience
### Playground Hub (`/playground`)
- Bento grid layout with tiles of different sizes
- Each tile is a "launcher" for a tool
- Tiles show:
  - Icon
  - Title
  - Short description (1 sentence)
  - "Launch" or "Open" button
- Tiles can have different states:
  - Available (clickable)
  - Coming Soon (grayed out)
  - New (badge)

### Tile Organization
**Large tiles** (featured):
- Chatbot
- Whiteboard

**Medium tiles**:
- Prompt Lab
- Mini-games

**Small tiles**:
- Jokes/Facts
- Spotify widget

### Navigation Pattern
Two approaches:
1. **Modal/Drawer**: Tool opens in overlay, can close back to hub
2. **Dedicated Route**: Navigate to `/playground/chat`, etc.

Recommendation: Use dedicated routes for complex tools (whiteboard, chatbot), modals for simple ones (jokes).

---

## Playground Tools (Summary)
### 1. Chatbot (`/playground/chat`)
- AI assistant for club questions
- See `chatbot.md` for details

### 2. Whiteboard (`/playground/whiteboard`)
- Drawing canvas
- See `whiteboard.md` for details

### 3. Prompt Lab (`/playground/prompt-lab`)
- Prompt generator and templates
- See `prompt-lab.md` for details

### 4. Jokes/Facts (`/playground/jokes`)
- Daily joke and fun fact
- See `joke-facts.md` for details

### 5. Mini-games (`/playground/minigames`)
- Simple browser games
- See `minigames.md` for details

### 6. Spotify (`/playground/music`)
- Music player/embed
- See `spotify.md` for details

---

## Data Model
PlaygroundTool (optional, if you want dynamic configuration)
- id
- slug (e.g., "chatbot", "whiteboard")
- title
- description
- iconUrl
- route
- isEnabled
- isNew (boolean, shows "New" badge)
- sortOrder
- size (small/medium/large)

---

## API Endpoints
If tools are dynamically configured:
- `GET /playground/tools` → list available tools

Otherwise, hardcode the tool list in frontend.

---

## Design Considerations
### Bento Grid Layout
Use CSS Grid with different tile sizes:
```
[Chatbot    ] [Whiteboard ]
[Prompt Lab ] [Mini-games ]
[Jokes] [Spotify]
```

### Responsive Behavior
- Desktop: 3-4 columns
- Tablet: 2 columns
- Mobile: 1 column (stack vertically)

### Visual Hierarchy
- Use different background colors or gradients per tile
- Subtle hover effects (lift, glow)
- Icons should be consistent style (outline or filled)

---

## Common edge cases
- Tool disabled: show "Coming Soon" state
- Tool fails to load: show error message with retry button
- Empty state: shouldn't happen, but show message if no tools available
- User not logged in: some tools may require auth (show "Login to use")

---

## Implementation Notes
### Frontend
- Lazy load tool components (code splitting)
- Use React.lazy() or Next.js dynamic imports
- Preload featured tools on hub page
- Track tool usage (analytics) to see what's popular

### Backend
- Each tool has its own API endpoints (see individual docs)
- Rate limiting per tool
- Usage tracking (optional)

---

## Phase 2 Enhancements
- User favorites (pin tools to top)
- Usage stats ("You've used Chatbot 15 times")
- Tool recommendations based on activity
- Shareable tool outputs (e.g., share a whiteboard drawing)
- Collaborative tools (multi-user whiteboard)

---

## Testing checklist
- All tiles render correctly
- Clicking tile navigates to tool
- Disabled tools show "Coming Soon"
- Layout responsive on mobile
- Tools load without blocking hub page
- Back navigation works from tools to hub
