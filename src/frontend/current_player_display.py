import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.property_owners.player import Player
from frontend.board_text_utils import draw_text

class CurrentPlayerDisplay:
    def __init__(self, x, y, width=300, height=130):
        """
        Initialize the current player display component.
        
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
        self.PANEL_BG_COLOR = (220, 240, 220)  # Light green
        self.HEADER_BG_COLOR = (50, 120, 50)   # Darker green for header
        self.HEADER_TEXT_COLOR = (255, 255, 255)  # White
        self.BORDER_COLOR = (30, 100, 30)  # Dark green
        self.MONEY_COLOR = (0, 100, 0)  # Dark green for money
        self.HIGHLIGHT_COLOR = (255, 215, 0)  # Gold for highlighting
        
        # Create rectangles for reuse
        self.panel_rect = pygame.Rect(x, y, width, height)
        self.shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
        self.header_rect = pygame.Rect(x, y, width, 40)
        self.header_bottom_rect = pygame.Rect(x, y + 20, width, 20)
        
        # Fonts
        self.header_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.name_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.money_font = pygame.font.SysFont('Arial', 22, bold=True)
        self.instruction_font = pygame.font.SysFont('Arial', 14)
    
    def draw(self, screen, current_player):
        """
        Draw the current player display component.
        
        Args:
            screen: The pygame surface to draw on
            current_player: The current Player object
        """
        # Draw shadow effect
        pygame.draw.rect(screen, (200, 200, 200, 150), self.shadow_rect, border_radius=12)
        
        # Main panel
        pygame.draw.rect(screen, self.PANEL_BG_COLOR, self.panel_rect, border_radius=10)
        pygame.draw.rect(screen, self.BORDER_COLOR, self.panel_rect, 3, border_radius=10)
        
        # Header
        pygame.draw.rect(screen, self.HEADER_BG_COLOR, self.header_rect, border_radius=10)
        pygame.draw.rect(screen, self.HEADER_BG_COLOR, self.header_bottom_rect)
        pygame.draw.rect(screen, self.BORDER_COLOR, self.header_rect, 2, border_radius=10)
        
        # Draw "CURRENT TURN" text
        header_text = "CURRENT TURN"
        header_surface = self.header_font.render(header_text, True, self.HEADER_TEXT_COLOR)
        header_text_rect = header_surface.get_rect(center=(self.x + self.width // 2, self.y + 20))
        screen.blit(header_surface, header_text_rect)
        
        # If there's no current player, show a message
        if not current_player:
            waiting_text = "Waiting for game to start..."
            waiting_surface = self.instruction_font.render(waiting_text, True, (100, 100, 100))
            waiting_rect = waiting_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(waiting_surface, waiting_rect)
            return
        
        # Draw player name with decorative elements
        name_y = self.y + 60
        name = current_player.get_name()
        
        # Create a decorative background for the player name
        name_bg_rect = pygame.Rect(self.x + 10, name_y - 10, self.width - 20, 40)
        pygame.draw.rect(screen, (240, 255, 240), name_bg_rect, border_radius=8)
        pygame.draw.rect(screen, self.HIGHLIGHT_COLOR, name_bg_rect, 2, border_radius=8)
        
        # Draw player name
        name_surface = self.name_font.render(name, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(self.x + self.width // 2, name_y + 10))
        screen.blit(name_surface, name_rect)
        
        # Draw cash balance with money symbol
        balance_y = self.y + 110
        cash_balance = current_player.get_cash_balance()
        cash_text = f"£{cash_balance:,}"
        
        # Create a decorative background for the cash balance
        balance_bg_rect = pygame.Rect(self.x + 30, balance_y - 5, self.width - 60, 30)
        pygame.draw.rect(screen, (235, 250, 235), balance_bg_rect, border_radius=5)
        pygame.draw.rect(screen, (200, 230, 200), balance_bg_rect, 1, border_radius=5)
        
        # Draw cash balance
        money_surface = self.money_font.render(cash_text, True, self.MONEY_COLOR)
        money_rect = money_surface.get_rect(center=(self.x + self.width // 2, balance_y + 10))
        screen.blit(money_surface, money_rect)
        