from pgzero.actor import Actor
from pgzero.constants import keys
import random
import mission_overlay

WIDTH = 1280
HEIGHT = 720

MOVE_SPEED = 6
SAND_SPEED = 4
SURVIVAL_SECONDS = 30

player = Actor("characters/character")
player.pos = (100, HEIGHT - 50)

goal = Actor("items/collectibles/water_skin")
goal.pos = (WIDTH - 100, HEIGHT - 50)

sand_particles = []
sand_spawn_timer = 0
timer_frames = SURVIVAL_SECONDS * 60
show_goal = False
win = False
game_over = False
show_mission = True

back_button = Actor("ui/back_btn", pos=(80, 50))
victory_seal = Actor("items/level_passed_seal", center=(WIDTH // 2, HEIGHT // 2))


def draw(screen):
    screen.clear()
    screen.blit("backgrounds/bg_timbuktu", (0, 0))

    player.draw()
    for sand in sand_particles:
        sand.draw()

    back_button.draw()

    if show_goal:
        goal.draw()
        screen.draw.text(
            "THE STORM HAS CLEARED! REACH THE OASIS!",
            center=(WIDTH // 2, 100),
            fontsize=40,
            color="cyan",
            owidth=1.5,
            ocolor="black",
        )
    else:
        seconds_left = max(0, timer_frames // 60)
        screen.draw.text(
            f"SURVIVE THE BLIZZARD: {seconds_left}s",
            center=(WIDTH // 2, 100),
            fontsize=60,
            color="white",
            owidth=2,
            ocolor="black",
        )

    if win:
        victory_seal.draw()
        screen.draw.text(
            "Press SPACE to Continue",
            center=(WIDTH // 2, HEIGHT // 2 + 60),
            fontsize=30,
            color="white",
            owidth=1.5,
            ocolor="black",
        )
    elif game_over:
        screen.draw.text(
            "CAUGHT IN THE STORM!",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=80,
            color="red",
            owidth=2,
            ocolor="black",
        )
        screen.draw.text(
            "Press SPACE to Retry",
            center=(WIDTH // 2, HEIGHT // 2 + 80),
            ocolor="black",
        )

    if show_mission:
        mission_overlay.draw(screen, "timbuktu")


def update(keyboard):
    global \
        sand_spawn_timer, \
        timer_frames, \
        show_goal, \
        sand_particles, \
        win, \
        game_over, \
        show_mission

    if show_mission:
        return

    if win or game_over:
        return

    if timer_frames > 0:
        timer_frames -= 1
    else:
        show_goal = True

    if keyboard.left:
        player.x -= MOVE_SPEED
    if keyboard.right:
        player.x += MOVE_SPEED

    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    sand_spawn_timer += 1
    if sand_spawn_timer > 3:
        sand_spawn_timer = 0
        new_sand = Actor("items/sand_particle")
        new_sand.pos = (random.randint(0, WIDTH), -50)
        sand_particles.append(new_sand)

    for sand in sand_particles:
        sand.y += SAND_SPEED
        if sand.colliderect(player):
            game_over = True

    sand_particles = [s for s in sand_particles if s.top < HEIGHT]

    if show_goal:
        if player.colliderect(goal):
            win = True


def on_mouse_down(pos):
    if back_button.collidepoint(pos):
        return "map"
    return None


def on_key_down(key):
    global win, game_over, show_mission

    if show_mission:
        if key == keys.SPACE:
            show_mission = False
        return

    if win and key == keys.SPACE:
        return "map"
    if game_over and key == keys.SPACE:
        reset()
    return None


def reset():
    global sand_particles, sand_spawn_timer, timer_frames, show_goal, game_over, win
    player.pos = (100, HEIGHT - 50)
    sand_particles.clear()
    sand_spawn_timer = 0
    timer_frames = SURVIVAL_SECONDS * 60
    show_goal = False
    game_over = False
    win = False
