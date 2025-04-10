import time
import os
import sys
from typing import Dict, List, Optional, Tuple

import pygame

from frontend.helpers.board_text_utils import draw_text
from frontend.main_game_display_components.popups.end_of_game_popup import \
    EndOfGamePopup

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art_assets")

class GameMenuDisplay:
    def __init__(
        self,
        x: int,
        y: int,
        screen: pygame.Surface,
        width: int,
        height: int,
        time_limit: int,
    ):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        self.time_limit: int = time_limit
        self.start_time: Optional[float] = None
        self.time_remaining: Optional[int] = None

        # Time limit display colors
        self.TIME_BG_COLOR: Tuple[int, int, int] = (
            240, 240, 240)  # Light gray
        self.TIME_BORDER_COLOR: Tuple[int, int, int] = (
            3, 26, 158)  # Dark green
        self.TIME_TEXT_COLOR: Tuple[int,
                                    int, int] = (0, 0, 0)  # Black
        self.TIME_WARNING_COLOR: Tuple[int, int, int] = (
            200, 0, 0)  # Red for low time

        # Define menu button identifiers
        self.GAME_RULES_BUTTON = "Game Rules"
        self.SAVE_GAME_BUTTON = "Save Game"
        self.END_GAME_BUTTON = "End Game"

        # Colors for styling the menu
        self.PANEL_BG_COLOR: Tuple[int, int, int] = (
            240, 240, 240)  # Light gray
        self.HEADER_BG_COLOR: Tuple[int, int, int] = (
            3, 26, 158)  # Royal blue
        self.HEADER_TEXT_COLOR: Tuple[int, int, int] = (
            255, 255, 255)  # White
        self.BORDER_COLOR: Tuple[int, int, int] = (
            3, 26, 158)  # Royal blue
        self.BUTTON_BG_COLOR: Tuple[int, int, int] = (
            153, 204, 255)  # Light blue
        self.BUTTON_TEXT_COLOR: Tuple[int, int, int] = (
            255, 255, 255)  # White
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            110, 10, 61)  # Dark blue

        # create rectangles for reuse in rendering
        self.panel_rect: pygame.Rect = pygame.Rect(
            x, y, width, height)
        self.shadow_rect: pygame.Rect = pygame.Rect(
            x + 5, y + 5, width, height)
        self.header_rect: pygame.Rect = pygame.Rect(x, y, width, 45)
        self.header_bottom_rect: pygame.Rect = pygame.Rect(
            x, y + 25, width, 20)

        # set fonts
        self.header_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 24, bold=True)
        self.button_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 18, bold=True)
        self.timer_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 20, bold=True)

        # Button layout
        self.button_height: int = 50
        self.button_spacing: int = 10

        # Time display rectangle
        self.time_display_rect: pygame.Rect = pygame.Rect(
            x + 20,
            y + 60 + 3 * (self.button_height + self.button_spacing),
            width - 40,
            50,
        )

        self.buttons: List[Dict] = [
            {
                "text": self.GAME_RULES_BUTTON,
                "rect": pygame.Rect(x + 20, y + 60, width - 40, self.button_height),
            },
            {
                "text": self.SAVE_GAME_BUTTON,
                "rect": pygame.Rect(
                    x + 20,
                    y + 60 + (self.button_height
                              + self.button_spacing),
                    width - 40,
                    self.button_height,
                ),
            },
            {
                "text": self.END_GAME_BUTTON,
                "rect": pygame.Rect(
                    x + 20,
                    y + 60 + 2 * (self.button_height
                                  + self.button_spacing),
                    width - 40,
                    self.button_height,
                ),
            },
        ]

        # Hover state tracking
        self.hovered_button: Optional[int] = None

        # Rules display state and image
        self.showing_rules: bool = False
        self.rules_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "game_rules.png")).convert_alpha()
        self.rules_image = pygame.transform.scale(
            self.rules_image,
            (self.screen.get_width() * 0.7,
             self.screen.get_height() * 0.7),
        )

    # Start the game timer if a time limit is set
    def start_timer(self) -> None:
        if self.time_limit > 0:
            self.start_time = time.time()
            self.time_remaining = self.time_limit * \
                60  # Convert minutes to seconds

    # Update the timer and return True if time is up, False otherwise
    def update_timer(self) -> bool:
        if self.time_limit <= 0 or self.start_time is None:
            return False

        elapsed = time.time() - self.start_time
        self.time_remaining = max(
            0, int(self.time_limit * 60 - elapsed))

        # Return True if time is up
        return self.time_remaining <= 0

    # Check if mouse is hovering over any menu buttons
    def check_hover(self, mouse_pos: Tuple[int, int]) -> None:
        for i, button in enumerate(self.buttons):
            if button["rect"].collidepoint(mouse_pos):
                self.hovered_button = i
                return
        self.hovered_button = None

    # handle button clicks and return the identifier of the clicked
    # button
    def handle_click(
            self, mouse_pos: Tuple[int, int], players: List[str]) -> Optional[str]:
        # check game rules button
        if self.buttons[0]["rect"].collidepoint(mouse_pos):
            print(f"Button clicked: {self.GAME_RULES_BUTTON}")
            self.showing_rules = True
            return self.GAME_RULES_BUTTON

        # Check Save Game button
        elif self.buttons[1]["rect"].collidepoint(mouse_pos):
            print(f"Button clicked: {self.SAVE_GAME_BUTTON}")
            return self.SAVE_GAME_BUTTON

        # Check End Game button
        elif self.buttons[2]["rect"].collidepoint(mouse_pos):
            print(f"Button clicked: {self.END_GAME_BUTTON}")
            # identify the winner
            winner = max(
                players, key=lambda x: x.get_player_net_worth())
            print(f"Winner: {winner}")
            # Create and show end of game popup
            end_popup = EndOfGamePopup(
                0,
                0,
                self.screen.get_width(),
                self.screen.get_height(),
                self.screen,
                winner,
            )
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    end_popup.handle_event(event)
                end_popup.draw()
                pygame.display.flip()
            return self.END_GAME_BUTTON

        # If we're showing rules and clicked anywhere else, hide them
        elif self.showing_rules:
            self.showing_rules = False

        # No button was clicked
        return None

    # Draw the game menu with all buttons and optional rules image
    def draw(
            self, mouse_pos: Optional[Tuple[int, int]] = None) -> None:
        # Update hover state if mouse position is provided
        if mouse_pos:
            self.check_hover(mouse_pos)

        pygame.draw.rect(self.screen, (200, 200, 200, 150),
                         self.shadow_rect, border_radius=12)

        # Draw main panel background
        pygame.draw.rect(
            self.screen,
            self.PANEL_BG_COLOR,
            self.panel_rect,
            border_radius=10)
        pygame.draw.rect(
            self.screen,
            self.BORDER_COLOR,
            self.panel_rect,
            3,
            border_radius=10)

        # Draw title
        pygame.draw.rect(
            self.screen,
            self.HEADER_BG_COLOR,
            self.header_rect,
            border_radius=10)
        pygame.draw.rect(
            self.screen,
            self.HEADER_BG_COLOR,
            self.header_bottom_rect)
        pygame.draw.rect(
            self.screen,
            self.BORDER_COLOR,
            self.header_rect,
            2,
            border_radius=10)

        # Draw header text
        header_text: str = "Menu"
        header_surface: pygame.Surface = self.header_font.render(
            header_text, True, self.HEADER_TEXT_COLOR)
        header_text_rect: pygame.Rect = header_surface.get_rect(
            center=(self.x + self.width // 2, self.y + 22))
        self.screen.blit(header_surface, header_text_rect)

        # Draw each menu button with hover effect
        for i, button in enumerate(self.buttons):
            # Determine button color based on hover state
            button_color = self.BUTTON_HOVER_COLOR if i == self.hovered_button else self.BUTTON_BG_COLOR

            # Draw button with rounded corners
            pygame.draw.rect(
                self.screen,
                button_color,
                button["rect"],
                border_radius=8)
            pygame.draw.rect(
                self.screen,
                self.BORDER_COLOR,
                button["rect"],
                2,
                border_radius=8)

            # Draw button text
            button_text: pygame.Surface = self.button_font.render(
                button["text"], True, self.BUTTON_TEXT_COLOR)
            button_text_rect: pygame.Rect = button_text.get_rect(
                center=button["rect"].center)
            self.screen.blit(button_text, button_text_rect)

        # Draw time limit countdown if a time limit is set
        if self.time_limit > 0 and self.time_remaining is not None:
            # Draw the time display rectangle using
            # self.time_display_rect
            pygame.draw.rect(
                self.screen,
                self.TIME_BG_COLOR,
                self.time_display_rect,
                border_radius=8)
            pygame.draw.rect(
                self.screen,
                self.TIME_BORDER_COLOR,
                self.time_display_rect,
                2,
                border_radius=8,
            )

            # Format time remaining as MM:SS
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            time_text = f"Time: {minutes:02d}:{seconds:02d}"

            # Choose text color based on time remaining (red if less than 1
            # minute)
            text_color = self.TIME_WARNING_COLOR if self.time_remaining < 60 else self.TIME_TEXT_COLOR

            # Render and center text
            timer_surface = self.timer_font.render(
                time_text, True, text_color)
            timer_rect = timer_surface.get_rect(
                center=self.time_display_rect.center)
            self.screen.blit(timer_surface, timer_rect)

        # Display game rules image when requested
        if self.showing_rules:
            # Center the rules image on screen
            x = self.screen.get_width() // 2 - self.rules_image.get_width() // 2
            y = self.screen.get_height() // 2 - self.rules_image.get_height() // 2
            self.screen.blit(self.rules_image, (x, y))
