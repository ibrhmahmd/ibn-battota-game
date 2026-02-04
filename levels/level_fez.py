from pgzero.actor import Actor
from pgzero.constants import keys
import random

WIDTH = 1280
HEIGHT = 720

# Settings
GRID_SIZE = 4
TILE_SIZE = 120
TILE_SPACING = 20

# UI
menu_button = Actor("ui/start_btn", pos=(80, 680))
mute_button = Actor("ui/music_on", pos=(1220, 40))

# Variables
tiles = []
flipped_tiles = []
matched_pairs = 0
total_pairs = 8
time_remaining = 90
game_won = False
flip_back_timer = 0

SYMBOLS = [
    "law", "astronomy", "medicine", "theology",
    "mathematics", "philosophy", "geography", "literature",
]

# Create Grid
symbol_pairs = SYMBOLS + SYMBOLS
random.shuffle(symbol_pairs)

# Start position to center the 4x4 grid
start_x = 370
start_y = 90

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        index = row * GRID_SIZE + col
        
        # Calculate position
        x = start_x + col * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2
        y = start_y + row * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2

        tile_actor = Actor("items/fez_symbols/tile_back")
        tile_actor.pos = (x, y)

        tile = {
            "actor": tile_actor,
            "symbol": symbol_pairs[index],
            "matched": False,
            "flipped": False,
        }
        tiles.append(tile)


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_fez", (0, 0))

    # Draw Tiles
    for tile in tiles:
        if tile["matched"] or tile["flipped"]:
            symbol = Actor(f"items/fez_symbols/symbol_{tile['symbol']}")
            symbol.pos = tile["actor"].pos
            symbol.draw()
        else:
            tile["actor"].draw()

    menu_button.draw()
    mute_button.draw()

    # Draw Stats
    screen.draw.text(f"Time: {int(time_remaining)}s", topleft=(20, 20), fontsize=40)
    screen.draw.text(f"Pairs: {matched_pairs}/8", topleft=(20, 70), fontsize=40)

    # Messages
    if game_won:
        screen.draw.text("COMPLETE!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="gold", owidth=2, ocolor="black")
        screen.draw.text("Press SPACE", center=(WIDTH/2, HEIGHT/2 + 60), fontsize=40)
    elif time_remaining <= 0:
        screen.draw.text("TIME UP!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="red", owidth=2, ocolor="black")
        screen.draw.text("Press SPACE", center=(WIDTH/2, HEIGHT/2 + 60), fontsize=40)


def update():
    global time_remaining, flip_back_timer, flipped_tiles

    if game_won or time_remaining <= 0:
        return

    time_remaining -= 1 / 60

    # Flip back timer
    if flip_back_timer > 0:
        flip_back_timer -= 1 / 60
        if flip_back_timer <= 0:
            for tile in flipped_tiles:
                tile["flipped"] = False
            flipped_tiles = []


def on_mouse_down(pos):
    global flipped_tiles, matched_pairs, game_won, flip_back_timer

    if menu_button.collidepoint(pos):
        return "map"

    if mute_button.collidepoint(pos):
        toggle_sound()

    if game_won or time_remaining <= 0:
        return "map"

    # Wait for mismatched cards to flip back
    if len(flipped_tiles) >= 2:
        return

    for tile in tiles:
        if tile["actor"].collidepoint(pos) and not tile["matched"] and not tile["flipped"]:
            tile["flipped"] = True
            flipped_tiles.append(tile)
            check_match()
            break


def check_match():
    global matched_pairs, game_won, flip_back_timer, flipped_tiles

    if len(flipped_tiles) == 2:
        if flipped_tiles[0]["symbol"] == flipped_tiles[1]["symbol"]:
            # Match
            flipped_tiles[0]["matched"] = True
            flipped_tiles[1]["matched"] = True
            flipped_tiles = []
            matched_pairs += 1
            if matched_pairs >= 8:
                game_won = True
        else:
            # No match
            flip_back_timer = 1.0


def on_key_down(key):
    if game_won or time_remaining <= 0:
        if key == keys.SPACE:
            return "map"


def toggle_sound():
    try:
        if mute_button.image == "ui/music_on":
            music.stop()
            mute_button.image = "ui/music_off"
        else:
            music.play("background_music")
            mute_button.image = "ui/music_on"
    except:
        pass
