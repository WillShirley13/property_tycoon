import pygame
import random

# screen = pygame.display.set_mode([1280, 720])
# pygame.display.set_caption('Property tycoon')
# #font = pygame.font.Font('freesansbold.ttf', 30)
# timer = pygame.time.Clock()
# fps = 60
# black = (0, 0, 0) 
# red= (255,0,0)
# white = (255, 255, 255)

class Dice:
    def __init__(self, x, y, size=50, color=(255, 0, 0)):
        """
        Initialize a dice component.
        
        Args:
            x (int): X position of the dice
            y (int): Y position of the dice
            size (int): Size of the dice square
            color (tuple): RGB color of the dice
        """
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.value = 1
        self.dot_color = (0, 0, 0)
        self.dot_radius = size // 10
    
    def draw(self, surface, value=6):
        """
        Draw the dice with the specified value on the given surface.
        
        Args:
            surface (pygame.Surface): The surface to draw on
            value (int, optional): The value to display on the dice (1-6).
            If None, uses the current value.
        """
        # Update the value if provided
        if value is not None and 1 <= value <= 6:
            self.value = value
        
        # Draw the dice square
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size), 0, 10)
        
        # Draw the dots based on the dice value
        dots = {
            1: [(self.x + self.size//2, self.y + self.size//2)],
            2: [(self.x + self.size//3, self.y + self.size//3), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            3: [(self.x + self.size//3, self.y + self.size//3), 
                (self.x + self.size//2, self.y + self.size//2), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            4: [(self.x + self.size//3, self.y + self.size//3), 
                (self.x + 2*self.size//3, self.y + self.size//3), 
                (self.x + self.size//3, self.y + 2*self.size//3), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            5: [(self.x + self.size//3, self.y + self.size//3), 
                (self.x + 2*self.size//3, self.y + self.size//3), 
                (self.x + self.size//2, self.y + self.size//2), 
                (self.x + self.size//3, self.y + 2*self.size//3), 
                (self.x + 2*self.size//3, self.y + 2*self.size//3)],
            6: [(self.x + self.size//3, self.y + self.size//4), 
                (self.x + 2*self.size//3, self.y + self.size//4), 
                (self.x + self.size//3, self.y + self.size//2), 
                (self.x + 2*self.size//3, self.y + self.size//2), 
                (self.x + self.size//3, self.y + 3*self.size//4), 
                (self.x + 2*self.size//3, self.y + 3*self.size//4)]
        }
        
        # Draw the dots
        for dot in dots[self.value]:
            pygame.draw.circle(surface, self.dot_color, dot, self.dot_radius)

class DiceManager:
    """
    A manager class for handling a pair of dice in the game.
    This class positions the dice in the center of the game board.
    """
    def __init__(self, screen_width, screen_height, dice_size=50, dice_spacing=20, color=(255, 0, 0)):
        """
        Initialize the dice manager.
        
        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
            dice_size (int): Size of each dice
            dice_spacing (int): Spacing between the two dice
            color (tuple): RGB color of the dice
        """
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Calculate positions for the dice to be centered
        dice1_x = center_x - dice_size - dice_spacing // 2
        dice2_x = center_x + dice_spacing // 2
        dice_y = center_y - dice_size // 2
        
        self.dice1 = Dice(dice1_x, dice_y, dice_size, color)
        self.dice2 = Dice(dice2_x, dice_y, dice_size, color)
        
    def draw(self, surface, dice1_value=6, dice2_value=6):
        """
        Draw both dice on the given surface with the specified values.
        
        Args:
            surface (pygame.Surface): The surface to draw on
            dice1_value (int, optional): Value for the first dice (1-6)
            dice2_value (int, optional): Value for the second dice (1-6)
        """
        self.dice1.draw(surface, dice1_value)
        self.dice2.draw(surface, dice2_value)
        
    def get_dice_values(self):
        """
        Get the current values of both dice.
        
        Returns:
            tuple: (dice1_value, dice2_value)
        """
        return (self.dice1.value, self.dice2.value)