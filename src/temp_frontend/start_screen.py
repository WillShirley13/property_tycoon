import pygame
import sys

def display_start_screen(screen, screen_width, screen_height):
    """
    Display a start screen with player name inputs and a start button.
    Adapts to dynamic screen sizes.
    
    Args:
        screen (pygame.Surface): The game screen
        screen_width (int): Width of the screen
        screen_height (int): Height of the screen
        
    Returns:
        list: List of player names (empty strings removed)
    """
    # Initialize pygame font
    pygame.font.init()
    
    # Colors
    BACKGROUND_COLOR = (240, 240, 240)
    TITLE_COLOR = (50, 120, 50)  # Dark green for title
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (70, 130, 70)  # Green for button
    BUTTON_HOVER_COLOR = (90, 150, 90)  # Lighter green for hover
    INPUT_BG_COLOR = (255, 255, 255)
    INPUT_BORDER_COLOR = (200, 200, 200)
    
    # Scale fonts based on screen size
    title_size = max(int(screen_height * 0.09), 36)
    subtitle_size = max(int(screen_height * 0.035), 18)
    button_size = max(int(screen_height * 0.04), 20)
    input_size = max(int(screen_height * 0.03), 16)
    
    # Fonts
    try:
        title_font = pygame.font.SysFont('Arial', title_size, bold=True)
        subtitle_font = pygame.font.SysFont('Arial', subtitle_size)
        button_font = pygame.font.SysFont('Arial', button_size, bold=True)
        input_font = pygame.font.SysFont('Arial', input_size)
    except:
        title_font = pygame.font.SysFont(None, title_size, bold=True)
        subtitle_font = pygame.font.SysFont(None, subtitle_size)
        button_font = pygame.font.SysFont(None, button_size, bold=True)
        input_font = pygame.font.SysFont(None, input_size)
    
    # Input boxes setup - scale based on screen size
    input_boxes = []
    input_texts = [""] * 5  # Up to 5 players
    active_box = -1
    
    # Create input box rectangles - scale based on screen size
    box_width = int(screen_width * 0.4)
    box_height = int(screen_height * 0.05)
    box_margin = int(screen_height * 0.025)
    
    for i in range(5):
        box_x = (screen_width - box_width) // 2
        box_y = screen_height // 2 - 50 + (box_height + box_margin) * i
        input_boxes.append(pygame.Rect(box_x, box_y, box_width, box_height))
    
    # Start button - scale based on screen size
    button_width = int(screen_width * 0.25)
    button_height = int(screen_height * 0.075)
    button_x = (screen_width - button_width) // 2
    button_y = input_boxes[-1].bottom + box_margin * 2
    start_button = pygame.Rect(button_x, button_y, button_width, button_height)
    
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
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_box = i
                        break
                else:
                    active_box = -1
                
                # Check if start button was clicked
                if start_button.collidepoint(event.pos):
                    # Filter out empty player names
                    player_names = [name for name in input_texts if name.strip()]
                    if player_names:  # Ensure at least one player
                        return player_names
                    
            if event.type == pygame.KEYDOWN:
                if active_box != -1:
                    if event.key == pygame.K_RETURN:
                        active_box = -1  # Deselect on Enter
                    elif event.key == pygame.K_BACKSPACE:
                        input_texts[active_box] = input_texts[active_box][:-1]
                    else:
                        # Limit input length to prevent overflow
                        if len(input_texts[active_box]) < 20:
                            input_texts[active_box] += event.unicode
        
        # Fill background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_surface = title_font.render("Property Tycoon", True, TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = subtitle_font.render("Enter player names (2-5 players)", True, TEXT_COLOR)
        subtitle_rect = subtitle_surface.get_rect(center=(screen_width // 2, title_rect.bottom + 30))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw input boxes and labels
        for i, box in enumerate(input_boxes):
            # Draw box
            border_color = (0, 150, 0) if i == active_box else INPUT_BORDER_COLOR
            pygame.draw.rect(screen, INPUT_BG_COLOR, box)
            pygame.draw.rect(screen, border_color, box, 2)
            
            # Draw label
            label_text = f"Player {i+1} name:"
            label_surface = input_font.render(label_text, True, TEXT_COLOR)
            label_x = box.x - label_surface.get_width() - 10
            if label_x < 10:  # Ensure label doesn't go off screen
                label_x = box.x
                label_y = box.y - label_surface.get_height() - 5
            else:
                label_y = box.y + (box.height - label_surface.get_height()) // 2
            screen.blit(label_surface, (label_x, label_y))
            
            # Draw input text
            text_surface = input_font.render(input_texts[i], True, TEXT_COLOR)
            screen.blit(text_surface, (box.x + 10, box.y + (box.height - text_surface.get_height()) // 2))
        
        # Draw start button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if start_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, start_button, border_radius=10)
        pygame.draw.rect(screen, (30, 100, 30), start_button, 2, border_radius=10)  # Border
        
        # Draw button text
        button_text = button_font.render("Start Game", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=start_button.center)
        screen.blit(button_text, button_text_rect)
        
        pygame.display.flip()
        clock.tick(30)
    
    # Default return if loop exits unexpectedly
    return ["Player 1"] 