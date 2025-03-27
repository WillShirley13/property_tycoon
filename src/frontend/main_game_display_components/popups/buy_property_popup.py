import pygame
from typing import Tuple, Optional, List

# Assuming these imports are correct based on your project structure
from backend.property_owners.player import Player
from backend.ownables.property import Property
from backend.property_owners.bank import Bank
from backend.errors import InsufficientFundsError
from frontend.main_game_display_components.popups.insufficient_funds_popup import InsufficientFundsPopup


class BuyPropertyPopup:
    def __init__(
        self, x: int, y: int, width: int, height: int, screen: pygame.Surface = None
    ):
        """
        Initialize the buy property popup.

        Args:
            screen: Main game screen to draw the popup on.
            width: Width of the popup.
            height: Height of the popup.
        """
        self.screen = screen
        self.width = width
        self.height = height

        # Center the popup on the screen
        self.x = (screen.get_width() - width) // 2
        self.y = (screen.get_height() - height) // 2

        # Define color scheme (similar to SellOrMortgagePopup)
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (240, 240, 240)
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (0, 0, 0)
        self.BUY_BUTTON_COLOR: Tuple[int, int, int] = (144, 238, 144)  # Light green
        self.CANCEL_BUTTON_COLOR: Tuple[int, int, int] = (
            220,
            100,
            100,
        )  # Light red
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (180, 180, 180)

        # Define font sizes
        title_size: int = 20
        detail_size: int = 16
        button_size: int = 14

        # Initialize fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", title_size, bold=True
            )
            self.detail_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", detail_size
            )
            self.button_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", button_size, bold=True
            )
        except:
            self.title_font = pygame.font.SysFont(None, title_size + 4, bold=True) # Adjust size slightly for default
            self.detail_font = pygame.font.SysFont(None, detail_size + 2)
            self.button_font = pygame.font.SysFont(None, button_size + 2, bold=True)


        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface((self.width, self.height))

        # Button rectangles (will be defined precisely in draw method)
        self.buy_button_rect: Optional[pygame.Rect] = None
        self.cancel_button_rect: Optional[pygame.Rect] = None

        # Hover states
        self.buy_hover: bool = False
        self.cancel_hover: bool = False

    def draw(self, player: Player, property_obj: Property) -> None:
        """
        Draw the buy property popup with details and options.

        Args:
            player: The player considering the purchase.
            property_obj: The property being offered for sale.
        """
        # Clear the popup surface
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw rounded border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )

        # --- Title ---
        title_text: str = (
            f"Would {player.get_name()} like to purchase {property_obj.get_name()}?"
        )
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR
        )
        # Adjust title position if text is too wide
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.width // 2, 30))
        if title_rect.width > self.width - 20: # Add padding
            # If too wide, maybe wrap text or shrink font (simple centering for now)
             title_rect.centerx = self.width // 2
        self.popup_surface.blit(title_surface, title_rect)


        # --- Property Details ---
        details = [
            f"Property Group: {property_obj.get_property_group().value.capitalize()}",
            f"Purchase Price: £{property_obj.get_cost()}",
            # Add more details if needed, e.g., rent
            f"Rent: £{property_obj.get_rent_cost()}",
        ]

        y_position = 70 # Start details below title
        for detail in details:
            detail_surface = self.detail_font.render(
                detail, True, self.POPUP_TEXT_COLOR
            )
            detail_rect = detail_surface.get_rect(left=20, top=y_position)
            self.popup_surface.blit(detail_surface, detail_rect)
            y_position += 25 # Spacing between detail lines

        # --- Buttons ---
        button_width = self.width // 3
        button_height = 40
        button_y = self.height - button_height - 20 # Position near bottom

        self.buy_button_rect = pygame.Rect(
            self.width // 4 - button_width // 2, button_y, button_width, button_height
        )
        self.cancel_button_rect = pygame.Rect(
            3 * self.width // 4 - button_width // 2, button_y, button_width, button_height
        )

        # Calculate mouse position relative to popup
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        adjusted_mouse_pos: Tuple[int, int] = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y,
        )

        # Update hover states
        self.buy_hover = self.buy_button_rect.collidepoint(adjusted_mouse_pos)
        self.cancel_hover = self.cancel_button_rect.collidepoint(adjusted_mouse_pos)

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
            self.cancel_button_rect,
            "Cancel",
            self.cancel_hover,
            self.CANCEL_BUTTON_COLOR,
        )

        # Display the popup on the main screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    def handle_events(self, event: pygame.event.Event, current_player: Player, other_players: List[Player], property_obj: Property, bank: Bank) -> Optional[str]:
        """
        Handle events for the buy property popup.

        Args:
            event: The pygame event to process.

        Returns:
            "buy" if the buy button is clicked,
            "cancel" if the cancel button is clicked,
            None otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
            # Adjust mouse position relative to popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - self.x,
                event.pos[1] - self.y,
            )

            if self.buy_button_rect and self.buy_button_rect.collidepoint(adjusted_pos):
                current_player.cash_balance = 0
                try:
                    current_player.purchase_property(property_obj, bank)
                    return "buy"
                except InsufficientFundsError:
                    # Show the insufficient funds popup
                    insufficient_funds_popup = InsufficientFundsPopup(
                        self.x, self.y, self.width, self.height, self.screen, current_player.get_name()
                    )
                    insufficient_funds_popup.show()
            if self.cancel_button_rect and self.cancel_button_rect.collidepoint(adjusted_pos):
                print("Cancel button clicked")
                return "cancel"
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: # Enter key confirms buy
                return "buy"
            if event.key == pygame.K_ESCAPE: # Escape key cancels
                return "cancel"

        return None # No relevant action

    def show(self, player: Player, other_players: List[Player], property_obj: Property, bank: Bank) -> Optional[str]:
        """
        Display the buy property popup and wait for user interaction.

        Args:
            player: The player considering the purchase.
            property_obj: The property being offered.

        Returns:
            "buy" if the player chooses to buy,
            "cancel" if the player cancels or closes the popup.
        """
        clock = pygame.time.Clock()
        running = True
        result: Optional[str] = "cancel" # Default to cancel if closed

        while running:
            # Draw the popup
            self.draw(player, property_obj)

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    result = "cancel" # Treat closing window as cancel

                action = self.handle_events(event, player, other_players, property_obj, bank)
                if action:
                    running = False
                    result = action

            # Cap the frame rate
            clock.tick(60)

        return result

    # Helper method to draw buttons (copied/adapted from SellOrMortgagePopup)
    def draw_button(
        self,
        surface: pygame.Surface,
        button_rect: pygame.Rect,
        text: str,
        hover: bool,
        color: Tuple[int, int, int],
    ) -> None:
        """
        Helper method to draw a styled button with hover effects.

        Args:
            surface: The surface to draw the button on (the popup surface).
            button_rect: The rectangle defining button position and size.
            text: The text to display on the button.
            hover: Whether the mouse is hovering over the button.
            color: The base color of the button.
        """
        current_color = self.BUTTON_HOVER_COLOR if hover else color

        # Draw button with rounded corners
        pygame.draw.rect(surface, current_color, button_rect, 0, 5)
        pygame.draw.rect(surface, self.POPUP_BORDER_COLOR, button_rect, 1, 5)

        # Render and center text on button
        text_surface: pygame.Surface = self.button_font.render(
            text, True, self.POPUP_TEXT_COLOR
        )
        text_rect: pygame.Rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

