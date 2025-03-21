import pygame
import sys
import os
from typing import Dict, List, Tuple, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.helpers.space_data import SPACE_NAMES, SPACE_COLORS, BOARD_CONFIG, PROPERTY_COLORS, SPACE_PROPERTY_GROUPS
from frontend.helpers.board_text_utils import render_text_for_space

class Board:
    def __init__(self, screen_width: int, screen_height: int):
        # Initialize board properties
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        
        # Board should occupy the specified percentage of the screen width
        self.board_width: int = int(screen_width * BOARD_CONFIG["board_width_percentage"])
        
        # Board height will be the same as width to make a square
        self.board_height: int = self.board_width
        
        # If the board height is too large for the screen, adjust it
        if self.board_height > screen_height * BOARD_CONFIG["max_height_percentage"]:
            self.board_height = int(screen_height * BOARD_CONFIG["max_height_percentage"])
            self.board_width = self.board_height
        
        # Calculate the position to center the board
        self.board_x: int = (screen_width - self.board_width) // 2
        self.board_y: int = (screen_height - self.board_height) // 2
        
        # Number of spaces on each side of the board (excluding corners)
        self.spaces_per_side: int = BOARD_CONFIG["spaces_per_side"]
        
        # Calculate space dimensions
        self.corner_size: int = int(self.board_width / BOARD_CONFIG["corner_size_divisor"])
        
        # Calculate the width of regular spaces
        # Each side has 9 regular spaces, and we need to fit them between the corners
        self.space_width: int = int((self.board_width - 2 * self.corner_size) / self.spaces_per_side)
        
        # Create the spaces
        self.spaces: List[pygame.Rect] = self._create_spaces()
        self.space_centers: Dict[int, Tuple[int, int]] = self.get_space_centers()
    
    def _create_spaces(self) -> List[pygame.Rect]:
        spaces: List[pygame.Rect] = []
        
        # Bottom-left corner (GO) - Space 0
        spaces.append(pygame.Rect(
            self.board_x, 
            self.board_y + self.board_height - self.corner_size,
            self.corner_size, 
            self.corner_size
        ))
        
        # Left side spaces (1-9) - from bottom to top
        for i in range(self.spaces_per_side):
            spaces.append(pygame.Rect(
                self.board_x,
                self.board_y + self.board_height - self.corner_size - (i + 1) * self.space_width,
                self.corner_size,
                self.space_width
            ))
        
        # Top-left corner (JAIL) - Space 10
        spaces.append(pygame.Rect(
            self.board_x,
            self.board_y,
            self.corner_size,
            self.corner_size
        ))
        
        # Top row spaces (11-19) - from left to right
        for i in range(self.spaces_per_side):
            spaces.append(pygame.Rect(
                self.board_x + self.corner_size + i * self.space_width,
                self.board_y,
                self.space_width,
                self.corner_size
            ))
        
        # Top-right corner (FREE PARKING) - Space 20
        spaces.append(pygame.Rect(
            self.board_x + self.board_width - self.corner_size,
            self.board_y,
            self.corner_size,
            self.corner_size
        ))
        
        # Right side spaces (21-29) - from top to bottom
        for i in range(self.spaces_per_side):
            spaces.append(pygame.Rect(
                self.board_x + self.board_width - self.corner_size,
                self.board_y + self.corner_size + i * self.space_width,
                self.corner_size,
                self.space_width
            ))
        
        # Bottom-right corner (GO TO JAIL) - Space 30
        spaces.append(pygame.Rect(
            self.board_x + self.board_width - self.corner_size,
            self.board_y + self.board_height - self.corner_size,
            self.corner_size,
            self.corner_size
        ))
        
        # Bottom row spaces (31-39) - from right to left
        for i in range(self.spaces_per_side):
            spaces.append(pygame.Rect(
                self.board_x + self.board_width - self.corner_size - (i + 1) * self.space_width,
                self.board_y + self.board_height - self.corner_size,
                self.space_width,
                self.corner_size
            ))
        
        return spaces
    
    def get_space_centers(self) -> Dict[int, Tuple[int, int]]:
        centers: Dict[int, Tuple[int, int]] = {}
        for i, space in enumerate(self.spaces):
            centers[i] = space.center
        return centers
    
    def draw(self, screen: pygame.Surface) -> None:
        # Draw the board background (center area)
        center_x: int = self.board_x + self.corner_size
        center_y: int = self.board_y + self.corner_size
        center_width: int = self.board_width - 2 * self.corner_size
        center_height: int = self.board_height - 2 * self.corner_size
        
        pygame.draw.rect(screen, SPACE_COLORS["board_bg"], (
            center_x, 
            center_y, 
            center_width, 
            center_height
        ))
        
        # Draw each space
        for i, space in enumerate(self.spaces):
            # Get the property group for this space
            property_group: str = SPACE_PROPERTY_GROUPS[i]
            
            # Get the base color for this space
            if property_group == "SPECIAL":
                if i in [0, 10, 20, 30]:  # Corner spaces
                    base_color: Tuple[int, int, int] = SPACE_COLORS["corner"]
                else:
                    base_color = SPACE_COLORS["default"][i % 2]
            else:
                # Use a light background for property spaces
                base_color = (240, 240, 240)
            
            # Draw the space with the base color
            pygame.draw.rect(screen, base_color, space)
            
            # Draw the property group color strip
            if property_group != "SPECIAL":
                color: Tuple[int, int, int] = PROPERTY_COLORS[property_group]
                
                # Determine the position and size of the color strip based on space orientation
                if i in [0, 10, 20, 30]:  # Corner spaces
                    # No color strip for corner spaces
                    pass
                elif i >= 1 and i <= 9:  # Left side
                    strip_width: int = int(self.corner_size * BOARD_CONFIG["color_strip_height"])
                    color_rect: pygame.Rect = pygame.Rect(
                        space.right - strip_width,
                        space.top,
                        strip_width,
                        space.height
                    )
                    pygame.draw.rect(screen, color, color_rect)
                elif i >= 11 and i <= 19:  # Top row
                    strip_height: int = int(self.corner_size * BOARD_CONFIG["color_strip_height"])
                    color_rect = pygame.Rect(
                        space.left,
                        space.bottom - strip_height,
                        space.width,
                        strip_height
                    )
                    pygame.draw.rect(screen, color, color_rect)
                elif i >= 21 and i <= 29:  # Right side
                    strip_width = int(self.corner_size * BOARD_CONFIG["color_strip_height"])
                    color_rect = pygame.Rect(
                        space.left,
                        space.top,
                        strip_width,
                        space.height
                    )
                    pygame.draw.rect(screen, color, color_rect)
                elif i >= 31 and i <= 39:  # Bottom row
                    strip_height = int(self.corner_size * BOARD_CONFIG["color_strip_height"])
                    color_rect = pygame.Rect(
                        space.left,
                        space.top,
                        space.width,
                        strip_height
                    )
                    pygame.draw.rect(screen, color, color_rect)
            
            # Draw the border
            pygame.draw.rect(screen, SPACE_COLORS["border"], space, 1)
            
            # Add space name
            name: str = SPACE_NAMES[i]
            
            # Choose font size based on space type
            font_size: int = BOARD_CONFIG["corner_font_size"] if i in [0, 10, 20, 30] else BOARD_CONFIG["regular_font_size"]
            
            # Determine space type for text rendering
            space_type: str = ''
            if i in [0, 10, 20, 30]:
                space_type = 'corner'
            elif i >= 1 and i <= 9:
                space_type = 'left'
            elif i >= 11 and i <= 19:
                space_type = 'top'
            elif i >= 21 and i <= 29:
                space_type = 'right'
            else:  # i >= 31 and i <= 39
                space_type = 'bottom'
            
            # Render the text
            render_text_for_space(screen, space, name, font_size, space_type, self.space_width)
