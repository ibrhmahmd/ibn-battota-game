from pgzero.actor import Actor
from pgzero.builtins import music, clock
from pgzero.constants import keys
import random
import mission_overlay

WIDTH = 1280
HEIGHT = 720

back_button = Actor("ui/back_btn", pos=(80, 50))

tiles = []
flipped_tiles = []
matched_pairs = 0
time_remaining = 90
game_won = False
show_mission = True
victory_seal = Actor("items/level_passed_seal", center=(WIDTH // 2, HEIGHT // 2))

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
pool = SYMBOLS + SYMBOLS
random.shuffle(pool)

# Row 0
t = Actor("items/fez_symbols/tile_back", pos=(440, 160))
t.secret = f"items/fez_symbols/symbol_{pool[0]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(580, 160))
t.secret = f"items/fez_symbols/symbol_{pool[1]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(720, 160))
t.secret = f"items/fez_symbols/symbol_{pool[2]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(860, 160))
t.secret = f"items/fez_symbols/symbol_{pool[3]}"
t.is_matched = False
tiles.append(t)

# Row 1
t = Actor("items/fez_symbols/tile_back", pos=(440, 300))
t.secret = f"items/fez_symbols/symbol_{pool[4]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(580, 300))
t.secret = f"items/fez_symbols/symbol_{pool[5]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(720, 300))
t.secret = f"items/fez_symbols/symbol_{pool[6]}"
t.is_matched = False
tiles.append(t)
t = Actor("items/fez_symbols/tile_back", pos=(860, 300))
t.secret = f"items/fez_symbols/symbol_{pool[7]}"
t.is_matched = False
tiles.append(t)

# Row 2
t = Actor("items/fez_symbols/tile_back", pos=(440, 440))
t.secret = f"items/fez_symbols/symbol_{pool[8]}"
t.is_matched = False
tiles.append(t)
t = Actor("items/fez_symbols/tile_back", pos=(580, 440))
t.secret = f"items/fez_symbols/symbol_{pool[9]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(720, 440))
t.secret = f"items/fez_symbols/symbol_{pool[10]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(860, 440))
t.secret = f"items/fez_symbols/symbol_{pool[11]}"
t.is_matched = False
tiles.append(t)

# Row 3
t = Actor("items/fez_symbols/tile_back", pos=(440, 580))
t.secret = f"items/fez_symbols/symbol_{pool[12]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(580, 580))
t.secret = f"items/fez_symbols/symbol_{pool[13]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(720, 580))
t.secret = f"items/fez_symbols/symbol_{pool[14]}"
t.is_matched = False
tiles.append(t)

t = Actor("items/fez_symbols/tile_back", pos=(860, 580))
t.secret = f"items/fez_symbols/symbol_{pool[15]}"
t.is_matched = False
tiles.append(t)


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_fez", (0, 0))

    for t in tiles:
        t.draw()

    back_button.draw()

    screen.draw.text(f"Time: {int(time_remaining)}s", topleft=(20, 100), fontsize=40)
    screen.draw.text(f"Pairs: {matched_pairs}/8", topleft=(20, 150), fontsize=40)

    if game_won:
        victory_seal.draw()
        screen.draw.text("Press SPACE", center=(640, 450), fontsize=50)
    elif time_remaining <= 0:
        screen.draw.text(
            "GAME OVER!",
            center=(640, 360),
            fontsize=100,
            color="red",
            owidth=2,
            ocolor="black",
        )
        screen.draw.text("Press SPACE", center=(640, 450), fontsize=50)

    if show_mission:
        mission_overlay.draw(screen, "fez")


def update():
    global time_remaining, show_mission

    if show_mission:
        return

    if not game_won and time_remaining > 0:
        time_remaining -= 1 / 60


def on_mouse_down(pos):
    global matched_pairs, game_won

    if back_button.collidepoint(pos):
        return "map"

    if game_won or time_remaining <= 0:
        return "map"

    if len(flipped_tiles) >= 2:
        return

    for t in tiles:
        if (
            t.collidepoint(pos)
            and not t.is_matched
            and t.image == "items/fez_symbols/tile_back"
        ):
            t.image = t.secret
            flipped_tiles.append(t)

            if len(flipped_tiles) == 2:
                if flipped_tiles[0].secret == flipped_tiles[1].secret:
                    flipped_tiles[0].is_matched = True
                    flipped_tiles[1].is_matched = True
                    flipped_tiles.clear()
                    matched_pairs += 1
                    if matched_pairs == 8:
                        game_won = True
                else:
                    clock.schedule(flip_back, 1.0)
            break


def flip_back():
    for t in flipped_tiles:
        t.image = "items/fez_symbols/tile_back"
    flipped_tiles.clear()


def on_key_down(key):
    global show_mission

    if show_mission:
        if key == keys.SPACE:
            show_mission = False
        return

    if (game_won or time_remaining <= 0) and key == keys.SPACE:
        return "map"
    flipped_tiles.clear()
