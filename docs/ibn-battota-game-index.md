# Ibn Battota Game - Project Index

## Project Overview
**Educational platformer game** based on the travels of Ibn Battota (14th-century Moroccan explorer)
- Built with **Pygame Zero** (pgzrun)
- Resolution: 1280x720
- 5 playable levels: Tangier, Fez, Cairo, Damascus, Timbuktu
- World map navigation system

---

## Core Architecture

### Screen States (main.py)
- `"start"` → Start screen with play button
- `"map"` → World map with 13 cities (navigate character to select level)
- `"tangier"` → Level 1 (Tangier)
- `"fez"` → Level 2 (Fez)
- `"cairo"` → Level 3 (Cairo)
- `"damascus"` → Level 4 (Damascus)
- `"timbuktu"` → Level 5 (Timbuktu)

### Global Systems
- **Mute button**: UI element in top-right (WIDTH-60, 60) for sound control
- **Screen management**: `current_screen` global variable
- **Event handling**: draw() → update() → on_mouse_down() → on_key_down()

---

## File Structure

### Root Level Python Files
| File | Purpose |
|------|---------|
| `main.py` | Entry point, screen routing, event dispatcher, mute button |
| `start_screen.py` | Start menu with play button |
| `world_map.py` | World map with 13 city icons, character movement |
| `mission_overlay.py` | Mission briefing overlay system |

### Levels Directory (`levels/`)
All level files follow same pattern:
- `level_tangier.py` - **Fully implemented** (10 collectibles, platforms, particles)
- `level_fez.py` - Level 2
- `level_cairo.py` - Level 3
- `level_damascus.py` - Level 4
- `level_timbuktu.py` - Level 5

### Assets Structure (`images/`)
- `backgrounds/` → Map, level BGs, city icons, start screen
- `characters/` → Character sprites
- `items/` → Collectibles, platforms, mission briefing frame, level passed seal
- `ui/` → Buttons (start, back), music toggle icon
- `levels_texts/` → Mission text images per level

### Audio (`music/`)
- Background music tracks (not indexed yet)

---

## Core Game Mechanics (From level_tangier.py)

### Physics
- **GRAVITY**: 0.5
- **JUMP_STRENGTH**: -12
- **MOVE_SPEED**: 6
- **GROUND_Y**: 650

### Level Components
1. **Player**: Character actor with position, speed_y
2. **Platforms**: 10 static platform actors
3. **Collectibles**: 10 items to collect (prayer_mat, compass, quran, etc.)
4. **Victory Condition**: Collect all 10 items → show seal → press SPACE to continue
5. **UI**: Back button (80, 50), item counter (top-left)

### Visual Features
- Leaf particles effect
- Victory seal animation
- Mission briefing overlay (semi-transparent dark background)

---

## World Map Configuration (13 Cities)
```
(name, x, y) positions:
- Tangier, Fez, Granada → North Africa
- Istanbul, Persia, Baghdad → Middle East
- Cairo, Damascus, Medina, Mecca → Levant/Arabian Peninsula
- Delhi → India
- Timbuktu → Sub-Saharan Africa
- Beijing → Far East
```

---

## Key Implementation Patterns

### Screen Module Pattern
Each screen module (start_screen, world_map, level_*.py) provides:
- `draw(screen)` - Render frame
- `update(keyboard)` - Game logic
- `on_mouse_down(pos)` - Click handling (returns new screen name or None)

### Actor Positioning
- Actors use `.pos`, `.x`, `.y`, `.center` properties
- Collision detection: `.collidepoint(pos)`

### Event Flow
1. `draw()` renders current screen
2. `update()` processes input (keyboard state)
3. `on_mouse_down()` handles clicks, may return screen name to transition

---

## Dependencies
- `pgzrun` - Pygame Zero runtime
- `pygame` - Low-level graphics
- Standard library: `os`, `random`

---

## Status Notes
- ✅ Start screen complete
- ✅ World map complete with 13 cities
- ✅ Level Tangier fully implemented as template
- ⏳ Levels Fez, Cairo, Damascus, Timbuktu (structure exists, needs content)
- ⏳ Music system (directory exists, integration unknown)
