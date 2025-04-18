import os
import sys
from typing import Optional, Tuple

import pygame

from backend.property_owners.player import Player
from frontend.helpers.board_text_utils import draw_text


class CurrentPlayerDisplay:
    # Initialize the current player display component
    def __init__(
        self,
        x: int,
        y: int,
        screen: pygame.Surface,
        width: int,
        height: int,
    ):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        
        # Colors for styling the menu
        self.PANEL_BG_COLOR: Tuple[int, int, int] = (
            240, 240, 240)  # Light gray
        self.HEADER_BG_COLOR: Tuple[int, int, int] = (
            3, 26, 158)  # Royal blue
        self.HEADER_TEXT_COLOR: Tuple[int, int, int] = (
            153, 204, 255)  # Light blue
        self.BORDER_COLOR: Tuple[int, int, int] = (
            3, 26, 158)  # Royal blue
        self.MONEY_COLOR: Tuple[int, int, int] = (
            153, 204, 255)  # Light blue
        self.HIGHLIGHT_COLOR: Tuple[int, int, int] = (
            255, 255, 255)  # White

        self.panel_rect: pygame.Rect = pygame.Rect(
            x, y, width, height)
        self.shadow_rect: pygame.Rect = pygame.Rect(
            x + 5, y + 5, width, height)
        self.header_rect: pygame.Rect = pygame.Rect(x, y, width, 40)
        self.header_bottom_rect: pygame.Rect = pygame.Rect(
            x, y + 20, width, 20)

        # Font configurations for different text elements
        self.header_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 24, bold=True)
        self.name_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 28, bold=True)
        self.money_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 22, bold=True)
        self.instruction_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 14)

    # Draw the current player panel with player information
    def draw(self, current_player: Optional[Player]) -> None:
        # Draw shadow effect for 3D appearance
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

        # Draw header with title
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

        # Draw "CURRENT TURN" text in header
        header_text: str = "Current Player"
        header_surface: pygame.Surface = self.header_font.render(
            header_text, True, self.HEADER_TEXT_COLOR)
        header_text_rect: pygame.Rect = header_surface.get_rect(
            center=(self.x + self.width // 2, self.y + 20))
        self.screen.blit(header_surface, header_text_rect)
        
        # Draw player name with decorative background
        name_y: int = self.y + 60
        name: str = current_player.get_name()

        # Create background for the player name
        name_bg_rect: pygame.Rect = pygame.Rect(
            self.x + 10, name_y - 10, self.width - 20, 40)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         name_bg_rect, border_radius=8)
        pygame.draw.rect(
            self.screen,
            self.BORDER_COLOR,
            name_bg_rect,
            2,
            border_radius=8)

        # Render player name centered in its background
        name_surface: pygame.Surface = self.name_font.render(
            name, True, self.HEADER_TEXT_COLOR)
        name_rect: pygame.Rect = name_surface.get_rect(
            center=(self.x + self.width // 2, name_y + 10))
        self.screen.blit(name_surface, name_rect)

        # Draw cash balance with money symbol
        balance_y: int = self.y + 110
        cash_balance: int = current_player.get_cash_balance()
        cash_text: str = f"£{cash_balance:,}"

        # Create background for the cash balance
        balance_bg_rect: pygame.Rect = pygame.Rect(
            self.x + 30, balance_y - 5, self.width - 60, 30)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         balance_bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.BORDER_COLOR,
                         balance_bg_rect, 1, border_radius=5)

        # Render cash balance centered in its background
        money_surface: pygame.Surface = self.money_font.render(
            cash_text, True, self.MONEY_COLOR)
        money_rect: pygame.Rect = money_surface.get_rect(
            center=(self.x + self.width // 2, balance_y + 10))
        self.screen.blit(money_surface, money_rect)
