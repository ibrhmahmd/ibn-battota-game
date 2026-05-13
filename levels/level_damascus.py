from pgzero.actor import Actor
from pgzero.constants import keys
import random
import mission_overlay

WIDTH = 1280
HEIGHT = 720

player = Actor("characters/character")
player.pos = (WIDTH // 2, 650)
MOVE_SPEED = 10

score = 0
win = False
show_mission = True
victory_seal = Actor("items/level_passed_seal", center=(WIDTH // 2, HEIGHT // 2))
back_button = Actor("ui/back_btn", pos=(80, 50))


items = []
spawn_timer = 0

ITEM_TYPES = [
    {"image": "items/collectibles/holy_quran", "points": 1, "type": "good"},
    {"image": "items/collectibles/oil_lamp", "points": 2, "type": "good"},
    {"image": "items/collectibles/silver_dirhams", "points": 5, "type": "good"},
    {"image": "items/damascus/scorpion", "points": -10, "type": "bad"},
    {"image": "items/damascus/rock", "points": -5, "type": "bad"},
]


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_damascus", (0, 0))

    back_button.draw()
    player.draw()

    for item in items:
        item.draw()

    screen.draw.text(
        f"SCORE: {score}/50",
        topleft=(20, 100),
        fontsize=50,
        color="white",
        owidth=1.5,
        ocolor="black",
    )

    if win:
        victory_seal.draw()
        screen.draw.text(
            "Press SPACE to return",
            center=(WIDTH // 2, HEIGHT // 2 + 100),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )

    if show_mission:
        mission_overlay.draw(screen, "damascus")


def update(keyboard):
    global score, spawn_timer, win, show_mission

    if show_mission or win:
        return

    if keyboard.left and player.left > 0:
        player.x -= MOVE_SPEED
    if keyboard.right and player.right < WIDTH:
        player.x += MOVE_SPEED

    spawn_timer += 1
    if spawn_timer > 7:
        spawn_timer = 0
        props = random.choice(ITEM_TYPES)
        new_item = Actor(props["image"])
        new_item.x = random.randint(50, WIDTH - 50)
        new_item.y = -50
        new_item.points = props["points"]
        items.append(new_item)

    for item in items[:]:
        item.y += 5

        if player.colliderect(item):
            score += item.points
            if score < 0:
                score = 0
            items.remove(item)
            if score >= 50:
                win = True
        elif item.top > HEIGHT:
            items.remove(item)


def on_key_down(key):
    global show_mission

    if show_mission:
        if key == keys.SPACE:
            show_mission = False
        return

    if win and key == keys.SPACE:
        return "map"


def on_mouse_down(pos):
    if back_button.collidepoint(pos):
        return "map"
    return None
