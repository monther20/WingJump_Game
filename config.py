# config.py
import pygame

# Screen settings
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 800
FPS = 120

# Game physics
GRAVITY = 0.15  # Reduced for slower movement
FLAP_STRENGTH = -6  # Reduced for better control
PIPE_SPEED = 3  # Starting speed
MAX_PIPE_SPEED = 6  # Maximum pipe speed
SPEED_INCREASE_RATE = 0.07  # How much to increase speed per point
ANIMATION_SPEED = 0.07

# Add these to config.py
BIRD_SIZE = (44, 34)

# Game settings
INITIAL_HEARTS = 3
INITIAL_PIPE_GAP = 400  # Starting gap
MIN_PIPE_GAP = 120  # Minimum gap size
GAP_DECREASE_RATE = 2  # How much to decrease gap per point
PIPE_GAP_UPDATE_FREQUENCY = 5  # Update gap every X points

# Event timings (milliseconds)
PIPE_SPAWN_TIME = 1500  # Increased for better spacing
POWER_UP_SPAWN_TIME = 5000
BIRD_FLAP_TIME = 200

# Power up settings
POWER_UP_SPAWN_CHANCE = 0.3  # 30% chance
PIPES_FOR_FOGGY = 3
PIPES_FOR_INVINCIBLE = 3
POWER_UP_SIZE = (30, 30)

# Game position constants
BIRD_START_POS = (100, SCREEN_HEIGHT // 2)
SCORE_Y_POS = 100
FLOOR_Y_POS = SCREEN_HEIGHT - 100

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# UI Settings
FONT_SIZE = 24
TITLE_FONT_SIZE = 32
FOG_ALPHA = 150  # Transparency for fog effect
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 30
BUTTON_SPACING = 20

# Button colors
BUTTON_COLORS = {
    'yellow_bird': (200, 200, 0),
    'red_bird': (200, 0, 0),
    'blue_bird': (0, 0, 200),
    'day_bg': (100, 150, 200),
    'night_bg': (50, 50, 100),
    'green_pipe': (0, 200, 0),
    'red_pipe': (200, 0, 0),
    'customize': (100, 100, 200)
}

# Button positions (adjusted for smaller screen)
BUTTON_POSITIONS = {
    'customize': (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 100, 120, 40),
    'bird_row': SCREEN_HEIGHT - 250,
    'background_row': SCREEN_HEIGHT - 200,
    'pipe_row': SCREEN_HEIGHT - 150,
    'column_spacing': [30, 140, 250],
    'button_size': (100, 30)
}

# Asset paths
ASSET_PATHS = {
    'backgrounds': {
        'day': 'images/background-day.png',
        'night': 'images/background-night.png'
    },
    'birds': {
        'yellow': {
            'downflap': 'images/yellowbird-downflap.png',
            'midflap': 'images/yellowbird-midflap.png',
            'upflap': 'images/yellowbird-upflap.png'
        },
        'red': {
            'downflap': 'images/redbird-downflap.png',
            'midflap': 'images/redbird-midflap.png',
            'upflap': 'images/redbird-upflap.png'
        },
        'blue': {
            'downflap': 'images/bluebird-downflap.png',
            'midflap': 'images/bluebird-midflap.png',
            'upflap': 'images/bluebird-upflap.png'
        }
    },
    'pipes': {
        'green': 'images/pipe-green.png',
        'red': 'images/pipe-red.png'
    },
    'base': 'images/base.png',
    'gameover': 'images/gameover.png',
    'message': 'images/message.png',
    'numbers': ['images/{}.png'.format(i) for i in range(10)],
    'sounds': {
        'die': 'audio/die.wav',
        'hit': 'audio/hit.wav',
        'point': 'audio/point.wav',
        'swoosh': 'audio/swoosh.wav',
        'wing': 'audio/wing.wav'
    }
}

# Custom event IDs
EVENTS = {
    'BIRDFLAP': pygame.USEREVENT + 0,
    'SPAWNPIPE': pygame.USEREVENT + 1,
    'SPAWNPOWERUP': pygame.USEREVENT + 2
}

# Default settings
DEFAULT_SETTINGS = {
    'bird_color': 'yellow',
    'background': 'day',
    'pipe_color': 'green'
}

# Game state flags
INITIAL_GAME_STATE = {
    'game_active': False,
    'show_customization': False,
    'paused': False,
    'foggy_mode': False
}