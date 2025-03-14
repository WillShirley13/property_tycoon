import pygame

from backend.property_owners.player import Player


class JailPopup:
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize the jail popup component.
        
        Args:
            x (int): X position of the popup
            y (int): Y position of the popup
            width (int): Width of the popup
            height (int): Height of the popup
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.result = None
        
        # Colors
        self.POPUP_BG_COLOR = (240, 240, 240)  # Light gray background
        self.POPUP_BORDER_COLOR = (0, 0, 0)
        self.POPUP_TEXT_COLOR = (0, 0, 0)
        self.BUTTON_COLOR = (144, 238, 144)  # Light green
        self.BUTTON_HOVER_COLOR = (180, 180, 180)
        self.BUTTON_DISABLED_COLOR = (150, 150, 150)
        
        # Define font sizes
        title_size = 20
        button_size = 14
        
        # Fonts - properly assign them to self attributes
        try:
            self.title_font = pygame.font.SysFont('Arial', title_size, bold=True)
            self.button_font = pygame.font.SysFont('Arial', button_size, bold=True)
        except:
            self.title_font = pygame.font.SysFont(None, title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, button_size, bold=True)
        
        # Create a surface for the popup with a solid background
        self.popup_surface = pygame.Surface((width, height))
        
        # Create buttons vertically stacked
        button_width = width - 40  # Leave some margin on both sides
        button_height = 50
        
        # Button positions (y coordinates)
        roll_y = 80
        card_y = roll_y + button_height + 10
        pay_y = card_y + button_height + 10
        
        # Create button rectangles
        self.stay_in_jail_button = pygame.Rect(self.x + 20, self.y + roll_y, button_width, button_height)
        self.use_card_button = pygame.Rect(self.x + 20, self.y + card_y, button_width, button_height)
        self.pay_fine_button = pygame.Rect(self.x + 20, self.y + pay_y, button_width, button_height)
        
        # Button states
        self.stay_in_jail_hover = False
        self.use_card_hover = False
        self.pay_fine_hover = False
        
    def draw(self, screen, player: Player):
        """
        Draw the jail popup on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw on
            player (Player): The player who is in jail
        """
        # # Draw semi-transparent overlay
        # overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        # overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        # screen.blit(overlay, (0, 0))
        
        # Draw popup background
        pygame.draw.rect(screen, self.POPUP_BG_COLOR, (self.x, self.y, self.width, self.height), 0, 10)
        pygame.draw.rect(screen, self.POPUP_BORDER_COLOR, (self.x, self.y, self.width, self.height), 2, 10)
        
        # Draw title
        title_text = "You're in Jail!"
        title_surface = self.title_font.render(title_text, True, self.POPUP_TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.x + self.width // 2, self.y + 30))
        screen.blit(title_surface, title_rect)
        
        # Draw buttons
        self.draw_button(screen, self.stay_in_jail_button, "Stay in Jail", self.stay_in_jail_hover, self.BUTTON_COLOR)
        
        # Check if player has a get out of jail card
        has_card = player.get_get_out_of_jail_cards() > 0
        card_color = self.BUTTON_COLOR if has_card else self.BUTTON_DISABLED_COLOR
        self.use_card_hover = self.use_card_hover if has_card else False
        self.draw_button(screen, self.use_card_button, "Use Get Out of Jail Free Card", self.use_card_hover, card_color)
        
        # Check if player has enough money to pay the fine
        has_money = player.get_cash_balance() >= 50  # Assuming fine is 50
        pay_color = self.BUTTON_COLOR if has_money else self.BUTTON_DISABLED_COLOR
        self.pay_fine_hover = self.pay_fine_hover if has_money else False
        self.draw_button(screen, self.pay_fine_button, "Pay £50 Fine", self.pay_fine_hover, pay_color)
    
    def draw_button(self, screen, button_rect, text, hover, color):
        """
        Draw a button on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw on
            button_rect (pygame.Rect): The rectangle defining the button position and size
            text (str): The text to display on the button
            hover (bool): Whether the mouse is hovering over the button
            color (tuple, optional): The color of the button. If None, uses the default button color.
        """
        if hover:
            color = self.BUTTON_HOVER_COLOR
            
        pygame.draw.rect(screen, color, button_rect, 0, 5)
        pygame.draw.rect(screen, self.POPUP_BORDER_COLOR, button_rect, 1, 5)
        
        text_surface = self.button_font.render(text, True, self.POPUP_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_events(self, event, player):
        """
        Handle events for the jail popup.
        
        Args:
            event (pygame.event.Event): The event to handle
            player (Player): The player who is in jail
            
        Returns:
            bool: True if the popup should close, False otherwise
        """
        # Check for mouse motion for hover effects
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.stay_in_jail_hover = self.stay_in_jail_button.collidepoint(mouse_pos)
            self.use_card_hover = self.use_card_button.collidepoint(mouse_pos) and player.get_get_out_of_jail_cards() > 0
            self.pay_fine_hover = self.pay_fine_button.collidepoint(mouse_pos) and player.get_cash_balance() >= 50
        
        # Check for mouse clicks on buttons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            
            # Roll doubles button
            if self.stay_in_jail_button.collidepoint(mouse_pos):
                # Logic for rolling doubles would go here
                # For now, just set the result and return True to close the popup
                print("Stay in Jail button clicked")
                self.result = 'stayed'
                return True
            
            # Use card button
            if self.use_card_button.collidepoint(mouse_pos) and player.get_get_out_of_jail_cards() > 0:
                print("Use card button clicked")
                self.result = 'used_card'
                return True
            
            # Pay fine button
            if self.pay_fine_button.collidepoint(mouse_pos) and player.get_cash_balance() >= 50:
                print("Pay fine button clicked")
                self.result = 'paid_fine'
                return True
        
        return False
    
    def show(self, screen, player: Player):
        """
        Display the jail popup and handle all interactions until a button is clicked.
        
        Args:
            screen (pygame.Surface): The surface to draw on
            player (Player): The player who is in jail
            
        Returns:
            str: The result of the interaction ('used_card', 'paid_fine', or 'stayed')
        """
        # Create a clock for controlling frame rate
        clock = pygame.time.Clock()
        
        running = True
        self.result = None
        
        while running:
            # Draw the popup
            self.draw(screen, player)
            
            # Update the display
            pygame.display.flip()
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                
                # Handle popup events
                if self.handle_events(event, player):
                    running = False
            
            # Cap the frame rate
            clock.tick(60)
        
        return self.result
        