import pygame
from typing import List, Tuple
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.enums.game_token import GameToken
from temp_frontend.text_utils import draw_text

class PlayerDisplay:
    def __init__(self, x: int, y: int, width: int = 300, height: int = 420):
        """
        Initialize the player display component.
        
        Args:
            x: X position of the component
            y: Y position of the component
            width: Width of the component
            height: Height of the component
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Colors
        self.PANEL_BG_COLOR = (240, 240, 240)  # Light gray
        self.HEADER_BG_COLOR = (70, 130, 70)   # Green to match buttons
        self.HEADER_TEXT_COLOR = (255, 255, 255)  # White
        self.PLAYER_BG_COLOR = (252, 252, 252)  # Almost white
        self.BORDER_COLOR = (30, 100, 30)  # Dark green
        self.PLAYER_NAME_COLOR = (0, 0, 0)  # Black
        self.TOKEN_TEXT_COLOR = (80, 80, 80)  # Dark gray
        
        # Create rectangles for reuse
        self.panel_rect = pygame.Rect(x, y, width, height)
        self.shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
        self.header_rect = pygame.Rect(x, y, width, 45)
        self.header_bottom_rect = pygame.Rect(x, y + 25, width, 20)
        
        # Fonts
        self.header_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.player_font = pygame.font.SysFont('Arial', 18)
        self.token_font = pygame.font.SysFont('Arial', 14)
    
    def draw(self, screen: pygame.Surface, players: List[Tuple[str, GameToken]]) -> None:
        """
        Draw the player display component.
        
        Args:
            screen: The pygame surface to draw on
            players: List of tuples containing (player_name, game_token)
        """
        # Draw shadow effect
        pygame.draw.rect(screen, (200, 200, 200, 150), self.shadow_rect, border_radius=12)
        
        # Draw main panel
        pygame.draw.rect(screen, self.PANEL_BG_COLOR, self.panel_rect, border_radius=10)
        pygame.draw.rect(screen, self.BORDER_COLOR, self.panel_rect, 3, border_radius=10)
        
        # Draw header
        pygame.draw.rect(screen, self.HEADER_BG_COLOR, self.header_rect, border_radius=10)
        pygame.draw.rect(screen, self.HEADER_BG_COLOR, self.header_bottom_rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, self.header_rect, 2, border_radius=10)
        
        # Draw header text
        header_text = "Players"
        header_surface = self.header_font.render(header_text, True, self.HEADER_TEXT_COLOR)
        header_text_rect = header_surface.get_rect(center=(self.x + self.width // 2, self.y + 22))
        screen.blit(header_surface, header_text_rect)
        
        # Draw each player
        player_height = 70  # Increased height for more space
        for i, (player_name, token) in enumerate(players):
            player_y = self.y + 55 + i * player_height
            
            # Player background with subtle gradient effect
            player_rect = pygame.Rect(self.x + 10, player_y, self.width - 20, player_height - 2)
            pygame.draw.rect(screen, self.PLAYER_BG_COLOR, player_rect, border_radius=8)
            
            # Add highlight effect to the top of each player card
            highlight_rect = pygame.Rect(self.x + 10, player_y, self.width - 20, 5)
            pygame.draw.rect(screen, (255, 255, 255), highlight_rect, border_radius=8)
            
            # Draw player card border
            pygame.draw.rect(screen, self.BORDER_COLOR, player_rect, 2, border_radius=8)
            
            # Draw player name - bold and same size as header (24)
            draw_text(screen, player_name, (self.x + 20, player_y + player_height//2 - 20), 
                    color=self.PLAYER_NAME_COLOR, font_size=24, bold=True)
            
            # Draw token name - use name attribute for consistency
            try:
                token_text = f"Token: {token.name}"
            except AttributeError:
                # Fallback to value if name doesn't exist
                token_text = f"Token: {token.value}"
                
            draw_text(screen, token_text, (self.x + 20, player_y + player_height//2 + 15), 
                    color=self.TOKEN_TEXT_COLOR, font_size=16)
            
            # Draw colored circle representing token (simple visual representation)
            token_colors = {
                "boot": (139, 69, 19),      # Brown
                "smartphone": (0, 0, 255),  # Blue
                "ship": (0, 128, 128),      # Teal
                "hatstand": (128, 0, 128),  # Purple
                "cat": (255, 165, 0),       # Orange
                "iron": (169, 169, 169),     # Gray
                "boat": (0, 0, 0)           # Black
            }
            
            # Get token identifier for color lookup
            try:
                token_id = token.value
            except AttributeError:
                token_id = token.name
                
            color = token_colors.get(token_id, (0, 0, 0))
            
            # Create a glow effect for the token
            for r in range(3, 0, -1):
                glow_alpha = 100 - r * 30
                glow_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*color, glow_alpha), (20, 20), 15 + r)
                screen.blit(glow_surface, (self.x + self.width - 50, player_y + player_height//2 - 20))
            
            # Draw token circle
            pygame.draw.circle(screen, color, (self.x + self.width - 30, player_y + player_height//2), 15)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.width - 30, player_y + player_height//2), 15, 2)  # Border 