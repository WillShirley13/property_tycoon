from pyexpat import errors
import pygame
import sys
import os
from typing import List, Optional, Tuple, Dict, Any, Union

from backend.enums.game_token import GameToken
from frontend.main_game_display_components.board_component import Board
from frontend.main_game_display_components.all_players_component import PlayerDisplay
from frontend.main_game_display_components.game_menu_component import GameMenuDisplay
from frontend.helpers.space_data import SPACE_COLORS
from backend.property_owners.player import Player
from backend.property_owners.bank import Bank
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.non_ownables.game_card import GameCard
from backend.ownables.ownable import Ownable
from frontend.main_game_display_components.current_player_component import (
    CurrentPlayerDisplay,
)
from frontend.main_game_display_components.popups.jail_popup import JailPopup
from frontend.main_game_display_components.dice_component import DiceManager
from frontend.main_game_display_components.popups.sell_asset_popup import (
    SellOrMortgagePopup,
)
from frontend.main_game_display_components.popups.game_card_popup import GameCardPopup
from frontend.main_game_display_components.popups.go_popup import GoPopup
from frontend.main_game_display_components.popups.jail_visit_popup import JailVisitPopup
from frontend.main_game_display_components.popups.free_parking_popup import (
    FreeParkingPopup,
)


# Temporary helper method to populate player with assets for testing the sell/mortgage popup
def temp_method_to_test_sell_or_mortgage_popup(
    current_player: Player, bank: Bank
) -> None:
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
    # mortgage 12 properties
    for prop_group in current_player.get_owned_properties().values():
        # Create a copy of the property group for iteration
        properties_to_process = prop_group.copy()
        for prop in properties_to_process:
            if count <= 12:
                current_player.mortgage_property(prop, bank)
                count += 1


