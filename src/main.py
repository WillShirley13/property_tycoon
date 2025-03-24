import pygame
import sys
import os
from typing import List, Tuple, Dict, Optional

from backend.admin import Admin
from backend.enums.game_token import GameToken
from frontend.start_screen_display import StartScreenDisplay
from frontend.main_game_display import MainGameDisplay
from frontend.helpers.space_data import BOARD_CONFIG, SPACE_COLORS
from frontend.time_limit_choice_display import TimeLimitChoiceDisplay
from backend.property_owners.bank import Bank
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.non_ownables.game_card import GameCard
from backend.ownables.ownable import Ownable
from frontend.main_game_display_components.board_component import Board


def main() -> None:
    # Initialize pygame
    pygame.init()

    # Get the screen info to set up a dynamic display
    screen_info: pygame.display.Info = pygame.display.Info()
    screen_width: int = screen_info.current_w
    screen_height: int = screen_info.current_h

    # Create a window based on the configured percentage of the screen size
    window_width: int = int(screen_width * BOARD_CONFIG["screen_size_percentage"])
    window_height: int = int(screen_height * BOARD_CONFIG["screen_size_percentage"])
    screen: pygame.Surface = pygame.display.set_mode((window_width, window_height))

    # Set the window title
    pygame.display.set_caption("Property Tycoon")

    # Display the start screen and get player names
    start_screen: StartScreenDisplay = StartScreenDisplay(
        window_width, window_height, screen
    )
    player_names: List[str] = start_screen.display()

    # Display the time limit dialog and get the time limit
    time_limit_screen: TimeLimitChoiceDisplay = TimeLimitChoiceDisplay(
        window_width, window_height, screen
    )
    time_limit: int = time_limit_screen.display()

    game_tokens: List[GameToken] = [
        GameToken.BOOT,
        GameToken.CAT,
        GameToken.TOPHAT,
        GameToken.IRON,
        GameToken.SMARTPHONE,
        GameToken.BOAT,
    ]
    # Frontend must pass names and tokens for each player
    player_data: List[Tuple[str, GameToken]] = [
        (player_names[i], game_tokens[i]) for i in range(len(player_names))
    ]

    # Initialize Admin with player data and time limit
    admin: Admin = Admin(player_data, time_limit)

    # Create and run the main game display
    game_display: MainGameDisplay = MainGameDisplay(
        window_width, window_height, screen, player_data, admin
    )
    game_display.run()


if __name__ == "__main__":
    main()
