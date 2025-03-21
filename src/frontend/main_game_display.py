import pygame
import sys
import os
from typing import List, Optional, Tuple, Dict, Any, Union

from backend.enums.game_token import GameToken
from frontend.main_game_display_components.board_component import Board
from frontend.main_game_display_components.all_players_component import PlayerDisplay
from frontend.helpers.space_data import SPACE_COLORS
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.non_ownables.game_card import GameCard
from backend.ownables.ownable import Ownable
from frontend.main_game_display_components.current_player_component import CurrentPlayerDisplay
from backend.property_owners.player import Player
from frontend.main_game_display_components.jail_popup import JailPopup
from frontend.main_game_display_components.dice_component import DiceManager
from frontend.main_game_display_components.sell_asset_popup import SellOrMortgagePopup


def temp_method_to_test_sell_or_mortgage_popup(current_player: Player, bank: Bank) -> None:
    # For testing: add money and properties to current player
    count = 0
    current_player.add_cash_balance(10000)
    
    # Transfer properties from bank to player for demo
    for prop_group in bank.get_owned_properties().values():
        # Create a copy of the property group for iteration
        properties_to_process = prop_group.copy()
        for prop in properties_to_process:
            if count <= 24:
                current_player.purchase_property(prop, bank)
                count += 1
    
    count = 0
    # Transfer properties from bank to player for demo
    for prop_group in current_player.get_owned_properties().values():
        # Create a copy of the property group for iteration
        properties_to_process = prop_group.copy()
        for prop in properties_to_process:
            if count <= 12:
                current_player.mortgage_property(prop, bank)
                count += 1

