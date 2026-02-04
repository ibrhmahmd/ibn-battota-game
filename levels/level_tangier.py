import game_states
from game_states import *
from pgzero.actor import Actor
from pgzero.constants import keys

WIDTH = 1280
HEIGHT = 720

GRAVITY = 0.5
JUMP_STRENGTH = -12
MOVE_SPEED = 6

player = None
platforms = []
items = []
items_collected = 0
total_items = 0
ground_y = 650
on_ground = False

menu_button = None
mute_button = None


def init():
    global \
        player, \
        platforms, \
        items, \
        items_collected, \
        total_items, \
        menu_button, \
        mute_button

    player = Actor("characters/character")
    player.pos = (150, 500)
    player.vx = 0
    player.vy = 0

    menu_button = Actor("ui/start_btn", pos=(80, 680))
    mute_button = Actor("ui/music_on", pos=(1220, 40))

    platforms = []

    def add_plat(x, y):
        platforms.append(Actor("items/platforms/platform_tangier", center=(x, y)))

    add_plat(300, 600)
    add_plat(600, 550)
    add_plat(900, 500)
    add_plat(450, 450)
    add_plat(750, 400)
    add_plat(1100, 450)
    add_plat(450, 265)
    add_plat(950, 220)

    def make_item(name, image, x, y):
        a = Actor(image)
        a.pos = (x, y)
        return {"actor": a, "collected": False, "name": name}

    items = [
        make_item("Silver Dirhams", "items/collectibles/silver_dirhams", 300, 560),
        make_item("Compass", "items/collectibles/compass", 600, 510),
        make_item("Water Skin", "items/collectibles/water_skin", 900, 460),
        make_item("Leather Sandals", "items/collectibles/leather_sandals", 450, 410),
        make_item("Prayer Mat", "items/collectibles/prayer_mat", 200, 630),
        make_item("Oil Lamp", "items/collectibles/oil_lamp", 500, 630),
        make_item("Woolen Djellaba", "items/collectibles/woolen_djellaba", 800, 630),
        make_item("Holy Quran", "items/collectibles/holy_quran", 750, 360),
        make_item("Inkwell & Kalam", "items/collectibles/inkwell_and_kalam", 1100, 410),
        make_item("Travel Documents", "items/collectibles/travel_documents", 1050, 630),
    ]

    items_collected = 0
    total_items = len(items)


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_tangier", (0, 0))

    for p in platforms:
        p.draw()

    for item in items:
        if not item["collected"]:
            item["actor"].draw()

    player.draw()

    menu_button.draw()
    mute_button.draw()

    screen.draw.text(
        f"Items: {items_collected}/{total_items}",
        topleft=(20, 20),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )

    collected_x = WIDTH - 60
    for item in items:
        if item["collected"]:
            small_actor = Actor(item["actor"].image)
            small_actor.pos = (collected_x, 80)
            small_actor.draw()
            collected_x -= 50

    if items_collected >= total_items:
        screen.draw.text(
            "READY FOR PILGRIMAGE!",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="gold",
            owidth=2,
            ocolor="black",
        )
        screen.draw.text(
            "Press SPACE to Depart",
            center=(WIDTH / 2, HEIGHT / 2 + 60),
            fontsize=40,
            color="white",
            owidth=1.5,
            ocolor="black",
        )


def handle_movement(keyboard):
    player.vx = 0
    if keyboard.left:
        player.vx = -MOVE_SPEED
    if keyboard.right:
        player.vx = MOVE_SPEED

    player.x += player.vx

    for p in platforms:
        if player.colliderect(p):
            if player.vx > 0:
                player.right = p.left
            elif player.vx < 0:
                player.left = p.right

    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH


def handle_collisions():
    global on_ground

    player.vy += GRAVITY
    player.y += player.vy

    on_ground = False

    if player.bottom >= ground_y:
        player.bottom = ground_y
        player.vy = 0
        on_ground = True

    for p in platforms:
        if player.colliderect(p):
            if player.vy > 0:
                player.bottom = p.top
                player.vy = 0
                on_ground = True
            elif player.vy < 0:
                player.top = p.bottom
                player.vy = 0

    if player.top > HEIGHT:
        player.pos = (150, 500)
        player.vy = 0


def handle_items():
    global items_collected

    for item in items:
        if not item["collected"] and player.colliderect(item["actor"]):
            item["collected"] = True
            items_collected += 1


def update(keyboard):
    if items_collected >= total_items:
        return

    handle_movement(keyboard)
    handle_collisions()
    handle_items()


def on_mouse_down(pos):
    if menu_button.collidepoint(pos):
        return STATE_WORLD_MAP

    if mute_button.collidepoint(pos):
        toggle_sound()

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
    global items_collected

    if items_collected >= total_items:
        if key == keys.SPACE:
            return STATE_WORLD_MAP
    else:
        if (key == keys.SPACE or key == keys.UP) and on_ground:
            player.vy = JUMP_STRENGTH

    return None
