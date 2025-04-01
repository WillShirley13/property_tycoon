import pygame
from typing import Tuple, Optional


class InsufficientFundsPopup:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        screen: pygame.Surface,
        player_name: str,
    ):
        """
        Initialize the insufficient funds popup.

        Args:
            screen: Main game screen to draw the popup on.
            width: Width of the popup.
            height: Height of the popup.
            player_name: Name of the player who has insufficient funds.
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.player_name = player_name

        # Center the popup on the screen
        self.x = (screen.get_width() - width) // 2
        self.y = (screen.get_height() - height) // 2

        # Define color scheme
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (240, 240, 240)
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (0, 0, 0)

        # Define font sizes
        title_size: int = 20
        detail_size: int = 16

        # Initialize fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", title_size, bold=True)
            self.detail_font: pygame.font.Font = pygame.font.SysFont("Arial", detail_size)
        except:
            self.title_font = pygame.font.SysFont(None, title_size + 4, bold=True)
            self.detail_font = pygame.font.SysFont(None, detail_size + 2)

        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface((self.width, self.height))

    def draw(self) -> None:
        """
        Draw the insufficient funds popup with the error message.
        """
        # Clear the popup surface
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw rounded border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )

        # --- Title ---
        title_text: str = "Insufficient Funds"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # --- Message ---
        # Split message at the full stop
        message_lines = [
            f"{self.player_name} does not have enough money to purchase this property.",
            "Moving to auction!",
        ]

        # Render and position each line
        line_spacing = 5  # Space between lines
        start_y = self.height // 2 - (self.detail_font.get_height() + line_spacing)

        for i, line in enumerate(message_lines):
            message_surface = self.detail_font.render(line, True, self.POPUP_TEXT_COLOR)
            message_rect = message_surface.get_rect(
                center=(
                    self.width // 2,
                    start_y + i * (self.detail_font.get_height() + line_spacing),
                )
            )
            self.popup_surface.blit(message_surface, message_rect)

        # Display the popup on the main screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    def show(self) -> None:
        """
        Display the insufficient funds popup and wait for a short time before closing.
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            # Draw the popup
            self.draw()

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Wait for 3 seconds before closing
            pygame.time.wait(3000)
            running = False

            # Cap the frame rate
            clock.tick(60)
