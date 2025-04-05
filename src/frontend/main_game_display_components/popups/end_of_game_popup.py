from typing import Optional, Tuple

import pygame


class EndOfGamePopup:
    def __init__(self, x: int, y: int, width: int,
                 height: int, screen: pygame.Surface, winner):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.winner = winner
        self.surface = pygame.Surface((width, height))

        # Define color scheme for the popup
        self.BG_COLOR = (240, 240, 240)  # Light gray
        self.BORDER_COLOR = (0, 0, 0)  # Black
        self.TEXT_COLOR = (0, 0, 0)  # Black
        self.TITLE_COLOR = (50, 120, 50)  # Dark green
        self.BUTTON_COLOR = (0, 100, 0) # Dark green
        self.BUTTON_HOVER_COLOR = (100, 200, 100)  # Darker green
        self.BUTTON_TEXT_COLOR = (0, 0, 0)  # Black

        # Set fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", 36, bold=True)
            self.subtitle_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", 28, bold=True)
            self.details_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", 20)
            self.button_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", 24, bold=True)
        except BaseException:
            self.title_font = pygame.font.SysFont(None, 36, bold=True)
            self.subtitle_font = pygame.font.SysFont(
                None, 28, bold=True)
            self.details_font = pygame.font.SysFont(None, 20)
            self.button_font = pygame.font.SysFont(
                None, 24, bold=True)

        # Configure button layout
        self.button_width = 200
        self.button_height = 50
        self.close_button = pygame.Rect(
            (self.width - self.button_width) // 2,
            self.height - 80,
            self.button_width,
            self.button_height,
        )

        # Initialise hover state for button
        self.button_hover = False

    def draw(self) -> None:
        # Fill background
        self.surface.fill(self.BG_COLOR)

        # Draw border
        pygame.draw.rect(self.surface, self.BORDER_COLOR,
                         (0, 0, self.width, self.height), 3, 10)

        # Draw title
        title_text = "Game Over!"
        title_surface = self.title_font.render(
            title_text, True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(
            center=(self.width // 2, 50))
        self.surface.blit(title_surface, title_rect)

        # Draw winner text
        winner_text = f"The winner is {self.winner.get_name()}!"
        winner_surface = self.subtitle_font.render(
            winner_text, True, self.TEXT_COLOR)
        winner_rect = winner_surface.get_rect(
            center=(self.width // 2, 100))
        self.surface.blit(winner_surface, winner_rect)

        # Draw player stats
        y_pos = 150
        details = [
            f"Cash: £{self.winner.get_cash_balance()}",
            f"Net Worth: £{self.winner.get_player_net_worth()}",
            f"Properties Owned: {
                sum(
                    len(properties) for properties in self.winner.get_owned_properties().values())}",
        ]

        for detail in details:
            detail_surface = self.details_font.render(
                detail, True, self.TEXT_COLOR)
            detail_rect = detail_surface.get_rect(
                center=(self.width // 2, y_pos))
            self.surface.blit(detail_surface, detail_rect)
            y_pos += 35

        # Draw congrats message
        congrats_text = "Congratulations on becoming the Property Tycoon!"
        congrats_surface = self.subtitle_font.render(
            congrats_text, True, self.TITLE_COLOR)
        congrats_rect = congrats_surface.get_rect(
            center=(self.width // 2, y_pos + 20))
        self.surface.blit(congrats_surface, congrats_rect)

        # Check for button hover
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y)
        self.button_hover = self.close_button.collidepoint(
            relative_mouse_pos)

        # Draw close button with hover effect
        button_color = self.BUTTON_HOVER_COLOR if self.button_hover else self.BUTTON_COLOR
        pygame.draw.rect(
            self.surface,
            button_color,
            self.close_button,
            0,
            10)
        pygame.draw.rect(
            self.surface,
            self.BORDER_COLOR,
            self.close_button,
            2,
            10)

        # Add button text
        button_text = "Exit Game"
        button_text_surface = self.button_font.render(
            button_text, True, self.BUTTON_TEXT_COLOR)
        button_text_rect = button_text_surface.get_rect(
            center=self.close_button.center)
        self.surface.blit(button_text_surface, button_text_rect)

        # Display popup on the screen
        self.screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            mouse_pos = pygame.mouse.get_pos()
            relative_mouse_pos = (
                mouse_pos[0] - self.x,
                mouse_pos[1] - self.y)
            self.button_hover = self.close_button.collidepoint(
                relative_mouse_pos)
            self.draw()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            relative_mouse_pos = (
                mouse_pos[0] - self.x,
                mouse_pos[1] - self.y)

            if self.close_button.collidepoint(relative_mouse_pos):
                print("End game popup: Exit button clicked")
                return True  # Signal to exit the game

        return False  # Continue showing the popup
