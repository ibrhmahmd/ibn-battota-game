import game_states
from game_states import *
from pgzero.actor import Actor
from pgzero.constants import keys
import random

WIDTH = 1280
HEIGHT = 720

GRID_SIZE = 4
TILE_SIZE = 120
TILE_SPACING = 20

tiles = []
flipped_tiles = []
matched_pairs = 0
total_pairs = 8
time_remaining = 90
game_won = False
flip_back_timer = 0

menu_button = None
mute_button = None

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


def init():
    global \
        tiles, \
        flipped_tiles, \
        matched_pairs, \
        time_remaining, \
        game_won, \
        menu_button, \
        mute_button, \
        flip_back_timer

    menu_button = Actor("ui/start_btn", pos=(80, 680))
    mute_button = Actor("ui/music_on", pos=(1220, 40))

    tiles = []
    flipped_tiles = []
    matched_pairs = 0
    time_remaining = 90
    game_won = False
    flip_back_timer = 0

    symbol_pairs = SYMBOLS + SYMBOLS
    random.shuffle(symbol_pairs)

    grid_start_x = (
        WIDTH - (GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * TILE_SPACING)
    ) // 2
    grid_start_y = (
        HEIGHT - (GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * TILE_SPACING)
    ) // 2

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            index = row * GRID_SIZE + col
            x = grid_start_x + col * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2
            y = grid_start_y + row * (TILE_SIZE + TILE_SPACING) + TILE_SIZE // 2

            tile_actor = Actor("items/fez_symbols/tile_back")
            tile_actor.pos = (x, y)

            tile = {
                "actor": tile_actor,
                "symbol": symbol_pairs[index],
                "matched": False,
                "flipped": False,
                "row": row,
                "col": col,
            }
            tiles.append(tile)


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_fez", (0, 0))

    for tile in tiles:
        if tile["matched"] or tile["flipped"]:
            symbol_actor = Actor(f"items/fez_symbols/symbol_{tile['symbol']}")
            symbol_actor.pos = tile["actor"].pos
            symbol_actor.draw()
        else:
            tile["actor"].draw()

    menu_button.draw()
    mute_button.draw()

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
            "Press SPACE to Retry",
            center=(WIDTH // 2, HEIGHT // 2 + 60),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )


def update():
    global time_remaining, flip_back_timer, flipped_tiles

    if game_won or time_remaining <= 0:
        return

    time_remaining -= 1 / 60
    if time_remaining < 0:
        time_remaining = 0

    if flip_back_timer > 0:
        flip_back_timer -= 1 / 60
        if flip_back_timer <= 0:
            for tile in flipped_tiles:
                tile["flipped"] = False
            flipped_tiles = []


def on_mouse_down(pos):
    global flipped_tiles, matched_pairs, game_won, flip_back_timer

    if menu_button.collidepoint(pos):
        return STATE_WORLD_MAP

    if mute_button.collidepoint(pos):
        toggle_sound()
        return None

    if game_won:
        return STATE_WORLD_MAP

    if time_remaining <= 0:
        init()
        return None

    if len(flipped_tiles) >= 2 or flip_back_timer > 0:
        return None

    for tile in tiles:
        if (
            tile["actor"].collidepoint(pos)
            and not tile["matched"]
            and not tile["flipped"]
        ):
            flip_tile(tile)
            check_match()
            break

    return None


def flip_tile(tile):
    tile["flipped"] = True
    flipped_tiles.append(tile)


def check_match():
    global matched_pairs, game_won, flip_back_timer, flipped_tiles

    if len(flipped_tiles) == 2:
        if flipped_tiles[0]["symbol"] == flipped_tiles[1]["symbol"]:
            # Match!
            flipped_tiles[0]["matched"] = True
            flipped_tiles[1]["matched"] = True
            flipped_tiles = []
            matched_pairs += 1
            if matched_pairs >= total_pairs:
                game_won = True
        else:
            # No match
            flip_back_timer = 1.0

    return None


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


def on_key_down(key):
    if game_won or time_remaining <= 0:
        if key == keys.SPACE:
            if game_won:
                return STATE_WORLD_MAP
            else:
                init()
    return None
