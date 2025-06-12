# models.py
from enum import Enum
import pygame
import random
from config import *


class GameState:
    def __init__(self):
        # Game physics
        self.gravity = GRAVITY
        self.bird_movement = 0
        self.current_speed = PIPE_SPEED
        self.current_pipe_gap = INITIAL_PIPE_GAP

        # Game state flags
        self.game_active = False
        self.paused = False
        self.show_customization = False

        # Player stats
        self.hearts = INITIAL_HEARTS
        self.score = 0

        # Power-up states
        self.invincible = False
        self.invincible_pipes = 0
        self.pipes_passed = 0
        self.foggy_mode = False
        self.foggy_pipes_remaining = 0

        # Power-up effect states
        self.heart_effect_timer = 0
        self.wider_gap_effect = False
        self.wider_gap_timer = 0

        # Customization settings
        self.current_bird = DEFAULT_SETTINGS['bird_color']
        self.current_bg = DEFAULT_SETTINGS['background']
        self.current_pipe = DEFAULT_SETTINGS['pipe_color']

    def update_difficulty(self):
        """Update game difficulty based on score"""
        # Increase speed
        self.current_speed = min(
            PIPE_SPEED + (self.score * SPEED_INCREASE_RATE),
            MAX_PIPE_SPEED
        )

        # Decrease pipe gap every X points
        if self.score > 0 and self.score % PIPE_GAP_UPDATE_FREQUENCY == 0:
            self.current_pipe_gap = max(
                INITIAL_PIPE_GAP - (self.score // PIPE_GAP_UPDATE_FREQUENCY * GAP_DECREASE_RATE),
                MIN_PIPE_GAP
            )

    def reset(self):
        """Reset game state while keeping customization settings"""
        # Store current customization
        current_bg = self.current_bg
        current_pipe = self.current_pipe
        current_bird = self.current_bird

        # Reset all states
        self.__init__()

        # Restore customization
        self.current_bg = current_bg
        self.current_pipe = current_pipe
        self.current_bird = current_bird
        self.game_active = True


class BirdColor(Enum):
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"


class PowerUpType(Enum):
    HEART = 1
    INVINCIBLE = 2
    WIDER_GAP = 3


class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, POWER_UP_SIZE[0], POWER_UP_SIZE[1])
        self.type = random.choice(list(PowerUpType))
        self.collected = False

    def move(self, speed):
        self.rect.x -= speed


class Pipe:
    def __init__(self, x, height, is_bottom=True):
        self.rect = pygame.Rect(x, height, 0, 0)
        self.is_bottom = is_bottom
        self.passed = False

    def move(self, speed):
        self.rect.x -= speed

    @property
    def off_screen(self):
        return self.rect.right < -50