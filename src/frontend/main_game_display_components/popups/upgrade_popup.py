import pygame
from typing import List, Tuple, Dict, Optional, Any

from backend.property_owners.player import Player
from backend.enums.property_group import PropertyGroup
from backend.ownables.property import Property
from backend.property_owners.bank import Bank
from backend.constants import PROPERTY_BUILD_COSTS


class UpgradePropertyPopup:
    def __init__(self, x: int, y: int, width: int, height: int, screen: pygame.Surface):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen

        # Get screen dimensions for centering
        self.screen_width, self.screen_height = self.screen.get_size()

        # define color scheme
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (
            240,
            240,
            240,
        )  # light gray background
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)  # black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (0, 0, 0)  # black text
        self.BUTTON_COLOR: Tuple[int, int, int] = (
            144,
            238,
            144,
        )  # Light green for buttons
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (
            180,
            180,
            180,
        )  # Gray hover effect
        self.CANCEL_BUTTON_COLOR: Tuple[int, int, int] = (
            220,
            100,
            100,
        )  # Light red for cancel button

        # Define font sizes
        title_size: int = 20
        button_size: int = 14

        # set fonts
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont("Arial", button_size, bold=True)
        except:
            self.title_font = pygame.font.SysFont(None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, button_size, bold=True)

        # Create a surface for the initial popup view
        self.popup_surface: pygame.Surface = pygame.Surface((width, height // 2))

        # property player chooses to upgrade
        self.selected_property: Optional[Property] = None

        # Store references to player and bank
        self.current_player: Optional[Player] = None
        self.bank: Optional[Bank] = None

    # Draw the property selection popup for the player to choose a property.
    def draw_select_property_popup(self, player: Player) -> None:
        # Count how many properties the player owns for sizing the popup
        property_count: int = 0
        for property_group in player.get_owned_properties().values():
            property_count += len(property_group)

        # Calculate needed height for the popup (ensuring enough space for all properties)
        needed_height: int = 70 + (8 * 60) + 10  # 70px for title area, rows of 60px high buttons, 10px padding

        # Create a wider popup for property selection
        popup_width: int = self.width * 2

        # create a new surface with the calculated dimensions
        self.popup_surface = pygame.Surface((popup_width, needed_height))

        # Calculate centered position for the popup in the screen
        centered_x: int = (self.screen_width - popup_width) // 2
        centered_y: int = (self.screen_height - needed_height) // 2

        # Fill the popup background
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw rounded border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, popup_width, needed_height),
            2,
            10,
        )

        # Set title for property selection
        title_text: str = "Select a property to upgrade with a house or hotel"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(popup_width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # Create a list to store property buttons and references
        self.property_buttons: List[Tuple[pygame.Rect, Property]] = []

        # Set up layout for property buttons
        start_x: int = 10
        start_y: int = 70
        property_count = 0

        # Add a button for each eligible property the player owns
        for property_group in player.get_owned_properties().values():
            for property in property_group:
                # Skip properties that are not eligible for upgrade
                if not isinstance(property, Property) or not property.get_is_eligible_for_upgrade():
                    continue

                property_name: str = property.get_name()
                property_group_name: str = property.get_property_group().value

                # If we'd overflow the bottom, start a new column
                if start_y + (property_count * 60) > needed_height - 20:
                    start_x += popup_width // 3
                    property_count = 0

                # Create property button rectangle
                property_rect: pygame.Rect = pygame.Rect(start_x, start_y + property_count * 60, popup_width // 3 - 20, 50)

                # Store the rectangle and corresponding property
                self.property_buttons.append((property_rect, property))

                # Draw the property button with property name and group
                self.draw_button(
                    self.popup_surface,
                    property_rect,
                    f"{property_name} (Property group: {property_group_name.capitalize()})",
                    False,
                    self.BUTTON_COLOR,
                )
                property_count += 1

        # draw close button
        self.close_button_rect = pygame.Rect(popup_width - 120, 20, 100, 40)
        self.draw_button(
            self.popup_surface,
            self.close_button_rect,
            "Close",
            False,
            self.CANCEL_BUTTON_COLOR,
        )

        # display popup centered on screen
        self.screen.blit(self.popup_surface, (centered_x, centered_y))

        # store popup's position for event handling
        self.property_popup_x = centered_x
        self.property_popup_y = centered_y

    # Draw the popup displaying upgrade details about the selected property.
    def draw_upgrade_popup(self) -> None:
        self.popup_surface: pygame.Surface = pygame.Surface((self.width, self.height // 2))
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height // 2),
            2,
            10,
        )

        # Draw title text
        title_text: str = "Property Upgrade Details:"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # Get appropriate upgrade cost
        property_group = self.selected_property.get_property_group().value
        houses = self.selected_property.get_houses()
        has_hotel = self.selected_property.get_hotel() == 1

        if houses == 4 and not has_hotel:
            upgrade_type = "hotel"
            upgrade_cost = PROPERTY_BUILD_COSTS[property_group]["hotel"]
        else:
            upgrade_type = "house"
            upgrade_cost = PROPERTY_BUILD_COSTS[property_group]["house"]

        # create property details as separate lines
        details = [
            f"Property Name: {self.selected_property.get_name()}",
            f"Property Group: {property_group.capitalize()}",
            f"Current Houses: {houses}",
            f"Current Hotel: {'Yes' if has_hotel else 'No'}",
            f"Player Cash: £{self.current_player.get_cash_balance()}",
            f"Upgrade Cost: £{upgrade_cost} for {upgrade_type}",
        ]

        # draw each line of property details text
        y_position = 70
        for detail in details:
            detail_surface = self.button_font.render(detail, True, self.POPUP_TEXT_COLOR)
            detail_rect = detail_surface.get_rect(left=20, top=y_position)
            self.popup_surface.blit(detail_surface, detail_rect)
            y_position += 30  # Increment y position for next line

        # draw upgrade button
        self.upgrade_button_rect = pygame.Rect(self.width // 4 - 55, self.height // 2 - 55, 110, 50)
        self.draw_button(
            self.popup_surface,
            self.upgrade_button_rect,
            f"Upgrade",
            False,
            self.BUTTON_COLOR,
        )

        # draw cancel button
        self.cancel_button_rect = pygame.Rect(self.width // 4 + 65, self.height // 2 - 55, 110, 50)
        self.draw_button(
            self.popup_surface,
            self.cancel_button_rect,
            "Cancel",
            False,
            self.CANCEL_BUTTON_COLOR,
        )

        # Calculate centered position for the details popup
        centered_x = (self.screen_width - self.width) // 2
        centered_y = (self.screen_height - self.height // 2) // 2

        # display popup centered on screen
        self.screen.blit(self.popup_surface, (centered_x, centered_y))

        # store popup's position for event handling
        self.details_popup_x = centered_x
        self.details_popup_y = centered_y

    # Handle events for the property details popup.
    def handle_upgrade_property_events(self, event: pygame.event.Event) -> Tuple[bool, bool]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get correct position for details popup
            x_position = getattr(self, "details_popup_x", self.x)
            y_position = getattr(self, "details_popup_y", self.y)

            # adjust mouse position relative to popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - x_position,
                event.pos[1] - y_position,
            )

            # check if upgrade button was clicked
            if self.upgrade_button_rect.collidepoint(adjusted_pos):
                print(f"Upgrading property: {self.selected_property.get_name()}")
                try:
                    self.selected_property.upgrade_property(self.bank)
                    # Return to property selection, don't close the popup
                    return True, False
                except Exception as e:
                    print(f"Error upgrading property: {e}")
                    # Return to property selection, don't close the popup
                    return True, False

            # check if cancel button was clicked
            elif self.cancel_button_rect.collidepoint(adjusted_pos):
                # Return to property selection, don't close the popup
                return True, False

        # Handle Enter key to confirm upgrade
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            print(f"Upgrading property: {self.selected_property.get_name()}")
            try:
                self.selected_property.upgrade_property(self.bank)
                # Return to property selection, don't close the popup
                return True, False
            except Exception as e:
                print(f"Error upgrading property: {e}")
                # Return to property selection, don't close the popup
                return True, False

        # No action taken
        return False, False

    # Handle events for the property selection popup.
    def select_property_handle_events(self, event: pygame.event.Event, player: Player) -> Tuple[bool, Optional[Property], bool]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get correct position for property popup
            x_position: int = getattr(self, "property_popup_x", self.x)
            y_position: int = getattr(self, "property_popup_y", self.y)

            # adjust mouse position relative to property popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - x_position,
                event.pos[1] - y_position,
            )

            # check if close button was clicked
            if self.close_button_rect.collidepoint(adjusted_pos):
                print("Close button clicked")  # Debug print
                # signal to close the entire popup
                return False, None, True

            # check if any property button was clicked
            for i, (button_rect, property) in enumerate(self.property_buttons):
                if button_rect.collidepoint(adjusted_pos):
                    self.selected_property = property
                    # return the selected property, but don't close
                    return True, property, False

        # no property was selected and don't close
        return False, None, False

    # Main method to display the full upgrade popup flow.
    def show(self, player: Player, bank: Bank) -> Tuple[Optional[Property], bool]:
        self.current_player = player
        self.bank = bank
        clock: pygame.time.Clock = pygame.time.Clock()

        # Track if any upgrade was completed
        upgrade_completed: bool = False
        last_property_upgraded: Optional[Property] = None

        # display property selection popup
        property_running: bool = True
        property_details_showing: bool = False

        while property_running:
            # determine which view to display
            if self.selected_property and property_details_showing:
                # show property details with upgrade button
                self.draw_upgrade_popup()
            else:
                # Show property selection view
                self.draw_select_property_popup(player)

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return last_property_upgraded, upgrade_completed

                if property_details_showing:
                    # Handle property details events
                    return_to_selection, close_popup = self.handle_upgrade_property_events(event)
                    if return_to_selection:
                        # Record that an upgrade was completed
                        upgrade_completed = True
                        last_property_upgraded = self.selected_property
                        # Clear selection and return to property selection view
                        property_details_showing = False
                        self.selected_property = None
                    if close_popup:
                        property_running = False
                else:
                    # Handle property selection events
                    selected, prop, should_close = self.select_property_handle_events(event, player)
                    if selected:
                        property_details_showing = True
                    if should_close:
                        print("Closing property selection popup")  # Debug print
                        # Exit the loop and return to main game/calling popup
                        property_running = False

            clock.tick(60)

        # Return both the last selected property that was upgraded and a flag indicating if an upgrade was completed
        return last_property_upgraded, upgrade_completed

    # Helper method to draw button
    def draw_button(
        self,
        screen: pygame.Surface,
        button_rect: pygame.Rect,
        text: str,
        hover: bool,
        color: Tuple[int, int, int],
    ) -> None:

        # Apply hover effect if mouse is over button
        if hover:
            color = self.BUTTON_HOVER_COLOR

        # Draw button
        pygame.draw.rect(screen, color, button_rect, 0, 5)
        pygame.draw.rect(screen, self.POPUP_BORDER_COLOR, button_rect, 1, 5)

        # Render and center text on button
        text_surface: pygame.Surface = self.button_font.render(text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
