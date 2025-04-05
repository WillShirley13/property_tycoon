import pygame
from typing import Optional, Tuple, Any
import time

from backend.property_owners.player import Player
from backend.non_ownables.game_card import GameCard
from frontend.main_game_display_components.popups.sell_asset_popup import (
    SellOrMortgagePopup,
)
from backend import errors
from backend.non_ownables.go import Go


class GameCardPopup:
    # Initialize the popup for when a player lands on a game card space
    def __init__(self, x: int, y: int, width: int, height: int, screen: pygame.Surface):
        # Store position and dimensions
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        self.corner_size = 350
        self.result: Optional[str] = None  # Store the player's decision

        # Define color scheme for the popup
        self.POPUP_BG_COLOR = pygame.image.load("src/frontend/art_assets/card_face.png").convert_alpha() # change Light gray background
        new_size = (self.width, self.height)
        self.POPUP_BG_COLOR = pygame.transform.scale(self.POPUP_BG_COLOR, new_size)
        
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)  # Black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # White text
        self.BUTTON_COLOR: Tuple[int, int, int] = (144, 238, 144)  # Light green buttons
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            180,
            180,
            180,
        )  # Gray hover effect

        # Define font sizes for different text elements
        title_size: int = 20
        button_size: int = 14

        # Initialize fonts with fallback to default if Arial not available
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont("Arial", button_size, bold=True)
        except:
            self.title_font = pygame.font.SysFont(None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, button_size, bold=True)

        # Create a surface for the popup
        self.popup_surface: pygame.Surface = pygame.Surface((width, height))

        # Configure button layout
        self.button_width: int = width - 150  # Leave margin on both sides
        self.button_height: int = 50
        self.button_y: int = self.height - 120  # Match the position used in draw()

        # Create button rectangle for the continue option (this is for collision detection)
        self.continue_button: pygame.Rect = pygame.Rect(
            self.x + 20,  # 20px from left edge of popup
            self.y + self.button_y,  # Position corresponds to the y-position used in draw()
            self.button_width,
            self.button_height,
        )

        # Initialize hover state for button
        self.continue_hover: bool = False

    # Helper method to show insufficient funds notification
    def show_insufficient_funds_notification(self, card_info) -> None:
        # Create a notification surface
        notif_width = 400
        notif_height = 200
        notif_x = self.screen.get_width() // 2 - notif_width // 2
        notif_y = self.screen.get_height() // 2 - notif_height // 2
        notif_surface = pygame.Surface((notif_width, notif_height))

        # Draw notification
        notif_surface.blit(self.POPUP_BG_COLOR,(0,0))
        pygame.draw.rect(
            notif_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, notif_width, notif_height),
            2,
            10,
        )

        # Draw title
        title_text = "Insufficient Funds"
        title_surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(notif_width // 2, 40))
        notif_surface.blit(title_surface, title_rect)

        # Draw message
        message_lines = [
            f"You landed on a game card,",
            f"but you don't have enough funds",
            f"to act on the card instructions.",
            f"Please sell some assets.",
        ]

        y_offset = 50
        for line in message_lines:
            message_surface = self.button_font.render(line, True, self.POPUP_TEXT_COLOR)
            message_rect = message_surface.get_rect(center=(notif_width // 2, y_offset))
            notif_surface.blit(message_surface, message_rect)
            y_offset += 25

        # Display on screen
        self.screen.blit(notif_surface, (notif_x, notif_y))
        pygame.display.flip()

        # Wait for a few seconds
        start_time = time.time()
        while time.time() - start_time < 5:  # 5 second delay
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.time.Clock().tick(60)

    # Draw the game card popup and its contents
    def draw(self, player: Player, card_info: Tuple[str, int]) -> None:
        # Clear the popup surface with background color
        self.popup_surface.blit(self.POPUP_BG_COLOR,(0,0))

        # Draw a border around the popup
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )  # 10px corner radius

        # Draw the title (player landed on a Game Card)
        title_text: str = f"{player.get_name()} landed on a Game Card"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.width // 2, 150))
        self.popup_surface.blit(title_surface, title_rect)

        # Draw explanation text
        info_text: str = card_info[0]
        info_surface: pygame.Surface = self.button_font.render(info_text, True, self.POPUP_TEXT_COLOR)
        info_rect: pygame.Rect = info_surface.get_rect(center=(self.width // 2, 200))
        self.popup_surface.blit(info_surface, info_rect)

        # Calculate mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is hovering over continue button
        # Adjust mouse position relative to popup surface
        relative_mouse_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        continue_button_local = pygame.Rect(self.width // 2 - self.button_width // 4, self.button_y, self.button_width // 2, self.button_height)
        self.continue_hover = continue_button_local.collidepoint(relative_mouse_pos)

        # Draw the continue button
        self.draw_button(self.popup_surface, continue_button_local, "Continue", self.continue_hover)

        # Display the popup on the screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    # Helper method to draw a button with hover effect
    def draw_button(self, surface: pygame.Surface, button_rect: pygame.Rect, text: str, hover: bool) -> None:
        # Choose the button color based on hover state
        button_color = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR

        # Draw the button with rounded corners
        pygame.draw.rect(surface, button_color, button_rect, 0, 5)  # Filled button
        pygame.draw.rect(surface, self.POPUP_BORDER_COLOR, button_rect, 1, 5)  # Border

        # Add text to the button
        text_surface: pygame.Surface = self.button_font.render(text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

    # Process user input events for the popup
    def handle_events(self, event: pygame.event.Event) -> bool:
        # Handle user interaction events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            relative_mouse_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
            continue_button_local = pygame.Rect(20, self.button_y, self.button_width, self.button_height)

            if continue_button_local.collidepoint(relative_mouse_pos):
                self.result = "continue"
                return True  # Return True to indicate the popup is done

        return False  # Return False to keep the popup open

    # Display the popup and wait for user interaction
    def show(
        self,
        player: Player,
        bank,
        free_parking,
        jail,
        other_players,
        card_info: Tuple[str, int],
        card_pack: GameCard,
        go: Go,
    ) -> str:
        # Set up game loop for the popup
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True
        self.result = None
        
        # Center the popup on the screen
        self.x = self.screen.get_width() // 2 - self.width // 2
        self.y = self.screen.get_height() // 2 - self.height // 2
        
        # Update the continue button position
        self.continue_button = pygame.Rect(
            self.x + 20,  # 20px from left edge of popup
            self.y + self.button_y,  # Position corresponds to the y-position used in draw()
            self.button_width,
            self.button_height,
        )

        # Try to process the card, allow player to sell assets if they don't have enough money
        card_processed = False
        while not card_processed:
            try:
                card_pack.process_card(player, bank, card_info[1], free_parking, jail, other_players, go)
                card_processed = True
            except errors.InsufficientFundsError:
                # Show notification first
                self.show_insufficient_funds_notification(card_info)

                # Then show sell assets popup
                sell_asset_popup = SellOrMortgagePopup(
                    self.screen.get_width() // 2 - 225,
                    self.screen.get_height() // 2 - 300,
                    450,
                    600,
                    self.screen,
                )
                # Show sell assets popup and get the result
                action, selected_property = sell_asset_popup.show(player, bank)
                # If player closed the popup without selling anything
                if action is None:
                    print("Player closed the popup without selling anything")
                    try:
                        # Try processing the card again
                        card_pack.process_card(
                            player,
                            bank,
                            card_info[1],
                            free_parking,
                            jail,
                            other_players,
                            go,
                        )
                        card_processed = True
                    except errors.InsufficientFundsError:
                        # If still can't afford, declare player bankrupt
                        player.set_is_bankrupt()
                        card_processed = True  # End the loop and return to main game

        while running:
            # Draw the popup
            self.draw(player, card_info)

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Handle popup interaction events
                if self.handle_events(event):
                    running = False  # Exit the popup if a choice was made

            # Cap the frame rate
            clock.tick(60)

        # Return the player's decision
        return self.result