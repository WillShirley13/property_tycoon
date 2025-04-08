from typing import Dict, List, Optional, Tuple

import pygame

from backend.ownables.property import Property
from backend.property_owners.bank import Bank
from backend.property_owners.player import Player


class AuctionPopup:
    def __init__(self, x: int, y: int, width: int,
                 height: int, screen: pygame.Surface):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen

        # Store the auction result
        self.auction_result: Optional[Dict[str, any]] = None

        # Define color scheme for the popup
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (
            240,
            240,
            240,
        )  # Light gray background
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (
            0, 0, 0)  # Black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (
            0, 0, 0)  # Black text
        self.BUTTON_COLOR: Tuple[int, int, int] = (0, 100, 0)  # Dark green buttons
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            180,
            180,
            180,
        )  # Gray hover effect
        self.INPUT_BG_COLOR: Tuple[int, int, int] = (
            255,
            255,
            255,
        )  # White input box background

        # Define font sizes
        title_size: int = 20
        text_size: int = 16
        button_size: int = 14

        # Set fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", title_size, bold=True)
            self.text_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", text_size)
            self.button_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", button_size, bold=True)
        except BaseException:
            self.title_font = pygame.font.SysFont(
                None, title_size, bold=True)
            self.text_font = pygame.font.SysFont(None, text_size)
            self.button_font = pygame.font.SysFont(
                None, button_size, bold=True)

        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface(
            (width, self.height))

        # Configure input and button layout
        self.input_height: int = 30
        self.input_width: int = 100
        self.button_height: int = 40
        self.button_width: int = width - 40

        # Set up input fields and buttons
        self.input_fields: Dict[str, pygame.Rect] = {}
        self.input_texts: Dict[str, str] = {}
        self.input_active: Dict[str, bool] = {}
        self.submit_button: Optional[pygame.Rect] = None
        self.submit_hover: bool = False

    # Reset input fields and texts for a new auction
    def reset_inputs(self) -> None:
        self.input_fields = {}
        self.input_texts = {}
        self.input_active = {}
        self.submit_button = None
        self.submit_hover = False
        self.auction_result = None

    def draw(self, property_obj: Property,
             players: List[Player], current_player: Player) -> None:
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )

        # Draw title
        title_text: str = f"Auctioning {property_obj.get_name()}..."
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.width // 2, 40))
        self.popup_surface.blit(title_surface, title_rect)

        # Draw property details
        details = [
            f"Property Group: {
                property_obj.get_property_group().value.capitalize()}",
            f"Current Value: £{property_obj.get_cost()}",
            f"Rent: £{property_obj.get_rent_cost()}",
        ]

        y_position = 80
        for detail in details:
            detail_surface = self.text_font.render(
                detail, True, self.POPUP_TEXT_COLOR)
            detail_rect = detail_surface.get_rect(
                left=20, top=y_position)
            self.popup_surface.blit(detail_surface, detail_rect)
            y_position += 25

        # Draw bid inputs for each player (except current player)
        y_position += 20

        # Set up input fields for all players (except current player)
        for player in players:
            if player != current_player:
                if player.get_name() not in self.input_fields:
                    input_rect = pygame.Rect(
                        self.width - self.input_width - 20,
                        y_position,
                        self.input_width,
                        self.input_height,
                    )
                    self.input_fields[player.get_name()] = input_rect
                    if player.get_name() not in self.input_texts:
                        self.input_texts[player.get_name()] = ""
                    if player.get_name() not in self.input_active:
                        self.input_active[player.get_name()] = False
                    y_position += 40

        # Draw the input fields
        y_position = 180
        for player in players:
            if player != current_player:
                # Player name and cash balance
                player_text = f"{player.get_name()}'s bid:"
                player_surface = self.text_font.render(
                    player_text, True, self.POPUP_TEXT_COLOR)
                player_rect = player_surface.get_rect(
                    left=20, top=y_position)
                self.popup_surface.blit(player_surface, player_rect)
                
                # Display player's cash balance
                balance_text = f"£{player.get_cash_balance()}"
                balance_surface = self.text_font.render(
                    balance_text, True, self.POPUP_TEXT_COLOR)
                balance_rect = balance_surface.get_rect(
                    left=20, top=y_position + 20)
                self.popup_surface.blit(balance_surface, balance_rect)

                # Get the input field
                input_rect = self.input_fields[player.get_name()]
                input_rect.y = y_position  # Update y position

                # Draw input field with different color when active
                bg_color = (220, 255, 220) if self.input_active.get(
                    player.get_name(), False) else self.INPUT_BG_COLOR
                pygame.draw.rect(
                    self.popup_surface, bg_color, input_rect, 0, 5)

                # Draw border
                pygame.draw.rect(
                    self.popup_surface,
                    self.POPUP_BORDER_COLOR,
                    input_rect,
                    1,
                    5)

                # Draw input text
                if self.input_texts[player.get_name()]:
                    # Mask the actual bid with asterisks
                    text_to_display = "*" * len(self.input_texts[player.get_name()])
                else:
                    text_to_display = "Enter bid..." if self.input_active[player.get_name()] else ""
                
                text_surface = self.text_font.render(
                    text_to_display, True, self.POPUP_TEXT_COLOR)
                text_rect = text_surface.get_rect(
                    left=input_rect.left + 5, top=input_rect.top + 5)
                self.popup_surface.blit(text_surface, text_rect)

                y_position += 40

        # Draw submit button
        self.submit_button = pygame.Rect(
            20,
            self.height - self.button_height - 20,
            self.button_width,
            self.button_height,
        )

        # Calculate mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y)
        self.submit_hover = self.submit_button.collidepoint(
            relative_mouse_pos)

        button_color = self.BUTTON_HOVER_COLOR if self.submit_hover else self.BUTTON_COLOR

        # Draw button with rounded corners
        pygame.draw.rect(
            self.popup_surface,
            button_color,
            self.submit_button,
            0,
            5)
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            self.submit_button,
            1,
            5)

        # Add text to the button
        text_surface = self.button_font.render(
            "Submit Bids", True, self.POPUP_TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=self.submit_button.center)

        self.popup_surface.blit(text_surface, text_rect)

        # Display the popup on the screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    # Handle events for the auction popup
    def handle_events(self, event: pygame.event.Event,
                      players: List[Player]) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            # Calculate relative mouse position
            relative_mouse_pos = (
                mouse_pos[0] - self.x,
                mouse_pos[1] - self.y)

            # Check if submit button was clicked
            if self.submit_button.collidepoint(relative_mouse_pos):
                # Validate all bids
                valid_bids = {}
                for player_name, bid_text in self.input_texts.items():
                    try:
                        # If bid is empty or non-numeric, skip it
                        if not bid_text.strip():
                            continue
                            
                        bid = int(bid_text)
                        
                        # Find the player object
                        current_player = None
                        for player in players:
                            if player.get_name() == player_name:
                                current_player = player
                                break
                        
                        # Check if player has valid bid
                        if current_player and bid > 0:
                            # If bid exceeds cash balance, use all cash
                            if bid > current_player.get_cash_balance():
                                bid = current_player.get_cash_balance()
                            valid_bids[current_player] = bid
                    except ValueError:
                        continue

                if valid_bids:
                    # Find highest bidder
                    # compare each bid (value for player:bid
                    # dictionary)
                    highest_bidder = max(
                        valid_bids.items(), key=lambda x: x[1])
                    self.auction_result = {
                        "winner": highest_bidder[0],
                        "amount": highest_bidder[1],
                        "bids": valid_bids,
                    }
                return True

            # Check if any input field was clicked
            for player_name, input_rect in self.input_fields.items():
                if input_rect.collidepoint(relative_mouse_pos):
                    self.input_active[player_name] = True
                    for other_player in self.input_active:
                        if other_player != player_name:
                            self.input_active[other_player] = False
                    break
            else:
                # Deactivate all input fields if clicking elsewhere
                for player_name in self.input_active:
                    self.input_active[player_name] = False

        elif event.type == pygame.KEYDOWN:
            # Handle text input for active input field
            for player_name, is_active in self.input_active.items():
                if is_active:
                    # if enter key is pressed, deactivate input field
                    if event.key == pygame.K_RETURN:
                        self.input_active[player_name] = False
                    # if backspace key is pressed, remove last character
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_texts[player_name] = self.input_texts[player_name][:-1]
                    # Only accept numeric characters
                    elif event.unicode.isdigit():
                        # Find the current player to check their balance
                        current_player = None
                        for player in players:
                            if player.get_name() == player_name:
                                current_player = player
                                break
                        
                        # Allow input, and if it exceeds cash balance, just use all cash
                        if current_player:
                            # Add the digit
                            self.input_texts[player_name] += event.unicode
                            
                            # Check if the bid exceeds player's cash balance
                            try:
                                bid_amount = int(self.input_texts[player_name])
                                if bid_amount > current_player.get_cash_balance():
                                    # Set the bid to the player's total cash
                                    self.input_texts[player_name] = str(current_player.get_cash_balance())
                            except ValueError:
                                pass

        return False

    # Display the auction popup and handle the auction process
    def show(
        self,
        current_player: Player,
        players: List[Player],
        property_obj: Property,
        bank: Bank,
    ) -> Optional[Dict[str, any]]:
        # Reset input fields for a new auction
        self.reset_inputs()
        
        clock = pygame.time.Clock()
        running = True

        while running:
            # Draw the popup
            self.draw(property_obj, players, current_player)

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if self.handle_events(event, players):
                    if self.auction_result:
                        self.auction_result["winner"].purchase_property(
                            property_obj, bank, self.auction_result["amount"])
                        print(
                            f"{
                                self.auction_result['winner'].get_name()} purchased {
                                property_obj.get_name()} for £{
                                self.auction_result['amount']}.")
                    running = False

            clock.tick(60)

        return self.auction_result
