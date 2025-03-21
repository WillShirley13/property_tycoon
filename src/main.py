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
    start_screen: StartScreenDisplay = StartScreenDisplay(window_width, window_height)
    player_names: List[str] = start_screen.display(screen)
    
    # Display the time limit dialog and get the time limit
    time_limit_screen: TimeLimitChoiceDisplay = TimeLimitChoiceDisplay(window_width, window_height)
    time_limit: int = time_limit_screen.display(screen)
    
    game_tokens: List[GameToken] = [GameToken.BOOT, GameToken.CAT, GameToken.HATSTAND, GameToken.IRON, GameToken.SMARTPHONE, GameToken.BOAT]
    # Frontend must pass names and tokens for each player
    player_data: List[Tuple[str, GameToken]] = [(player_names[i], game_tokens[i]) for i in range(len(player_names))]
    
    centre_spaces: Dict[int, Tuple[int, int]] = Board(window_width, window_height).get_space_centers()

    # Initialize Admin with player data and time limit
    admin: Admin = Admin(player_data, time_limit)

    # Print the player names (for debugging)
    print(f"Players: {player_data}")
    print(f"Time limit: {time_limit} minutes")
    
    # Create the main game display with the admin object
    main_game_display: MainGameDisplay = MainGameDisplay(window_width, window_height, player_data, admin, centre_spaces)
    
    # Start the game timer if a time limit was set
    if time_limit > 0:
        admin.start_timer()
    
    # Main game loop
    running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()
    
    while running:
        # Process events directly in the main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT event detected in main loop")
                running = False
                break
        
        if not running:
            break
            
        # Let the main game display handle game-specific events
        running = main_game_display.handle_events(screen)
        
        # Draw the main game display (includes board and player info)
        main_game_display.draw(screen)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS
    
    # Clean up
    print("Exiting game...")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 