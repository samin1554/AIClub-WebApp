# Mini-games Module

## What is this?
Small games embedded in a window (e.g., Tic-tac-toe, Snake, Memory).

## Rules
- Games must be sandboxed (no access to auth tokens)
- Must not slow down core pages
- Load only when user visits the mini-games route

## UX
- `/playground/minigames` lists game cards
- Each game loads in its own route:
  - `/playground/minigames/tictactoe`

## Testing checklist
- Works on mobile
- Doesn’t freeze UI