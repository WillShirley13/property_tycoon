import pygame
from typing import Optional, Tuple, Any

from backend.property_owners.player import Player
from backend.errors import InsufficientFundsError
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.jail import Jail
from frontend.main_game_display_components.popups.sell_asset_popup import (
    SellOrMortgagePopup,
)
from backend.property_owners.bank import Bank


class JailPopup:
    # Initialize the popup for when a player is in jail with jail options
    def __init__(self, x: int, y: int, width: int, height: int, screen: pygame.Surface):
        # Store position and dimensions
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        self.result: Optional[str] = None  # Store the player's jail decision

        # Define color scheme for the popup
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (
            240,
            240,
            240,
        )  # Light gray background
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)  # Black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (0, 0, 0)  # Black text
        self.BUTTON_COLOR: Tuple[int, int, int] = (144, 238, 144)  # Light green buttons
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

        # Define font sizes for different text elements
        title_size: int = 20
        button_size: int = 14

        # Initialize fonts with fallback to default if Arial not available
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", title_size, bold=True
            )
            self.button_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", button_size, bold=True
            )
        except:
            self.title_font = pygame.font.SysFont(None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, button_size, bold=True)

        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface((width, height))

        # Configure button layout
        button_width: int = width - 40  # Leave margin on both sides
        button_height: int = 50

        # Calculate vertical positions for the three buttons
        roll_y: int = 80
        card_y: int = roll_y + button_height + 10
        pay_y: int = card_y + button_height + 10

        # Create button rectangles for the jail options
        self.stay_in_jail_button: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + roll_y, button_width, button_height
        )
        self.use_card_button: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + card_y, button_width, button_height
        )
        self.pay_fine_button: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + pay_y, button_width, button_height
        )

        # Initialize hover states for buttons
        self.stay_in_jail_hover: bool = False
        self.use_card_hover: bool = False
        self.pay_fine_hover: bool = False

    # Draw the jail popup with all available options for the player
    def draw(self, player: Player) -> None:
        # Draw popup background with rounded corners
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
            title_text, True, self.POPUP_TEXT_COLOR
        )
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.x + self.width // 2, self.y + 30)
        )
        self.screen.blit(title_surface, title_rect)

        # Draw first option button: Stay in Jail
        self.draw_button(
            self.stay_in_jail_button,
            "Stay in Jail",
            self.stay_in_jail_hover,
            self.BUTTON_COLOR,
        )

        # Draw second option button: Use Get Out of Jail Free card (if player has one)
        has_card: bool = player.get_get_out_of_jail_cards() > 0
        card_color: Tuple[int, int, int] = (
            self.BUTTON_COLOR if has_card else self.BUTTON_DISABLED_COLOR
        )
        self.use_card_hover = self.use_card_hover if has_card else False
        self.draw_button(
            self.use_card_button,
            "Use Get Out of Jail Free Card",
            self.use_card_hover,
            card_color,
        )

        # Draw third option button: Pay fine (if player has enough money)
        has_money: bool = player.get_cash_balance() >= 50  # Fine amount is £50
        pay_color: Tuple[int, int, int] = (
            self.BUTTON_COLOR if has_money else self.BUTTON_DISABLED_COLOR
        )
        self.pay_fine_hover = self.pay_fine_hover if has_money else False
        self.draw_button(
            self.pay_fine_button, "Pay £50 Fine", self.pay_fine_hover, pay_color
        )

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

        # Draw button with rounded corners
        pygame.draw.rect(self.screen, color, button_rect, 0, 5)
        pygame.draw.rect(self.screen, self.POPUP_BORDER_COLOR, button_rect, 1, 5)

        # Draw button text centered on the button
        text_surface: pygame.Surface = self.button_font.render(
            text, True, self.POPUP_TEXT_COLOR
        )
        text_rect: pygame.Rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    # Process user input events, handle button hover and clicks
    def handle_events(
        self,
        event: pygame.event.Event,
        player: Player,
        jail: Jail,
        free_parking: FreeParking,
        bank: Bank,
    ) -> bool:
        # Update hover states when mouse moves
        if event.type == pygame.MOUSEMOTION:
            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            # Check if mouse is over any button and update hover state
            self.stay_in_jail_hover = self.stay_in_jail_button.collidepoint(mouse_pos)
            self.use_card_hover = (
                self.use_card_button.collidepoint(mouse_pos)
                and player.get_get_out_of_jail_cards() > 0
            )
            self.pay_fine_hover = (
                self.pay_fine_button.collidepoint(mouse_pos)
                and player.get_cash_balance() >= 50
            )

        # Handle button clicks
        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Left mouse button
            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

            # Option 1: Stay in jail
            if self.stay_in_jail_button.collidepoint(mouse_pos):
                print("Stay in Jail button clicked")
                self.result = "stayed"
                return True

            # Option 2: Use Get Out of Jail Free card (if available)
            if (
                self.use_card_button.collidepoint(mouse_pos)
                and player.get_get_out_of_jail_cards() > 0
            ):
                print("Use card button clicked")
                self.result = "used_card"
                return True

            # Option 3: Pay fine (if player has enough money)
            if self.pay_fine_button.collidepoint(mouse_pos):
                running = True
                while running:
                    try:
                        # Try to pay the fine - will throw exception if not enough funds
                        jail.pay_fine_for_release(player, free_parking)
                        print(player.get_is_in_jail())
                        self.result = "paid_fine"
                        running = False
                    except InsufficientFundsError:
                        print("Error paying fine")
                        # Show sell assets popup if player doesn't have enough money
                        sell_asset_popup = SellOrMortgagePopup(
                            self.screen.get_width() // 2 - 225,  # Centered horizontally
                            self.screen.get_height() // 2 - 300,  # Centered vertically
                            450,  # Width
                            600,  # Height
                            self.screen,
                        )
                        # Show popup and get the result
                        action, selected_property = sell_asset_popup.show(player, bank)
                        running = False

                        # No need for continue here - the loop will naturally retry the payment
                return True

        # Return False if no button was clicked
        return False

    # Display the popup and handle player's jail decision
    def show(
        self, player: Player, jail: Jail, free_parking: FreeParking, bank: Bank
    ) -> Optional[str]:
        # Set up game loop for the popup
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True
        self.result = None

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
                if self.handle_events(event, player, jail, free_parking, bank):
                    running = False  # Exit the popup if a choice was made

            # Cap the frame rate
            clock.tick(60)

        # Return the player's jail decision
        return self.result
