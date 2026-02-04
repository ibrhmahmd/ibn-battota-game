from pgzero.actor import Actor
from game_states import *
from constants import WIDTH, HEIGHT
import game_states


background = Actor("backgrounds/start_screen_background")
start_button = Actor("ui/start_btn", pos=(WIDTH // 2, HEIGHT // 2 - 90))
mute_button = Actor("ui/music_on", pos=(WIDTH - 50, 50))


def init():
    pass


def draw(screen):
    background.draw()
    start_button.draw()
    mute_button.draw()


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


def on_mouse_down(pos):
    if start_button.collidepoint(pos):
        return STATE_WORLD_MAP

    if mute_button.collidepoint(pos):
        toggle_sound()

    return None
