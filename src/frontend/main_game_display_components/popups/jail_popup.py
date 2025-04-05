from typing import Any, Optional, Tuple

import pygame

from backend.errors import InsufficientFundsError
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.property_owners.bank import Bank
from backend.property_owners.player import Player
from frontend.main_game_display_components.popups.sell_asset_popup import \
    SellOrMortgagePopup


class JailPopup:
    def __init__(self, x: int, y: int, width: int,
                 height: int, screen: pygame.Surface):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        # Store the player's jail decision
        self.result: Optional[str] = None

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
        self.BUTTON_COLOR: Tuple[int, int, int] = (
            0, 100, 0)  # Dark green buttons
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            180,
            180,
            180,
        )  # Gray hover effect
        self.BUTTON_DISABLED_COLOR: Tuple[int, int, int] = (
            150,
            150,
            150,
        )  # Gray for disabled buttons

        # Define font sizes
        title_size: int = 20
        button_size: int = 14

        # Set fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", button_size, bold=True)
        except BaseException:
            self.title_font = pygame.font.SysFont(
                None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(
                None, button_size, bold=True)

        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface(
            (width, height))

        # Configure button layout
        button_width: int = width - 40
        button_height: int = 50

        # Calculate vertical positions for the three buttons
        roll_y: int = 80
        card_y: int = roll_y + button_height + 10
        pay_y: int = card_y + button_height + 10

        # Create button rectangles for the jail options
        self.stay_in_jail_button: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + roll_y, button_width, button_height)
        self.use_card_button: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + card_y, button_width, button_height)
        self.pay_fine_button: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + pay_y, button_width, button_height)

        # Initialise hover states for buttons
        self.stay_in_jail_hover: bool = False
        self.use_card_hover: bool = False
        self.pay_fine_hover: bool = False

    # Draw the jail popup
    def draw(self, player: Player) -> None:
        pygame.draw.rect(
            self.screen,
            self.POPUP_BG_COLOR,
            (self.x, self.y, self.width, self.height),
            0,
            10,
        )
        pygame.draw.rect(
            self.screen,
            self.POPUP_BORDER_COLOR,
            (self.x, self.y, self.width, self.height),
            2,
            10,
        )

        # Draw title text
        title_text: str = "You're in Jail!"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.x + self.width // 2, self.y + 30))
        self.screen.blit(title_surface, title_rect)

        # Draw first option button: Stay in Jail
        self.draw_button(
            self.stay_in_jail_button,
            "Stay in Jail",
            self.stay_in_jail_hover,
            self.BUTTON_COLOR,
        )

        # Draw second option button: Use Get Out of Jail Free card (if player
        # has one, else disable button)
        has_card: bool = player.get_get_out_of_jail_cards() > 0
        card_color: Tuple[int, int,
                int] = self.BUTTON_COLOR if has_card else self.BUTTON_DISABLED_COLOR
        self.use_card_hover = self.use_card_hover if has_card else False
        self.draw_button(
            self.use_card_button,
            "Use Get Out of Jail Free Card",
            self.use_card_hover,
            card_color,
        )

        # Draw third option button: Pay fine (if player has enough
        # money)
        has_enough_money: bool = player.get_cash_balance() >= 50
        pay_color: Tuple[int, int,
                         int] = self.BUTTON_COLOR if has_enough_money else self.BUTTON_DISABLED_COLOR
        self.pay_fine_hover = self.pay_fine_hover if has_enough_money else False
        self.draw_button(
            self.pay_fine_button,
            "Pay £50 Fine",
            self.pay_fine_hover,
            pay_color)

    # Helper method to draw a button with specified text and state
    def draw_button(
        self,
        button_rect: pygame.Rect,
        text: str,
        hover: bool,
        color: Tuple[int, int, int],
    ) -> None:
        # Change color if button is being hovered
        if hover:
            color = self.BUTTON_HOVER_COLOR

        # Draw button
        pygame.draw.rect(self.screen, color, button_rect, 0, 5)
        pygame.draw.rect(
            self.screen,
            self.POPUP_BORDER_COLOR,
            button_rect,
            1,
            5)

        # Draw button text
        text_surface: pygame.Surface = self.button_font.render(
            text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(
            center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    # Helper method to show insufficient funds notification
    def show_insufficient_funds_notification(self) -> None:
        # Create a notification surface
        notif_width = 400
        notif_height = 200
        notif_x = self.screen.get_width() // 2 - notif_width // 2
        notif_y = self.screen.get_height() // 2 - notif_height // 2
        notif_surface = pygame.Surface((notif_width, notif_height))

        # Draw notification
        notif_surface.fill(self.POPUP_BG_COLOR)
        pygame.draw.rect(
            notif_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, notif_width, notif_height),
            2,
            10,
        )

        # Draw title
        title_text = "Insufficient Funds"
        title_surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect = title_surface.get_rect(
            center=(notif_width // 2, 40))
        notif_surface.blit(title_surface, title_rect)

        # Draw message
        message_lines = [
            f"You don't have enough funds",
            f"to pay the £50 jail fine.",
            f"Please sell some assets.",
        ]

        y_offset = 80
        for line in message_lines:
            message_surface = self.button_font.render(
                line, True, self.POPUP_TEXT_COLOR)
            message_rect = message_surface.get_rect(
                center=(notif_width // 2, y_offset))
            notif_surface.blit(message_surface, message_rect)
            y_offset += 25

        # Display on screen
        self.screen.blit(notif_surface, (notif_x, notif_y))
        pygame.display.flip()

        # Wait for a few seconds
        import time

        start_time = time.time()
        while time.time() - start_time < 3:  # 3 second delay
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.time.Clock().tick(60)

    # Process user input events
    def handle_events(
        self,
        event: pygame.event.Event,
        player: Player,
        jail: Jail,
        free_parking: FreeParking,
        bank: Bank,
        go: Go,
    ) -> bool:
        # Update hover states when mouse moves
        if event.type == pygame.MOUSEMOTION:
            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            # Check if mouse is over any button and update hover state
            self.stay_in_jail_hover = self.stay_in_jail_button.collidepoint(
                mouse_pos)
            self.use_card_hover = self.use_card_button.collidepoint(
                mouse_pos) and player.get_get_out_of_jail_cards() > 0
            self.pay_fine_hover = self.pay_fine_button.collidepoint(
                mouse_pos) and player.get_cash_balance() >= 50

        # # If player is already bankrupt, close the popup immediately
        # if player.get_is_bankrupt():
        #     self.result = "bankrupt"
        #     return True

        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

            # Option 1: Stay in jail
            if self.stay_in_jail_button.collidepoint(mouse_pos):
                print("Stay in Jail button clicked")
                self.result = "stayed"
                return True

            # Option 2: Use Get Out of Jail Free card (if available)
            if self.use_card_button.collidepoint(
                    mouse_pos) and player.get_get_out_of_jail_cards() > 0:
                print("Use card button clicked")
                self.result = "used_card"
                return True

            # Option 3: Pay fine (Option to sell assets if not enough
            # funds)
            if self.pay_fine_button.collidepoint(mouse_pos):
                try:
                    # Try to pay the fine - will throw exception if not enough
                    # funds
                    jail.pay_fine_for_release(
                        player, free_parking, go, bank)
                    print(player.get_is_in_jail())
                    self.result = "paid_fine"
                    return True
                except InsufficientFundsError:
                    print("Error paying fine")
                    # Show notification first
                    self.show_insufficient_funds_notification()

                    # Then show sell assets popup
                    sell_asset_popup = SellOrMortgagePopup(
                        self.screen.get_width() // 2 - 225,
                        self.screen.get_height() // 2 - 300,
                        450,
                        600,
                        self.screen,
                    )
                    # Show sell assets popup and get the result
                    action, selected_property = sell_asset_popup.show(
                        player, bank)

                    # Try to pay the fine again after selling assets
                    try:
                        jail.pay_fine_for_release(
                            player, free_parking, go, bank)
                        self.result = "paid_fine"
                        return True
                    except InsufficientFundsError:
                        # If still can't afford, declare player
                        # bankrupt
                        player.set_is_bankrupt()
                        print(
                            f"Player {
                                player.get_name()} has been declared bankrupt!")
                        self.result = "bankrupt"
                        return True

        # Return False if no button was clicked
        return False

    # Display the popup and handle player's jail decision
    def show(self, player: Player, jail: Jail,
             free_parking: FreeParking, bank: Bank, go: Go) -> Optional[str]:
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True
        self.result = None

        # Check if player is already bankrupt before starting
        if player.get_is_bankrupt():
            return "bankrupt"

        while running:
            # Draw the popup
            self.draw(player)

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Handle popup interaction events
                if self.handle_events(
                        event, player, jail, free_parking, bank, go):
                    running = False  # Exit the popup if a choice was made

                # Check again if player became bankrupt during event
                # handling
                if player.get_is_bankrupt():
                    self.result = "bankrupt"
                    running = False

            clock.tick(60)

        # Return the player's jail decision
        return self.result
