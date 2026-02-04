import pgzrun
import pygame

# === SCREEN SETTINGS ===
WIDTH = 1280
HEIGHT = 720

# === GAME STATE ===
# This variable keeps track of which screen to show
# Options: "start", "map", "tangier", "fez"
current_screen = "start"

# === IMPORT OTHER FILES ===
import start_screen
import world_map
import levels.level_tangier as level_tangier
import levels.level_fez as level_fez


# === DRAW LOOP ===
# This function runs every frame to draw images on the screen
def draw():
    screen.clear()

    # Check which screen is active and draw it
    if current_screen == "start":
        start_screen.draw(screen)

    elif current_screen == "map":
        world_map.draw(screen)

    elif current_screen == "tangier":
        level_tangier.draw(screen)

    elif current_screen == "fez":
        level_fez.draw(screen)


# === UPDATE LOOP ===
# This function runs every frame to update game logic
def update():
    if current_screen == "map":
        world_map.update(keyboard)

    elif current_screen == "tangier":
        level_tangier.update(keyboard)

    elif current_screen == "fez":
        level_fez.update()


# === INPUT HANDLERS ===
def on_mouse_down(pos):
    global current_screen

    # Store the new screen name (or None if no change)
    new_screen = None

    if current_screen == "start":
        new_screen = start_screen.on_mouse_down(pos)

    elif current_screen == "map":
        new_screen = world_map.on_mouse_down(pos)

    elif current_screen == "tangier":
        new_screen = level_tangier.on_mouse_down(pos)

    elif current_screen == "fez":
        new_screen = level_fez.on_mouse_down(pos)

    # If a new screen was requested, switch to it
    if new_screen:
        current_screen = new_screen


def on_key_down(key):
    global current_screen

    # Check for key presses in the current level
    new_screen = None

    if current_screen == "tangier":
        new_screen = level_tangier.on_key_down(key)
    elif current_screen == "fez":
        new_screen = level_fez.on_key_down(key)

    # Convert numeric keypad presses to number keys for level testing shortcuts (optional)
    # No shortcuts implemented for simplification

    if new_screen:
        current_screen = new_screen


# === START MUSIC ===
try:
    music.play("background_music")
except:
    pass

# === START GAME ===
pgzrun.go()
