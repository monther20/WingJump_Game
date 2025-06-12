# utils.py
import pygame
from config import *


def load_scaled_image(path):
    """Load and scale an image."""
    return pygame.transform.scale2x(pygame.image.load(path).convert_alpha())


def draw_heart(screen, x, y, scale=15):
    """Draw a heart shape."""
    color = RED

    # Draw the two circles for the top of the heart
    pygame.draw.circle(screen, color, (int(x - scale / 2), int(y - scale / 4)), int(scale / 2))
    pygame.draw.circle(screen, color, (int(x + scale / 2), int(y - scale / 4)), int(scale / 2))

    # Draw the bottom triangle of the heart
    points = [
        (x - scale, y - scale / 4),  # Left point
        (x + scale, y - scale / 4),  # Right point
        (x, y + scale)  # Bottom point
    ]
    pygame.draw.polygon(screen, color, points)


def draw_score(screen, score, number_images):
    """Draw the score using number images."""
    score_str = str(score)
    total_width = sum(number_images[int(digit)].get_width() for digit in score_str)
    x_pos = (SCREEN_WIDTH - total_width) // 2

    for digit in score_str:
        screen.blit(number_images[int(digit)], (x_pos, 100))
        x_pos += number_images[int(digit)].get_width()


def draw_fog_effect(screen):
    """Draw a foggy overlay effect."""
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fog_surface.fill(WHITE)
    fog_surface.set_alpha(100)
    screen.blit(fog_surface, (0, 0))


def load_sound_assets():
    """Load all sound assets."""
    sounds = {}
    for sound_name, path in ASSET_PATHS['sounds'].items():
        sounds[sound_name] = pygame.mixer.Sound(path)
    return sounds


def check_collision(bird_rect, pipes):
    """Check for collisions between bird and pipes."""
    for pipe in pipes:
        if bird_rect.colliderect(pipe.rect):
            return True
    return False


def is_off_screen(sprite):
    """Check if a sprite is off the screen."""
    return sprite.rect.right < -50