from pgzero.actor import Actor
from pgzero.constants import keys

# === SETTINGS ===
WIDTH = 1280
HEIGHT = 720

# Physics constants
GRAVITY = 0.5  # How fast the player falls
JUMP_STRENGTH = -12  # Initial upward speed when jumping
MOVE_SPEED = 6  # Horizontal movement speed

# === PLAYER ===
player = Actor("characters/character")
player.pos = (150, 500)
# We track vertical speed for gravity calculations
player.speed_y = 0

# === UI ELEMENTS ===
menu_button = Actor("ui/start_btn", pos=(80, 680))
mute_button = Actor("ui/music_on", pos=(1220, 40))

# === PLATFORMS ===
# Create a list of platform actors hardcoded to specific positions
platforms = [
    Actor("items/platforms/platform_tangier", center=(300, 600)),
    Actor("items/platforms/platform_tangier", center=(600, 550)),
    Actor("items/platforms/platform_tangier", center=(900, 500)),
    Actor("items/platforms/platform_tangier", center=(450, 450)),
    Actor("items/platforms/platform_tangier", center=(750, 400)),
    Actor("items/platforms/platform_tangier", center=(1100, 450)),
    Actor("items/platforms/platform_tangier", center=(450, 265)),
    Actor("items/platforms/platform_tangier", center=(950, 220)),
]

# === ITEMS TO COLLECT ===
# List of dictionaries containing the actor and its name
items = [
    {"actor": Actor("items/collectibles/silver_dirhams", pos=(300, 560))},
    {"actor": Actor("items/collectibles/compass", pos=(600, 510))},
    {"actor": Actor("items/collectibles/water_skin", pos=(900, 460))},
    {"actor": Actor("items/collectibles/leather_sandals", pos=(450, 410))},
    {"actor": Actor("items/collectibles/prayer_mat", pos=(200, 630))},
    {"actor": Actor("items/collectibles/oil_lamp", pos=(500, 630))},
    {"actor": Actor("items/collectibles/woolen_djellaba", pos=(800, 630))},
    {"actor": Actor("items/collectibles/holy_quran", pos=(750, 360))},
    {"actor": Actor("items/collectibles/inkwell_and_kalam", pos=(1100, 410))},
    {"actor": Actor("items/collectibles/travel_documents", pos=(1050, 630))},
]

# === GAME VARIABLES ===
items_collected = 0
ground_y = 650
on_ground = False


# === DRAWING ===
def draw(screen):
    """Draws the game world, platforms, items, and UI."""
    screen.clear()
    screen.blit("backgrounds/bg_tangier", (0, 0))

    # Draw all platforms
    for p in platforms:
        p.draw()

    # Draw items (only those still in the list are drawn)
    for item in items:
        item["actor"].draw()

    # Draw player
    player.draw()

    # Draw UI buttons
    menu_button.draw()
    mute_button.draw()

    # Draw score text
    screen.draw.text(
        f"Items: {items_collected}/10",
        topleft=(20, 20),
        fontsize=40,
        color="white",
        owidth=1.5,
        ocolor="black",
    )

    # If all items are collected, show victory message
    if items_collected >= 10:
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


# === GAME UPDATE LOOP ===
def update(keyboard):
    """Handles movement, physics, collisions, and item collection."""
    global items_collected, on_ground

    # If game is won, stop updating physics
    if items_collected >= 10:
        return

    # --- 1. HORIZONTAL MOVEMENT ---

    # Check Left Arrow
    if keyboard.left:
        player.x -= MOVE_SPEED
        # Check if we hit a platform from the right
        for p in platforms:
            if player.colliderect(p):
                player.left = p.right

    # Check Right Arrow
    if keyboard.right:
        player.x += MOVE_SPEED
        # Check if we hit a platform from the left
        for p in platforms:
            if player.colliderect(p):
                player.right = p.left

    # Screen Boundaries (keep player inside screen)
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    # --- 2. VERTICAL MOVEMENT (GRAVITY) ---

    # Apply gravity to pull player down
    player.speed_y += GRAVITY
    player.y += player.speed_y

    on_ground = False  # Assume in air until we hit something

    # Check Ground Collision
    if player.bottom >= ground_y:
        player.bottom = ground_y
        player.speed_y = 0
        on_ground = True

    # Check Platform Collision (falling onto them or hitting head)
    for p in platforms:
        if player.colliderect(p):
            if player.speed_y > 0:  # Falling down onto platform
                player.bottom = p.top
                player.speed_y = 0
                on_ground = True
            elif player.speed_y < 0:  # Jumping up into platform
                player.top = p.bottom
                player.speed_y = 0

    # Respawn if falling off screen (safety check)
    if player.top > HEIGHT:
        player.pos = (150, 500)
        player.speed_y = 0

    # --- 3. ITEM COLLECTION ---
    # Check if player overlaps with any item
    for item in items:
        if player.colliderect(item["actor"]):
            # Item collected! Remove it from list
            items.remove(item)
            items_collected += 1
            break  # Stop checking this frame


# === INPUT HANDLING ===
def on_mouse_down(pos):
    """Handles button clicks."""

    # Return to map if menu button clicked
    if menu_button.collidepoint(pos):
        return "map"

    # Toggle music
    if mute_button.collidepoint(pos):
        toggle_sound()

    return None


def on_key_down(key):
    """Handles jumping and victory exit."""
    global items_collected

    # If game won, SPACE returns to map
    if items_collected >= 10:
        if key == keys.SPACE:
            return "map"
    else:
        # Normal jump if on ground
        if (key == keys.SPACE or key == keys.UP) and on_ground:
            player.speed_y = JUMP_STRENGTH

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
