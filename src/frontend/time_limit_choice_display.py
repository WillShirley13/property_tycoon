import pygame
import sys
from typing import List, Tuple, Optional


class TimeLimitChoiceDisplay:
    def __init__(self, screen_width: int, screen_height: int, screen: pygame.Surface) -> None:
        # Store screen
        self.screen: pygame.Surface = screen

        # Store screen dimensions for responsive layout
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height

        # Define color scheme
        self.BACKGROUND_COLOR: Tuple[int, int, int] = (
            1,
            10,
            61,
        )  # White background
        self.BUTTON_COLOR: Tuple[int, int, int] = (
            148,
            0, 
            0
        )  # Red for button
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            255,
            0,
            0,
        )  # Lighter red for hover state
        self.BUTTON_INACTIVE_COLOR: Tuple[int, int, int] = (
            150,
            150,
            150,
        )  # Gray for inactive buttons

        # Calculate font sizes proportional to screen size
        self.title_size: int = max(int(screen_height * 0.05), 24)  # Minimum size of 24
        self.button_size: int = max(int(screen_height * 0.04), 20)  # Minimum size of 20

        # Initialize fonts with fallback to default font if Arial not available
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", self.title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont("Arial", self.button_size)
        except:
            self.title_font: pygame.font.Font = pygame.font.SysFont(None, self.title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont(None, self.button_size)

        # Create button layout
        self.time_options: List[int] = []  # Will be set in setup_buttons
        self.buttons: List[Tuple[pygame.Rect, int]] = []  # Will be set in setup_buttons
        self.setup_buttons()

    def setup_buttons(self) -> None:
        # Calculate responsive button dimensions
        button_width: int = int(self.screen_width * 0.25)
        button_height: int = int(self.screen_height * 0.075)
        button_margin: int = int(self.screen_height * 0.02)

        # Define available time limit options
        self.time_options = [0, 30, 60, 90, 120]  # 0 means no time limit
        self.buttons = []

        # Create a button for each time option, positioned vertically
        for i, time in enumerate(self.time_options):
            # Center buttons horizontally, stack vertically with margin
            button_x: int = (self.screen_width - button_width) // 2
            button_y: int = self.screen_height // 2 - 50 + (button_height + button_margin) * i

            # Store button rect and associated time value
            self.buttons.append((pygame.Rect(button_x, button_y, button_width, button_height), time))

    def display(self) -> int:
        # Create a game loop for the time limit selection screen
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True

        while running:
            # Handle events (quit and button clicks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any time limit button was clicked
                    for button, time in self.buttons:
                        if button.collidepoint(event.pos):
                            return time  # Return the selected time limit

            # Render the screen
            self.draw()
            pygame.display.flip()
            clock.tick(30)  # Limit to 30 FPS

        # Default return if loop exits unexpectedly
        return 0

    def draw(self) -> None:
        # Fill background with light gray
        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw title at the top of the screen
        title_text: str = "Select Game Time Limit"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_surface, title_rect)

        # Get current mouse position for hover effects
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

        # Draw each time limit button
        for button, time in self.buttons:
            # Change button color if mouse is hovering over it
            button_color: Tuple[int, int, int] = self.BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else self.BUTTON_COLOR

            # Draw button with rounded corners
            pygame.draw.rect(self.screen, button_color, button, border_radius=10)
            pygame.draw.rect(self.screen, (30, 100, 30), button, 2, border_radius=10)  # Add border

            # Format text based on time value
            if time == 0:
                button_text: str = "No Time Limit"
            else:
                button_text: str = f"{time} Minutes"

            # Render and center the text on the button
            text_surface: pygame.Surface = self.button_font.render(button_text, True, (255, 255, 255))
            text_rect: pygame.Rect = text_surface.get_rect(center=button.center)
            self.screen.blit(text_surface, text_rect)
