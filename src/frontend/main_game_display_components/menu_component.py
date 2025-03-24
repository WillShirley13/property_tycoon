import pygame
import time

# Initialize Pygame
pygame.init()

# Screen settings to change
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test - In-Game Menu")

# Colors dont matter
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 200, 0)

# Fonts
FONT = pygame.font.Font(None, 40)

# Menu options
MENU_OPTIONS = ["Rules", "Save Game", "Exit"]
BUTTONS = []

# Timer setup
start_time = time.time()

# Background placeholder
BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
BACKGROUND.fill((30, 30, 30))  # Dark gray background

def draw_timer(screen):
    """Displays the elapsed time in the menu."""
    elapsed_time = int(time.time() - start_time)
    timer_text = FONT.render(f"Time: {elapsed_time}s", True, WHITE)
    screen.blit(timer_text, (650, 20))

def draw_menu(screen, mouse_pos):
    """Draws the options menu."""
    screen.blit(BACKGROUND, (0, 0))
    BUTTONS.clear()

    for i, option in enumerate(MENU_OPTIONS):
        text = FONT.render(option, True, WHITE)
        text_rect = text.get_rect(center=(400, 200 + i * 80))

        # Highlight button if mouse is over it
        if text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, text_rect.inflate(20, 10), border_radius=10)

        screen.blit(text, text_rect)
        BUTTONS.append((option, text_rect))

    draw_timer(screen)
    pygame.display.flip()

def show_rules(screen):
    """Displays a placeholder rules screen and waits for click to return."""
    rules_image = pygame.Surface((WIDTH, HEIGHT))
    rules_image.fill((50, 50, 50))  # Gray placeholder

    screen.blit(rules_image, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    return True

def options_menu(screen, background, return_to_game=None):
    """Main menu loop."""
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        draw_menu(screen, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option, rect in BUTTONS:
                    if rect.collidepoint(event.pos):
                        if option == "Rules":
                            running = show_rules(screen)
                        elif option == "Save Game":
                            print("Game saved!")
                        elif option == "Exit":
                            if return_to_game:
                                return_to_game()
                            else:
                                return False  # If running standalone, just exit

        clock.tick(30)
    return True

def main():
    """Test mode: Run the menu independently."""
    options_menu(SCREEN, BACKGROUND)

if __name__ == "__main__":
    main()