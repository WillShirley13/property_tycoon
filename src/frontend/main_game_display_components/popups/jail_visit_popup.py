from typing import Any, Optional, Tuple

import pygame

from backend.property_owners.player import Player


class JailVisitPopup:
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
        )
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
        self.button_width: int = width - 40
        self.button_height: int = 50
        self.button_y: int = 100

        # Create button rectangle for the continue option
        self.continue_button: pygame.Rect = pygame.Rect(
            self.x + 20,
            self.y + self.button_y,
            self.button_width,
            self.button_height,
        )

        # Initialise hover state for button
        self.continue_hover: bool = False

    # Draw the jail visit popup
    def draw(self, player: Player) -> None:
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
        title_text: str = f"{player.get_name()} is visiting Jail"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.width // 2, 40))
        self.popup_surface.blit(title_surface, title_rect)

        # Draw message
        info_text: str = "Just visiting, not in trouble!"
        info_surface: pygame.Surface = self.button_font.render(
            info_text, True, self.POPUP_TEXT_COLOR)
        info_rect: pygame.Rect = info_surface.get_rect(
            center=(self.width // 2, 80))
        self.popup_surface.blit(info_surface, info_rect)

        # calculate mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        # check if mouse is hovering over continue button
        relative_mouse_pos = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y)
        continue_button_local = pygame.Rect(
            20, self.button_y, self.button_width, self.button_height)
        self.continue_hover = continue_button_local.collidepoint(
            relative_mouse_pos)

        # Choose the button color based on hover state
        button_color = self.BUTTON_HOVER_COLOR if self.continue_hover else self.BUTTON_COLOR

        # Draw the button with rounded corners
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
        text_surface: pygame.Surface = self.button_font.render(
            "Continue", True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(
            center=continue_button_local.center)
        self.popup_surface.blit(text_surface, text_rect)

        # Display the popup on the screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

    # handle user input events
    def handle_events(self, event: pygame.event.Event) -> bool:
        # handle left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            relative_mouse_pos = (
                mouse_pos[0] - self.x,
                mouse_pos[1] - self.y)
            continue_button_local = pygame.Rect(
                20, self.button_y, self.button_width, self.button_height)

            if continue_button_local.collidepoint(relative_mouse_pos):
                return True  # Return True to indicate the popup is done

        return False  # Return False to keep the popup open

    # Display the popup and wait for user input
    def show(self, player: Player) -> str:
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True

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
                if self.handle_events(event):
                    running = False  # Exit the popup if a choice was made

            clock.tick(60)

        # Return the player's decision
        return
