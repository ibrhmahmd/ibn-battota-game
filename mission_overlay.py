from pgzero.actor import Actor
import pygame
import os

WIDTH = 1280
HEIGHT = 720

briefing_frame = Actor("items/mission_briefing", center=(WIDTH // 2, HEIGHT // 2))

_overlay = pygame.Surface((WIDTH, HEIGHT))
_overlay.set_alpha(180)
_overlay.fill((0, 0, 0))

_text_actors = {}


def _get_text_actor(level_id):
    if level_id not in _text_actors:
        try:
            _text_actors[level_id] = Actor(
                f"levels_texts/text_{level_id}", center=(WIDTH // 2, HEIGHT // 2)
            )
        except Exception:
            _text_actors[level_id] = None
    return _text_actors.get(level_id)


def draw(screen, level_id):
    screen.blit(_overlay, (0, 0))

    briefing_frame.draw()

    text_actor = _get_text_actor(level_id)
    if text_actor:
        text_actor.draw()
