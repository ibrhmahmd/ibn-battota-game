from pgzero.actor import Actor

# === CONFIGURATION ===
# List of cities with their names and (x, y) coordinates
# You can add more cities here by just adding a new line!
CITIES_CONFIG = [
    ("tangier", (106, 420)),
    ("fez", (32, 490)),
    ("granada", (186, 455)),
    ("istanbul", (390, 350)),
    ("cairo", (480, 525)),
    ("damascus", (600, 434)),
    ("baghdad", (773, 470)),
    ("medina", (640, 525)),
    ("mecca", (720, 577)),
    ("persia", (853, 455)),
    ("delhi", (1226, 535)),
    ("timbuktu", (53, 595)),
    ("beijing", (1173, 210)),
]

# === ACTORS ===
# The player character
character = Actor("characters/character", pos=(150, 600))

# Create city icons from the config list above
cities = []
for name, position in CITIES_CONFIG:
    city = Actor(f"backgrounds/icons/{name}")
    city.pos = position
    city.home_y = position[1]  # Kept for reference
    cities.append(city)


# === DRAWING ===
def draw(screen):
    """Draws the map background, cities, and character."""
    # Draw Map Background
    screen.blit("backgrounds/map", (0, 0))

    # Draw all City Icons
    for city in cities:
        city.draw()

    # Draw Character on top
    character.draw()


# === UPDATE (MOVEMENT) ===
def update(keyboard):
    """Handles character movement using arrow keys."""

    # Move Left (don't go off screen edge < 50)
    if keyboard.left and character.x > 50:
        character.x -= 4

    # Move Right (don't go off screen edge > 1230)
    if keyboard.right and character.x < 1230:
        character.x += 4

    # Move Up
    if keyboard.up and character.y > 50:
        character.y -= 4

    # Move Down
    if keyboard.down and character.y < 670:
        character.y += 4


# === INPUT HANDLING ===
def on_mouse_down(pos):
    """Handles clicking on cities to enter levels."""

    for city in cities:
        # Check if mouse clicked on this city
        if city.collidepoint(pos):
            print(f"Clicked on {city.image}")

            # Check which city it is and return the screen name
            if city.image == "backgrounds/icons/tangier":
                return "tangier"
            elif city.image == "backgrounds/icons/fez":
                return "fez"

    # If no city clicked
    return None
