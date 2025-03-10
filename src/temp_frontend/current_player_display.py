import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.property_owners.player import Player
from temp_frontend.text_utils import draw_text

def draw_current_player_display(screen, current_player, x, y, width, height):
    """
    Draw a component displaying the current player's information and game controls.
    
    Args:
        screen: The pygame surface to draw on
        current_player: The current Player object
        x: X position of the component
        y: Y position of the component
        width: Width of the component
        height: Height of the component
    """
    # Colors
    PANEL_BG_COLOR = (220, 240, 220)  # Light green
    HEADER_BG_COLOR = (50, 120, 50)   # Darker green for header
    HEADER_TEXT_COLOR = (255, 255, 255)  # White
    BORDER_COLOR = (30, 100, 30)  # Dark green
    MONEY_COLOR = (0, 100, 0)  # Dark green for money
    HIGHLIGHT_COLOR = (255, 215, 0)  # Gold for highlighting
    
    # Draw panel with shadow
    shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
    pygame.draw.rect(screen, (200, 200, 200, 150), shadow_rect, border_radius=12)
    
    # Main panel
    panel_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, PANEL_BG_COLOR, panel_rect, border_radius=10)
    pygame.draw.rect(screen, BORDER_COLOR, panel_rect, 3, border_radius=10)
    
    # Header
    header_rect = pygame.Rect(x, y, width, 40)
    pygame.draw.rect(screen, HEADER_BG_COLOR, header_rect, border_radius=10)
    # Only round the top corners
    header_bottom_rect = pygame.Rect(x, y + 20, width, 20)
    pygame.draw.rect(screen, HEADER_BG_COLOR, header_bottom_rect)
    
    # Draw border for header
    pygame.draw.rect(screen, BORDER_COLOR, header_rect, 2, border_radius=10)
    
    # Draw "CURRENT TURN" text
    font_size = 24
    draw_text(screen, "CURRENT TURN", (x + width // 2, y + 20), 
            color=HEADER_TEXT_COLOR, font_size=font_size, center=True, bold=True)
    
    # If there's no current player, show a message
    if not current_player:
        draw_text(screen, "Waiting for game to start...", 
                 (x + width // 2, y + height // 2), 
                color=(100, 100, 100), font_size=18, center=True)
        return
    
    # Draw player name with decorative elements
    name_y = y + 60
    name = current_player.get_name()
    
    # Create a decorative background for the player name
    name_bg_rect = pygame.Rect(x + 10, name_y - 10, width - 20, 40)
    pygame.draw.rect(screen, (240, 255, 240), name_bg_rect, border_radius=8)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, name_bg_rect, 2, border_radius=8)
    
    # Draw player name with larger font
    draw_text(screen, name, (x + width // 2, name_y + 10), 
             color=(0, 0, 0), font_size=28, center=True, bold=True)
    
    # Draw cash balance with money symbol
    balance_y = y + 110
    cash_balance = current_player.get_cash_balance()
    cash_text = f"£{cash_balance:,}"
    
    # Create a decorative background for the cash balance
    balance_bg_rect = pygame.Rect(x + 30, balance_y - 5, width - 60, 30)
    pygame.draw.rect(screen, (235, 250, 235), balance_bg_rect, border_radius=5)
    pygame.draw.rect(screen, (200, 230, 200), balance_bg_rect, 1, border_radius=5)
    
    # Draw cash balance with money symbol
    draw_text(screen, cash_text, (x + width // 2, balance_y + 10), 
             color=MONEY_COLOR, font_size=22, center=True, bold=True)
    
    # Add a small instruction at the bottom
    instruction_y = y + height - 25
    draw_text(screen, "Press SPACE to advance turn", 
             (x + width // 2, instruction_y), 
             color=(80, 80, 80), font_size=14, center=True, bold=False) 