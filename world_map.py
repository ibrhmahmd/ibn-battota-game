from pgzero.actor import Actor
from constants import *
from game_states import *
import math

# --- Actors ---
character = None
cities = []

# Camera
camera_x = 0
camera_y = 0
game_time = 0


def init():
    global character, cities, camera_x, camera_y

    # Character
    character = Actor("characters/character", pos=(150, 600))
    character.is_jumping = False
    character.jump_timer = 0

    # Cities
    cities.clear()
    for name, position in CITIES_CONFIG:
        city = Actor(f"backgrounds/icons/{name}")
        city.pos = position
        city.home_y = position[1]
        cities.append(city)

    camera_x = 0
    camera_y = 0


def draw(screen):
    # Draw Map
    screen.blit("backgrounds/map", (-camera_x, -camera_y))

    # Draw Cities
    for city in cities:
        draw_at_camera(screen, city)

    # Draw Character
    draw_character(screen)


def update(keyboard):
    global game_time, camera_x, camera_y
    game_time += 0.05

    # Movement
    if keyboard.left and character.x > 0:
        character.x -= CHARACTER_SPEED
    if keyboard.right and character.x < MAP_WIDTH:
        character.x += CHARACTER_SPEED
    if keyboard.up and character.y > 0:
        character.y -= CHARACTER_SPEED
    if keyboard.down and character.y < MAP_HEIGHT:
        character.y += CHARACTER_SPEED

    # Camera Follow
    target_x = character.x - WIDTH / 2
    target_y = character.y - HEIGHT / 2
    target_x = max(0, min(target_x, MAP_WIDTH - WIDTH))
    target_y = max(0, min(target_y, MAP_HEIGHT - HEIGHT))
    camera_x += (target_x - camera_x) * 0.1
    camera_y += (target_y - camera_y) * 0.1

    # # Interactions
    # for city in cities:
    #     dist = math.hypot(character.x - city.x, character.y - city.y)
    #     if dist < 80:
    #         city.y = city.home_y + math.sin(game_time * 2) * 8
    #         if dist < 40 and not character.is_jumping:
    #             character.is_jumping = True
    #             character.jump_timer = JUMP_TIME
    #     else:
    #         city.y = city.home_y

    # Jump Animation
    if character.is_jumping:
        character.jump_timer -= 1
        if character.jump_timer <= 0:
            character.is_jumping = False


def on_mouse_down(pos):
    world_pos_x = pos[0] + camera_x
    world_pos_y = pos[1] + camera_y

    for city in cities:
        dist = math.hypot(world_pos_x - city.x, world_pos_y - city.y)
        if dist < 50:
            print(f"Clicked on {city.image}")
            if city.image == "backgrounds/icons/tangier":
                return STATE_MINI_GAME_TANGIER
            elif city.image == "backgrounds/icons/fez":
                return STATE_MINI_GAME_FEZ

    return None


# --- Helpers ---
def draw_at_camera(screen, actor):
    old_pos = actor.pos
    actor.pos = (actor.x - camera_x, actor.y - camera_y)
    actor.draw()
    actor.pos = old_pos


def draw_character(screen):
    jump_offset = 0
    if character.is_jumping:
        progress = (JUMP_TIME - character.jump_timer) / float(JUMP_TIME)
        jump_offset = math.sin(progress * math.pi) * JUMP_HEIGHT

    old_pos = character.pos
    character.pos = (character.x - camera_x, (character.y - jump_offset) - camera_y)
    character.draw()
    character.pos = old_pos
