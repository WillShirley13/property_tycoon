import pygame
import random
from typing import Tuple, Optional, List

class Dice:
    def __init__(self, x: int, y: int, size: int = 50, color: Tuple[int, int, int] = (255, 0, 0)):
        # Store dice position and appearance properties
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.color: Tuple[int, int, int] = color
        self.value: int = 1  # Default starting value
        self.dot_color: Tuple[int, int, int] = (0, 0, 0)  # Black dots
        self.dot_radius: int = size // 10  # Scale dot size based on dice size
    
    def draw(self, surface: pygame.Surface, value: Optional[int] = None) -> None:
        # Update the value if provided
        if value is not None and 1 <= value <= 6:
            self.value = value
        
        # Draw the dice square with rounded corners
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size), 0, 10)
        
        # Define dot positions for each possible dice value (1-6)
        dots: dict[int, List[Tuple[int, int]]] = {
            1: [(self.x + self.size//2, self.y + self.size//2)],  # Center
            2: [(self.x + self.size//3, self.y + self.size//3),   # Top-left to bottom-right diagonal
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            3: [(self.x + self.size//3, self.y + self.size//3),   # Same as 2 plus center
                (self.x + self.size//2, self.y + self.size//2), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            4: [(self.x + self.size//3, self.y + self.size//3),   # Four corners
                (self.x + 2*self.size//3, self.y + self.size//3), 
                (self.x + self.size//3, self.y + 2*self.size//3), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            5: [(self.x + self.size//3, self.y + self.size//3),   # Four corners plus center
                (self.x + 2*self.size//3, self.y + self.size//3), 
                (self.x + self.size//2, self.y + self.size//2), 
                (self.x + self.size//3, self.y + 2*self.size//3), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            6: [(self.x + self.size//3, self.y + self.size//4),   # 3 dots on each side (left and right)
                (self.x + 2*self.size//3, self.y + self.size//4), 
                (self.x + self.size//3, self.y + self.size//2), 
                (self.x + 2*self.size//3, self.y + self.size//2), 
                (self.x + self.size//3, self.y + 3*self.size//4), 
                (self.x + 2*self.size//3, self.y + 3*self.size//4)]
        }
        
        # Draw each dot for the current dice value
        for dot in dots[self.value]:
            pygame.draw.circle(surface, self.dot_color, dot, self.dot_radius)

class DiceManager:
    def __init__(self, screen_width: int, screen_height: int, dice_size: int = 50, 
                 dice_spacing: int = 20, color: Tuple[int, int, int] = (255, 0, 0)):
        # Calculate center position of the screen
        center_x: int = screen_width // 2
        center_y: int = screen_height // 2
        
        # Position the dice centered on the screen with spacing between them
        dice1_x: int = center_x - dice_size - dice_spacing // 2
        dice2_x: int = center_x + dice_spacing // 2
        dice_y: int = center_y - dice_size // 2
        
        # Create two dice objects
        self.dice1: Dice = Dice(dice1_x, dice_y, dice_size, color)
        self.dice2: Dice = Dice(dice2_x, dice_y, dice_size, color)
        
    def draw(self, surface: pygame.Surface, dice1_value: Optional[int] = None, 
             dice2_value: Optional[int] = None) -> None:
        # Draw both dice with specified values (or keep current values if None)
        self.dice1.draw(surface, dice1_value)
        self.dice2.draw(surface, dice2_value)
        
    def get_dice_values(self) -> Tuple[int, int]:
        # Return the current values of both dice as a tuple
        return (self.dice1.value, self.dice2.value)