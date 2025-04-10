from typing import Any, Dict, List, Optional, Tuple

import pygame

from backend.enums.property_group import PropertyGroup
from backend.ownables.property import Property
from backend.property_owners.bank import Bank
from backend.property_owners.player import Player
from frontend.helpers.space_data import PROPERTY_COLORS


class SellOrMortgagePopup:
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
        )  # light gray background
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (
            0, 0, 0)  # black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (
            0, 0, 0)  # black text
        self.BUTTON_COLOR: Tuple[int, int, int] = (
            0,
            100,
            0,
        )  # Dark green for buttons
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

        # Create a surface for the initial popup view
        self.popup_surface: pygame.Surface = pygame.Surface(
            (width, height // 2))

        # Initialise hover states
        self.sell_hover: bool = False
        self.mortgage_hover: bool = False

        # Will store the user's choice (sell or mortgage)
        self.sell_or_mortgage_choice: Optional[str] = None

        # property player chooses to mortgage or sell
        self.selected_property: Optional[Property] = None

    # Draw the initial popup asking if the player wants to sell or mortgage a
    # property.
    def draw_sell_or_mortgage_choice_popup(self) -> None:
        self.popup_surface.fill(self.POPUP_BG_COLOR)

        # Draw border
        pygame.draw.rect(
            self.popup_surface,
            self.POPUP_BORDER_COLOR,
            (0, 0, self.width, self.height / 2),
            2,
            10,
        )

        # Draw the title text
        title_text: str = "Would you like to sell or mortgage your property?"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # Calculate mouse position relative to popup for hover
        # detection
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        adjusted_mouse_pos: Tuple[int, int] = (
            mouse_pos[0] - self.x,
            mouse_pos[1] - self.y,
        )

        # Create local button rectangles for proper collision
        # detection
        sell_button: pygame.Rect = pygame.Rect(
            10, 70, self.width - 20, 50)
        mortgage_button: pygame.Rect = pygame.Rect(
            10, 130, self.width - 20, 50)

        # Update hover states based on mouse position
        self.sell_hover = sell_button.collidepoint(adjusted_mouse_pos)
        self.mortgage_hover = mortgage_button.collidepoint(
            adjusted_mouse_pos)

        # Draw the option buttons
        self.draw_button(
            self.popup_surface,
            sell_button,
            "Sell",
            self.sell_hover,
            self.BUTTON_COLOR)
        self.draw_button(
            self.popup_surface,
            mortgage_button,
            "Mortgage",
            self.mortgage_hover,
            self.BUTTON_COLOR,
        )

        # Display the popup on the main screen
        self.screen.blit(self.popup_surface, (self.x, self.y))

        # Handle events for the sell/mortgage choice popup.

    def sell_or_mortgage_choice_handle_events(
            self, event: pygame.event.Event) -> bool:
        # handle events for the sell/mortgage choice popup
        if event.type == pygame.MOUSEBUTTONDOWN:
            # adjust mouse position relative to popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - self.x,
                event.pos[1] - self.y,
            )

            # create button rectangles for collision detection
            local_sell_button: pygame.Rect = pygame.Rect(
                10, 70, self.width - 20, 50)
            local_mortgage_button: pygame.Rect = pygame.Rect(
                10, 130, self.width - 20, 50)

            # check if sell button was clicked
            sell_hit: bool = adjusted_pos[0] >= 10 and adjusted_pos[0] <= 10 + (
                self.width - 20) and adjusted_pos[1] >= 70 and adjusted_pos[1] <= 70 + 50

            # check if mortgage button was clicked
            mortgage_hit: bool = adjusted_pos[0] >= 10 and adjusted_pos[0] <= 10 + (
                self.width - 20) and adjusted_pos[1] >= 130 and adjusted_pos[1] <= 130 + 50

            # check if either button was clicked
            if local_sell_button.collidepoint(
                    adjusted_pos) or sell_hit:
                self.sell_or_mortgage_choice = "sell"
                return True
            elif local_mortgage_button.collidepoint(adjusted_pos) or mortgage_hit:
                self.sell_or_mortgage_choice = "mortgage"
                return True

    # Draw the property selection popup for the player to choose a
    # property.
    def draw_select_property_popup(
            self, player: Player, sell: bool = False, mortgage: bool = False) -> None:
        # Count how many properties the player owns for sizing the
        # popup
        property_count: int = 0
        for property_group in player.get_owned_properties().values():
            property_count += len(property_group)

        # Calculate needed height for the popup (ensuring enough space for all
        # properties)
        # 70px for title area, rows of 60px high buttons, 10px padding
        needed_height: int = 70 + (8 * 60) + 10

        # Create a wider popup for property selection
        popup_width: int = self.width * 2

        # create a new surface with the calculated dimensions
        self.popup_surface = pygame.Surface(
            (popup_width, needed_height))

        # Calculate the centered x position for this wider popup
        centered_x: int = self.x - (popup_width - self.width) // 2

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

        # Set appropriate title based on whether selling or mortgaging
        title_text: str = "Select a property, property house or property hotel to sell" if sell else "Select a property to mortgage"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(popup_width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # Create a list to store property buttons and references
        self.property_buttons: List[Tuple[pygame.Rect, Property]] = []

        # Set up layout for property buttons
        start_x: int = 10
        start_y: int = 70
        property_count = 0

        # Add a button for each property the player owns
        for property_group in player.get_owned_properties().values():
            for property in property_group:
                # If player is mortgaging and the property is already
                # mortgaged, skip it
                if mortgage and property.get_is_mortgaged():
                    continue
                property_name: str = property.get_name()
                property_group_name: str = property.get_property_group().value

                # If we'd overflow the bottom, start a new column
                if start_y + (property_count
                              * 60) > needed_height - 20:
                    start_x += popup_width // 3
                    property_count = 0

                # Create property button rectangle
                property_rect: pygame.Rect = pygame.Rect(
                    start_x, start_y + property_count * 60, popup_width // 3 - 20, 50)

                # Store the rectangle and corresponding property
                self.property_buttons.append(
                    (property_rect, property))

                # Draw the property button with property name and
                # group
                match property_group_name:
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
                
                self.draw_button(
                    self.popup_surface,
                    property_rect,
                    f"{property_name} (Property group: {
                        property_group_name.capitalize()})",
                    False,
                    self.BUTTON_COLOR,
                )
                property_count += 1

        # draw close button
        self.close_button_rect = pygame.Rect(
            popup_width - 120, 20, 100, 40)
        self.draw_button(
            self.popup_surface,
            self.close_button_rect,
            "Close",
            False,
            (220,
             100,
             100))

        # display popup
        self.screen.blit(self.popup_surface, (centered_x, self.y))

        # store popup's x position
        self.property_popup_x = centered_x

    # Handle events for the property selection popup.
    def select_property_handle_events(
            self, event: pygame.event.Event, player: Player) -> Tuple[bool, Optional[Property], bool]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # get correct x position for property popup
            x_position: int = getattr(
                self, "property_popup_x", self.x)

            # adjust mouse position relative to property popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - x_position,
                event.pos[1] - self.y,
            )

            # check if close button was clicked
            if self.close_button_rect.collidepoint(adjusted_pos):
                # signal to close the entire popup
                return False, None, True

            # check if any property button was clicked
            for i, (button_rect, property) in enumerate(
                    self.property_buttons):
                if button_rect.collidepoint(adjusted_pos):
                    self.selected_property = property
                    # return the selected property, but don't close
                    return True, property, False

        # no property was selected and don't close
        return False, None, False

    # Draw the popup displaying details about the selected property.
    def draw_sell_or_mortgage_popup(self) -> None:
        self.popup_surface: pygame.Surface = pygame.Surface(
            (self.width, self.height // 2))
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
        title_text: str = "Selected property details:"
        title_surface: pygame.Surface = self.title_font.render(
            title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(
            center=(self.width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)

        # create property details as separate lines
        details = [
            f"Property Name: {self.selected_property.get_name()}",
            f"Property Group: {
                self.selected_property.get_property_group().value.capitalize()}",
            f"Property Total Value: £{
                self.selected_property.get_total_value()}",
            (f"Property Houses: {self.selected_property.get_houses()}" if isinstance(
                self.selected_property, Property) else "No houses"),
            (f"Property Hotel: {self.selected_property.get_hotel()}" if isinstance(
                self.selected_property, Property) else "No hotel"),
            f"Current Sell Value: £{
                self.selected_property.get_current_sell_value()} (£{
                self.selected_property.get_total_value()
                / 2} if mortgaged)",
        ]

        # draw each line of property details text
        y_position = 70
        for detail in details:
            detail_surface = self.button_font.render(
                detail, True, self.POPUP_TEXT_COLOR)
            detail_rect = detail_surface.get_rect(
                left=20, top=y_position)
            self.popup_surface.blit(detail_surface, detail_rect)
            y_position += 30  # Increment y position for next line

        # draw sell button
        self.sell_button_rect = pygame.Rect(
            self.width // 4, self.height // 2 - 55, self.width // 2, 50)
        self.draw_button(
            self.popup_surface,
            self.sell_button_rect,
            "Sell" if self.sell_or_mortgage_choice == "sell" else "Mortgage",
            False,
            self.BUTTON_COLOR,
        )

        # display popup
        self.screen.blit(self.popup_surface, (self.x, self.y))

        # No button was clicked
        return False

    # Handle events for the property details popup.
    def handle_sell_or_mortgage_property_events(
            self, event: pygame.event.Event) -> Tuple[bool, bool]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # adjust mouse position relative to popup
            adjusted_pos: Tuple[int, int] = (
                event.pos[0] - self.x,
                event.pos[1] - self.y,
            )

            # check if sell button was clicked
            if self.sell_button_rect.collidepoint(adjusted_pos):
                print(
                    f"Selling property: {
                        self.selected_property.get_name()} for {
                        self.selected_property.get_current_sell_value()}")
                (self.current_player.sell_property(self.selected_property, self.bank) if self.sell_or_mortgage_choice
                 == "sell" else self.current_player.mortgage_property(self.selected_property, self.bank))
                # Return to property selection, don't close the popup
                return True, False
            else:
                # Clicking elsewhere also returns to property
                # selection
                return True, False

        # Handle Enter key to confirm sale
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            print(
                f"Selling property: {
                    self.selected_property.get_name()} for {
                    self.selected_property.get_current_sell_value()}")
            (self.current_player.sell_property(self.selected_property, self.bank) if self.sell_or_mortgage_choice
             == "sell" else self.current_player.mortgage_property(self.selected_property, self.bank))
            # Return to property selection, don't close the popup
            return True, False

        # No action taken
        return False, False

    # Main method to display the full sell/mortgage popup flow.
    def show(self, player: Player,
             bank: Bank) -> Tuple[Optional[str], Optional[Property]]:
        self.current_player = player
        self.bank = bank
        clock: pygame.time.Clock = pygame.time.Clock()

        # STEP 1: First display the sell or mortgage choice popup
        sell_or_mortgage_running: bool = True
        while sell_or_mortgage_running:
            # draw the initial popup
            self.draw_sell_or_mortgage_choice_popup()

            # update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sell_or_mortgage_running = False
                    return None, None

                # Handle sell/mortgage decision events
                if self.sell_or_mortgage_choice_handle_events(event):
                    sell_or_mortgage_running = False

            clock.tick(60)

        # If user closed the popup without selecting
        if self.sell_or_mortgage_choice is None:
            return None, None

        # STEP 2: Show property selection popup based on first choice
        action: str = self.sell_or_mortgage_choice
        # Store whether they chose sell or mortgage
        self.selected_property = None

        # track if any transaction was completed
        transaction_completed: bool = False
        last_property_sold: Optional[Property] = None

        # display property selection popup
        property_running: bool = True
        property_details_showing: bool = False

        while property_running:
            # determine which view to display
            if self.selected_property and property_details_showing:
                # show property details with sell button
                self.draw_sell_or_mortgage_popup()
            else:
                # Show property selection view
                self.draw_select_property_popup(
                    player, sell=(
                        action == "sell"), mortgage=(
                        action == "mortgage"))

            # Update the display
            pygame.display.flip()

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return action if transaction_completed else None, last_property_sold

                if property_details_showing:
                    # Handle property details events
                    return_to_selection, close_popup = self.handle_sell_or_mortgage_property_events(
                        event)
                    if return_to_selection:
                        # Record that a transaction was completed
                        transaction_completed = True
                        last_property_sold = self.selected_property
                        # Clear selection and return to property
                        # selection view
                        property_details_showing = False
                        self.selected_property = None
                    if close_popup:
                        property_running = False
                else:
                    # Handle property selection events
                    selected, prop, should_close = self.select_property_handle_events(
                        event, player)
                    if selected:
                        property_details_showing = True
                    if should_close:
                        # Exit the loop and return to main
                        # game/calling popup
                        property_running = False

            clock.tick(60)

        # Return both the action (sell/mortgage) and the last selected property
        # that was sold/mortgaged
        return action if transaction_completed else None, last_property_sold

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
        pygame.draw.rect(
            screen,
            self.POPUP_BORDER_COLOR,
            button_rect,
            1,
            5)

        # Render and center text on button
        text_surface: pygame.Surface = self.button_font.render(
            text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(
            center=button_rect.center)
        screen.blit(text_surface, text_rect)
