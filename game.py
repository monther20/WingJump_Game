# game.py
import pygame
import sys
import random
from config import *
from models import *
from ui import *
from sprites import *
from utils import *


class FlappyBird:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Flappy Bird')

        # Setup display and clock
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Initialize game state and UI
        self.state = GameState()
        self.ui = CustomizationMenu()

        # Load assets
        self.load_assets()

        # Initialize sprites
        self.setup_sprites()

        # Initialize game objects
        self.pipe_list = []
        self.power_ups = []

        # Setup game events
        self.setup_events()

    def load_assets(self):
        """Load all game assets."""
        # Load backgrounds
        self.bg_surfaces = {
            'day': load_scaled_image(ASSET_PATHS['backgrounds']['day']),
            'night': load_scaled_image(ASSET_PATHS['backgrounds']['night'])
        }

        # Load pipes
        self.pipe_surfaces = {
            'green': load_scaled_image(ASSET_PATHS['pipes']['green']),
            'red': load_scaled_image(ASSET_PATHS['pipes']['red'])
        }

        # Load UI elements
        self.game_over_surface = load_scaled_image(ASSET_PATHS['gameover'])
        self.message_surface = load_scaled_image(ASSET_PATHS['message'])

        # Load numbers for score
        self.number_surfaces = [
            load_scaled_image(path) for path in ASSET_PATHS['numbers']
        ]

        # Load sounds
        self.sounds = load_sound_assets()

    def setup_sprites(self):
        """Initialize game sprites."""
        self.bird = Bird(self.state.current_bird)
        self.floor = Floor()

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.all_sprites.add(self.floor)

    def setup_events(self):
        """Setup pygame custom events."""
        pygame.time.set_timer(EVENTS['BIRDFLAP'], BIRD_FLAP_TIME)
        pygame.time.set_timer(EVENTS['SPAWNPIPE'], PIPE_SPAWN_TIME)
        pygame.time.set_timer(EVENTS['SPAWNPOWERUP'], POWER_UP_SPAWN_TIME)

    def create_pipe(self):
        """Create new pipe obstacles."""
        pipe_surface = self.pipe_surfaces[self.state.current_pipe]
        pipe_height = pipe_surface.get_height()

        # Calculate gap position (leaving space at top and bottom)
        min_y = 200
        max_y = SCREEN_HEIGHT - 200
        gap_y = random.randint(min_y, max_y)

        # Create pipes
        bottom_pipe = Pipe(SCREEN_WIDTH, gap_y + self.state.current_pipe_gap // 2, True)
        top_pipe = Pipe(SCREEN_WIDTH, gap_y - self.state.current_pipe_gap // 2 - pipe_height, False)

        bottom_pipe.rect.size = pipe_surface.get_size()
        top_pipe.rect.size = pipe_surface.get_size()

        return bottom_pipe, top_pipe

    def create_power_up(self):
        """Create a new power-up."""
        random_y = random.randint(200, SCREEN_HEIGHT - 200)
        return PowerUp(SCREEN_WIDTH, random_y)

    def handle_input(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # First, handle customization menu if it's open
            if self.state.show_customization:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    category, option = self.ui.handle_events(event)
                    if category == 'exit':
                        self.state.show_customization = False
                        self.sounds['swoosh'].play()
                    elif category:
                        print(f"Applying customization: {category} - {option}")
                        self.apply_customization(category, option)
                        self.sounds['swoosh'].play()
                continue  # Skip other input handling while in customization menu

            # Handle customize button when menu is closed
            if not self.state.game_active:
                mouse_pos = pygame.mouse.get_pos()
                self.ui.customize_button.hover = self.ui.customize_button.rect.collidepoint(mouse_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.customize_button.rect.collidepoint(event.pos):
                        self.state.show_customization = not self.state.show_customization
                        continue  # Skip other input handling after clicking customize button

            # Handle game input only if not in customization
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.handle_jump_input()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.ui.customize_button.rect.collidepoint(event.pos):
                    self.handle_jump_input()

            # Handle game events
            if event.type == EVENTS['SPAWNPIPE'] and self.state.game_active and not self.state.paused:
                self.pipe_list.extend(self.create_pipe())

            if event.type == EVENTS['SPAWNPOWERUP'] and self.state.game_active and not self.state.paused:
                if random.random() < POWER_UP_SPAWN_CHANCE:
                    self.power_ups.append(self.create_power_up())

    def handle_jump_input(self):
        """Handle jump input from either keyboard or mouse."""
        if self.state.game_active:
            if self.state.paused:
                # When game is paused after collision, reset bird position and unpause
                self.bird.reset_position()
                self.state.paused = False
                # Ensure foggy mode is active
                self.state.foggy_mode = True
                self.state.foggy_pipes_remaining = PIPES_FOR_FOGGY
                self.state.pipes_passed = 0
            else:
                self.bird.flap()
                self.sounds['wing'].play()
        else:
            self.reset_game()

    def apply_customization(self, category, option):
        """Apply customization options."""
        if not option:
            return

        print(f"Applying {category} customization: {option}")  # Debug print

        if category == 'bird':
            color = option.lower()
            self.state.current_bird = color
            # Create new bird with selected color
            new_bird = Bird(color)
            new_bird.rect.center = self.bird.rect.center
            new_bird.movement = self.bird.movement
            self.bird = new_bird
            # Recreate sprite group with new bird
            self.all_sprites = pygame.sprite.Group()
            self.all_sprites.add(self.bird)
            self.all_sprites.add(self.floor)
        elif category == 'background':
            self.state.current_bg = option.lower()
        elif category == 'pipe':
            self.state.current_pipe = option.lower()

        # Force update active buttons
        self.ui.update_active_buttons(self.state)

        # Print current state for debugging
        print(
            f"Current state - Bird: {self.state.current_bird}, BG: {self.state.current_bg}, Pipe: {self.state.current_pipe}")

    def check_collisions(self):
        """Check for collisions between bird and obstacles."""
        if self.state.invincible:
            return True

        collision_occurred = False

        # Check pipe collisions
        if check_collision(self.bird.rect, self.pipe_list):
            collision_occurred = True

        # Check boundary collisions (including ground)
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= FLOOR_Y_POS:
            collision_occurred = True
            # Ensure bird doesn't go below the floor
            if self.bird.rect.bottom > FLOOR_Y_POS:
                self.bird.rect.bottom = FLOOR_Y_POS
                self.bird.movement = 0

        if collision_occurred:
            self.sounds['hit'].play()
            self.state.hearts -= 1
            self.state.paused = True  # Pause the game on collision

            if self.state.hearts <= 0:
                self.sounds['die'].play()
                return False
            else:
                # Don't reset position immediately - wait for player input
                # Clear pipes and setup foggy mode
                self.pipe_list.clear()
                self.state.foggy_mode = True
                self.state.foggy_pipes_remaining = PIPES_FOR_FOGGY
                self.state.pipes_passed = 0
                return True

        return True

    def check_power_up_collisions(self):
        """Check for collisions with power-ups."""
        for power_up in self.power_ups:
            if not power_up.collected and self.bird.rect.colliderect(power_up.rect):
                power_up.collected = True
                self.apply_power_up(power_up.type)

    def apply_power_up(self, power_up_type):
        """Apply power-up effects."""
        # Play power-up sound
        self.sounds['point'].play()

        if power_up_type == PowerUpType.HEART:
            self.state.hearts = min(self.state.hearts + 1, INITIAL_HEARTS)
            self.state.heart_effect_timer = 60  # Effect lasts for 60 frames

        elif power_up_type == PowerUpType.INVINCIBLE:
            self.state.invincible = True
            self.state.invincible_pipes = PIPES_FOR_INVINCIBLE
            # Display invincibility message
            font = pygame.font.Font(None, 48)
            text = font.render("INVINCIBLE!", True, (255, 215, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(text, text_rect)

        elif power_up_type == PowerUpType.WIDER_GAP:
            self.state.current_pipe_gap = INITIAL_PIPE_GAP
            self.state.wider_gap_effect = True
            self.state.wider_gap_timer = 60

    def update(self):
        """Update game state and sprites."""
        if self.state.game_active and not self.state.paused:
            # Update sprites
            self.all_sprites.update()

            # Move pipes and check for score
            for pipe in self.pipe_list:
                pipe.move(self.state.current_speed)
                # Check for score
                if pipe.rect.centerx < self.bird.rect.centerx and not pipe.passed and pipe.is_bottom:
                    self.state.score += 1
                    pipe.passed = True
                    self.sounds['point'].play()

            # Clean up off-screen pipes
            self.pipe_list = [pipe for pipe in self.pipe_list if not pipe.off_screen]

            # Update power-ups
            for power_up in self.power_ups:
                if not power_up.collected:
                    power_up.move(self.state.current_speed)
            self.power_ups = [p for p in self.power_ups if p.rect.right > -50 and not p.collected]

            # Check collisions
            self.state.game_active = self.check_collisions()
            self.check_power_up_collisions()

            # Update difficulty
            self.state.update_difficulty()

            # Update fog mode
            if self.state.foggy_mode:
                if any(pipe.passed for pipe in self.pipe_list if pipe.is_bottom):
                    self.state.pipes_passed += 1
                    if self.state.pipes_passed >= PIPES_FOR_FOGGY:
                        self.state.foggy_mode = False
                        self.state.foggy_pipes_remaining = 0
                        self.state.pipes_passed = 0

            # Update power-up effects
            if self.state.invincible:
                self.state.invincible_pipes -= 1
                if self.state.invincible_pipes <= 0:
                    self.state.invincible = False

            if self.state.heart_effect_timer > 0:
                self.state.heart_effect_timer -= 1

            if self.state.wider_gap_effect:
                self.state.wider_gap_timer -= 1
                if self.state.wider_gap_timer <= 0:
                    self.state.wider_gap_effect = False

    def draw(self):
        """Draw all game elements."""
        # Draw background
        bg_surface = self.bg_surfaces['night' if self.state.current_bg == 'night' else 'day']
        self.screen.blit(bg_surface, (0, -150))

        if self.state.game_active:
            # Draw pipes
            pipe_surface = self.pipe_surfaces[self.state.current_pipe]
            for pipe in self.pipe_list:
                if pipe.is_bottom:
                    self.screen.blit(pipe_surface, pipe.rect)
                else:
                    flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                    self.screen.blit(flip_pipe, pipe.rect)

            # Draw power-ups
            for power_up in self.power_ups:
                if not power_up.collected:
                    pygame.draw.rect(self.screen, YELLOW, power_up.rect)
                    font = pygame.font.Font(None, 36)
                    text = font.render("!", True, BLACK)
                    text_rect = text.get_rect(center=power_up.rect.center)
                    self.screen.blit(text, text_rect)
                    

            # Draw power-up effects
            if self.state.invincible:
                # Draw invincibility effect on pipes
                for pipe in self.pipe_list:
                    pipe_surface = self.pipe_surfaces[self.state.current_pipe].copy()
                    pipe_surface.set_alpha(128)  # Make pipes semi-transparent
                    if pipe.is_bottom:
                        self.screen.blit(pipe_surface, pipe.rect)
                    else:
                        flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                        self.screen.blit(flip_pipe, pipe.rect)

                    if self.state.wider_gap_effect:
                        # Draw wider gap effect
                        if len(self.pipe_list) > 0:
                            pygame.draw.rect(self.screen, (0, 191, 255, 50),
                                             pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)


            # Draw sprites
            self.all_sprites.draw(self.screen)

            # Draw UI elements
            for i in range(self.state.hearts):
                draw_heart(self.screen, 40 + i * 40, 50)

            draw_score(self.screen, self.state.score, self.number_surfaces)

            if self.state.foggy_mode:
                fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fog_surface.fill(WHITE)
                fog_surface.set_alpha(FOG_ALPHA)
                self.screen.blit(fog_surface, (0, 0))

        else:
            # Draw start/game over screen
            self.screen.blit(self.message_surface, (SCREEN_WIDTH // 2 - self.message_surface.get_width() // 2, 100))
            if self.state.show_customization:
                self.ui.draw(self.screen, self.state)
            else:
                self.ui.customize_button.draw(self.screen)

    def reset_game(self):
        """Reset the game state."""
        self.state.reset()
        self.pipe_list.clear()
        self.power_ups.clear()
        self.bird.reset_position()

    def run(self):
        """Main game loop."""
        while True:
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)