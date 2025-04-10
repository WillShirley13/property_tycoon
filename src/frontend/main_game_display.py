import os
import sys
from pyexpat import errors
from typing import Any, Dict, List, Optional, Tuple, Union

import pygame

from backend.enums.game_token import GameToken
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.game_card import GameCard
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.ownables.ownable import Ownable
from backend.ownables.property import Property
from backend.property_owners.bank import Bank
from backend.property_owners.player import Player
from frontend.helpers.space_data import SPACE_COLORS
from frontend.main_game_display_components.all_players_component import \
    PlayerDisplay
from frontend.main_game_display_components.board_component import Board
from frontend.main_game_display_components.current_player_component import \
    CurrentPlayerDisplay
from frontend.main_game_display_components.dice_component import DiceManager
from frontend.main_game_display_components.game_menu_component import \
    GameMenuDisplay
from frontend.main_game_display_components.popups.auction_popup import \
    AuctionPopup
from frontend.main_game_display_components.popups.bankrupt_popup import \
    BankruptPopup
from frontend.main_game_display_components.popups.buy_property_popup import \
    BuyPropertyPopup
from frontend.main_game_display_components.popups.free_parking_popup import \
    FreeParkingPopup
from frontend.main_game_display_components.popups.game_card_popup import \
    GameCardPopup
from frontend.main_game_display_components.popups.go_popup import GoPopup
from frontend.main_game_display_components.popups.jail_popup import JailPopup
from frontend.main_game_display_components.popups.jail_visit_popup import \
    JailVisitPopup
from frontend.main_game_display_components.popups.rent_paid_popup import \
    RentPaidPopup
from frontend.main_game_display_components.popups.sell_asset_popup import \
    SellOrMortgagePopup
from frontend.main_game_display_components.popups.upgrade_popup import \
    UpgradePropertyPopup
from frontend.main_game_display_components.popups.player_properties_popup import \
    PlayerPropertiesPopup

# Define base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art_assets")
GAME_PIECES_DIR = os.path.join(ASSETS_DIR, "game_pieces")
PROPERTY_CARDS_DIR = os.path.join(ASSETS_DIR, "property_cards")

