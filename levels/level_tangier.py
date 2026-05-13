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

player = Actor("characters/character")
player.pos = (150, 500)
player.speed_y = 0

back_button = Actor("ui/back_btn", pos=(80, 50))

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

items = [
    {"actor": Actor("items/collectibles/prayer_mat", pos=(200, 630))},
    {"actor": Actor("items/collectibles/leather_sandals", pos=(450, 410))},
    {"actor": Actor("items/collectibles/compass", pos=(600, 510))},
    {"actor": Actor("items/collectibles/holy_quran", pos=(750, 360))},
    {"actor": Actor("items/collectibles/woolen_djellaba", pos=(800, 630))},
    {"actor": Actor("items/collectibles/water_skin", pos=(900, 460))},
    {"actor": Actor("items/collectibles/silver_dirhams", pos=(300, 560))},
    {"actor": Actor("items/collectibles/oil_lamp", pos=(500, 630))},
    {"actor": Actor("items/collectibles/travel_documents", pos=(1080, 550))},
    {"actor": Actor("items/collectibles/inkwell_and_kalam", pos=(1100, 330))},
]

items_collected = 0
ground_y = 650
on_ground = False
show_mission = True

# Visual Effects
leaf_particles = []
victory_seal = Actor("items/level_passed_seal", center=(WIDTH // 2, HEIGHT // 2))


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_tangier", (0, 0))

    for p in platforms:
        p.draw()

    for item in items:
        item["actor"].draw()

    player.draw()

    back_button.draw()

    screen.draw.text(
        f"Items: {items_collected}/10",
        topleft=(20, 100),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )

    if items_collected >= 10:
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

    if items_collected >= 10:
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
    for item in items:
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

    if items_collected >= 10:
        if key == keys.SPACE:
            return "map"
    else:
        if (key == keys.SPACE or key == keys.UP) and on_ground:
            player.speed_y = JUMP_STRENGTH
    return None
