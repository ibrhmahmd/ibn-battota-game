import pgzrun
from pgzero.actor import Actor
from pgzero.builtins import music
import start_screen
import world_map
from levels import level_tangier, level_fez, level_cairo, level_damascus, level_timbuktu

WIDTH = 1280
HEIGHT = 720

current_screen = "start"
mute_button = Actor("ui/music_on", pos=(WIDTH - 60, 60))

LEVELS = {
    "tangier": level_tangier,
    "fez": level_fez,
    "cairo": level_cairo,
    "damascus": level_damascus,
    "timbuktu": level_timbuktu,
}


def draw():
    screen.clear()

    if current_screen == "start":
        start_screen.draw(screen)
    elif current_screen == "map":
        world_map.draw(screen)
    elif current_screen in LEVELS:
        LEVELS[current_screen].draw(screen)

    mute_button.draw()


def update():
    if current_screen == "map":
        world_map.update(keyboard)
    elif current_screen in LEVELS:
        LEVELS[current_screen].update(keyboard)


def _switch_screen(new_screen):
    global current_screen
    if new_screen in LEVELS:
        LEVELS[new_screen].reset()
    current_screen = new_screen


def on_mouse_down(pos):
    if mute_button.collidepoint(pos):
        toggle_sound()
        return

    new_screen = None

    if current_screen == "start":
        new_screen = start_screen.on_mouse_down(pos)
    elif current_screen == "map":
        new_screen = world_map.on_mouse_down(pos)
    elif current_screen in LEVELS:
        new_screen = LEVELS[current_screen].on_mouse_down(pos)

    if new_screen:
        _switch_screen(new_screen)


def on_key_down(key):
    new_screen = None

    if current_screen in LEVELS:
        new_screen = LEVELS[current_screen].on_key_down(key)

    if new_screen:
        _switch_screen(new_screen)


def toggle_sound():
    try:
        if mute_button.image == "ui/music_on":
            music.stop()
            mute_button.image = "ui/music_off"
        else:
            music.play("background_music")
            mute_button.image = "ui/music_on"
    except Exception:
        pass


try:
    music.play("background_music")
except Exception:
    pass


pgzrun.go()
