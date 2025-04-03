from typing import Dict, List, Tuple

import pygame

from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.game_card import GameCard
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.ownables.ownable import Ownable
from backend.ownables.property import Property
from frontend.helpers.board_text_utils import render_text_for_space
from frontend.helpers.space_data import (BOARD_CONFIG, PROPERTY_COLORS,
                                         SPACE_COLORS, SPACE_NAMES,
                                         SPACE_PROPERTY_GROUPS)


class Board:
    # Set up the game board with appropriate dimensions and spacing
    def __init__(self, screen_width: int, screen_height: int,
                 screen: pygame.Surface):
        # Set up the board properties
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.screen: pygame.Surface = screen

        # Board should occupy the specified percentage of the screen
        # width
        self.board_width: int = int(
            screen_width * BOARD_CONFIG["board_width_percentage"])

        # Board height will be the same as width to make a square
        self.board_height: int = self.board_width

        # If the board height is too large for the screen, adjust it
        if self.board_height > screen_height * \
                BOARD_CONFIG["max_height_percentage"]:
            self.board_height = int(
                screen_height
                * BOARD_CONFIG["max_height_percentage"])
            self.board_width = self.board_height

        # Calculate the position to center the board
        self.board_x: int = (screen_width - self.board_width) // 2
        self.board_y: int = (screen_height - self.board_height) // 2

        # Number of spaces on each side of the board (excluding
        # corners)
        self.spaces_per_side: int = BOARD_CONFIG["spaces_per_side"]

        # Calculate space dimensions
        self.corner_size: int = int(
            self.board_width
            / BOARD_CONFIG["corner_size_divisor"])

        # Calculate the width of regular spaces
        self.space_width: int = int(
            (self.board_width - 2 * self.corner_size) / self.spaces_per_side)

        # Create the spaces
        self.spaces: List[pygame.Rect] = self._create_spaces()
        self.space_centers: Dict[int, Tuple[int, int]
                                 ] = self.get_space_centers()

    # Create all board space rectangles with proper positioning
    def _create_spaces(self) -> List[pygame.Rect]:
        spaces: List[pygame.Rect] = []

        # Bottom-left corner (GO)
        spaces.append(
            pygame.Rect(
                self.board_x,
                self.board_y + self.board_height - self.corner_size,
                self.corner_size,
                self.corner_size,
            )
        )

        # Left side spaces (1-9)
        for i in range(self.spaces_per_side):
            spaces.append(
                pygame.Rect(
                    self.board_x,
                    self.board_y + self.board_height
                    - self.corner_size - (i + 1) * self.space_width,
                    self.corner_size,
                    self.space_width,
                )
            )

        # Top-left corner (JAIL)
        spaces.append(
            pygame.Rect(
                self.board_x,
                self.board_y,
                self.corner_size,
                self.corner_size))

        # Top row spaces (11-19)
        for i in range(self.spaces_per_side):
            spaces.append(
                pygame.Rect(
                    self.board_x + self.corner_size + i * self.space_width,
                    self.board_y,
                    self.space_width,
                    self.corner_size,
                )
            )

        # Top-right corner (FREE PARKING)
        spaces.append(
            pygame.Rect(
                self.board_x + self.board_width - self.corner_size,
                self.board_y,
                self.corner_size,
                self.corner_size,
            )
        )

        # Right side spaces (21-29)
        for i in range(self.spaces_per_side):
            spaces.append(
                pygame.Rect(
                    self.board_x + self.board_width - self.corner_size,
                    self.board_y + self.corner_size + i * self.space_width,
                    self.corner_size,
                    self.space_width,
                )
            )

        # Bottom-right corner (GO TO JAIL)
        spaces.append(
            pygame.Rect(
                self.board_x + self.board_width - self.corner_size,
                self.board_y + self.board_height - self.corner_size,
                self.corner_size,
                self.corner_size,
            )
        )

        # Bottom row spaces (31-39)
        for i in range(self.spaces_per_side):
            spaces.append(
                pygame.Rect(
                    self.board_x + self.board_width
                    - self.corner_size - (i + 1) * self.space_width,
                    self.board_y + self.board_height - self.corner_size,
                    self.space_width,
                    self.corner_size,
                )
            )

        return spaces

    # Calculate the center coordinates of each board space
    def get_space_centers(self) -> Dict[int, Tuple[int, int]]:
        centers: Dict[int, Tuple[int, int]] = {}
        for i, space in enumerate(self.spaces):
            centers[i] = space.center
        return centers

    # Draw the complete game board with all spaces and properties
    def draw(self, game_board: List[Ownable
             | FreeParking | Jail | Go | GameCard]) -> None:
        # Draw the board background
        center_x: int = self.board_x + self.corner_size
        center_y: int = self.board_y + self.corner_size
        center_width: int = self.board_width - 2 * self.corner_size
        center_height: int = self.board_height - 2 * self.corner_size

        pygame.draw.rect(
            self.screen,
            SPACE_COLORS["board_bg"],
            (center_x, center_y, center_width, center_height),
        )

        # Draw each space
        for i, space_info in enumerate(self.spaces):
            space = space_info

            # Get the property group for this space
            property_group: str = SPACE_PROPERTY_GROUPS[i]

            # Get the base color for this space
            if property_group == "SPECIAL":
                if i in [0, 10, 20, 30]:  # Corner spaces
                    base_color: Tuple[int, int,
                                      int] = SPACE_COLORS["corner"]
                else:
                    base_color = SPACE_COLORS["default"][i % 2]
            else:
                # Use a light background for property spaces
                base_color = (240, 240, 240)

            # Draw the space with the base color
            pygame.draw.rect(self.screen, base_color, space)

            # Draw the property group color strip
            if property_group != "SPECIAL":
                color: Tuple[int, int,
                             int] = PROPERTY_COLORS[property_group]

                # Determine the position and size of the color strip based on
                # space orientation
                if i in [0, 10, 20, 30]:  # Corner spaces
                    # No color strip for corner spaces
                    pass
                elif i >= 1 and i <= 9:  # Left side
                    strip_width: int = int(
                        self.corner_size * BOARD_CONFIG["color_strip_height"])
                    color_rect: pygame.Rect = pygame.Rect(
                        space.right - strip_width, space.top, strip_width, space.height)
                    pygame.draw.rect(self.screen, color, color_rect)
                elif i >= 11 and i <= 19:  # Top row
                    strip_height: int = int(
                        self.corner_size * BOARD_CONFIG["color_strip_height"])
                    color_rect = pygame.Rect(
                        space.left,
                        space.bottom - strip_height,
                        space.width,
                        strip_height,
                    )
                    pygame.draw.rect(self.screen, color, color_rect)
                elif i >= 21 and i <= 29:  # Right side
                    strip_width = int(
                        self.corner_size
                        * BOARD_CONFIG["color_strip_height"])
                    color_rect = pygame.Rect(
                        space.left, space.top, strip_width, space.height)
                    pygame.draw.rect(self.screen, color, color_rect)
                elif i >= 31 and i <= 39:  # Bottom row
                    strip_height = int(
                        self.corner_size
                        * BOARD_CONFIG["color_strip_height"])
                    color_rect = pygame.Rect(
                        space.left, space.top, space.width, strip_height)
                    pygame.draw.rect(self.screen, color, color_rect)

                # Draw houses and hotels after drawing the color strip
                if isinstance(game_board[i], Property):
                    # Get number of houses and hotel for this property
                    houses = game_board[i].get_houses()
                    hotel = game_board[i].get_hotel()

                    if i >= 1 and i <= 9:  # Left side
                        strip_width = int(
                            self.corner_size * BOARD_CONFIG["color_strip_height"])
                        color_rect = pygame.Rect(
                            space.right - strip_width, space.top, strip_width, space.height)

                        # Draw houses/hotel in the color strip
                        house_size = min(
                            strip_width // 2, space.height // 5)
                        if hotel == 1:
                            # Draw a black square for hotel
                            hotel_rect = pygame.Rect(
                                color_rect.centerx - house_size // 2,
                                color_rect.centery - house_size // 2,
                                house_size,
                                house_size)
                            pygame.draw.rect(
                                self.screen, (0, 0, 0), hotel_rect)
                        else:
                            # Draw green squares for houses
                            for h in range(houses):
                                house_rect = pygame.Rect(
                                    color_rect.centerx - house_size // 2,
                                    color_rect.top
                                    + (h + 1) * color_rect.height // (houses
                                                                      + 1) - house_size // 2,
                                    house_size,
                                    house_size,
                                )
                                pygame.draw.rect(
                                    self.screen, (0, 150, 0), house_rect)

                    elif i >= 11 and i <= 19:  # Top row
                        strip_height = int(
                            self.corner_size * BOARD_CONFIG["color_strip_height"])
                        color_rect = pygame.Rect(
                            space.left, space.bottom - strip_height, space.width, strip_height)

                        # Draw houses/hotel in the color strip
                        house_size = min(
                            strip_height // 2, space.width // 5)
                        if hotel == 1:
                            # Draw a black square for hotel
                            hotel_rect = pygame.Rect(
                                color_rect.centerx - house_size // 2,
                                color_rect.centery - house_size // 2,
                                house_size,
                                house_size)
                            pygame.draw.rect(
                                self.screen, (0, 0, 0), hotel_rect)
                        else:
                            # Draw green squares for houses
                            for h in range(houses):
                                house_rect = pygame.Rect(
                                    color_rect.left
                                    + (h + 1) * color_rect.width // (houses
                                                                     + 1) - house_size // 2,
                                    color_rect.centery - house_size // 2,
                                    house_size,
                                    house_size,
                                )
                                pygame.draw.rect(
                                    self.screen, (0, 150, 0), house_rect)

                    elif i >= 21 and i <= 29:  # Right side
                        strip_width = int(
                            self.corner_size * BOARD_CONFIG["color_strip_height"])
                        color_rect = pygame.Rect(
                            space.left, space.top, strip_width, space.height)

                        # Draw houses/hotel in the color strip
                        house_size = min(
                            strip_width // 2, space.height // 5)
                        if hotel == 1:
                            # Draw a black square for hotel
                            hotel_rect = pygame.Rect(
                                color_rect.centerx - house_size // 2,
                                color_rect.centery - house_size // 2,
                                house_size,
                                house_size)
                            pygame.draw.rect(
                                self.screen, (0, 0, 0), hotel_rect)
                        else:
                            # Draw green squares for houses
                            for h in range(houses):
                                house_rect = pygame.Rect(
                                    color_rect.centerx - house_size // 2,
                                    color_rect.top
                                    + (h + 1) * color_rect.height // (houses
                                                                      + 1) - house_size // 2,
                                    house_size,
                                    house_size,
                                )
                                pygame.draw.rect(
                                    self.screen, (0, 150, 0), house_rect)

                    elif i >= 31 and i <= 39:  # Bottom row
                        strip_height = int(
                            self.corner_size * BOARD_CONFIG["color_strip_height"])
                        color_rect = pygame.Rect(
                            space.left, space.top, space.width, strip_height)

                        # Draw houses/hotel in the color strip
                        house_size = min(
                            strip_height // 2, space.width // 5)
                        if hotel == 1:
                            # Draw a black square for hotel
                            hotel_rect = pygame.Rect(
                                color_rect.centerx - house_size // 2,
                                color_rect.centery - house_size // 2,
                                house_size,
                                house_size)
                            pygame.draw.rect(
                                self.screen, (0, 0, 0), hotel_rect)
                        else:
                            # Draw green squares for houses
                            for h in range(houses):
                                house_rect = pygame.Rect(
                                    color_rect.left
                                    + (h + 1) * color_rect.width // (houses
                                                                     + 1) - house_size // 2,
                                    color_rect.centery - house_size // 2,
                                    house_size,
                                    house_size,
                                )
                                pygame.draw.rect(
                                    self.screen, (0, 150, 0), house_rect)

            # Draw the border
            pygame.draw.rect(
                self.screen,
                SPACE_COLORS["border"],
                space,
                1)

            # Add space name
            name: str = SPACE_NAMES[i]

            # Choose font size based on space type
            font_size: int = BOARD_CONFIG["corner_font_size"] if i in [
                0, 10, 20, 30] else BOARD_CONFIG["regular_font_size"]

            # Determine space type for text rendering
            space_type: str = ""
            if i in [0, 10, 20, 30]:
                space_type = "corner"
            elif i >= 1 and i <= 9:
                space_type = "left"
            elif i >= 11 and i <= 19:
                space_type = "top"
            elif i >= 21 and i <= 29:
                space_type = "right"
            else:  # i >= 31 and i <= 39
                space_type = "bottom"

            # Render the text
            render_text_for_space(
                self.screen,
                space,
                name,
                font_size,
                space_type,
                self.space_width)
