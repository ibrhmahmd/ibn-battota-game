import pgzrun
import pygame
import game_states
from game_states import *
from constants import *

import start_screen
import world_map
import levels.level_tangier as level_tangier
import levels.level_fez as level_fez

start_screen.init()
world_map.init()
level_tangier.init()
level_fez.init()


def draw():
    screen.clear()

    if game_states.current_state == STATE_START_MENU:
        start_screen.draw(screen)

    elif game_states.current_state == STATE_WORLD_MAP:
        world_map.draw(screen)

    elif game_states.current_state == STATE_MINI_GAME_TANGIER:
        level_tangier.draw(screen)

    elif game_states.current_state == STATE_MINI_GAME_FEZ:
        level_fez.draw(screen)


def update():
    if game_states.current_state == STATE_START_MENU:
        pass

    elif game_states.current_state == STATE_WORLD_MAP:
        world_map.update(keyboard)

    elif game_states.current_state == STATE_MINI_GAME_TANGIER:
        level_tangier.update(keyboard)

    elif game_states.current_state == STATE_MINI_GAME_FEZ:
        level_fez.update()


def on_mouse_down(pos):
    new_state = None

    if game_states.current_state == STATE_START_MENU:
        new_state = start_screen.on_mouse_down(pos)

    elif game_states.current_state == STATE_WORLD_MAP:
        new_state = world_map.on_mouse_down(pos)

    elif game_states.current_state == STATE_MINI_GAME_TANGIER:
        new_state = level_tangier.on_mouse_down(pos)

    elif game_states.current_state == STATE_MINI_GAME_FEZ:
        new_state = level_fez.on_mouse_down(pos)

    if new_state:
        change_state(new_state)


def on_key_down(key):
    if key == keys.F:
        screen.surface = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.FULLSCREEN
            if not screen.surface.get_flags() & pygame.FULLSCREEN
            else 0,
        )

    # State specific keys
    new_state = None
    if game_states.current_state == STATE_MINI_GAME_TANGIER:
        new_state = level_tangier.on_key_down(key)
    elif game_states.current_state == STATE_MINI_GAME_FEZ:
        new_state = level_fez.on_key_down(key)

    # Handle state transition
    if new_state:
        change_state(new_state)


def change_state(new_state):
    game_states.current_state = new_state

    if new_state == STATE_MINI_GAME_TANGIER:
        level_tangier.init()
    elif new_state == STATE_MINI_GAME_FEZ:
        level_fez.init()


if game_states.current_state == STATE_START_MENU:
    try:
        music.play("background_music")
    except:
        pass

pgzrun.go()
