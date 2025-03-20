import pygame
from typing import List, Tuple, Dict, Optional, Any

from backend.property_owners.player import Player
from backend.enums.property_group import PropertyGroup
from backend.ownables.property import Property

class SellOrMortgagePopup:
    def __init__(self, x: int, y: int, width: int, height: int):
        # Store position and dimensions
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        
        # Define color scheme
        self.POPUP_BG_COLOR: Tuple[int, int, int] = (240, 240, 240)  # Light gray background
        self.POPUP_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)    # Black border
        self.POPUP_TEXT_COLOR: Tuple[int, int, int] = (0, 0, 0)      # Black text
        self.BUTTON_COLOR: Tuple[int, int, int] = (144, 238, 144)    # Light green for buttons
        self.BUTTON_HOVER_COLOR: Tuple[int, int, int] = (180, 180, 180)  # Gray hover effect
        
        # Define font sizes
        title_size: int = 20
        button_size: int = 14
        
        # Initialize fonts with fallback to default if Arial not available
        try:
            self.title_font: pygame.font.Font = pygame.font.SysFont('Arial', title_size, bold=True)
            self.button_font: pygame.font.Font = pygame.font.SysFont('Arial', button_size, bold=True)
        except:
            self.title_font = pygame.font.SysFont(None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, button_size, bold=True)
            
        # Create a surface for the initial popup view
        self.popup_surface: pygame.Surface = pygame.Surface((width, height//2))
        
        # Initialize hover states
        self.sell_hover: bool = False
        self.mortgage_hover: bool = False
        
        self.sell_or_mortgage_choice: Optional[str] = None  # Will store the user's choice
        
        # property player chooses to mortgage or sell
        self.selected_property: Optional[Property] = None
        
    def draw_sell_or_mortgage_popup(self, screen: pygame.Surface) -> None:
        # Clear the popup surface with background color
        self.popup_surface.fill(self.POPUP_BG_COLOR)
        
        # Draw rounded border around popup
        pygame.draw.rect(self.popup_surface, self.POPUP_BORDER_COLOR, (0, 0, self.width, self.height/2), 2, 10)
        
        # Draw the title text
        title_text: str = "Would you like to sell or mortgage your property?"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(self.width // 2, 30))
        self.popup_surface.blit(title_surface, title_rect)
        
        # Calculate mouse position relative to popup for hover detection
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        adjusted_mouse_pos: Tuple[int, int] = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        
        # Create local button rectangles for proper collision detection
        sell_button: pygame.Rect = pygame.Rect(10, 70, self.width - 20, 50)
        mortgage_button: pygame.Rect = pygame.Rect(10, 130, self.width - 20, 50)
        
        # Update hover states based on mouse position
        self.sell_hover = sell_button.collidepoint(adjusted_mouse_pos)
        self.mortgage_hover = mortgage_button.collidepoint(adjusted_mouse_pos)

        # Draw the option buttons
        self.draw_button(self.popup_surface, sell_button, "Sell", self.sell_hover, self.BUTTON_COLOR)
        self.draw_button(self.popup_surface, mortgage_button, "Mortgage", self.mortgage_hover, self.BUTTON_COLOR)

        # Display the popup on the main screen
        screen.blit(self.popup_surface, (self.x, self.y))
        
    def draw_select_property_popup(self, screen: pygame.Surface, player: Player, sell: bool = False, 
            mortgage: bool = False) -> None:
        # Count how many properties the player owns for sizing the popup
        property_count: int = 0
        for property_group in player.get_owned_properties().values():
            property_count += len(property_group)
        
        # Calculate needed height for the popup (ensuring enough space for all properties)
        needed_height: int = 70 + (8 * 60) + 10  # 70px for title area, rows of 60px high buttons, 10px padding

        # Create a wider popup for property selection
        popup_width: int = self.width * 2
        
        # Create a new surface with the calculated dimensions
        self.popup_surface = pygame.Surface((popup_width, needed_height))
        
        # Calculate the centered x position for this wider popup
        centered_x: int = self.x - (popup_width - self.width) // 2
        
        # Fill the popup background
        self.popup_surface.fill(self.POPUP_BG_COLOR)
        
        # Draw rounded border
        pygame.draw.rect(self.popup_surface, self.POPUP_BORDER_COLOR, (0, 0, popup_width, needed_height), 2, 10)
        
        # Set appropriate title based on whether selling or mortgaging
        title_text: str = "Select a property, property house or property hotel to sell" if sell else "Select a property to mortgage"
        title_surface: pygame.Surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect: pygame.Rect = title_surface.get_rect(center=(popup_width // 2, 30))
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
                # If player is mortgaging and the property is already mortgaged, skip it
                if mortgage and property.get_is_mortgaged():
                    continue
                property_name: str = property.get_name()
                property_group_name: str = property.get_property_group().value
                    
                # If we'd overflow the bottom, start a new column
                if start_y + (property_count * 60) > needed_height - 20:
                    start_x += popup_width//3
                    property_count = 0  # Reset counter for the new column
                
                # Create property button rectangle
                property_rect: pygame.Rect = pygame.Rect(start_x, start_y + property_count * 60, popup_width//3 - 20, 50)
                
                # Store the rectangle and corresponding property
                self.property_buttons.append((property_rect, property))
                
                # Draw the property button with property name and group
                self.draw_button(self.popup_surface, property_rect, 
                                f'{property_name} (Property group: {property_group_name.capitalize()})', 
                                False, self.BUTTON_COLOR)
                property_count += 1
        
        # Display the centered popup on the main screen
        screen.blit(self.popup_surface, (centered_x, self.y))
        
        # Store the popup's x position for correct event handling
        self.property_popup_x = centered_x

    def sell_or_mortgage_handle_events(self, event: pygame.event.Event) -> bool:
        # Handle events for the sell/mortgage choice popup
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Adjust mouse position relative to popup
            adjusted_pos: Tuple[int, int] = (event.pos[0] - self.x, event.pos[1] - self.y)
            
            # Create button rectangles for collision detection
            local_sell_button: pygame.Rect = pygame.Rect(10, 70, self.width - 20, 50)
            local_mortgage_button: pygame.Rect = pygame.Rect(10, 130, self.width - 20, 50)
            
            # Alternative collision detection method (more reliable in some cases)
            sell_hit: bool = (adjusted_pos[0] >= 10 and 
                        adjusted_pos[0] <= 10 + (self.width - 20) and
                        adjusted_pos[1] >= 70 and 
                        adjusted_pos[1] <= 70 + 50)
                        
            mortgage_hit: bool = (adjusted_pos[0] >= 10 and 
                            adjusted_pos[0] <= 10 + (self.width - 20) and
                            adjusted_pos[1] >= 130 and 
                            adjusted_pos[1] <= 130 + 50)
            
            # Check if either button was clicked
            if local_sell_button.collidepoint(adjusted_pos) or sell_hit:
                self.sell_or_mortgage_choice = "sell"
                return True
            elif local_mortgage_button.collidepoint(adjusted_pos) or mortgage_hit:
                self.sell_or_mortgage_choice = "mortgage"
                return True
        
        # No button was clicked
        return False
    
    def select_property_handle_events(self, event: pygame.event.Event, player: Player) -> Tuple[bool, Optional[Property]]:
        # Handle events for property selection popup
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the correct x position for the property popup
            x_position: int = getattr(self, 'property_popup_x', self.x)
            
            # Adjust mouse position relative to property popup
            adjusted_pos: Tuple[int, int] = (event.pos[0] - x_position, event.pos[1] - self.y)
            
            # Check if any property button was clicked
            for i, (button_rect, property) in enumerate(self.property_buttons):
                if button_rect.collidepoint(adjusted_pos):
                    self.selected_property = property
                    return True, property
                
        # No property was selected
        return False, None
    
    def show(self, screen: pygame.Surface, player: Player) -> Tuple[Optional[str], Optional[Property]]:
        # Create clock for controlling the frame rate
        clock: pygame.time.Clock = pygame.time.Clock()
        
        # STEP 1: First display the sell or mortgage choice popup
        sell_or_mortgage_running: bool = True
        while sell_or_mortgage_running:
            # Draw the initial popup
            self.draw_sell_or_mortgage_popup(screen)
            
            # Update the display
            pygame.display.flip()
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Allow graceful exit without crashing
                    sell_or_mortgage_running = False
                    return None, None
                
                # Handle sell/mortgage decision events
                if self.sell_or_mortgage_handle_events(event):
                    sell_or_mortgage_running = False  # Exit this step once an option is selected
            
            # Cap the frame rate
            clock.tick(60)
        
        # If user closed the popup without selecting
        if self.sell_or_mortgage_choice is None:
            return None, None
        
        # STEP 2: Show property selection popup based on first choice
        action: str = self.sell_or_mortgage_choice  # Store whether they chose sell or mortgage
        self.selected_property = None
        
        # Display property selection popup
        property_running: bool = True
        while property_running:
            # Draw the property selection popup (different for sell vs mortgage)
            self.draw_select_property_popup(screen, player, sell=(action == "sell"), mortgage=(action == "mortgage"))
            
            # Update the display
            pygame.display.flip()
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None
                
                # Handle property selection events
                selected, prop = self.select_property_handle_events(event, player)
                if selected:
                    property_running = False
            
            # Cap the frame rate
            clock.tick(60)
        
        # Return both the action (sell/mortgage) and the selected property
        return action, self.selected_property

    def draw_button(self, screen: pygame.Surface, button_rect: pygame.Rect, text: str, 
            hover: bool, color: Tuple[int, int, int]) -> None:
        # Apply hover effect if mouse is over button
        if hover:
            color = self.BUTTON_HOVER_COLOR
        
        # Draw button with rounded corners
        pygame.draw.rect(screen, color, button_rect, 0, 5)
        pygame.draw.rect(screen, self.POPUP_BORDER_COLOR, button_rect, 1, 5)
        
        # Render and center text on button
        text_surface: pygame.Surface = self.button_font.render(text, True, self.POPUP_TEXT_COLOR)
        text_rect: pygame.Rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
    
    

