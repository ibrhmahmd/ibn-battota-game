# Code Architecture Plan: Ibn Batota's Journey (pgzero)

This document outlines a simple, beginner-friendly code architecture and folder structure for the "Ibn Batota's Journey" game, utilizing the Python `pgzero` library. The design prioritizes readability, modularity, and ease of understanding for developers new to Python and game development.

## 1. Project Folder Structure

The game will be organized into a clear and logical directory structure to manage various components and assets. This structure facilitates easy navigation, asset management, and future expansion.

```
ibn_batota_game/
├── main.py
├── game_states.py
├── constants.py
├── levels/
│   ├── __init__.py
│   ├── level_tangier.py
│   ├── level_fez.py
│   ├── level_granada.py
│   ├── level_cairo.py
│   ├── level_damascus.py
│   ├── level_medina.py
│   ├── level_mecca.py
│   ├── level_baghdad.py
│   ├── level_persia.py
│   ├── level_istanbul.py
│   ├── level_delhi.py
│   ├── level_beijing.py
│   └── level_timbuktu.py
├── assets/
│   ├── images/
│   │   ├── backgrounds/
│   │   │   ├── bg_tangier.png
│   │   │   ├── bg_fez.png
│   │   │   └── ... (all 13 city backgrounds)
│   │   ├── story_frames/
│   │   │   ├── story_intro_01.png
│   │   │   ├── story_intro_02.png
│   │   │   └── ... (all 30 story frames)
│   │   └── ui/
│   │       ├── start_button.png
│   │       ├── mute_button_on.png
│   │       └── mute_button_off.png
│   ├── music/
│   │   ├── tangier_music.mp3
│   │   ├── fez_music.mp3
│   │   └── ... (all 13 city music tracks)
│   └── sounds/
│       ├── click.wav
│       └── level_complete.wav
├── data/
│   ├── save_game.json
│   └── historical_facts.json
└── utils/
    ├── __init__.py
    └── game_utils.py
```

### File Descriptions:

*   **`main.py`**: This is the central entry point of the game. It initializes the `pgzero` window, manages the main game loop (`draw`, `update`), and orchestrates transitions between different game states (e.g., start menu, world map, mini-games, story cinematics). It will import and call functions from other modules based on the current game state.
*   **`game_states.py`**: This file will define constants representing the various states the game can be in (e.g., `STATE_START_MENU`, `STATE_WORLD_MAP`, `STATE_MINI_GAME_TANGIER`, `STATE_STORY_INTRO`). Using constants makes the code more readable and less prone to errors.
*   **`constants.py`**: Contains all global configuration variables, such as screen dimensions (`WIDTH`, `HEIGHT`), character movement speed, jump parameters, and the structured data for city configurations (names, positions, unlock status).
*   **`levels/`**: This directory acts as a Python package, holding individual modules for each city's mini-game logic. Each `level_*.py` file will encapsulate the specific `draw()`, `update()`, and event handling (`on_mouse_down`, `on_key_down`) functions for its respective mini-game.
    *   **`__init__.py`**: An empty file that marks `levels/` as a Python package.
    *   **`level_tangier.py`, `level_fez.py`, etc.**: Each file will contain the game logic, actors, and functions necessary for that city's mini-game. This modular approach keeps the code organized and prevents a single, monolithic file.
*   **`assets/`**: This top-level directory is where `pgzero` automatically looks for game resources. It is further subdivided for clarity:
    *   **`images/`**: Contains all visual assets.
        *   **`backgrounds/`**: Stores the 13 pixel art city backgrounds.
        *   **`story_frames/`**: Holds the 30 pixel art story frames (10 for each of the 3 story levels).
        *   **`ui/`**: Contains images for user interface elements like buttons and icons.
    *   **`music/`**: Stores background music tracks for each city and general game themes.
    *   **`sounds/`**: Contains short sound effects for interactions, successes, and failures.
*   **`data/`**: Used for persistent game data.
    *   **`save_game.json`**: A JSON file to store the player's progress, such as completed cities, unlocked facts, and current game state. This allows players to resume their game.
    *   **`historical_facts.json`**: A JSON file containing all the unlockable historical facts associated with each city, to be displayed as player rewards.
*   **`utils/`**: A directory for general utility functions that might be used across different parts of the game.
    *   **`__init__.py`**: Marks `utils/` as a Python package.
    *   **`game_utils.py`**: Could contain helper functions for tasks like managing sound playback, handling file I/O for save games, or common calculations.

## 2. Core Game Architecture and State Management

The game's architecture will revolve around a simple **state machine pattern**, which is ideal for managing different screens and gameplay modes in `pgzero`. This approach makes the game flow predictable and easy to debug.

