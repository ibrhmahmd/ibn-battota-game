from pgzero.actor import Actor

# === IMPORTS AND SETTINGS ===
WIDTH = 1280
HEIGHT = 720


# === UI ELEMENTS ===
# The background image for the start screen
background = Actor("backgrounds/start_screen_background")

# Buttons for the user to click
# We place the start button in the middle of the screen
start_button = Actor("ui/start_btn", pos=(WIDTH // 2, HEIGHT // 2 - 90))
# The music button goes in the top-right corner
mute_button = Actor("ui/music_on", pos=(WIDTH - 50, 50))


# === DRAWING ===
def draw(screen):
    """Draws the start screen background and buttons."""
    background.draw()
    start_button.draw()
    mute_button.draw()


# === HELPER FUNCTIONS ===
def toggle_sound():
    """Turns music on or off when the button is clicked."""
    try:
        # Check if music is currently on (by looking at the button image)
        if mute_button.image == "ui/music_on":
            music.stop()
            mute_button.image = "ui/music_off"
        else:
            music.play("background_music")
            mute_button.image = "ui/music_on"
    except:
        # If music fails to load, just ignore it
        pass


# === INPUT HANDLING ===
def on_mouse_down(pos):
    """Handles mouse clicks on the start screen."""

    # Check if player clicked the Start Game button
    if start_button.collidepoint(pos):
        # Return the name of the next screen to go to
        return "map"

    # Check if player clicked the music toggle
    if mute_button.collidepoint(pos):
        toggle_sound()

    # If nothing important was clicked, stay on this screen
    return None
