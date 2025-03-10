import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.admin import Admin
from backend.enums.game_token import GameToken
from temp_frontend.start_screen import display_start_screen
from temp_frontend.main_game_display import MainGameDisplay
from temp_frontend.space_data import BOARD_CONFIG, SPACE_COLORS
from backend.property_owners.bank import Bank
from backend.non_ownables.free_parking import FreeParking
from backend.non_ownables.go import Go
from backend.non_ownables.jail import Jail
from backend.non_ownables.game_card import GameCard
from backend.ownables.ownable import Ownable

def display_time_limit_dialog(screen, screen_width, screen_height):
    """
    Display a dialog to get the time limit for the game.
    
    Args:
        screen (pygame.Surface): The game screen
        screen_width (int): Width of the screen
        screen_height (int): Height of the screen
        
    Returns:
        int: The time limit in minutes (0 for no time limit)
    """
    # Colors
    BACKGROUND_COLOR = (240, 240, 240)
    BUTTON_COLOR = (70, 130, 70)  # Green for button
    BUTTON_HOVER_COLOR = (90, 150, 90)  # Lighter green for hover
    BUTTON_INACTIVE_COLOR = (150, 150, 150)  # Inactive button
    
    # Fonts
    title_size = max(int(screen_height * 0.05), 24)
    button_size = max(int(screen_height * 0.04), 20)
    
    try:
        title_font = pygame.font.SysFont('Arial', title_size, bold=True)
        button_font = pygame.font.SysFont('Arial', button_size)
    except:
        title_font = pygame.font.SysFont(None, title_size, bold=True)
        button_font = pygame.font.SysFont(None, button_size)
    
    # Create button rectangles - scale based on screen size
    button_width = int(screen_width * 0.25)
    button_height = int(screen_height * 0.075)
    button_margin = int(screen_height * 0.02)
    
    # Time limit options
    time_options = [0, 30, 60, 90, 120]
    buttons = []
    
    # Create buttons for each time option
    for i, time in enumerate(time_options):
        button_x = (screen_width - button_width) // 2
        button_y = screen_height // 2 - 50 + (button_height + button_margin) * i
        buttons.append((pygame.Rect(button_x, button_y, button_width, button_height), time))
    
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
                for button, time in buttons:
                    if button.collidepoint(event.pos):
                        return time
        
        # Fill background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_text = "Select Game Time Limit"
        title_surface = title_font.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_surface, title_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button, time in buttons:
            # Check if mouse is over button
            button_color = BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else BUTTON_COLOR
            
            # Draw button
            pygame.draw.rect(screen, button_color, button, border_radius=10)
            pygame.draw.rect(screen, (30, 100, 30), button, 2, border_radius=10)  # Border
            
            # Draw button text
            if time == 0:
                button_text = "No Time Limit"
            else:
                button_text = f"{time} Minutes"
                
            text_surface = button_font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        clock.tick(30)
    
    # Default return if loop exits unexpectedly
    return 0

def main():
    """
    Main function to run the Property Tycoon game.
    Displays the start screen first, then the board after player names are entered.
    """
    # Initialize pygame
    pygame.init()
    
    # Get the screen info to set up a dynamic display
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    
    # Create a window based on the configured percentage of the screen size
    window_width = int(screen_width * BOARD_CONFIG["screen_size_percentage"])
    window_height = int(screen_height * BOARD_CONFIG["screen_size_percentage"])
    screen = pygame.display.set_mode((window_width, window_height))
    
    # Set the window title
    pygame.display.set_caption("Property Tycoon")
    
    # Display the start screen and get player names
    player_names = display_start_screen(screen, window_width, window_height)
    
    # Display the time limit dialog and get the time limit
    time_limit = display_time_limit_dialog(screen, window_width, window_height)
    
    game_tokens = [GameToken.BOOT, GameToken.CAT, GameToken.HATSTAND, GameToken.IRON, GameToken.SHIP]
    # Frontend must pass names and tokens for each player
    player_data = [(player_names[i], game_tokens[i]) for i in range(len(player_names))]

    # Initialize Admin with player data and time limit
    admin = Admin(player_data, time_limit)

    # Print the player names (for debugging)
    print(f"Players: {player_data}")
    print(f"Time limit: {time_limit} minutes")
    
    # Create the main game display with the admin object
    main_game_display = MainGameDisplay(window_width, window_height, player_data, admin)
    
    # Start the game timer if a time limit was set
    if time_limit > 0:
        admin.start_timer()
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            # Handle events through the main game display
            running = main_game_display.handle_events()
        
        # Draw the main game display (includes board and player info)
        main_game_display.draw(screen)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 