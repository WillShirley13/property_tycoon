import pygame
from typing import List, Tuple, Dict, Optional, Any

from backend.property_owners.player import Player
from backend.ownables.property import Property
from frontend.helpers.space_data import PROPERTY_COLORS


class PlayerPropertiesPopup:
    def __init__(self, x: int, y: int, width: int, height: int, screen: pygame.Surface, player: Player):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        self.player: Player = player

        # Define color scheme
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (240, 240, 240)  # light gray background
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)      # black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (0, 0, 0)        # black text
        self.BUTTON_COLOR: Tuple[int, int, int] = (50, 182, 10)  # Light green for buttons (default if no match found for property group)
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (180, 180, 180)  # Gray hover effect

        # Define font sizes
        title_size: int = 20
        button_size: int = 14

        # Set fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont("Arial", button_size, bold=True)
        except:
            self.title_font = pygame.font.SysFont(None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, button_size, bold=True)

        # Create a surface for the popup; here we use the full height passed in.
        self.popup_surface: pygame.Surface = pygame.Surface((self.width, self.height))
        
        # List to store property buttons (each button is a tuple: (pygame.Rect, Property))
        self.property_buttons: List[Tuple[pygame.Rect, Property]] = []

        # Close button rectangle
        self.close_button_rect: Optional[pygame.Rect] = None

        # The property selected by the user (if any)
        self.selected_property: Optional[Property] = None

    # Draw the property popup with all the player's properties.
    def draw_properties_popup(self) -> None:
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw border with rounded corners
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height),
            2,
            10,
        )

        # Draw title text
        title_text: str = f"{self.player.get_name()}'s Properties"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # Clear previous buttons
        self.property_buttons = []

        # Retrieve all properties owned by the player.
        # Assuming player.get_owned_properties() returns a dict of property groups to list of properties.
        properties: List[Property] = []
        owned_props: Dict[Any, List[Property]] = self.player.get_owned_properties()
        for prop_list in owned_props.values():
            properties.extend(prop_list)

        # Set up layout for property buttons
        start_y: int = 60
        button_height: int = 40
        spacing: int = 10
        start_x: int = 10
        current_y: int = start_y

        for prop in properties:
            # Create a button rectangle for each property.
            btn_rect: pygame.Rect = pygame.Rect(start_x, current_y, self.width - 20, button_height)
            self.property_buttons.append((btn_rect, prop))

            # Determine hover state
            mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
            adjusted_mouse: Tuple[int, int] = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
            hover: bool = btn_rect.collidepoint(adjusted_mouse)
                            # Draw the property button with property name and
                # group
            match prop.get_property_group().value:
                case "brown":
                    self.BUTTON_COLOR = PROPERTY_COLORS["BROWN"]
                case "blue":
                    self.BUTTON_COLOR = PROPERTY_COLORS["BLUE"]
                case "purple":
                    self.BUTTON_COLOR = PROPERTY_COLORS["PURPLE"]
                case "orange":
                    self.BUTTON_COLOR = PROPERTY_COLORS["ORANGE"]
                case "red":
                    self.BUTTON_COLOR = PROPERTY_COLORS["RED"]
                case "yellow":
                    self.BUTTON_COLOR = PROPERTY_COLORS["YELLOW"]
                case "green":
                    self.BUTTON_COLOR = PROPERTY_COLORS["GREEN"]
                case "deep_blue":
                    self.BUTTON_COLOR = PROPERTY_COLORS["DEEP_BLUE"]
                case "utility":
                    self.BUTTON_COLOR = PROPERTY_COLORS["UTILITY"]
                case "station":
                    self.BUTTON_COLOR = PROPERTY_COLORS["STATION"]
                case _:
                    self.BUTTON_COLOR = self.BUTTON_COLOR

            color: Tuple[int, int, int] = self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR

            # Draw button and its border
            pygame.draw.rect(self.popup_surface, color, btn_rect, 0, 5)
            pygame.draw.rect(self.popup_surface, self.POPUP_BORDER_COLOR, btn_rect, 1, 5)

            # Render property name on the button
            prop_text: str = prop.get_name()
            text_surface: pygame.Surface = self.button_font.render(prop_text, True, self.POPUP_TEXT_COLOR)
            text_rect: pygame.Rect = text_surface.get_rect(center=btn_rect.center)
            self.popup_surface.blit(text_surface, text_rect)

            current_y += button_height + spacing

        # Draw close button at the top-right of the popup
        self.close_button_rect = pygame.Rect(self.width - 110, 10, 100, 30)
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        hover_close = self.close_button_rect.collidepoint(adjusted_mouse)
        close_color = self.BUTTON_HOVER_COLOR if hover_close else (220, 100, 100)
        pygame.draw.rect(self.popup_surface, close_color, self.close_button_rect, 0, 5)
        pygame.draw.rect(self.popup_surface, self.POPUP_BORDER_COLOR, self.close_button_rect, 1, 5)
        close_text = self.button_font.render("Close", True, self.POPUP_TEXT_COLOR)
        close_text_rect = close_text.get_rect(center=self.close_button_rect.center)
        self.popup_surface.blit(close_text, close_text_rect)

        # Blit the popup surface onto the main screen at the specified position
        self.screen.blit(self.popup_surface, (self.x, self.y))

    # Handle events for the property popup.
    # Returns True if the popup should close.
    def handle_events(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Adjust mouse position relative to the popup
            adjusted_mouse: Tuple[int, int] = (event.pos[0] - self.x, event.pos[1] - self.y)
            # Check if close button was clicked
            if self.close_button_rect and self.close_button_rect.collidepoint(adjusted_mouse):
                return True  # Close the popup

            # Check if any property button was clicked
            for btn_rect, prop in self.property_buttons:
                if btn_rect.collidepoint(adjusted_mouse):
                    self.selected_property = prop
                    return True  # Close popup after selection

        # Optionally, handle key events here if needed (e.g., Esc to close)
        return False

    # Main method to display the popup and return the selected property (or None if closed)
    def show(self) -> Optional[Property]:
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True

        while running:
            self.draw_properties_popup()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.handle_events(event):
                    running = False

            clock.tick(60)

        return self.selected_property