class MainGameDisplay:
    def __init__(self, screen_width: int, screen_height: int, players: List[Dict[str, Any]], 
            admin: Optional[Any] = None, center_spaces: Optional[List[Tuple[int, int]]] = None):
        # Store screen dimensions and game references
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.players_data: List[Dict[str, Any]] = players
        self.admin: Optional[Any] = admin
        self.running: bool = True
        self.center_spaces: Optional[List[Tuple[int, int]]] = center_spaces
        
        # Initialize the game board component
        self.board: Board = Board(screen_width, screen_height)
        
        # Initialize the player information display
        self.player_display: PlayerDisplay = PlayerDisplay(
            15,                   # X position
            20,                   # Y position
            screen_width/5,       # Width (20% of screen)
            85 * 5                # Height (adjusted for player count)
        )
        
        # Position current player display below the player list
        player_display_bottom: float = self.player_display.y + self.player_display.height
        current_player_display_y: float = player_display_bottom + 20  # Add spacing between components
        
        # Initialize current player information display
        self.current_player_display: CurrentPlayerDisplay = CurrentPlayerDisplay(
            15,                   # Same X position as player display
            current_player_display_y,  # Y position calculated from player display
            screen_width/5,       # Same width as player display
            screen_height/4       # Height (25% of screen)
        )
        
        # Initialize dice manager for rolling dice
        self.dice_manager: DiceManager = DiceManager(self.screen_width, self.screen_height)
        
        # Initialize jail popup for when players land on jail
        self.jail_popup: JailPopup = JailPopup(
            self.screen_width // 2 - 175,  # Centered horizontally
            self.screen_height // 2 - 150, # Centered vertically
            350,                           # Width
            300                            # Height
        )
        
        # Initialize sell/mortgage popup for property management
        self.sell_or_mortgage_popup: SellOrMortgagePopup = SellOrMortgagePopup(
            self.screen_width // 2 - 225,  # Centered horizontally
            self.screen_height // 2 - 300, # Centered vertically
            450,                           # Width
            600                            # Height
        )
        
        # Initialize game flow tracking variables
        self.current_player: Optional[Player] = None
        self.current_player_index: int = 0
        self.current_player_turn_finished: bool = False
        self.players_objects: List[Player] = []
        
        # Initialize game state from admin
        
        # Store reference to game admin
        self.admin = admin
        
        # Get game state from admin
        self.players_objects = admin.get_players()
        self.bank = admin.get_bank()
        self.game_board = admin.get_game_board()
        self.game_space_helper = admin.get_game_space_helper()
        self.time_limit = admin.get_time_limit()
        self.free_parking = admin.get_free_parking()
        self.go = admin.get_go()
        self.jail = admin.get_jail()
        self.pot_luck_cards = admin.get_pot_luck_cards()
        self.opportunity_knocks = admin.get_opportunity_knocks()
        
        # Initialize game flow with the first player
        if self.players_objects:
            self.current_player_index = 0
            self.current_player = self.players_objects[self.current_player_index] 
    
    def draw(self, screen: pygame.Surface) -> None:
        # Clear the screen with a white background
        screen.fill((255, 255, 255))
        
        # Draw the game board
        self.board.draw(screen)
        
        # Draw player game pieces on the board
        game_piece_pngs: List[str] = ['boot.png', 'cat.png', 'iron.png', 'tophat.png', 'smartphone.png', 'boat.png']
        for player in self.players_objects:
            # Get the player's token and place it on the board
            game_token: GameToken = player.get_game_token()
            
            # Position the token based on its type
            match game_token:
                case GameToken.BOOT:
                    game_piece_png = game_piece_pngs[0]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))                    
                case GameToken.CAT:
                    game_piece_png = game_piece_pngs[1]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))                   
                case GameToken.IRON:
                    game_piece_png = game_piece_pngs[2]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))                   
                case GameToken.HATSTAND:
                    game_piece_png = game_piece_pngs[3]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))  
                case GameToken.SMARTPHONE:
                    game_piece_png = game_piece_pngs[4]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                case GameToken.BOAT:
                    game_piece_png = game_piece_pngs[5]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))

            pos_index = player.get_current_position()

     
            if pos_index in range(len(self.center_spaces)):
                x, y = self.center_spaces[pos_index]

                token_offsets = {
                GameToken.BOOT: (0, 0),
                GameToken.CAT: (0, 0),
                GameToken.IRON: (0, 0),
                GameToken.HATSTAND: (0, 0),
                GameToken.SMARTPHONE: (0, 0),
                GameToken.BOAT: (0, 0)}
                x_offset, y_offset = token_offsets.get(game_token, (0, 0))  
                screen.blit(token_png, (x + x_offset, y + y_offset))
                
            else:
                print(f"[WARN] Invalid player position: {pos_index}")         
        
        # Draw the player list display
        self.player_display.draw(screen, self.players_data)
        
        # Draw current player information if available
        if self.players_objects and self.current_player:
            self.current_player_display.draw(screen, self.current_player)
        
        # Draw the dice
        self.dice_manager.draw(screen)
        
    def handle_events(self, screen: pygame.Surface) -> bool:
        # Make sure the game is displayed
        self.draw(screen)
        
        # Get current keyboard state
        keys = pygame.key.get_pressed()
        
        # Check if current player is in jail and show jail popup if needed
        if self.current_player and self.current_player.get_is_in_jail():
            # Show the jail popup and get the player's decision
            result = self.jail_popup.show(screen, self.current_player)
        
        # Show the sell/mortgage popup when M key is pressed
        if keys[pygame.K_m] and self.current_player and self.bank:
            # For testing: add money and properties to current player
            temp_method_to_test_sell_or_mortgage_popup(self.current_player, self.bank)
            
            # Show sell/mortgage popup and get result
            sell_or_mortgage_result = self.sell_or_mortgage_popup.show(screen, self.current_player)
        
        # End current player's turn when space key is pressed
        if keys[pygame.K_SPACE]:
            self.current_player_turn_finished = True
            
        # Move to the next player if current turn is finished
      #  if self.current_player_turn_finished:
       #     self.next_player()
        #    self.current_player_turn_finished = False  # Reset for the next player
       #NEW CODE
        if keys[pygame.K_l]:  
            move_result = self.current_player.move_player()  # roll and move

            if move_result:
                dice_rolls, new_pos = move_result
                print(f"{self.current_player.get_name()} rolled {dice_rolls} → moved to {new_pos}")
            self.next_player()
            
        # Return game running state
        return self.running

    def process_player_turn(self) -> None:
        # Placeholder for full turn logic including dice, movement, property actions
        # When all required actions for a turn are completed, set the flag
        
        # Example: After dice roll, movement, and any required actions
        if self.all_turn_actions_completed():
            self.current_player_turn_finished = True
    
    def all_turn_actions_completed(self) -> bool:
        # Placeholder method to check if all required actions are completed
        # In a real implementation, would check various conditions for turn completion
        
        # Placeholder implementation - in a real game, this would check various conditions
        return False
        
    def next_player(self) -> None:
        # Check if we have admin and players
        if not self.admin or not self.players_objects:
            return
            
        # Find all non-bankrupt players
        active_players: List[Player] = [p for p in self.players_objects if not p.get_is_bankrupt()]
        
        # Check if game is over (only one player left)
        if len(active_players) <= 1:
            print("Game over! Only one player remains.")
            return
            
        # Find the next non-bankrupt player
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players_objects)
            if not self.players_objects[self.current_player_index].get_is_bankrupt():
                break
                
        # Set the new current player
        self.current_player = self.players_objects[self.current_player_index]
        print(f"Current Player: {self.current_player.get_name()}")
        