# sprites.py
import pygame
from config import *


class Bird(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.frames = self.load_frames(color)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.frame_index = 0
        self.animation_speed = 0.1
        self.movement = 0

    def load_frames(self, color):
        frames = []
        for position in ['downflap', 'midflap', 'upflap']:
            image_path = ASSET_PATHS['birds'][color][position]
            # Load image and scale to specific size
            frame = pygame.image.load(image_path).convert_alpha()
            frame = pygame.transform.scale(frame, BIRD_SIZE)
            frames.append(frame)
        return frames

    def animate(self):
        self.frame_index = (self.frame_index + self.animation_speed) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def flap(self):
        self.movement = FLAP_STRENGTH

    def update(self):
        # Apply gravity
        self.movement += GRAVITY
        # Prevent bird from going below floor
        new_y = self.rect.centery + self.movement
        if new_y + self.rect.height/2 > FLOOR_Y_POS:
            new_y = FLOOR_Y_POS - self.rect.height/2
            self.movement = 0
        self.rect.centery = new_y

        # Update animation
        self.animate()

    def reset_position(self):
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.movement = 0


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load(ASSET_PATHS['base']).convert())
        self.rect = self.image.get_rect(bottomleft=(0, SCREEN_HEIGHT+100))
        self.x_pos = 0

    def update(self):
        self.x_pos -= 1
        if self.x_pos <= -SCREEN_WIDTH:
            self.x_pos = 0