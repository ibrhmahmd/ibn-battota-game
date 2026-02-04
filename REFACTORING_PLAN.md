# Refactoring Plan: Ibn Batota's Journey - Simplified Edition

## 1. Executive Summary

This plan outlines the steps to transform the current "Ibn Batota's Journey" codebase into a beginner-friendly, maintenance-ready project. The goal is to remove complex mechanics (camera, state management overhead) and enforce a straightforward procedural coding style that a teenager with basic Python knowledge can understand.

## 2. Core Requirements Implementation

### 2.1 Screen Display Simplification
*   **Action**: Remove all Fullscreen toggles (F key).
*   **Action**: Lock resolution to `1280x720` for all states.
*   **Action**: Eliminate the Camera system in `world_map.py`.
*   **Strategy**: Resize the `2400x1024` world map asset to fit exactly into `1280x720`.
    *   *Note*: This changes the aspect ratio. We will accept the distortion for the sake of simplicity (no scrolling logic).
    *   **Scaling Factors**:
        *   X Scale: `1280 / 2400 ≈ 0.533`
        *   Y Scale: `720 / 1024 ≈ 0.703`

### 2.2 Architecture Simplification
*   **Action**: Flatten the module structure where possible.
*   **Action**: Replace `init()` functions with a unified `reset_level()` naming convention that explicitly resets global variables at the top of the file.
*   **Action**: Remove `game_states.py` imports where unnecessary and use string literals or simple global constants in `main.py` for clarity.

### 2.3 Beginner Code Standards
*   **Variable Naming**: Replace `vx`, `vy` with `velocity_x`, `velocity_y`.
*   **Control Flow**: Use simple `if/elif/else`. Avoid list comprehensions or complex lambdas.
*   **Comments**: Add "Step 1", "Step 2" style comments to logic blocks.

---

## 3. Step-by-Step Migration Strategy

### Step 1: Asset Standardization (Pre-Code)
Before touching code, we must ensure the background fits the screen.
1.  **Task**: Resize `images/backgrounds/map.png` from `2400x1024` to `1280x720`.
2.  **Task**: Update `CITIES_CONFIG` coordinates in `constants.py` to match the new resolution.

### Step 2: World Map Simplification
**File**: `world_map.py`
1.  **Remove**: `camera_x`, `camera_y`, `draw_at_camera`, `draw_character` (camera offset logic).
2.  **Modify**: `update()` to simply check `if character.x > WIDTH: character.x = WIDTH`.
3.  **Simplify**: City interaction logic. Instead of `math.hypot`, use `actor.collidepoint()` or simple distance check.

### Step 3: Architecture Flattening
**File**: `main.py`
1.  **Refactor**: Remove the dynamic state method calls if they are too indirect.
    *   *Current*: `level_module.update()`
    *   *Proposed*: Keep this, but ensure `level_module` has a standardized API (`draw`, `update`, `reset`).
2.  **Refactor**: Remove `game_states.py` dependency if it only holds 4 strings. Define them at the top of `main.py` for immediate visibility.

### Step 4: Level Logic Refactoring
**File**: `levels/level_tangier.py`
1.  **Rename**: `vx` -> `velocity_x`, `vy` -> `velocity_y`.
2.  **Simplify**: Physics loop.
    *   *Before*: Separated `handle_movement`, `handle_collisions`.
    *   *After*: A single `update_player_physics()` function with clear step-by-step comments.

---

## 4. Complex Components to Simplify

| Component | Current Implementation | Simplified Implementation |
| :--- | :--- | :--- |
| **Camera** | `camera_x` offset, `draw_at_camera` helper, smooth interpolation. | **None**. Map is static 1280x720 image. Character moves directly on screen coordinates. |
| **City Coordinates** | Large map coordinates (e.g., `2300, 765`). | Scaled screen coordinates (e.g., `1226, 538`). |
| **State Machine** | `game_states.py` imports, `change_state()` function. | Simple string variable `current_level = "map"`. Direct assignment. |
| **Physics** | `vx`, `vy`, separated collision checks. | `velocity_x`, `velocity_y`. Explicit `if player.colliderect(platform):` blocks. |
| **Initialization** | `init()` called on module load. | `reset()` function called explicitly when entering a level. |

---

## 5. Coordinate Mapping (For World Map)

To fit the map on one screen, we must update `constants.py`.

| City | Old (X, Y) | New (X, Y) `[x*0.53, y*0.70]` |
| :--- | :--- | :--- |
| **Tangier** | (200, 600) | **(106, 420)** |
| **Fez** | (60, 700) | **(32, 490)** |
| **Granada** | (350, 650) | **(186, 455)** |
| **Istanbul** | (730, 500) | **(390, 350)** |
| **Cairo** | (900, 750) | **(480, 525)** |
| **Damascus** | (1125, 620) | **(600, 434)** |
| **Baghdad** | (1450, 670) | **(773, 470)** |
| **Medina** | (1200, 750) | **(640, 525)** |
| **Mecca** | (1350, 825) | **(720, 577)** |
| **Persia** | (1600, 650) | **(853, 455)** |
| **Delhi** | (2300, 765) | **(1226, 535)** |
| **Beijing** | (2200, 300) | **(1173, 210)** |
| **Timbuktu** | (100, 850) | **(53, 595)** |

*Note: New coordinates are approximate and may need minor visual tuning.*

---

## 6. Testing Checklist

- [ ] **Startup**: Game opens in 1280x720 window immediately.
- [ ] **Map**: Entire world map is visible without scrolling.
- [ ] **Movement**: Character moves to edges of screen but not beyond.
- [ ] **Interaction**: Clicking a city icon correctly enters the mini-game.
- [ ] **Return**: Finishing/Exiting a mini-game returns to the Map state.
- [ ] **Physics**: Tangier level platforming feels responsive (jumping/landing works).
- [ ] **Restart**: Re-entering a level resets all items and player position.

## 7. Performance Benchmarks

Since we are removing the camera and reducing the map drawing complexity (drawing 1 image vs calculating offsets), performance is expected to **improve** or remain stable.
- **Target FPS**: 60 FPS (standard for pgzero).
- **Memory**: Lower texture memory usage (smaller background if resized, or same if scaled).