class MainGameDisplay:
    # Initialize the main game display with all necessary components and game state
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        screen: pygame.Surface,
        player_data: List[Tuple[str, Any]],
        admin: Optional[Any] = None,
    ):
        # Store screen and dimensions
        self.screen: pygame.Surface = screen
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.player_data: List[Tuple[str, Any]] = player_data
        self.admin: Optional[Any] = admin
        self.running: bool = True

        # Initialize the game board component
        self.board: Board = Board(screen_width, screen_height, screen)

        # Store space centers for positioning game pieces
        self.center_spaces: Optional[Dict[int, Tuple[int, int]]] = (
            self.board.get_space_centers()
        )

        # Initialize the player information display
        self.player_display: PlayerDisplay = PlayerDisplay(
            15,  # X position
            20,  # Y position
            screen,  # Pass screen to the component
            screen_width / 5,  # Width (20% of screen)
            85 * 5,  # Height (adjusted for player count)
        )

        # Position current player display below the player list
        player_display_bottom: float = (
            self.player_display.y + self.player_display.height
        )
        current_player_display_y: float = (
            player_display_bottom + 20
        )  # Add spacing between components

        # Initialize current player information display
        self.current_player_display: CurrentPlayerDisplay = CurrentPlayerDisplay(
            15,  # Same X position as player display
            current_player_display_y,  # Y position calculated from player display
            screen,  # Pass screen to the component
            screen_width / 5,  # Same width as player display
            screen_height / 4,  # Height (25% of screen)
        )

        # Initialize game menu component
        self.game_menu: GameMenuDisplay = GameMenuDisplay(
            self.screen_width - screen_width / 5 - 15,
            20,
            screen,
            screen_width / 5,
            screen_height / 3,
        )

        # Initialize dice manager for rolling dice
        self.dice_manager: DiceManager = DiceManager(
            screen_width,
            screen_height,
            self.screen,
            dice_size=60,
            dice_spacing=20,
            color=(200, 50, 50),
        )

        # Initialize jail popup for when players land on jail
        self.jail_popup: JailPopup = JailPopup(
            screen_width // 2 - 175,  # Centered horizontally
            screen_height // 2 - 150,  # Centered vertically
            350,  # Width
            300,  # Height
            self.screen,
        )

        # Initialize sell/mortgage popup for property management
        self.sell_or_mortgage_popup: SellOrMortgagePopup = SellOrMortgagePopup(
            screen_width // 2 - 225,  # Centered horizontally
            screen_height // 2 - 300,  # Centered vertically
            450,  # Width
            600,  # Height
            self.screen,
        )

        # Initialize game card popup for when players land on game card spaces
        self.game_card_popup: GameCardPopup = GameCardPopup(
            screen_width // 2 - 175,  # Centered horizontally
            screen_height // 2 + 60,  # Centered vertically
            350,  # Width
            175,  # Height
            self.screen,
        )

        # Initialize go popup for when players land on go spaces
        self.go_popup: GoPopup = GoPopup(
            screen_width // 2 - 175,  # Centered horizontally
            screen_height // 2 + 60,  # Centered vertically
            350,  # Width
            175,  # Height
            self.screen,
        )

        # Initialize jail visit popup for when players land on jail spaces
        self.jail_visit_popup: JailVisitPopup = JailVisitPopup(
            screen_width // 2 - 175,  # Centered horizontally
            screen_height // 2 + 60,  # Centered vertically
            350,  # Width
            175,  # Height
            self.screen,
        )

        # initialize free parking popup for when players land on free parking spaces
        self.free_parking_popup: FreeParkingPopup = FreeParkingPopup(
            screen_width // 2 - 175,  # Centered horizontally
            screen_height // 2 + 60,  # Centered vertically
            350,  # Width
            175,  # Height
            self.screen,
        )

        # Initialize game flow tracking variables
        self.current_player: Optional[Player] = None
        self.current_player_index: int = 0
        self.current_player_turn_finished: bool = False
        self.players_objects: List[Tuple[Player, pygame.Surface]] = []

        # Store reference to game admin
        self.admin = admin

        # Get game state from admin
        raw_players = admin.get_players()
        self.bank = admin.get_bank()
        self.game_board = admin.get_game_board()
        self.game_space_helper = admin.get_game_space_helper()
        self.time_limit = admin.get_time_limit()
        self.free_parking = admin.get_free_parking()
        self.go = admin.get_go()
        self.jail = admin.get_jail()
        self.pot_luck_cards = admin.get_pot_luck_cards()
        self.opportunity_knocks = admin.get_opportunity_knocks()

        # Load player tokens and create player objects with tokens
        self.load_player_tokens(raw_players)

        # Initialize game flow with the first player
        if self.players_objects:
            self.current_player_index = 0
            # current_player is a tuple of (player, player_token_png)
            self.current_player = self.players_objects[self.current_player_index]

        # Property card display in bottom right corner
        self.property_card: pygame.image.load | None = None

    # Load token images for each player and create players_objects list
    def load_player_tokens(self, players: List[Player]) -> None:
        """Load token images for each player and create players_objects list."""
        game_piece_pngs: List[str] = [
            "boot.png",
            "cat.png",
            "iron.png",
            "tophat.png",
            "smartphone.png",
            "boat.png",
        ]

        for player in players:
            game_token: GameToken = player.get_game_token()
            token_png_path = ""

            # Get the corresponding PNG file for this token
            match game_token:
                case GameToken.BOOT:
                    token_png_path = game_piece_pngs[0]
                case GameToken.CAT:
                    token_png_path = game_piece_pngs[1]
                case GameToken.IRON:
                    token_png_path = game_piece_pngs[2]
                case GameToken.TOPHAT:
                    token_png_path = game_piece_pngs[3]
                case GameToken.SMARTPHONE:
                    token_png_path = game_piece_pngs[4]
                case GameToken.BOAT:
                    token_png_path = game_piece_pngs[5]

            # Load and scale the token image
            token_png = pygame.image.load(
                f"src/frontend/art_assets/game_pieces/{token_png_path}"
            ).convert_alpha()
            token_png = pygame.transform.scale(token_png, (40, 40))

            # Add player and token to the players_objects list
            self.players_objects.append((player, token_png))

    # Draw all game components to the screen
    def draw(self) -> None:
        # Clear the screen with a white background
        self.screen.fill((255, 255, 255))

        # Draw the game board
        self.board.draw()

        # Draw player game pieces on the board
        for player, token_png in self.players_objects:
            # Get the player's position on the board
            position_index = player.get_current_position()
            # Get the coordinates for this position
            if position_index in self.center_spaces:
                # Position based on space center coordinates
                x, y = self.center_spaces[position_index]
                # Center the token on these coordinates
                token_width, token_height = token_png.get_size()
                token_x = x - token_width // 2
                token_y = y - token_height // 2
                self.screen.blit(token_png, (token_x, token_y))

        # Draw the player list display
        self.player_display.draw(self.player_data)

        # Draw current player information if available
        if self.players_objects and self.current_player[0]:
            self.current_player_display.draw(self.current_player[0])

        # Draw the dice
        self.dice_manager.draw()

        # Draw the property card, if it exists
        if self.property_card:
            self.screen.blit(
                self.property_card,
                (
                    self.screen.get_width() - self.screen.get_width() / 5 - 15,
                    self.screen.get_height() - self.screen.get_height() / 2 - 15,
                ),
            )
            
        # Draw the game menu
        mouse_pos = pygame.mouse.get_pos()
        self.game_menu.draw(mouse_pos)

    # Process dice roll action and update player position
    def handle_dice_roll(self) -> None:
        print("Handling dice roll...")
        current_player = self.current_player
        dice_roll_info = current_player[0].move_player(self.go, self.bank)

        if dice_roll_info is None:
            # player rolled 3 doubles and goes to jail
            print("Player rolled 3 doubles, going to jail!")
            self.jail.put_in_jail(current_player[0])
            # Move to next player
            self.current_player_index += 1
            if self.current_player_index >= len(self.players_objects):
                self.current_player_index = 0
            self.current_player = self.players_objects[self.current_player_index]
            # Redraw the screen to update positions
            self.draw()
            pygame.display.update()
        else:
            dice_rolls, new_position_index = dice_roll_info
            # The player's position has already been updated in the player object
            print(f"Player now at position: {new_position_index}")

            # Update the dice visuals with the rolled values
            self.dice_manager.draw(dice_rolls[0], dice_rolls[1])

            # Redraw everything to show the new player position and dice
            self.draw()
            pygame.display.update()

    # Handle jail actions if player is currently in jail
    def handle_is_in_jail(self) -> None:
        if self.current_player[0].get_is_in_jail():
            # Show the jail popup and get the player's decision
            result = self.jail_popup.show(
                self.current_player[0], self.jail, self.free_parking, self.bank
            )
            print(f"result from jail popup: {result}")
            if result == "stayed":
                self.next_players_turn()
            elif result == "used_card":
                self.jail.player_used_get_out_of_jail_card(self.current_player[0])
            # Remove the duplicate call to pay_fine_for_release - the jail popup already handles this
            # The jail popup will set result to 'paid_fine' only if the payment was successful
            # If we reach here with result == 'paid_fine', the payment already succeeded

    # Process events based on player's new position on the board
    def handle_players_new_position(self) -> None:
        space_on_board: Ownable | FreeParking | Jail | Go | GameCard = self.game_board[
            self.current_player[0].get_current_position()
        ]

        match space_on_board:
            case Ownable():
                # Draw the property image
                self.property_card = pygame.image.load(
                    f"src/frontend/art_assets/property_cards/{space_on_board.png_name}"
                ).convert_alpha()
                self.property_card = pygame.transform.scale(
                    self.property_card,
                    (self.screen.get_width() / 5, self.screen.get_height() / 2),
                )

                print(
                    f"{self.current_player[0].get_name()} landed on {space_on_board.get_name()}, which is an ownable property."
                )
                # Player landed on an ownable property that is owned by themselves
                if space_on_board.get_owner() == self.current_player[0]:
                    print(
                        f"{self.current_player[0].get_name()} landed on their own property, {space_on_board.get_name()}. No action required."
                    )
                    return
                # Player landed on an ownable property that is owned by the bank
                elif space_on_board.get_owner() == self.bank:
                    print(
                        f"{self.current_player[0].get_name()} landed on a property that is owned by the bank, {space_on_board.get_name()}. Offer to purchase the property."
                    )
                    # OR AUCTION
                    return
                # Player landed on an ownable property that is owned by another player
                else:
                    print(
                        f"{self.current_player[0].get_name()} landed on {space_on_board.get_name()} and is being charged rent"
                    )
                    return
            case FreeParking():
                print(
                    f"{self.current_player[0].get_name()} landed on Free Parking. All previous fines that have been collected are now being paid out to the player."
                )
                self.free_parking.payout_fines(self.current_player[0])
                self.free_parking_popup.show(self.current_player[0])
            case Jail():
                print(f"{self.current_player[0].get_name()} is just visiting Jail.")
                self.jail_visit_popup.show(self.current_player[0])
            case Go():
                print(
                    f"{self.current_player[0].get_name()} landed on Go and collects £200!"
                )
                self.go_popup.show(self.current_player[0])
            case GameCard():
                print(
                    f"{self.current_player[0].get_name()} landed on a Game Card space. Drawing a card..."
                )
                self.game_card_popup.show(self.current_player[0])
            case _:
                print(
                    f"{self.current_player[0] .get_name()} landed on an unknown space."
                )

    # Process game events and redraw the display
    def handle_events(self) -> bool:
        # Make sure the game is displayed
        self.draw()

        # Check if current player is in jail and show jail popup if needed
        self.handle_is_in_jail()

        return True

    # Advance to the next player's turn
    def next_players_turn(self) -> None:
        self.current_player_index += 1
        if self.current_player_index >= len(self.players_objects):
            self.current_player_index = 0
        self.current_player = self.players_objects[self.current_player_index]

    # Main game loop to run the game
    def run(self) -> None:
        # Start the game timer if a time limit was set
        if self.admin and self.admin.get_time_limit() > 0:
            self.admin.start_timer()

        # Main game loop
        clock: pygame.time.Clock = pygame.time.Clock()
        while self.running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUIT event detected in main game loop")
                    self.running = False
                    break
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):  # Left mouse button
                    # Check if dice button was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if self.dice_manager.button_rect.collidepoint(mouse_pos):
                        print("Dice button clicked!")  # Debug message
                        self.handle_dice_roll()
                        # Handle the player's new position on the board
                        self.handle_players_new_position()
                        # Move to next player's turn
                        self.next_players_turn()

                    # Check if game menu button was clicked
                    self.game_menu.handle_click(mouse_pos)

            if not self.running:
                break

            # Handle game-specific events
            self.handle_events()

            # Draw the game display
            self.draw()

            # Update the display
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        # Clean up
        print("Exiting game...")
        pygame.quit()
        sys.exit()
