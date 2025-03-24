import pygame
from typing import List, Tuple, Dict

from backend.enums.game_token import GameToken
from frontend.helpers.board_text_utils import draw_text


class PlayerDisplay:
    # Initialize the player list display component
    def __init__(
        self,
        x: int,
        y: int,
        screen: pygame.Surface,
        width: int = 300,
        height: int = 420,
    ):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen

        # Colors for styling the player panel
        self.PANEL_BG_COLOR: Tuple[int, int, int] = (240, 240, 240)  # Light gray
        self.HEADER_BG_COLOR: Tuple[int, int, int] = (
            70,
            130,
            70,
        )  # Green to match buttons
        self.HEADER_TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # White
        self.PLAYER_BG_COLOR: Tuple[int, int, int] = (252, 252, 252)  # Almost white
        self.BORDER_COLOR: Tuple[int, int, int] = (30, 100, 30)  # Dark green
        self.PLAYER_NAME_COLOR: Tuple[int, int, int] = (0, 0, 0)  # Black
        self.TOKEN_TEXT_COLOR: Tuple[int, int, int] = (80, 80, 80)  # Dark gray

        # Color mapping for different game tokens
        self.token_colors: Dict[GameToken, Tuple[int, int, int]] = {
            GameToken.BOOT: (139, 69, 19),  # Brown
            GameToken.SMARTPHONE: (0, 0, 255),  # Blue
            GameToken.BOAT: (0, 128, 128),  # Teal
            GameToken.TOPHAT: (128, 0, 128),  # Purple
            GameToken.CAT: (255, 165, 0),  # Orange
            GameToken.IRON: (169, 169, 169),  # Gray
        }

        # Create rectangles for reuse in drawing operations
        self.panel_rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.shadow_rect: pygame.Rect = pygame.Rect(x + 5, y + 5, width, height)
        self.header_rect: pygame.Rect = pygame.Rect(x, y, width, 45)
        self.header_bottom_rect: pygame.Rect = pygame.Rect(x, y + 25, width, 20)

        # Initialize fonts for text rendering
        self.header_font: pygame.font.Font = pygame.font.SysFont("Arial", 24, bold=True)
        self.player_font: pygame.font.Font = pygame.font.SysFont("Arial", 18)
        self.token_font: pygame.font.Font = pygame.font.SysFont("Arial", 14)

    # Draw the player list with all players and their tokens
    def draw(self, players: List[Tuple[str, GameToken]]) -> None:
        # Draw shadow effect for depth perception
        pygame.draw.rect(
            self.screen, (200, 200, 200, 150), self.shadow_rect, border_radius=12
        )

        # Draw main panel background
        pygame.draw.rect(
            self.screen, self.PANEL_BG_COLOR, self.panel_rect, border_radius=10
        )
        pygame.draw.rect(
            self.screen, self.BORDER_COLOR, self.panel_rect, 3, border_radius=10
        )

        # Draw header section with title
        pygame.draw.rect(
            self.screen, self.HEADER_BG_COLOR, self.header_rect, border_radius=10
        )
        pygame.draw.rect(self.screen, self.HEADER_BG_COLOR, self.header_bottom_rect)
        pygame.draw.rect(
            self.screen, self.BORDER_COLOR, self.header_rect, 2, border_radius=10
        )

        # Draw header text
        header_text: str = "Players"
        header_surface: pygame.Surface = self.header_font.render(
            header_text, True, self.HEADER_TEXT_COLOR
        )
        header_text_rect: pygame.Rect = header_surface.get_rect(
            center=(self.x + self.width // 2, self.y + 22)
        )
        self.screen.blit(header_surface, header_text_rect)

        # Draw each player card
        player_height: int = 70  # Height of each player card
        for i, (player_name, token) in enumerate(players):
            player_y: int = self.y + 55 + i * player_height

            # Player background with subtle gradient effect
            player_rect: pygame.Rect = pygame.Rect(
                self.x + 10, player_y, self.width - 20, player_height - 2
            )
            pygame.draw.rect(
                self.screen, self.PLAYER_BG_COLOR, player_rect, border_radius=8
            )

            # Add highlight effect to the top of each player card
            highlight_rect: pygame.Rect = pygame.Rect(
                self.x + 10, player_y, self.width - 20, 5
            )
            pygame.draw.rect(
                self.screen, (255, 255, 255), highlight_rect, border_radius=8
            )

            # Draw player card border
            pygame.draw.rect(
                self.screen, self.BORDER_COLOR, player_rect, 2, border_radius=8
            )

            # Draw player name - bold and same size as header (24)
            draw_text(
                self.screen,
                player_name,
                (self.x + 20, player_y + player_height // 2 - 20),
                color=self.PLAYER_NAME_COLOR,
                font_size=24,
                bold=True,
            )

            # Draw token name
            token_text: str = f"Token: {token.name}"
            draw_text(
                self.screen,
                token_text,
                (self.x + 20, player_y + player_height // 2 + 10),
                color=self.TOKEN_TEXT_COLOR,
                font_size=16,
            )
