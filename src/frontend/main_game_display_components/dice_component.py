import pygame
import random
from typing import Tuple, Optional, List


class Dice:
    # Initialize a single dice with visual properties
    def __init__(
        self,
        x: int,
        y: int,
        size: int = 50,
        color: Tuple[int, int, int] = (255, 0, 0),
        surface: pygame.Surface = None,
    ):
        # Store dice position and appearance properties
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.color: Tuple[int, int, int] = color
        self.surface: pygame.Surface = surface
        self.value: int = 1  # Default starting value
        self.dot_color: Tuple[int, int, int] = (0, 0, 0)  # Black dots
        self.dot_radius: int = size // 10  # Scale dot size based on dice size

    # Draw the dice with the current or specified value
    def draw(self, value: Optional[int] = None) -> None:
        if self.surface is None:
            return

        # Update the value if provided
        if value is not None and 1 <= value <= 6:
            self.value = value

        # Draw the dice square with rounded corners
        pygame.draw.rect(
            self.surface, self.color, (self.x, self.y, self.size, self.size), 0, 10
        )

        # Define dot positions for each possible dice value (1-6)
        dots: dict[int, List[Tuple[int, int]]] = {
            1: [(self.x + self.size // 2, self.y + self.size // 2)],  # Center
            2: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 3,
                ),  # Top-left to bottom-right diagonal
                (self.x + 2 * self.size // 3, self.y + 2 * self.size // 3),
            ],
            3: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 3,
                ),  # Same as 2 plus center
                (self.x + self.size // 2, self.y + self.size // 2),
                (self.x + 2 * self.size // 3, self.y + 2 * self.size // 3),
            ],
            4: [
                (self.x + self.size // 3, self.y + self.size // 3),  # Four corners
                (self.x + 2 * self.size // 3, self.y + self.size // 3),
                (self.x + self.size // 3, self.y + 2 * self.size // 3),
                (self.x + 2 * self.size // 3, self.y + 2 * self.size // 3),
            ],
            5: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 3,
                ),  # Four corners plus center
                (self.x + 2 * self.size // 3, self.y + self.size // 3),
                (self.x + self.size // 2, self.y + self.size // 2),
                (self.x + self.size // 3, self.y + 2 * self.size // 3),
                (self.x + 2 * self.size // 3, self.y + 2 * self.size // 3),
            ],
            6: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 4,
                ),  # 3 dots on each side (left and right)
                (self.x + 2 * self.size // 3, self.y + self.size // 4),
                (self.x + self.size // 3, self.y + self.size // 2),
                (self.x + 2 * self.size // 3, self.y + self.size // 2),
                (self.x + self.size // 3, self.y + 3 * self.size // 4),
                (self.x + 2 * self.size // 3, self.y + 3 * self.size // 4),
            ],
        }

        # Draw each dot for the current dice value
        for dot in dots[self.value]:
            pygame.draw.circle(self.surface, self.dot_color, dot, self.dot_radius)


class DiceManager:
    # Initialize the dice manager which handles two dice and the roll button
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        surface: pygame.Surface,
        dice_size: int = 50,
        dice_spacing: int = 20,
        color: Tuple[int, int, int] = (255, 0, 0),
    ):
        # Store the surface
        self.surface: pygame.Surface = surface

        # Calculate center position of the screen
        center_x: int = screen_width // 2
        center_y: int = screen_height // 2

        # Position the dice centered on the screen with spacing between them
        dice1_x: int = center_x - dice_size - dice_spacing // 2
        dice2_x: int = center_x + dice_spacing // 2
        dice_y: int = center_y - dice_size // 2

        # Create two dice objects
        self.dice1: Dice = Dice(dice1_x, dice_y, dice_size, color, surface)
        self.dice2: Dice = Dice(dice2_x, dice_y, dice_size, color, surface)

        # Create a button area that covers both dice plus some padding
        button_width = (dice_size * 2) + dice_spacing
        button_height = dice_size
        padding = dice_spacing * 2
        self.button_rect = pygame.Rect(
            dice1_x, dice_y, button_width, button_height + 20
        )

        # Button appearance settings
        self.button_color = (0, 0, 0, 0)  # Transparent
        self.hover_color = (200, 200, 200, 100)  # Semi-transparent gray when hovering
        self.is_hovering = False
        self.font = pygame.font.Font(None, 24)  # Initialize font for button text

    # Draw both dice and the roll button with optional hover effect
    def draw(
        self, dice1_value: Optional[int] = None, dice2_value: Optional[int] = None
    ) -> None:
        # Draw both dice with specified values (or keep current values if None)
        self.dice1.draw(dice1_value)
        self.dice2.draw(dice2_value)

        # Draw the transparent button over the dice
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.is_hovering = True
            # Create a transparent surface for the hover effect
            button_surface = pygame.Surface(
                (self.button_rect.width, self.button_rect.height), pygame.SRCALPHA
            )
            pygame.draw.rect(
                button_surface,
                self.hover_color,
                (0, 0, self.button_rect.width, self.button_rect.height),
                0,
                10,
            )
            self.surface.blit(button_surface, (self.button_rect.x, self.button_rect.y))

            # For debugging - uncomment to see the clickable area
            # pygame.draw.rect(self.surface, (255, 0, 0), self.button_rect, 2)
        else:
            self.is_hovering = False

        # Render and blit the button text
        text_surface = self.font.render("Click me to roll!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.button_rect.centerx, self.button_rect.bottom - 10)
        )
        self.surface.blit(text_surface, text_rect)

    # Return the current values of both dice
    def get_dice_values(self) -> Tuple[int, int]:
        # Return the current values of both dice as a tuple
        return (self.dice1.value, self.dice2.value)
