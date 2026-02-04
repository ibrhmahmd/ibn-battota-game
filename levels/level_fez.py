from pgzero.actor import Actor
from pgzero.constants import keys
import random

# === SETTINGS ===
WIDTH = 1280
HEIGHT = 720

# Grid Configuration
GRID_SIZE = 4  # 4x4 grid = 16 tiles
TILE_SIZE = 120  # Size of each tile in pixels
TILE_SPACING = 20  # Space between tiles

# === UI ELEMENTS ===
menu_button = Actor("ui/start_btn", pos=(80, 680))
mute_button = Actor("ui/music_on", pos=(1220, 40))

# === GAME VARIABLES ===
tiles = []  # List to hold all tile objects
flipped_tiles = []  # List of currently flipped tiles (max 2)
matched_pairs = 0  # Count of pairs found
total_pairs = 8  # Total pairs to find (16 tiles / 2)
time_remaining = 90  # Seconds to solve the puzzle
game_won = False
flip_back_timer = 0  # Timer to delay flipping back incorrect matches

# Symbols to match (Scientific subjects)
SYMBOLS = [
    "law",
    "astronomy",
    "medicine",
    "theology",
    "mathematics",
    "philosophy",
    "geography",
    "literature",
]


# === GRID SETUP ===
# Create pairs: [A, B, C] -> [A, B, C, A, B, C]
symbol_pairs = SYMBOLS + SYMBOLS
# Shuffle them randomly
random.shuffle(symbol_pairs)

# Calculate where to start drawing so grid is centered
grid_width = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * TILE_SPACING
grid_height = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * TILE_SPACING
grid_start_x = (WIDTH - grid_width) // 2
grid_start_y = (HEIGHT - grid_height) // 2

# Create the tiles
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        # Calculate list index (0 to 15)
        index = row * GRID_SIZE + col

        # Calculate position on screen
        x = grid_start_x + col * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2
        y = grid_start_y + row * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2

        # Create the tile actor (initially showing back)
        tile_actor = Actor("items/fez_symbols/tile_back")
        tile_actor.pos = (x, y)

        # Create tile data dictionary
        tile = {
            "actor": tile_actor,
            "symbol": symbol_pairs[index],  # Hidden symbol
            "matched": False,
            "flipped": False,
            "row": row,
            "col": col,
        }
        tiles.append(tile)


# === DRAWING ===
def draw(screen):
    """Draws bg, tiles, and UI."""
    screen.clear()
    screen.blit("backgrounds/bg_fez", (0, 0))

    # Draw Tiles
    for tile in tiles:
        # If matched or flipped, show the symbol
        if tile["matched"] or tile["flipped"]:
            symbol_actor = Actor(f"items/fez_symbols/symbol_{tile['symbol']}")
            symbol_actor.pos = tile["actor"].pos
            symbol_actor.draw()
        else:
            # Otherwise show the card back
            tile["actor"].draw()

    # Draw UI
    menu_button.draw()
    mute_button.draw()

    # Draw Stats
    screen.draw.text(
        f"Time: {int(time_remaining)}s",
        topleft=(20, 20),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )
    screen.draw.text(
        f"Pairs: {matched_pairs}/{total_pairs}",
        topleft=(20, 70),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )

    # Victory Message
    if game_won:
        screen.draw.text(
            "SCHOLAR'S PATH COMPLETE!",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="gold",
            owidth=2,
            ocolor="black",
        )
        screen.draw.text(
            "Press SPACE to Continue",
            center=(WIDTH // 2, HEIGHT // 2 + 60),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )
    # Failure Message
    elif time_remaining <= 0:
        screen.draw.text(
            "TIME'S UP!",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="red",
            owidth=2,
            ocolor="black",
        )
        screen.draw.text(
            "Press SPACE to Return",
            center=(WIDTH // 2, HEIGHT // 2 + 60),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )


# === UPDATE LOOP ===
def update():
    """Updates timers."""
    global time_remaining, flip_back_timer, flipped_tiles

    # Stop if game over
    if game_won or time_remaining <= 0:
        return

    # Count down timer
    time_remaining -= 1 / 60
    if time_remaining < 0:
        time_remaining = 0

    # Delay before flipping back mismatched cards
    if flip_back_timer > 0:
        flip_back_timer -= 1 / 60
        if flip_back_timer <= 0:
            # Time's up, flip them back
            for tile in flipped_tiles:
                tile["flipped"] = False
            flipped_tiles = []


# === INPUT HANDLING ===
def on_mouse_down(pos):
    """Handles logic for clicking tiles."""
    global flipped_tiles, matched_pairs, game_won, flip_back_timer

    # Menu Button
    if menu_button.collidepoint(pos):
        return "map"

    # Music Toggle
    if mute_button.collidepoint(pos):
        toggle_sound()
        return None

    # If game over, any click returns to map
    if game_won or time_remaining <= 0:
        return "map"

    # Don't allow clicking if already 2 tiles flipped (waiting for timer)
    if len(flipped_tiles) >= 2 or flip_back_timer > 0:
        return None

    # Check which tile was clicked
    for tile in tiles:
        if (
            tile["actor"].collidepoint(pos)
            and not tile["matched"]
            and not tile["flipped"]
        ):
            # Valid click!
            flip_tile(tile)
            check_match()
            break  # Only one click per frame

    return None


def flip_tile(tile):
    """Refeals a tile."""
    tile["flipped"] = True
    flipped_tiles.append(tile)


def check_match():
    """Checks if the two flipped tiles match."""
    global matched_pairs, game_won, flip_back_timer, flipped_tiles

    if len(flipped_tiles) == 2:
        # Compare symbols
        if flipped_tiles[0]["symbol"] == flipped_tiles[1]["symbol"]:
            # MATCH! Keep them flipped
            flipped_tiles[0]["matched"] = True
            flipped_tiles[1]["matched"] = True
            flipped_tiles = []  # Clear list so player can pick next pair
            matched_pairs += 1

            # Check Win Condition
            if matched_pairs >= total_pairs:
                game_won = True
        else:
            # NO MATCH. Set timer to flip them back after 1 second
            flip_back_timer = 1.0

    return None


def on_key_down(key):
    """Press SPACE to exit after game over."""
    if game_won or time_remaining <= 0:
        if key == keys.SPACE:
            return "map"
    return None


# === HELPERS ===
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
