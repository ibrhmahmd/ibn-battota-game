from pgzero.actor import Actor

CITIES_CONFIG = [
    ("tangier", (106, 420)),
    ("fez", (32, 490)),
    ("granada", (75, 300)),
    ("istanbul", (390, 350)),
    ("cairo", (480, 525)),
    ("damascus", (600, 434)),
    ("baghdad", (773, 470)),
    ("medina", (640, 525)),
    ("mecca", (720, 577)),
    ("persia", (853, 455)),
    ("delhi", (1226, 535)),
    ("timbuktu", (53, 680)),
    ("beijing", (1173, 210)),
]


character = Actor("characters/character", pos=(150, 600))

cities = []
for name, position in CITIES_CONFIG:
    city = Actor(f"backgrounds/icons/{name}")
    city.pos = position
    city.home_y = position[1]
    cities.append(city)


def draw(screen):
    screen.blit("backgrounds/map", (0, 0))

    for city in cities:
        city.draw()

    character.draw()

    for city in cities:
        name = city.image.split("/")[-1].replace("_", " ").title()

        screen.draw.text(
            name,
            center=(city.x, city.y - 40),
            fontsize=20,
            color="brown",
            owidth=1.5,
            ocolor="gold",
        )


def update(keyboard):
    if keyboard.left and character.x > 50:
        character.x -= 4
    if keyboard.right and character.x < 1230:
        character.x += 4
    if keyboard.up and character.y > 50:
        character.y -= 4
    if keyboard.down and character.y < 670:
        character.y += 4


def on_mouse_down(pos):
    for city in cities:
        if city.collidepoint(pos):
            if city.image == "backgrounds/icons/tangier":
                return "tangier"
            elif city.image == "backgrounds/icons/fez":
                return "fez"
            elif city.image == "backgrounds/icons/cairo":
                return "cairo"
            elif city.image == "backgrounds/icons/damascus":
                return "damascus"
            elif city.image == "backgrounds/icons/timbuktu":
                return "timbuktu"
    return None
