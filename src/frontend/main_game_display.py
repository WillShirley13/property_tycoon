import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.enums.game_token import GameToken
from frontend.board import Board
from frontend.player_display import PlayerDisplay
from frontend.space_data import SPACE_COLORS
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.non_ownables.game_card import GameCard
from backend.ownables.ownable import Ownable
from frontend.current_player_display import CurrentPlayerDisplay
from backend.property_owners.player import Player
from frontend.jail_popup import JailPopup
from frontend.dice import DiceManager

class MainGameDisplay:
    def __init__(self, screen_width, screen_height, players, admin=None, center_spaces=None):
        """
        Initialize the main game display that integrates the board and player info.
        
        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
            players (list): List of tuples containing (player_name, game_token)
            admin: Admin object containing game state
        """
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.players_data = players
        self.admin = admin
        self.running = True
        self.center_spaces = center_spaces
        
        # Initialize display components
        self.board = Board(screen_width, screen_height)
        self.player_display = PlayerDisplay(
            15,
            20, 
            screen_width/5, # player_display width
            85 * 5 # player_display height
        )
        
        # Calculate the y position for current_player_display based on player_display's position and height
        player_display_bottom = self.player_display.y + self.player_display.height
        current_player_display_y = player_display_bottom + 20  # Add a 20px gap between components
        
        self.current_player_display = CurrentPlayerDisplay(
            15,                   
            current_player_display_y, # Dynamic positioning based on player_display height
            screen_width/5,                  
            screen_height/4                    
        )
        
        # Initialize dice manager
        self.dice_manager = DiceManager(self.screen_width, self.screen_height)
        
        # Initialize game flow variables
        self.current_player = None
        self.current_player_index = 0
        self.current_player_turn_finished = False
        self.players_objects = []
        
        # Game state data from Admin
        if admin:
            self.set_admin(admin)
    
    def draw(self, screen: pygame.Surface) -> None:
        # Fill the screen with the background color
        screen.fill((255, 255, 255))  # White background
        
        # Draw the board
        self.board.draw(screen)
        
        game_piece_pngs = ['boot.png', 'cat.png', 'iron.png', 'tophat.png', 'smartphone.png', 'boat.png']
        for player in self.players_objects:
            game_token = player.get_game_token()
            match game_token:
                case GameToken.BOOT:
                    game_piece_png = game_piece_pngs[0]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                    screen.blit(token_png, (self.center_spaces[0][0] - 60, self.center_spaces[0][1] + 20))
                case GameToken.CAT:
                    game_piece_png = game_piece_pngs[1]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                    screen.blit(token_png, (self.center_spaces[0][0] - 60, self.center_spaces[0][1] - 60))
                case GameToken.IRON:
                    game_piece_png = game_piece_pngs[2]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                    screen.blit(token_png, (self.center_spaces[0][0] + 20, self.center_spaces[0][1] + 20))
                case GameToken.HATSTAND:
                    game_piece_png = game_piece_pngs[3]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                    screen.blit(token_png, (self.center_spaces[0][0] + 20, self.center_spaces[0][1] - 60))
                case GameToken.SMARTPHONE:
                    game_piece_png = game_piece_pngs[4]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                    screen.blit(token_png, (self.center_spaces[0][0] , self.center_spaces[0][1]))
                case GameToken.BOAT:
                    game_piece_png = game_piece_pngs[5]
                    token_png = pygame.image.load(f'src/frontend/game_pieces/{game_piece_png}').convert_alpha()
                    token_png = pygame.transform.scale(token_png, (40, 40))
                    screen.blit(token_png, (self.center_spaces[0][0] + 20, self.center_spaces[0][1] + 20))
            
        
        # Draw the player display
        self.player_display.draw(screen, self.players_data)
        
        # Draw current player display if we have player objects
        if self.players_objects and self.current_player:
            self.current_player_display.draw(screen, self.current_player)
        
        # Draw the dice
        self.dice_manager.draw(screen)
        
    def handle_events(self, screen):
        """
        Handle game-specific events and game state changes.
        
        Returns:
            bool: True if the game should continue running, False if it should exit
        """
        # Handle keyboard events for game control
        keys = pygame.key.get_pressed()
        
        # For testing purposes - uncomment to test jail popup
        self.current_player.is_in_jail = True
        
        if self.current_player.get_is_in_jail():
            # First draw the main game display to ensure it's visible
            self.draw(screen)
            
            # Create and show the jail popup
            jail_popup = JailPopup(
                self.screen_width // 2 - 175,  # Center horizontally
                self.screen_height // 2 - 150,   # Center vertically
                350, 300  # Width and height adjusted for vertical buttons
            )
            
            # Show the popup and get the result
            result = jail_popup.show(screen, self.current_player)
            
        
        if keys[pygame.K_SPACE]:
            # Space key advances the turn
            self.current_player_turn_finished = True
            
        # Check if the current player's turn is finished
        if self.current_player_turn_finished:
            self.next_player()
            self.current_player_turn_finished = False  # Reset the flag for the next player
            
        # Return the running state
        return self.running

    def process_player_turn(self):
        # This method would contain the game flow logic for a player's turn
        # When all required actions for a turn are completed, set the flag
        
        # Example: After dice roll, movement, and any required actions
        if self.all_turn_actions_completed():
            self.current_player_turn_finished = True
    
    def all_turn_actions_completed(self):
        """
        Check if all required actions for the current player's turn are completed.
        This is a placeholder method that should be implemented with actual game logic.
        
        Returns:
            bool: True if all actions are completed, False otherwise
        """
        # Placeholder implementation - in a real game, this would check various conditions
        return False
        
    def next_player(self):
        """
        Move to the next player in the game.
        """
        if not self.admin or not self.players_objects:
            return
            
        # Move to next non-bankrupt player
        active_players = [p for p in self.players_objects if not p.get_is_bankrupt()]
        if len(active_players) <= 1:
            # Game over - only one player left
            print("Game over! Only one player remains.")
            return
            
        # Find next non-bankrupt player
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players_objects)
            if not self.players_objects[self.current_player_index].get_is_bankrupt():
                break
                
        self.current_player = self.players_objects[self.current_player_index]
        print(f"Current Player: {self.current_player.get_name()}")
        
    def set_admin(self, admin):
        """
        Set the admin object and initialize game state.
        
        Args:
            admin: Admin object containing game state
        """
        self.admin = admin
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
        
        # Initialize game flow
        if self.players_objects:
            self.current_player_index = 0
            self.current_player = self.players_objects[self.current_player_index] 