*   **Global Game State Variable**: A single global variable, `current_game_state` (defined in `main.py` and updated using constants from `game_states.py`), will dictate the active screen or mini-game. For example, `current_game_state = STATE_START_MENU` means the start screen is active.
*   **Centralized Game Loop**: The `draw()` and `update()` functions in `main.py` will act as dispatchers. They will check the value of `current_game_state` and then call the appropriate `draw()` and `update()` functions belonging to the currently active screen or mini-game module.
    ```python
    # main.py
    import pgzrun
    from game_states import *
    import levels.level_tangier
    # ... import other level modules

    WIDTH = 800
    HEIGHT = 600

    current_game_state = STATE_START_MENU

    def draw():
        screen.clear()
        if current_game_state == STATE_START_MENU:
            draw_start_menu()
        elif current_game_state == STATE_WORLD_MAP:
            draw_world_map()
        elif current_game_state == STATE_MINI_GAME_TANGIER:
            levels.level_tangier.draw()
        # ... other states

    def update():
        global current_game_state
        if current_game_state == STATE_START_MENU:
            update_start_menu()
        elif current_game_state == STATE_WORLD_MAP:
            update_world_map()
        elif current_game_state == STATE_MINI_GAME_TANGIER:
            levels.level_tangier.update()
        # ... other states

    def on_mouse_down(pos):
        global current_game_state
        if current_game_state == STATE_START_MENU:
            handle_start_menu_click(pos)
        elif current_game_state == STATE_WORLD_MAP:
            handle_world_map_click(pos)
        elif current_game_state == STATE_MINI_GAME_TANGIER:
            levels.level_tangier.on_mouse_down(pos)
        # ... other states

    # Example placeholder functions for start menu and world map
    def draw_start_menu():
        screen.blit("ui/start_screen_background", (0,0))
        # ... draw start button

    def update_start_menu():
        pass # No continuous update needed for a static menu

    def handle_start_menu_click(pos):
        global current_game_state
        # Example: if start_button.collidepoint(pos):
        # current_game_state = STATE_WORLD_MAP

    def draw_world_map():
        screen.blit("images/map", (0,0))
        # ... draw city icons

    def update_world_map():
        pass

    def handle_world_map_click(pos):
        global current_game_state
        # Example: if city_tangier_icon.collidepoint(pos):
        # current_game_state = STATE_MINI_GAME_TANGIER

    pgzrun.go()
    ```
*   **Modular Mini-Game Logic**: Each mini-game in the `levels/` directory will be self-contained. For instance, `level_tangier.py` will have its own `draw()`, `update()`, and `on_mouse_down()` functions that only run when `current_game_state` is `STATE_MINI_GAME_TANGIER`. This keeps the logic for each mini-game separate and manageable.
*   **Asset Management**: `pgzero` simplifies asset loading. Images placed in `assets/images/` can be accessed directly by their filename (e.g., `Actor("ui/start_button")`). Music and sounds are similarly loaded (`music.play("tangier_music")`, `sound.play("click")`).

## 3. Beginner-Friendly Implementation Guide

Here's a step-by-step guide for a beginner to implement this architecture:

1.  **Set up the Project Folder**: Create the `ibn_batota_game/` directory and all subdirectories as outlined in Section 1.
2.  **`constants.py`**: Start by defining `WIDTH`, `HEIGHT`, and the `CITIES_CONFIG` list (similar to the demo, but ensure it aligns with the 13 cities in your design document).
3.  **`game_states.py`**: Define simple string constants for each major game state. For example:
    ```python
    STATE_START_MENU = "start_menu"
    STATE_WORLD_MAP = "world_map"
    STATE_STORY_INTRO = "story_intro"
    STATE_MINI_GAME_TANGIER = "mini_game_tangier"
    # ... and so on for all cities and story levels
    ```
4.  **`main.py` (Initial Setup)**: Copy the basic `pgzero` structure provided in Section 2. Implement the `draw_start_menu()`, `update_start_menu()`, and `handle_start_menu_click()` functions first. Get the start screen and the transition to the world map working.
5.  **`levels/level_tangier.py` (First Mini-Game)**: Create this file. It will need its own `draw()`, `update()`, and `on_mouse_down()` functions. For the "Packing for the Pilgrimage" mini-game, you'll need `Actor` objects for the items and the travel bag. Implement the drag-and-drop logic here. When the mini-game is complete, it should set `main.current_game_state = STATE_WORLD_MAP` (or the next story level).
6.  **World Map Logic**: In `main.py`, implement `draw_world_map()`, `update_world_map()`, and `handle_world_map_click()`. Use `Actor` objects for each city icon. When a city is clicked, check if it's unlocked. If so, transition to its mini-game state (e.g., `main.current_game_state = STATE_MINI_GAME_TANGIER`).
7.  **Story Level Implementation**: For story levels, you'll need a simple mechanism to display the 10 frames sequentially. This could be a dedicated `draw_story_intro()` function in `main.py` that manages a `current_frame_index` and displays `assets/images/story_frames/story_intro_01.png`, then `story_intro_02.png`, etc., perhaps advancing on a mouse click or after a short delay.
8.  **Save/Load System (`data/save_game.json` and `utils/game_utils.py`)**: Create a simple JSON file. In `game_utils.py`, write functions to `load_game_progress()` and `save_game_progress()`. These functions will read from and write to `save_game.json`. The `save_game.json` could store a list of completed city IDs and the current unlocked city.
9.  **Asset Integration**: Place all your pixel art images (backgrounds, story frames, UI elements) into the `assets/images/` subfolders. Place music and sounds into `assets/music/` and `assets/sounds/` respectively. `pgzero` will automatically find them.
10. **Iterate and Expand**: Develop one mini-game at a time. Test thoroughly. Once one mini-game is working, copy its structure to create the next, adapting the logic as needed. This iterative approach makes development manageable.

This architecture provides a clear separation of concerns, making it easier for a beginner to understand how different parts of the game interact and to implement new features without breaking existing ones.
