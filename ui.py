# ui.py
import pygame
from config import *


class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.active = False
        self.original_y = y  # Store original y position

    def draw(self, screen):
        # Brighten color when hovering or active
        color = self.color
        if self.hover:
            color = tuple(min(c + 20, 255) for c in self.color)
        if self.active:
            color = tuple(min(c + 40, 255) for c in self.color)

        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Draw text
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.hover = self.rect.collidepoint(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                return True
        return False


class CustomizationMenu:
    def __init__(self):
        self.create_buttons()
        self.font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.label_font = pygame.font.Font(None, FONT_SIZE)
        self.labels = {
            'bird': "Bird Color:",
            'background': "Background:",
            'pipe': "Pipe Color:"
        }

    def create_buttons(self):
        pos = BUTTON_POSITIONS
        size = pos['button_size']

        self.buttons = {
            'bird': [
                Button(pos['column_spacing'][0], pos['bird_row'], size[0], size[1], "Yellow", (200, 200, 0)),
                Button(pos['column_spacing'][1], pos['bird_row'], size[0], size[1], "Red", (200, 0, 0)),
                Button(pos['column_spacing'][2], pos['bird_row'], size[0], size[1], "Blue", (0, 0, 200))
            ],
            'background': [
                Button(pos['column_spacing'][0], pos['background_row'], size[0], size[1], "Day", (100, 150, 200)),
                Button(pos['column_spacing'][1], pos['background_row'], size[0], size[1], "Night", (50, 50, 100))
            ],
            'pipe': [
                Button(pos['column_spacing'][0], pos['pipe_row'], size[0], size[1], "Green", (0, 200, 0)),
                Button(pos['column_spacing'][1], pos['pipe_row'], size[0], size[1], "Red", (200, 0, 0))
            ]
        }

        self.customize_button = Button(
            pos['customize'][0], pos['customize'][1],
            pos['customize'][2], pos['customize'][3],
            "Customize", (100, 100, 200)
        )

        # Add exit button
        self.exit_button = Button(
            SCREEN_WIDTH - 100, SCREEN_HEIGHT - 400,  # Position in top right
            80, 30,  # Smaller size
            "Exit", (200, 50, 50)  # Red color
        )

    def update_active_buttons(self, game_state):
        """Update which buttons should be shown as active based on current game state"""
        for category, buttons in self.buttons.items():
            for button in buttons:
                if category == 'bird':
                    button.active = button.text.lower() == game_state.current_bird
                elif category == 'background':
                    button.active = button.text.lower() == game_state.current_bg
                elif category == 'pipe':
                    button.active = button.text.lower() == game_state.current_pipe

    def draw(self, screen, game_state=None):
        if game_state:
            self.update_active_buttons(game_state)

        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Draw title with more space at the top
        title = self.font.render("Customization", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 400))
        screen.blit(title, title_rect)

        # Draw exit button
        self.exit_button.draw(screen)

        # Draw category labels and buttons with proper spacing
        starting_y = SCREEN_HEIGHT - 350  # Start labels lower to avoid overlap with title
        spacing = 80  # Increased spacing between categories

        for i, (category, label_text) in enumerate(self.labels.items()):
            # Calculate y position for this category
            current_y = starting_y + (i * spacing)

            # Draw label
            text = self.label_font.render(label_text, True, WHITE)
            screen.blit(text, (10, current_y))

            # Update button positions
            for j, button in enumerate(self.buttons[category]):
                button.rect.y = current_y + 30  # Position buttons below their labels
                button.rect.x = BUTTON_POSITIONS['column_spacing'][j]  # Keep existing x positions
                button.draw(screen)

    def handle_events(self, event):
        # Handle exit button
        if self.exit_button.handle_event(event):
            return 'exit', None

        # Handle option buttons
        for category, button_list in self.buttons.items():
            for button in button_list:
                if button.handle_event(event):
                    print(f"Button clicked: {category} - {button.text}")  # Debug print
                    return category, button.text

        return None, None
