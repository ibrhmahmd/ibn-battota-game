# Level Implementation Template (Reference: level_tangier.py)

## Level Module Structure

### Module Globals
```python
GRAVITY = 0.5              # Physics constant
JUMP_STRENGTH = -12        # Jump velocity
MOVE_SPEED = 6            # Horizontal movement speed
player = Actor(...)        # Player character
back_button = Actor(...)   # Return to map button
platforms = [...]          # Platform list (collectibles landing spots)
items = [...]              # Collectible items (10 per level)
items_collected = 0        # Score counter
ground_y = 650             # Base ground level
on_ground = False          # Player state flag
show_mission = True        # Mission overlay flag
```

### Required Functions

#### `draw(screen)`
- Clears screen
- Blits background image
- Draws platforms
- Draws collectible items
- Draws player
- Draws back button
- Draws HUD (item counter)
- Conditional: Victory seal if items_collected >= 10
- Conditional: Leaf particles if not victory
- Mission overlay if `show_mission` is True

#### `update(keyboard)`
- Toggles `show_mission` on ESC key
- Handles player movement (LEFT/RIGHT/UP/DOWN keys)
- Applies gravity & jump mechanics
- Platform collision detection
- Item collection detection
- Triggers victory when items_collected = 10

#### `on_mouse_down(pos)`
- Back button collision → returns `"map"`
- Mission overlay click → hides overlay
- Returns None otherwise (stay in level)

## Level Collectibles Pattern
Each city has 10 thematic items:
- Tangier: prayer_mat, compass, holy_quran, etc.
- Format: `{"actor": Actor("items/collectibles/[NAME]")}`
- Each item has: `.pos` (x, y) set explicitly
- On collection: remove from list, increment counter

## Platform Arrangement Strategy
- 10 platforms per level
- Positioned to create jumping puzzle progression
- Use `.center` property for positioning
- Example: `Actor("items/platforms/platform", center=(300, 600))`

## UI/HUD Elements
- **Item Counter**: Top-left (20, 100), fontsize=40, white text
- **Victory Text**: Center (WIDTH/2, HEIGHT/2+60) when all items collected
- **Mission Overlay**: Semi-transparent black surface + briefing frame

## Visual Effects
- **Leaf Particles**: Drawn conditionally when not in victory state
- **Victory Seal**: Actor centered at (WIDTH/2, HEIGHT/2)

## State Flags
- `show_mission` - Toggle mission briefing (ESC key)
- `on_ground` - Player grounded state (for jump logic)
- `items_collected` - Running counter (0-10)

## Asset Paths (Tangier Reference)
```
images/
  backgrounds/bg_tangier          # Level background
  items/platforms/platform         # Platform sprite
  items/collectibles/[ITEM_NAME]  # 10 collectible sprites
  items/level_passed_seal         # Victory seal
  ui/back_btn                     # Return button
  levels_texts/text_tangier       # Mission briefing text
```

## Integration with main.py
- Added to import: `from levels import level_[CITY]`
- Added to draw(): `elif current_screen == "[CITY]": level_[CITY].draw(screen)`
- Added to update(): `elif current_screen == "[CITY]": level_[CITY].update(keyboard)`
- Added to on_mouse_down(): Similar elif block calling level_[CITY].on_mouse_down(pos)
- Added to on_key_down(): Similar elif block for level-specific key events

## Collectible Items Library (Tangier)
1. prayer_mat
2. leather_sandals
3. compass
4. holy_quran
5. woolen_djellaba
6. water_skin
7. silver_dirhams
8. oil_lamp
9. travel_documents
10. inkwell_and_kalam
