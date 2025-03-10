import pygame
from typing import List, Tuple
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.enums.game_token import GameToken
from temp_frontend.text_utils import draw_text

def draw_player_display(screen: pygame.Surface, players: List[Tuple[str, GameToken]], x: int, y: int, width: int = 300, height: int = 400) -> None:
    """
    Draw a component displaying all players and their game tokens.
    
    Args:
        screen: The pygame surface to draw on
        players: List of tuples containing (player_name, game_token)
        x: X position of the component
        y: Y position of the component
        width: Width of the component
        height: Height of the component
    """
    # Colors
    PANEL_BG_COLOR = (240, 240, 240)  # Light gray
    HEADER_BG_COLOR = (70, 130, 70)   # Green to match buttons
    HEADER_TEXT_COLOR = (255, 255, 255)  # White
    PLAYER_BG_COLOR = (252, 252, 252)  # Almost white
    BORDER_COLOR = (30, 100, 30)  # Dark green
    PLAYER_NAME_COLOR = (0, 0, 0)  # Black
    TOKEN_TEXT_COLOR = (80, 80, 80)  # Dark gray
    
    # Draw background panel with stylish border
    panel_rect = pygame.Rect(x, y, width, height)
    # Draw shadow effect
    shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
    pygame.draw.rect(screen, (200, 200, 200, 150), shadow_rect, border_radius=12)
    # Draw main panel
    pygame.draw.rect(screen, PANEL_BG_COLOR, panel_rect, border_radius=10)
    # Draw decorative border
    pygame.draw.rect(screen, BORDER_COLOR, panel_rect, 3, border_radius=10)
    
    # Draw header
    header_rect = pygame.Rect(x, y, width, 45)
    pygame.draw.rect(screen, HEADER_BG_COLOR, header_rect, border_radius=10)
    # Only round the top corners of the header
    header_bottom_rect = pygame.Rect(x, y + 25, width, 20)
    pygame.draw.rect(screen, HEADER_BG_COLOR, header_bottom_rect)
    # Draw header border
    pygame.draw.rect(screen, BORDER_COLOR, header_rect, 2, border_radius=10)
    
    # Draw "PLAYERS" header text
    font_size = 24
    draw_text(screen, "PLAYERS", (x + width // 2, y + 22), color=HEADER_TEXT_COLOR, font_size=font_size, center=True, bold=True)
    
    # Draw each player
    player_height = 70  # Increased height for more space
    for i, (player_name, token) in enumerate(players):
        player_y = y + 55 + i * player_height
        
        # Player background with subtle gradient effect
        player_rect = pygame.Rect(x + 10, player_y, width - 20, player_height - 10)
        pygame.draw.rect(screen, PLAYER_BG_COLOR, player_rect, border_radius=8)
        
        # Add highlight effect to the top of each player card
        highlight_rect = pygame.Rect(x + 10, player_y, width - 20, 5)
        pygame.draw.rect(screen, (255, 255, 255), highlight_rect, border_radius=8)
        
        # Draw player card border
        pygame.draw.rect(screen, BORDER_COLOR, player_rect, 2, border_radius=8)
        
        # Draw player name - bold and same size as header (24)
        draw_text(screen, player_name, (x + 20, player_y + player_height//2 - 20), 
                 color=PLAYER_NAME_COLOR, font_size=font_size, bold=True)
        
        # Draw token name
        token_text = f"Token: {token.value}"
        draw_text(screen, token_text, (x + 20, player_y + player_height//2 + 15), 
                 color=TOKEN_TEXT_COLOR, font_size=16)
        
        # Draw colored circle representing token (simple visual representation)
        token_colors = {
            "boot": (139, 69, 19),      # Brown
            "smartphone": (0, 0, 255),  # Blue
            "ship": (0, 128, 128),      # Teal
            "hatstand": (128, 0, 128),  # Purple
            "cat": (255, 165, 0),       # Orange
            "iron": (169, 169, 169)     # Gray
        }
        
        color = token_colors.get(token.value, (0, 0, 0))
        # Create a glow effect for the token
        for r in range(3, 0, -1):
            glow_alpha = 100 - r * 30
            glow_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*color, glow_alpha), (20, 20), 15 + r)
            screen.blit(glow_surface, (x + width - 50, player_y + player_height//2 - 20))
        
        # Draw token circle
        pygame.draw.circle(screen, color, (x + width - 30, player_y + player_height//2), 15)
        pygame.draw.circle(screen, (0, 0, 0), (x + width - 30, player_y + player_height//2), 15, 2)  # Border 