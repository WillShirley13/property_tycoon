import random
from typing import List, Optional, Tuple

import pygame


class Dice:
    def __init__(
        self,
        x: int,
        y: int,
        size: int = 50,
        color: Tuple[int, int, int] = (255, 0, 0),
        surface: pygame.Surface = None,
    ):
        # store dice position and appearance properties
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.color: Tuple[int, int, int] = color
        self.surface: pygame.Surface = surface
        self.value: int = 1  # default starting value
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
            self.surface,
            self.color,
            (self.x,
             self.y,
             self.size,
             self.size),
            0,
            10)

        # Define dot positions for each possible dice value (1-6)
        dots: dict[int, List[Tuple[int, int]]] = {
            # Center
            1: [(self.x + self.size // 2, self.y + self.size // 2)],
            2: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 3,
                ),  # Top-left to bottom-right diagonal
                (self.x + 2 * self.size // 3,
                 self.y + 2 * self.size // 3),
            ],
            3: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 3,
                ),  # Same as 2 plus center
                (self.x + self.size // 2, self.y + self.size // 2),
                (self.x + 2 * self.size // 3,
                 self.y + 2 * self.size // 3),
            ],
            4: [
                (self.x + self.size // 3, self.y
                 + self.size // 3),  # Four corners
                (self.x + 2 * self.size // 3, self.y + self.size // 3),
                (self.x + self.size // 3, self.y + 2 * self.size // 3),
                (self.x + 2 * self.size // 3,
                 self.y + 2 * self.size // 3),
            ],
            5: [
                (
                    self.x + self.size // 3,
                    self.y + self.size // 3,
                ),  # Four corners plus center
                (self.x + 2 * self.size // 3, self.y + self.size // 3),
                (self.x + self.size // 2, self.y + self.size // 2),
                (self.x + self.size // 3, self.y + 2 * self.size // 3),
                (self.x + 2 * self.size // 3,
                 self.y + 2 * self.size // 3),
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
                (self.x + 2 * self.size // 3,
                 self.y + 3 * self.size // 4),
            ],
        }

        # Draw each dot for the current dice value
        for dot in dots[self.value]:
            pygame.draw.circle(
                self.surface,
                self.dot_color,
                dot,
                self.dot_radius)


class DiceManager:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: pygame.Surface,
        dice_size: int = 60,
        dice_spacing: int = 20,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.dice_size = dice_size
        self.dice_spacing = dice_spacing

        # A button rectangle that the user can click to "roll" dice
        self.button_rect = pygame.Rect(
            self.screen_width // 2 - 40,  # center horizontally
            self.screen_height // 2 + 60,  # near bottom
            80,  # button width
            40,  # button height
        )

        # Pre-load the six dice-face images
        self.dice_faces = {
            1: pygame.transform.scale(
                pygame.image.load(
                    "src/frontend/art_assets/dice_numbers/1.png"),
                (dice_size, dice_size),
            ),
            2: pygame.transform.scale(
                pygame.image.load(
                    "src/frontend/art_assets/dice_numbers/2.png"),
                (dice_size, dice_size),
            ),
            3: pygame.transform.scale(
                pygame.image.load(
                    "src/frontend/art_assets/dice_numbers/3.png"),
                (dice_size, dice_size),
            ),
            4: pygame.transform.scale(
                pygame.image.load(
                    "src/frontend/art_assets/dice_numbers/4.png"),
                (dice_size, dice_size),
            ),
            5: pygame.transform.scale(
                pygame.image.load(
                    "src/frontend/art_assets/dice_numbers/5.png"),
                (dice_size, dice_size),
            ),
            6: pygame.transform.scale(
                pygame.image.load(
                    "src/frontend/art_assets/dice_numbers/6.png"),
                (dice_size, dice_size),
            ),
        }

        # Store the most recent dice values so we can re-draw them
        # every frame
        self.last_value1: Optional[int] = None
        self.last_value2: Optional[int] = None

    def draw(self, value1: Optional[int]
             = None, value2: Optional[int] = None):

        # If the player rolled new dice values, store them
        if value1 is not None:
            self.last_value1 = value1
        if value2 is not None:
            self.last_value2 = value2

        # Draw a simple "Roll Dice" button
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_rect, 2)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Roll Dice", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

        # If no valid dice values yet, stop
        if not self.last_value1 or not self.last_value2:
            return

        # Retrieve the images for the stored face values
        dice_img1 = self.dice_faces.get(self.last_value1)
        dice_img2 = self.dice_faces.get(self.last_value2)

        dice1_x = self.screen_width // 2 - self.dice_size - self.dice_spacing
        dice1_y = self.screen_height // 2 - 40
        dice2_x = self.screen_width // 2 + self.dice_spacing
        dice2_y = self.screen_height // 2 - 40

        # Blit  the dice images
        if dice_img1:
            self.screen.blit(dice_img1, (dice1_x, dice1_y))
        if dice_img2:
            self.screen.blit(dice_img2, (dice2_x, dice2_y))

    # Return the current values of both dice
    def get_dice_values(self) -> Tuple[int, int]:
        # Return the current values of both dice as a tuple
        return (self.dice1.value, self.dice2.value)