class MainGameDisplay:
    # Set up the main game display with all necessary components and
    # game state
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
        self.time_is_up: bool = False

        # Load and scale the background image
        self.background = pygame.image.load(
            os.path.join(ASSETS_DIR, "background.png")).convert()
        self.background = pygame.transform.scale(
            self.background, (screen_width, screen_height))

        # Set up the game board component
        self.board: Board = Board(screen_width, screen_height, screen)

        # Store space centers for positioning game pieces
        self.center_spaces: Optional[Dict[int,
                                          Tuple[int, int]]] = self.board.get_space_centers()

        # game flow tracking variables
        self.current_player: Optional[Player] = None
        self.current_player_index: int = 0
        self.current_player_turn_finished: bool = False
        self.players_objects: List[Tuple[Player, pygame.Surface]] = []

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

        # Set up game flow with the first player
        if self.players_objects:
            self.current_player_index = 0
            # current_player is a tuple of (player, player_token_png)
            self.current_player = self.players_objects[self.current_player_index]

        # Property card display in bottom right corner
        self.property_card: pygame.image.load | None = None

        # Set up the player information display
        self.player_display: PlayerDisplay = PlayerDisplay(
            15,  # X position
            20,  # Y position
            screen,
            screen_width / 5,  # Width
            85 * 5,  # Height
        )

        # Position current player display below the player list
        player_display_bottom: float = self.player_display.y + \
            self.player_display.height
        current_player_display_y: float = player_display_bottom + \
            20  # Add spacing between components

        # current player information display
        self.current_player_display: CurrentPlayerDisplay = CurrentPlayerDisplay(
            15,  # Same X position as player display
            current_player_display_y,  # Y position calculated from player display
            screen,
            screen_width / 5,  # Width
            screen_height / 4,  # Height
        )

        # game menu component
        self.game_menu: GameMenuDisplay = GameMenuDisplay(
            self.screen_width - screen_width / 5 - 15,  # X position
            20,  # Y position
            screen,
            screen_width / 5,  # Width
            screen_height * 0.40,  # Height
            self.time_limit,  # Time limit
        )

        # dice manager for rolling dice
        self.dice_manager: DiceManager = DiceManager(
            screen_width,  # X position
            screen_height,  # Y position
            self.screen,
            dice_size=80,  # Dice size
            dice_spacing=20,  # Dice spacing
        )

        # jail popup for when players land on jail
        self.jail_popup: JailPopup = JailPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 - 150,  # Y position
            350,  # Width
            300,  # Height
            self.screen,
        )

        # sell/mortgage popup for property management
        self.sell_or_mortgage_popup: SellOrMortgagePopup = SellOrMortgagePopup(
            screen_width // 2 - 225,  # X position
            screen_height // 2 - 300,  # Y position
            450,  # Width
            600,  # Height
            self.screen,
        )

        # upgrade property popup for when players land on upgrade property
        # spaces
        self.upgrade_property_popup: UpgradePropertyPopup = UpgradePropertyPopup(
            screen_width // 2 - 225,  # X position
            screen_height // 2 - 150,  # Y position
            450,  # Width
            300,  # Height
            self.screen,
        )
        # buy property popup for when players land on buy property
        # spaces
        self.buy_property_popup: BuyPropertyPopup = BuyPropertyPopup(
            screen_width // 2 - 225,  # X position
            screen_height // 2 - 150,  # Y position
            450,  # Width
            300,  # Height
            self.screen,
        )

        # auction popup for when players land on auction spaces
        self.auction_popup: AuctionPopup = AuctionPopup(
            screen_width // 2 - 225,  # X position
            screen_height // 2 - 150,  # Y position
            450,  # Width
            400,  # Height
            self.screen,
        )

        # game card popup for when players land on game card spaces
        self.game_card_popup: GameCardPopup = GameCardPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 + 60,  # Y position
            500,  # Width
            350,  # Height
            self.screen,
        )

        # go popup for when players land on go spaces
        self.go_popup: GoPopup = GoPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 + 60,  # Y position
            350,  # Width
            175,  # Height
            self.screen,
        )

        # jail visit popup for when players land on jail spaces
        self.jail_visit_popup: JailVisitPopup = JailVisitPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 + 60,  # Y position
            350,  # Width
            175,  # Height
            self.screen,
        )

        # free parking popup for when players land on free parking
        # spaces
        self.free_parking_popup: FreeParkingPopup = FreeParkingPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 + 60,  # Y position
            350,  # Width
            175,  # Height
            self.screen,
        )

        # rent paid popup for when players land on other player's
        # property
        self.rent_paid_popup: RentPaidPopup = RentPaidPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 - 100,  # Y position
            350,  # Width
            225,  # Height
            self.screen,
        )

        # bankrupt popup for when players go bankrupt
        self.bankrupt_popup: BankruptPopup = BankruptPopup(
            screen_width // 2 - 175,  # X position
            screen_height // 2 - 100,  # Y position
            350,  # Width
            175,  # Height
            self.screen,
        )

    # Load token images for each player and create players_objects
    # list
    def load_player_tokens(self, players: List[Player]) -> None:
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
                os.path.join(GAME_PIECES_DIR, token_png_path)).convert_alpha()
            token_png = pygame.transform.scale(token_png, (40, 40))

            # Add player and token to the players_objects list
            self.players_objects.append((player, token_png))

    # Draw all game components to the screen
    def draw(self) -> None:
        # Draw the background image
        self.screen.blit(self.background, (0, 0))

        # Draw the game board
        self.board.draw(self.game_board)

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
        self.player_data = []
        for player, token_png in self.players_objects:
            if not player.get_is_bankrupt():
                self.player_data.append(
                    (f'{player.get_name()} (£{player.get_cash_balance()})', player.get_game_token()))
            else:
                self.player_data.append(
                    (f"{player.get_name()} (Bankrupt)", player.get_game_token()))
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
        current_player = self.current_player
        dice_roll_info = current_player[0].move_player(
            self.go, self.bank)
        print(
            f"dice_roll_info: {dice_roll_info} for {
                current_player[0].get_name()}")

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
            # The player's position has already been updated in the player
            # object
            print(f"Player now at position: {new_position_index}")

            # Update the dice visuals with the rolled values
            self.dice_manager.draw(dice_rolls[0], dice_rolls[1])

            # Redraw everything to show the new player position and
            # dice
            self.draw()
            pygame.display.update()

    # Handle jail actions if player is currently in jail
    def handle_is_in_jail(self) -> None:
        if self.current_player[0].get_is_in_jail():
            # Show the jail popup and get the player's decision
            result = self.jail_popup.show(
                self.current_player[0],
                self.jail,
                self.free_parking,
                self.bank,
                self.go)
            print(f"result from jail popup: {result}")

            # Check if player is bankrupt after the jail popup
            if self.current_player[0].get_is_bankrupt(
            ) or result == "bankrupt":
                print(
                    "Player has been declared bankrupt after jail interaction")
                self.next_players_turn()
                return

            # Handle other jail popup results
            if result == "stayed":
                self.next_players_turn()
            elif result == "used_card":
                self.jail.player_used_get_out_of_jail_card(
                    self.current_player[0], self.go, self.bank)

    # Process events based on player's new position on the board
    def handle_players_new_position(self) -> None:
        space_on_board: Ownable | FreeParking | Jail | Go | GameCard = self.game_board[
            self.current_player[0].get_current_position()]
        match space_on_board:
            case Ownable():
                # Draw the property image (only if the player landed on an
                # ownable property)
                self.property_card = pygame.image.load(
                    os.path.join(PROPERTY_CARDS_DIR, space_on_board.png_name)).convert_alpha()
                self.property_card = pygame.transform.scale(
                    self.property_card,
                    (self.screen.get_width() / 5,
                     self.screen.get_height() / 2),
                )
                # Player landed on an ownable property that is owned by
                # themselves. Do nothing.
                if space_on_board.get_owner(
                ) == self.current_player[0]:
                    print(
                        f"{
                            self.current_player[0].get_name()} landed on their own property, {
                            space_on_board.get_name()}. No action required.")
                    return
                # Player landed on an ownable property that is owned by the
                # bank. Offer to purchase the property.
                elif space_on_board.get_owner() == self.bank:
                    print(
                        f"{
                            self.current_player[0].get_name()} landed on a property that is owned by the bank, {
                            space_on_board.get_name()}. Offer to purchase the property.")
                    # buy_property_popup.show() returns True if the player buys
                    # the property, False if they don't
                    if self.current_player[0].get_is_first_circuit_complete(
                    ):
                        move_to_auction = self.buy_property_popup.show(
                            space_on_board, self.current_player[0], self.bank)
                        if not move_to_auction:
                            self.auction_popup.show(
                                self.current_player[0],
                                [player[0] for player in self.players_objects if player[0]
                                    != self.current_player[0]],
                                space_on_board,
                                self.bank,
                            )
                    return
                # Player landed on an ownable property that is owned by another
                # player. Charge rent.
                else:
                    try:
                        print(
                            f"{
                                self.current_player[0].get_name()} landed on {
                                space_on_board.get_name()} and is being charged rent of £{
                                space_on_board.get_rent_cost()}.")
                        if not space_on_board.get_is_mortgaged(
                        ) and not space_on_board.get_owner().get_is_in_jail():
                            print("Showing rent paid popup")
                            self.rent_paid_popup.show(
                                self.current_player[0], space_on_board, self.bank)
                    except Exception as e:
                        print(f"Error processing rent: {e}")
                    return
            # Player landed on Free Parking. Pay out fines.
            case FreeParking():
                print(
                    f"{self.current_player[0].get_name()} landed on Free Parking. All previous fines that have been collected are now being paid out to the player.")
                self.free_parking.payout_fines(self.current_player[0])
                self.free_parking_popup.show(
                    self.current_player[0],
                    self.free_parking.get_fines_collected())
            # Player landed on Jail. Visit Jail.
            case Jail():
                # if player landed on jail space, put them in jail
                if self.current_player[0].get_current_position() == 30:
                    self.jail.put_in_jail(self.current_player[0])
                    self.current_player[0].move_player_to_position(10, self.go, self.bank)
                else:
                    # if player landed on visiting jail space, visit jail
                    print(
                    f"{self.current_player[0].get_name()} is just visiting Jail.")
                    self.jail_visit_popup.show(self.current_player[0])
            # Player landed on Go.
            case Go():
                print(
                    f"{self.current_player[0].get_name()} landed on Go and collects £200!")
                self.go_popup.show(self.current_player[0])
            # Player landed on a Game Card. Draw a card.
            case GameCard():
                # pot luck card positions on board
                pot_luck_card_positions = [0, 17, 33]
                # opportunity knocks card positions on board
                opportunity_knocks_card_positions = [7, 22, 36]
                if self.game_space_helper[space_on_board] in pot_luck_card_positions:
                    card_info = self.pot_luck_cards.get_card()
                    self.game_card_popup.show(
                        self.current_player[0],
                        self.bank,
                        self.free_parking,
                        self.jail,
                        [player[0] for player in self.players_objects if player[0]
                            != self.current_player[0]],
                        card_info,
                        self.pot_luck_cards,
                        self.go,
                    )
                elif self.game_space_helper[space_on_board] in opportunity_knocks_card_positions:
                    card_info = self.opportunity_knocks.get_card()
                    self.game_card_popup.show(
                        self.current_player[0],
                        self.bank,
                        self.free_parking,
                        self.jail,
                        [player[0] for player in self.players_objects if player[0]
                            != self.current_player[0]],
                        card_info,
                        self.opportunity_knocks,
                        self.go,
                    )
                self.draw()
                pygame.display.update()
                print(
                    f"{self.current_player[0].get_name()} landed on a Game Card space. Drawing a card...")
            # Should never happen...
            case _:
                print(
                    f"{self.current_player[0] .get_name()} landed on an unknown space.")

    # Process game events and redraw the display
    def handle_events(self) -> bool:
        # Make sure the game is displayed
        self.draw()

        # Check if current player is in jail and show jail popup if
        # needed
        self.handle_is_in_jail()

        return True

    # Facilitate next player's turn
    def next_players_turn(self) -> None:
        if self.time_is_up and self.current_player_index == 0:
            print("Time limit reached! Game over.")
            # Determine the winner based on net worth
            winner = max(
                [player[0] for player in self.players_objects],
                key=lambda x: x.get_player_net_worth(),
            )
            # Show end of game popup with the winner
            from frontend.main_game_display_components.popups.end_of_game_popup import \
                EndOfGamePopup

        # Check if the current player is bankrupt
        if self.current_player[0].get_is_bankrupt():
            print("Current player is bankrupt")
            # Show the bankrupt popup
            self.bankrupt_popup.show(self.current_player[0])
            # Remove the bankrupt player from the game
            self.players_objects.remove(self.current_player)
            # Adjust the index to account for the removed player
            self.current_player_index -= 1

        if len(self.players_objects) == 1:
            # determine the winner
            winner = self.players_objects[0][0]
            print(f"Game over! {winner.get_name()} is the winner!")
            # Show the end of game popup
            from frontend.main_game_display_components.popups.end_of_game_popup import \
                EndOfGamePopup

            end_game_popup = EndOfGamePopup(
                self.screen_width // 2 - 300,  # X position
                self.screen_height // 2 - 200,  # Y position
                600,  # Width
                400,  # Height
                self.screen,
                # Winner is the only player left
                self.players_objects[0][0],
            )
            end_game_popup.draw()
            pygame.display.flip()

            # Handle events until the popup is closed
            popup_active = True
            while popup_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    exit_game = end_game_popup.handle_event(event)
                    if exit_game:
                        popup_active = False
                pygame.time.Clock().tick(60)

            # Exit the game
            self.running = False
            return

        # Move to the next player
        self.current_player_index += 1
        if self.current_player_index >= len(self.players_objects):
            self.current_player_index = 0
        self.current_player = self.players_objects[self.current_player_index]

    # Main game loop to run the game
    def run(self) -> None:
        # Start the game timer if a time limit was set
        if self.admin and self.admin.get_time_limit() > 0:
            self.admin.start_timer()
            self.game_menu.start_timer()

        # Main game loop
        clock: pygame.time.Clock = pygame.time.Clock()
        while self.running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUIT event detected in main game loop")
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    # Check if dice button was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    if self.dice_manager.button_rect.collidepoint(
                            mouse_pos):
                        print("Dice button clicked!")  # Debug message
                        self.handle_dice_roll()
                        # Handle the player's new position on the
                        # board
                        self.handle_players_new_position()
                        if not self.current_player[0].get_is_in_jail(
                        ):
                            self.next_players_turn()

                        # If no properties are eligible for upgrade, show
                        # popup. else, don't.
                        has_property_to_upgrade = False
                        for property_group in self.current_player[0].get_owned_properties(
                        ).values():
                            for property in property_group:
                                if isinstance(
                                        property, Property) and property.get_is_eligible_for_upgrade():
                                    has_property_to_upgrade = True
                                    break
                        if has_property_to_upgrade:
                            self.upgrade_property_popup.show(
                                self.current_player[0], self.bank)
                            
                    clicked_player = self.player_display.get_player_at_pos(mouse_pos)
                    if clicked_player is not None:
                        player_name, token = clicked_player
                        selected_player_obj = next((p for p, _ in self.players_objects if p.get_name() == player_name), None)
                        if selected_player_obj:
                            print(f"Player {player_name} was clicked!")
                            player_properties_popup = PlayerPropertiesPopup(
                                self.screen_width // 2 - 225,
                                self.screen_height // 2 - 300,
                                450,
                                600,
                                self.screen,
                                selected_player_obj  # THIS IS THE REQUIRED PLAYER ARGUMENT
                            )
                            player_properties_popup.show()

                    # Check if game menu button was clicked
                    self.game_menu.handle_click(
                        mouse_pos, [player[0] for player in self.players_objects])

            if not self.running:
                break

            # Check if time limit is up
            if self.time_limit > 0:
                self.time_is_up = self.game_menu.update_timer()

            # Handle game-specific events
            self.handle_events()

            # Draw the game display
            self.draw()

            # Update the display
            pygame.display.flip()
            clock.tick(60)

        print("Exiting game...")
        pygame.quit()
        sys.exit()
