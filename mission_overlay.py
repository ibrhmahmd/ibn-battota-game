from pgzero.actor import Actor
import pygame
import os

WIDTH = 1280
HEIGHT = 720

briefing_frame = Actor("items/mission_briefing", center=(WIDTH // 2, HEIGHT // 2))


def draw(screen, level_id):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    briefing_frame.draw()
    text_image_path = f"levels_texts/text_{level_id}"

    try:
        text_actor = Actor(text_image_path, center=(WIDTH // 2, HEIGHT // 2))
        text_actor.draw()
    except Exception:
        pass
