import time
from typing import Any, Optional, Tuple

import pygame

from backend.errors import InsufficientFundsError
from backend.ownables.ownable import Ownable
from backend.property_owners.bank import Bank
from backend.property_owners.player import Player
from frontend.main_game_display_components.popups.sell_asset_popup import \
    SellOrMortgagePopup


class RentPaidPopup:
    def __init__(self, x: int, y: int, width: int,
                 height: int, screen: pygame.Surface):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen

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
            (width, height))

        # Configure button layout
        self.button_width: int = width - 40
        self.button_height: int = 50
        self.button_y: int = 150

        # Create button rectangle for the continue option
        self.continue_button: pygame.Rect = pygame.Rect(
            self.x + 20,
            self.y + self.button_y,
            self.button_width,
            self.button_height,
        )

        # Initialize hover state for button
        self.continue_hover: bool = False
        self.rent_paid: bool = False

    # Draw the rent paid popup
    def draw(self, player: Player, ownable: Ownable) -> None:
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw a border around the popup
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )

        # Draw the title
        owner_name = ownable.get_owner().get_name()
        property_name = ownable.get_name()
        title_text: str = f"{
            player.get_name()} landed on {owner_name}'s property"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.width // 2, 40))
        self.popup_surface.blit(title_surface, title_rect)

        # Draw property name
        property_text: str = f"Property: {property_name}"
        property_surface: pygame.Surface = self.text_font.render(
            property_text, True, self.POPUP_TEXT_COLOR)
        property_rect: pygame.Rect = property_surface.get_rect(
            center=(self.width // 2, 70))
        self.popup_surface.blit(property_surface, property_rect)

        # Draw rent amount
        rent_text: str = f"Rent Due: £{ownable.get_rent_cost()}"
        rent_surface: pygame.Surface = self.text_font.render(
            rent_text, True, self.POPUP_TEXT_COLOR)
        rent_rect: pygame.Rect = rent_surface.get_rect(
            center=(self.width // 2, 100))
        self.popup_surface.blit(rent_surface, rent_rect)

        # Calculate mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is hovering over continue button
        relative_mouse_pos = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y)

        continue_button_local = pygame.Rect(
            20, self.button_y, self.button_width, self.button_height)
        self.continue_hover = continue_button_local.collidepoint(
            relative_mouse_pos)

        # Choose the button color based on hover state
        button_color = self.BUTTON_HOVER_COLOR if self.continue_hover else self.BUTTON_COLOR

        # Draw the button
        pygame.draw.rect(
            self.popup_surface,
            button_color,
            continue_button_local,
            0,
            5)
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            continue_button_local,
            1,
            5)

        # Add text to the button
        button_text = "Continue" if self.rent_paid else "Pay Rent"
        text_surface: pygame.Surface = self.button_font.render(
            button_text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(
            center=continue_button_local.center)
        self.popup_surface.blit(text_surface, text_rect)

        # Display the popup on the screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    # Handle events for the rent paid popup
    def handle_events(
        self,
        event: pygame.event.Event,
        player: Player,
        ownable: Ownable,
        bank: Bank,
        rent_amount: int,
    ) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            relative_mouse_pos = (
                mouse_pos[0] - self.x,
                mouse_pos[1] - self.y)
            continue_button_local = pygame.Rect(
                20, self.button_y, self.button_width, self.button_height)

            if continue_button_local.collidepoint(relative_mouse_pos):
                if self.rent_paid:
                    return True  # Return True to indicate the popup is done
                else:
                    # Try to pay rent
                    running = True
                    while running:
                        try:
                            # Attempt to pay the rent to the property
                            # owner
                            ownable.get_rent_due_from_player(player)
                            self.rent_paid = True
                            running = False
                        except InsufficientFundsError:
                            # Show sell assets popup if player doesn't have
                            # enough money
                            sell_asset_popup = SellOrMortgagePopup(
                                self.screen.get_width() // 2 - 225,
                                self.screen.get_height() // 2 - 300,
                                450,
                                600,
                                self.screen,
                            )
                            # Show sell assets popup and get the
                            # result
                            action, selected_property = sell_asset_popup.show(
                                player, bank)

                            # If the player didn't sell or mortgage anything,
                            # keep the popup open
                            if not action:
                                return False

                            # Check if player now has enough funds after
                            # selling/mortgaging
                            if player.get_cash_balance() < ownable.get_rent_cost():
                                # Still not enough funds, continue showing the
                                # sell assets popup
                                continue
                            else:
                                # Player now has enough funds, try to pay rent
                                # again
                                continue

        return False  # Return False to keep the popup open

    # Display the popup and wait for user input
    def show(self, player: Player, ownable: Ownable,
             bank: Bank) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True
        self.rent_paid = False

        while running:
            # Draw the popup
            self.draw(player, ownable)

            # Update the display
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Handle popup interaction events
                if self.handle_events(
                        event, player, ownable, bank, ownable.get_rent_cost()):
                    running = False  # Exit the popup if a choice was made

            clock.tick(60)

        return
