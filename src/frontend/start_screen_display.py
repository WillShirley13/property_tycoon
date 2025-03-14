import pygame
import sys
from frontend.board_text_utils import wrap_text

class StartScreenDisplay:
    def __init__(self, screen_width, screen_height):
        """
        Initialize the start screen display.
        
        Args:
            screen_width (int): Width of the screen
            screen_height (int): Height of the screen
        """
        # Initialize pygame font
        pygame.font.init()
        
        # Colors
        self.BACKGROUND_COLOR = (240, 240, 240)
        self.TITLE_COLOR = (50, 120, 50)  # Dark green for title
        self.TEXT_COLOR = (0, 0, 0)
        self.BUTTON_COLOR = (70, 130, 70)  # Green for button
        self.BUTTON_HOVER_COLOR = (90, 150, 90)  # Lighter green for hover
        self.INPUT_BG_COLOR = (255, 255, 255)
        self.INPUT_BORDER_COLOR = (200, 200, 200)
        
        # Screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Scale fonts based on screen size
        self.title_size = max(int(screen_height * 0.09), 36)
        self.subtitle_size = max(int(screen_height * 0.035), 18)
        self.button_size = max(int(screen_height * 0.04), 20)
        self.input_size = max(int(screen_height * 0.03), 16)
        
        # Initialize fonts
        try:
            self.title_font = pygame.font.SysFont('Arial', self.title_size, bold=True)
            self.subtitle_font = pygame.font.SysFont('Arial', self.subtitle_size)
            self.button_font = pygame.font.SysFont('Arial', self.button_size, bold=True)
            self.input_font = pygame.font.SysFont('Arial', self.input_size)
        except:
            self.title_font = pygame.font.SysFont(None, self.title_size, bold=True)
            self.subtitle_font = pygame.font.SysFont(None, self.subtitle_size)
            self.button_font = pygame.font.SysFont(None, self.button_size, bold=True)
            self.input_font = pygame.font.SysFont(None, self.input_size)
        
        # Input boxes setup
        self.setup_input_boxes()
        
        # Setup start button
        self.setup_start_button()
    
    def setup_input_boxes(self):
        """Set up the input boxes for player names."""
        self.input_boxes = []
        self.input_texts = [""] * 5  # Up to 5 players
        self.active_box = -1
        
        # Create input box rectangles - scale based on screen size
        box_width = int(self.screen_width * 0.4)
        box_height = int(self.screen_height * 0.05)
        box_margin = int(self.screen_height * 0.025)
        
        for i in range(5):
            box_x = (self.screen_width - box_width) // 2
            box_y = self.screen_height // 2 - 50 + (box_height + box_margin) * i
            self.input_boxes.append(pygame.Rect(box_x, box_y, box_width, box_height))
    
    def setup_start_button(self):
        """Set up the start button."""
        button_width = int(self.screen_width * 0.25)
        button_height = int(self.screen_height * 0.075)
        button_x = (self.screen_width - button_width) // 2
        button_y = self.input_boxes[-1].bottom + int(self.screen_height * 0.025) * 2
        self.start_button = pygame.Rect(button_x, button_y, button_width, button_height)
    
    def display(self, screen):
        """
        Display the start screen and get player names.
        
        Args:
            screen (pygame.Surface): The game screen
            
        Returns:
            list: List of player names
        """
        # Main loop for start screen
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any input box was clicked
                    for i, box in enumerate(self.input_boxes):
                        if box.collidepoint(event.pos):
                            self.active_box = i
                            break
                    else:
                        self.active_box = -1
                    
                    # Check if start button was clicked
                    if self.start_button.collidepoint(event.pos):
                        # Filter out empty player names
                        player_names = [name.capitalize() for name in self.input_texts if name.strip()]
                        if player_names:  # Ensure at least one player
                            return player_names
                        
                if event.type == pygame.KEYDOWN:
                    if self.active_box != -1:
                        if event.key == pygame.K_RETURN:
                            self.active_box = -1  # Deselect on Enter
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_texts[self.active_box] = self.input_texts[self.active_box][:-1]
                        else:
                            # Limit input length to prevent overflow
                            if len(self.input_texts[self.active_box]) < 20:
                                self.input_texts[self.active_box] += event.unicode
            
            self.draw(screen)
            pygame.display.flip()
            clock.tick(30)
        
        # Default return if loop exits unexpectedly
        return []
    
    def draw(self, screen):
        """Draw the start screen elements."""
        # Fill background
        screen.fill(self.BACKGROUND_COLOR)
        
        # Draw title
        title_surface = self.title_font.render("Property Tycoon", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = self.subtitle_font.render("Enter player names (1-5 players)", True, self.TEXT_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, title_rect.bottom + 30))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw input boxes and labels
        for i, box in enumerate(self.input_boxes):
            # Draw box
            border_color = (0, 150, 0) if i == self.active_box else self.INPUT_BORDER_COLOR
            pygame.draw.rect(screen, self.INPUT_BG_COLOR, box)
            pygame.draw.rect(screen, border_color, box, 2)
            
            # Draw label
            label_text = f"Player {i+1} name:"
            label_surface = self.input_font.render(label_text, True, self.TEXT_COLOR)
            label_x = box.x - label_surface.get_width() - 10
            if label_x < 10:  # Ensure label doesn't go off screen
                label_x = box.x
                label_y = box.y - label_surface.get_height() - 5
            else:
                label_y = box.y + (box.height - label_surface.get_height()) // 2
            screen.blit(label_surface, (label_x, label_y))
            
            # Draw input text
            text_surface = self.input_font.render(self.input_texts[i], True, self.TEXT_COLOR)
            screen.blit(text_surface, (box.x + 10, box.y + (box.height - text_surface.get_height()) // 2))
        
        # Draw start button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.BUTTON_HOVER_COLOR if self.start_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        pygame.draw.rect(screen, button_color, self.start_button, border_radius=10)
        pygame.draw.rect(screen, (30, 100, 30), self.start_button, 2, border_radius=10)  # Border
        
        # Draw button text
        button_text = self.button_font.render("Start Game", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.start_button.center)
        screen.blit(button_text, button_text_rect) 