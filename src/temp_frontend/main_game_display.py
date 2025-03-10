import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.enums.game_token import GameToken
from temp_frontend.board import Board
from temp_frontend.player_display import draw_player_display
from temp_frontend.space_data import SPACE_COLORS
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.non_ownables.game_card import GameCard
from backend.ownables.ownable import Ownable
from temp_frontend.current_player_display import draw_current_player_display

class MainGameDisplay:
    def __init__(self, screen_width, screen_height, players, admin=None):
        """
        Initialize the main game display that integrates the board and player info.
        
        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
            players (list): List of tuples containing (player_name, game_token)
            admin: Admin object containing game state
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.players_data = players
        self.admin = admin
        
        # Game state data from Admin
        if admin:
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
            
            # Game flow state
            self.current_player_index = 0
            self.current_player = self.players_objects[self.current_player_index]
        else:
            # Default for initialization without admin
            self.current_player_index = 0
            self.current_player = None
        
        # Create the board
        self.board = Board(screen_width, screen_height)
        
        # Calculate display positions
        self.player_display_x = 20
        self.player_display_y = 20
        self.player_display_width = 250
        self.player_display_height = min(400, screen_height - 200)  # Ensure it fits on screen
        
        # Calculate current player display position (below player_display)
        self.current_player_display_x = self.player_display_x
        self.current_player_display_y = self.player_display_y + self.player_display_height + 20
        self.current_player_display_width = self.player_display_width
        self.current_player_display_height = 150
        
        self.current_player_turn_finished = False
        
    def draw(self, screen):
        """
        Draw the main game display including the board and player info.
        
        Args:
            screen (pygame.Surface): The game screen
        """
        # Fill the screen with the background color
        screen.fill(SPACE_COLORS["screen_bg"])
        
        # Draw the board
        self.board.draw(screen)
        
        # Draw the player display
        draw_player_display(
            screen, 
            self.players_data, 
            self.player_display_x, 
            self.player_display_y, 
            self.player_display_width, 
            self.player_display_height
        )
        
        # Draw current player display if we have player objects
        if self.current_player:
            draw_current_player_display(
                screen,
                self.current_player,
                self.current_player_display_x,
                self.current_player_display_y,
                self.current_player_display_width,
                self.current_player_display_height
            )
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Handle other events, but remove the space key handler
            
        # Check if the current player's turn is finished
        if self.current_player_turn_finished:
            self.process_player_turn()
            self.next_player()
            self.current_player_turn_finished = False  # Reset the flag for the next player

    def process_player_turn(self):
        # This method would contain the game flow logic for a player's turn
        # When all required actions for a turn are completed, set the flag
        
        return None
        
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
        self.current_player_index = 0
        self.current_player = self.players_objects[self.current_player_index] 