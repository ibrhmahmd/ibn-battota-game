from pgzero.actor import Actor
from pgzero.constants import keys
import mission_overlay

WIDTH = 1280
HEIGHT = 720

TOTAL_ITEMS = 8
GRAVITY = 0.5
JUMP_STRENGTH = -12
MOVE_SPEED = 6

back_button = Actor("ui/back_btn", pos=(80, 50))
victory_seal = Actor("items/level_passed_seal", center=(WIDTH // 2, HEIGHT // 2))

player = Actor("characters/character")

STATIC_PLATFORM_DATA = [
    (150, 650), (700, 550), (1180, 600), (300, 350), (1050, 250),
]
MOVING_PLATFORM_DATA = [
    (400, 550), (950, 450), (750, 150),
]

ITEM_DATA = [
    ("items/cairo/nile_water_glass", (300, 310)),
    ("items/cairo/medicine_bottle", (1050, 210)),
    ("items/collectibles/silver_dirhams", (700, 510)),
    ("items/collectibles/holy_quran", (1180, 560)),
    ("items/collectibles/oil_lamp", (450, 510)),
    ("items/collectibles/inkwell_and_kalam", (950, 410)),
    ("items/cairo/osterlab", (750, 110)),
    ("items/cairo/suger_cane", (150, 610)),
]

platforms = []
moving_platforms = []
items = []
found = 0
win = False
timer = 0
on_ground = False
show_mission = True


def reset():
    global platforms, moving_platforms, items, found, win, timer, on_ground, show_mission
    player.pos = (150, 500)
    player.speed_y = 0
    platforms = [Actor("items/platforms/platform", pos=pos) for pos in STATIC_PLATFORM_DATA]
    moving_platforms = [Actor("items/platforms/platform", pos=pos) for pos in MOVING_PLATFORM_DATA]
    items = [Actor(img, pos=pos) for img, pos in ITEM_DATA]
    found = 0
    win = False
    timer = 0
    on_ground = False
    show_mission = True


reset()


def draw(screen):
    screen.blit("backgrounds/bg_cairo", (0, 0))

    for p in platforms:
        p.draw()

    if timer < 50:
        moving_platforms[0].draw()
    elif timer < 100:
        moving_platforms[1].draw()
    elif timer < 150:
        moving_platforms[2].draw()

    for item in items:
        item.draw()

    player.draw()
    back_button.draw()

    screen.draw.text(
        f"Items Found: {found}/{TOTAL_ITEMS}",
        topleft=(20, 100),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )
    if win:
        victory_seal.draw()
        screen.draw.text(
            "Press SPACE",
            center=(640, 450),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )

    if show_mission:
        mission_overlay.draw(screen, "cairo")


def update(keyboard):
    global timer, found, win, on_ground, show_mission

    if show_mission:
        return

    if win:
        return

    timer = timer + 1
    if timer > 150:
        timer = 0

    if keyboard.left:
        player.x = player.x - MOVE_SPEED
    if keyboard.right:
        player.x = player.x + MOVE_SPEED

    player.speed_y += GRAVITY
    player.y += player.speed_y

    on_ground = False

    for p in platforms:
        if player.colliderect(p):
            if player.speed_y > 0:
                player.bottom = p.top
                player.speed_y = 0
                on_ground = True

    active_mover = None
    if timer < 50:
        active_mover = moving_platforms[0]
    elif timer < 100:
        active_mover = moving_platforms[1]
    elif timer < 150:
        active_mover = moving_platforms[2]

    if active_mover and player.colliderect(active_mover):
        if player.speed_y > 0:
            player.bottom = active_mover.top
            player.speed_y = 0
            on_ground = True

    if player.y > HEIGHT:
        player.pos = (150, 500)

    for item in items[:]:
        if player.colliderect(item):
            items.remove(item)
            found += 1

    if found >= TOTAL_ITEMS:
        win = True


def on_mouse_down(pos):
    if back_button.collidepoint(pos):
        return "map"
    return None


def on_key_down(key):
    global show_mission

    if show_mission:
        if key == keys.SPACE:
            show_mission = False
        return

    if win and key == keys.SPACE:
        return "map"

    if (key == keys.SPACE or key == keys.UP) and on_ground:
        player.speed_y = JUMP_STRENGTH
