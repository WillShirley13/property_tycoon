import pygame
import sys

class TimeLimitChoiceDisplay:
    def __init__(self, screen_width, screen_height):
        """
        Initialize the time limit choice display.
        
        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
        """
        # Store screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colors
        self.BACKGROUND_COLOR = (240, 240, 240)
        self.BUTTON_COLOR = (70, 130, 70)  # Green for button
        self.BUTTON_HOVER_COLOR = (90, 150, 90)  # Lighter green for hover
        self.BUTTON_INACTIVE_COLOR = (150, 150, 150)  # Inactive button
        
        # Fonts
        self.title_size = max(int(screen_height * 0.05), 24)
        self.button_size = max(int(screen_height * 0.04), 20)
        
        try:
            self.title_font = pygame.font.SysFont('Arial', self.title_size, bold=True)
            self.button_font = pygame.font.SysFont('Arial', self.button_size)
        except:
            self.title_font = pygame.font.SysFont(None, self.title_size, bold=True)
            self.button_font = pygame.font.SysFont(None, self.button_size)
        
        # Setup buttons
        self.setup_buttons()
    
    def setup_buttons(self):
        """Set up the buttons for time limit options."""
        # Create button rectangles - scale based on screen size
        button_width = int(self.screen_width * 0.25)
        button_height = int(self.screen_height * 0.075)
        button_margin = int(self.screen_height * 0.02)
        
        # Time limit options
        self.time_options = [0, 30, 60, 90, 120]
        self.buttons = []
        
        # Create buttons for each time option
        for i, time in enumerate(self.time_options):
            button_x = (self.screen_width - button_width) // 2
            button_y = self.screen_height // 2 - 50 + (button_height + button_margin) * i
            self.buttons.append((pygame.Rect(button_x, button_y, button_width, button_height), time))
    
    def display(self, screen):
        """
        Display a dialog to get the time limit for the game.
        
        Args:
            screen (pygame.Surface): The game screen
            
        Returns:
            int: The time limit in minutes (0 for no time limit)
        """
        # Main loop for time limit dialog
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any button was clicked
                    for button, time in self.buttons:
                        if button.collidepoint(event.pos):
                            return time
            
            self.draw(screen)
            pygame.display.flip()
            clock.tick(30)
        
        # Default return if loop exits unexpectedly
        return 0
    
    def draw(self, screen):
        """
        Draw the time limit choice screen elements.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Fill background
        screen.fill(self.BACKGROUND_COLOR)
        
        # Draw title
        title_text = "Select Game Time Limit"
        title_surface = self.title_font.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title_surface, title_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button, time in self.buttons:
            # Check if mouse is over button
            button_color = self.BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else self.BUTTON_COLOR
            
            # Draw button
            pygame.draw.rect(screen, button_color, button, border_radius=10)
            pygame.draw.rect(screen, (30, 100, 30), button, 2, border_radius=10)  # Border
            
            # Draw button text
            if time == 0:
                button_text = "No Time Limit"
            else:
                button_text = f"{time} Minutes"
                
            text_surface = self.button_font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect) 