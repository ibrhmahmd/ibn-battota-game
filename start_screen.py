from pgzero.actor import Actor

WIDTH = 1280
HEIGHT = 720


background = Actor("backgrounds/start_screen_background")

start_button = Actor("ui/start_btn", pos=(WIDTH // 2, HEIGHT // 2 - 90))

# eyad
def draw(screen):
    background.draw()
    start_button.draw()


def on_mouse_down(pos):

    if start_button.collidepoint(pos):
        return "map"

    return None
