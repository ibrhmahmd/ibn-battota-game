from pgzero.actor import Actor
from pgzero.builtins import music
from pgzero.constants import keys
import random
import mission_overlay

WIDTH = 1280
HEIGHT = 720

GRAVITY = 0.5
JUMP_STRENGTH = -12
MOVE_SPEED = 6
TOTAL_ITEMS = 10

back_button = Actor("ui/back_btn", pos=(80, 50))
victory_seal = Actor("items/level_passed_seal", center=(WIDTH // 2, HEIGHT // 2))

platforms = [
    Actor("items/platforms/platform", center=(300, 600)),
    Actor("items/platforms/platform", center=(600, 550)),
    Actor("items/platforms/platform", center=(900, 500)),
    Actor("items/platforms/platform", center=(450, 450)),
    Actor("items/platforms/platform", center=(750, 400)),
    Actor("items/platforms/platform", center=(1100, 370)),
    Actor("items/platforms/platform", center=(450, 265)),
    Actor("items/platforms/platform", center=(950, 220)),
    Actor("items/platforms/platform", center=(1020, 630)),
    Actor("items/platforms/platform", center=(1220, 630)),
]

ITEM_DATA = [
    ("items/collectibles/prayer_mat", (200, 630)),
    ("items/collectibles/leather_sandals", (450, 410)),
    ("items/collectibles/compass", (600, 510)),
    ("items/collectibles/holy_quran", (750, 360)),
    ("items/collectibles/woolen_djellaba", (800, 630)),
    ("items/collectibles/water_skin", (900, 460)),
    ("items/collectibles/silver_dirhams", (300, 560)),
    ("items/collectibles/oil_lamp", (500, 630)),
    ("items/collectibles/travel_documents", (1080, 550)),
    ("items/collectibles/inkwell_and_kalam", (1100, 330)),
]

player = Actor("characters/character")
ground_y = 650
items = []
items_collected = 0
on_ground = False
show_mission = True
leaf_particles = []


def reset():
    global items, items_collected, on_ground, show_mission, leaf_particles
    player.pos = (150, 500)
    player.speed_y = 0
    items = [{"actor": Actor(img, pos=pos)} for img, pos in ITEM_DATA]
    items_collected = 0
    on_ground = False
    show_mission = True
    leaf_particles = []


reset()


def draw(screen):
    screen.blit("backgrounds/bg_tangier", (0, 0))

    for p in platforms:
        p.draw()

    for item in items:
        item["actor"].draw()

    player.draw()

    back_button.draw()

    screen.draw.text(
        f"Items: {items_collected}/{TOTAL_ITEMS}",
        topleft=(20, 100),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )

    if items_collected >= TOTAL_ITEMS:
        victory_seal.draw()
        screen.draw.text(
            "Press SPACE to Continue",
            center=(WIDTH / 2, HEIGHT / 2 + 60),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )
    else:
        for leaf in leaf_particles:
            leaf["actor"].draw()

    if show_mission:
        mission_overlay.draw(screen, "tangier")


def update(keyboard):
    global items_collected, on_ground, leaf_particles, show_mission

    if show_mission:
        return

    if items_collected >= TOTAL_ITEMS:
        return

    if random.random() < 0.02:
        l = Actor("items/leaf")
        l.pos = (random.randint(0, WIDTH), -20)
        leaf_particles.append(
            {
                "actor": l,
                "speed_x": random.uniform(-1, 1),
                "speed_y": random.uniform(1, 3),
            }
        )

    for leaf in leaf_particles:
        leaf["actor"].x += leaf["speed_x"]
        leaf["actor"].y += leaf["speed_y"]
        leaf["actor"].angle += 1

    leaf_particles[:] = [l for l in leaf_particles if l["actor"].y < HEIGHT + 20]

    if keyboard.left:
        player.x -= MOVE_SPEED
        for platform in platforms:
            if player.colliderect(platform):
                player.left = platform.right

    if keyboard.right:
        player.x += MOVE_SPEED
        for platform in platforms:
            if player.colliderect(platform):
                player.right = platform.left

    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    player.speed_y += GRAVITY
    player.y += player.speed_y

    on_ground = False

    if player.bottom >= ground_y:
        player.bottom = ground_y
        player.speed_y = 0
        on_ground = True
    for p in platforms:
        if player.colliderect(p):
            if player.speed_y > 0:
                player.bottom = p.top
                player.speed_y = 0
                on_ground = True
            elif player.speed_y < 0:
                player.top = p.bottom
                player.speed_y = 0

    if player.top > HEIGHT:
        player.pos = (150, 500)
        player.speed_y = 0
    for item in items[:]:
        if player.colliderect(item["actor"]):
            items.remove(item)
            items_collected += 1
            break


def on_mouse_down(pos):
    if back_button.collidepoint(pos):
        return "map"

    return None


def on_key_down(key):
    global items_collected, show_mission

    if show_mission:
        if key == keys.SPACE:
            show_mission = False
        return

    if items_collected >= TOTAL_ITEMS:
        if key == keys.SPACE:
            return "map"
    else:
        if (key == keys.SPACE or key == keys.UP) and on_ground:
            player.speed_y = JUMP_STRENGTH
    return None
