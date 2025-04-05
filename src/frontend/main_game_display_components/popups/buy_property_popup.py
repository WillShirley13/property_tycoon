from typing import List, Optional, Tuple

import pygame

from backend.errors import InsufficientFundsError
from backend.ownables.property import Property
from backend.property_owners.bank import Bank
from backend.property_owners.player import Player
from frontend.main_game_display_components.popups.insufficient_funds_popup import \
    InsufficientFundsPopup


class BuyPropertyPopup:
    def __init__(self, x: int, y: int, width: int, height: int,
                 screen: pygame.Surface = None):
        self.screen = screen
        self.width = width
        self.height = height

        # Center the popup on the screen
        self.x = (screen.get_width() - width) // 2
        self.y = (screen.get_height() - height) // 2

        # Define color scheme for the popup
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (
            240, 240, 240)  # Light grey
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (
            0, 0, 0)  # Black
        self.POPUP_TEXT_COLOR: Tuple[int,
                                     int, int] = (0, 0, 0)  # Black
        self.BUY_BUTTON_COLOR: Tuple[int, int, int] = (
            0, 100, 0)  # Dark green
        self.NO_THANKS_BUTTON_COLOR: Tuple[int, int, int] = (
            220,
            100,
            100,
        )  # Light red
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            180, 180, 180)  # Grey

        # Define font sizes
        title_size: int = 20
        detail_size: int = 16
        button_size: int = 14

        # Set fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", title_size, bold=True)
            self.detail_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", detail_size)
            self.button_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", button_size, bold=True)
        except BaseException:
            self.title_font = pygame.font.SysFont(
                None, title_size + 4, bold=True)  # Adjust size slightly for default
            self.detail_font = pygame.font.SysFont(
                None, detail_size + 2)
            self.button_font = pygame.font.SysFont(
                None, button_size + 2, bold=True)

        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface(
            (self.width, self.height))

        # Button rects
        self.buy_button_rect: Optional[pygame.Rect] = None
        self.no_thanks_button_rect: Optional[pygame.Rect] = None

        # Initialise hover states
        self.buy_hover: bool = False
        self.no_thanks_hover: bool = False

        # Will be set to True if the player clicks the buy button, False if
        # they click the no thanks button or they have insufficient
        # funds
        self.made_purchase: Optional[bool] = None

    # Draw the buy property popup
    def draw(self, player: Player, property_obj: Property) -> None:
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw popup border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )

        # Title
        title_text: str = f"Would {
            player.get_name()} like to purchase {
            property_obj.get_name()}?"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        # Adjust title position if text is too wide
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.width // 2, 30))

        self.popup_surface.blit(title_surface, title_rect)

        # Property details
        details = [
            f"Property Group: {
                property_obj.get_property_group().value.capitalize()}",
            f"Purchase Price: £{property_obj.get_cost()}",
            f"Rent: £{property_obj.get_rent_cost()}",
        ]

        y_position = 70  # Start property details below title
        for detail in details:
            detail_surface = self.detail_font.render(
                detail, True, self.POPUP_TEXT_COLOR)
            detail_rect = detail_surface.get_rect(
                left=20, top=y_position)
            self.popup_surface.blit(detail_surface, detail_rect)
            y_position += 25  # Spacing between detail lines

        # Buttons
        button_width = self.width // 3
        button_height = 40
        button_y = self.height - button_height - 20  # Position near bottom

        self.buy_button_rect = pygame.Rect(
            self.width
            // 4
            - button_width
            // 2,
            button_y,
            button_width,
            button_height)
        self.no_thanks_button_rect = pygame.Rect(
            3 * self.width // 4 - button_width // 2,
            button_y,
            button_width,
            button_height,
        )

        # Calculate mouse position relative to popup
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        adjusted_mouse_pos: Tuple[int, int] = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y,
        )

        # Check if mouse is hovering over buttons
        self.buy_hover = self.buy_button_rect.collidepoint(
            adjusted_mouse_pos)
        self.no_thanks_hover = self.no_thanks_button_rect.collidepoint(
            adjusted_mouse_pos)

        # Draw buttons
        self.draw_button(
            self.popup_surface,
            self.buy_button_rect,
            "Buy",
            self.buy_hover,
            self.BUY_BUTTON_COLOR,
        )
        self.draw_button(
            self.popup_surface,
            self.no_thanks_button_rect,
            "No Thanks",
            self.no_thanks_hover,
            self.NO_THANKS_BUTTON_COLOR,
        )

        # Display the popup on the main screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    # Handle events for the buy property popup
    def handle_events(
        self,
        event: pygame.event.Event,
        current_player: Player,
        property_obj: Property,
        bank: Bank,
    ) -> bool:
        # Check if the left mouse button was clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Adjust mouse position relative to popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - self.x,
                event.pos[1] - self.y,
            )

            # Check if the buy button was clicked
            if self.buy_button_rect.collidepoint(adjusted_pos):
                # Try to purchase the property
                try:
                    current_player.purchase_property(
                        property_obj, bank)
                    self.made_purchase = True
                    return
                except InsufficientFundsError:
                    # Show the insufficient funds popup
                    insufficient_funds_popup = InsufficientFundsPopup(
                        self.x,
                        self.y,
                        self.width,
                        self.height,
                        self.screen,
                        current_player.get_name(),
                    )
                    insufficient_funds_popup.show()
                    self.made_purchase = False
                    return
            if self.no_thanks_button_rect.collidepoint(adjusted_pos):
                print("No Thanks button clicked")
                self.made_purchase = False
                return

        return

    # Show the buy property popup and wait for user interaction
    def show(self, property_obj: Property,
             player: Player, bank: Bank) -> bool:
        # Reset made_purchase at the start of each show
        self.made_purchase = None

        clock = pygame.time.Clock()
        running = True

        while running:
            # Draw the popup
            self.draw(player, property_obj)

            # Update the display
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.handle_events(event, player, property_obj, bank)
                if self.made_purchase is not None:
                    return self.made_purchase

            # Cap the frame rate
            clock.tick(60)

        # If the player fails to make a purchase, automatically return
        # False
        return False

    # Helper method to draw buttons
    def draw_button(
        self,
        surface: pygame.Surface,
        button_rect: pygame.Rect,
        text: str,
        hover: bool,
        color: Tuple[int, int, int],
    ) -> None:
        current_color = self.BUTTON_HOVER_COLOR if hover else color

        # Draw button
        pygame.draw.rect(surface, current_color, button_rect, 0, 5)
        pygame.draw.rect(
            surface,
            self.POPUP_BORDER_COLOR,
            button_rect,
            1,
            5)

        # Render and center text on button
        text_surface: pygame.Surface = self.button_font.render(
            text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(
            center=button_rect.center)
        surface.blit(text_surface, text_rect)
