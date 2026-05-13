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


def draw():
    screen.clear()

    if current_screen == "start":
        start_screen.draw(screen)

    elif current_screen == "map":
        world_map.draw(screen)

    elif current_screen == "tangier":
        level_tangier.draw(screen)

    elif current_screen == "fez":
        level_fez.draw(screen)

    elif current_screen == "cairo":
        level_cairo.draw(screen)

    elif current_screen == "damascus":
        level_damascus.draw(screen)

    elif current_screen == "timbuktu":
        level_timbuktu.draw(screen)

    mute_button.draw()


def update():
    if current_screen == "map":
        world_map.update(keyboard)

    elif current_screen == "tangier":
        level_tangier.update(keyboard)

    elif current_screen == "fez":
        level_fez.update()

    elif current_screen == "cairo":
        level_cairo.update(keyboard)

    elif current_screen == "damascus":
        level_damascus.update(keyboard)

    elif current_screen == "timbuktu":
        level_timbuktu.update(keyboard)


def on_mouse_down(pos):
    global current_screen

    new_screen = None

    if mute_button.collidepoint(pos):
        toggle_sound()
        return

    if current_screen == "start":
        new_screen = start_screen.on_mouse_down(pos)

    elif current_screen == "map":
        new_screen = world_map.on_mouse_down(pos)

    elif current_screen == "tangier":
        new_screen = level_tangier.on_mouse_down(pos)

    elif current_screen == "fez":
        new_screen = level_fez.on_mouse_down(pos)

    elif current_screen == "cairo":
        new_screen = level_cairo.on_mouse_down(pos)

    elif current_screen == "damascus":
        new_screen = level_damascus.on_mouse_down(pos)

    elif current_screen == "timbuktu":
        new_screen = level_timbuktu.on_mouse_down(pos)

    if new_screen:
        current_screen = new_screen


def on_key_down(key):
    global current_screen

    new_screen = None

    if current_screen == "tangier":
        new_screen = level_tangier.on_key_down(key)
    elif current_screen == "fez":
        new_screen = level_fez.on_key_down(key)
    elif current_screen == "cairo":
        new_screen = level_cairo.on_key_down(key)
    elif current_screen == "damascus":
        new_screen = level_damascus.on_key_down(key)
    elif current_screen == "timbuktu":
        new_screen = level_timbuktu.on_key_down(key)

    if new_screen:
        current_screen = new_screen


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


try:
    music.play("background_music")
except:
    pass


pgzrun.go()
