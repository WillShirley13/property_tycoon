import pygame
import os

pygame.init()
screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption('Property Tycoon')
timer = pygame.time.Clock()
fps = 60

# Color scheme
DARK_BLUE = (25, 25, 112)  # Darker blue
BABY_BLUE = (137, 207, 240)  # Light baby blue
GOLD = (255, 215, 0)
CREAM = (255, 248, 231)
SOFT_RED = (219, 80, 74)
FOREST_GREEN = (34, 139, 34)
black = (0, 0, 0)
white = (255, 255, 255)

# Font setup - assuming fonts are in a 'fonts' directory
try:
    text_font = pygame.font.Font('fonts/Montserrat-Regular.ttf', 15)
    big_font = pygame.font.Font('fonts/Montserrat-Bold.ttf', 80)
    button_font = pygame.font.Font('fonts/Montserrat-SemiBold.ttf', 20)
except:
    text_font = pygame.font.SysFont('Arial', 15)
    big_font = pygame.font.Font(None, 80)
    button_font = pygame.font.SysFont('Arial', 20)

def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))
#creates a variable to set font size and function to make texts

def draw_rotated_button(surface, text, center_pos, angle, bg_color, text_color, padding=20):
    # Create text surface
    text_surface = button_font.render(text, True, text_color)
    
    # Create button surface with padding
    button_width = text_surface.get_width() + padding * 2
    button_height = text_surface.get_height() + padding * 2
    button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    
    # Draw button background
    pygame.draw.rect(button_surface, bg_color, (0, 0, button_width, button_height), border_radius=10)
    
    # Add text to button
    button_surface.blit(text_surface, (padding, padding))
    
    # Rotate button
    rotated_button = pygame.transform.rotate(button_surface, angle)
    button_rect = rotated_button.get_rect(center=center_pos)
    
    # Draw to screen
    surface.blit(rotated_button, button_rect.topleft)
    return button_rect

rects = [
    pygame.Rect(200, 510, 120, 120),
    pygame.Rect(320, 510, 51, 120),
    pygame.Rect(371, 510, 51, 120),
    pygame.Rect(422, 510, 51, 120),
    pygame.Rect(473, 510, 51, 120),
    pygame.Rect(524, 510, 51, 120),
    pygame.Rect(575, 510, 51, 120),
    pygame.Rect(626, 510, 51, 120),
    pygame.Rect(677, 510, 120, 120),
    pygame.Rect(677, 450, 120, 60),
    pygame.Rect(677, 390, 120, 60),
    pygame.Rect(677, 330, 120, 60),
    pygame.Rect(677, 270, 120, 60),
    pygame.Rect(677, 210, 120, 60),
    pygame.Rect(677, 150, 120, 60),
    pygame.Rect(677, 30, 120, 120),
    pygame.Rect(617, 30, 60, 120),
    pygame.Rect(557, 30, 60, 120),
    pygame.Rect(497, 30, 60, 120),
    pygame.Rect(437, 30, 60, 120),
    pygame.Rect(377, 30, 60, 120),
    pygame.Rect(317, 30, 60, 120),
]



#main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill(CREAM)  # Changed background to cream color

    # Color and draw all board squares
    # Left side squares
    for i in range(7):
        if i == 0:
            continue  # Skip the first square as it's handled by corner squares
        color = BABY_BLUE if i % 2 == 0 else DARK_BLUE
        pygame.draw.rect(screen, color, (200, 150 + ((i-1) * 60), 120, 60))
        pygame.draw.rect(screen, DARK_BLUE, (200, 150 + ((i-1) * 60), 120, 60), 2)

    # Bottom row squares
    for i, rect in enumerate(rects[:9]):
        if i == 0:  # Skip GO square
            continue
        color = BABY_BLUE if i % 2 == 1 else DARK_BLUE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK_BLUE, rect, 2)

    # Right side squares
    for i, rect in enumerate(rects[9:15]):
        color = BABY_BLUE if i % 2 == 0 else DARK_BLUE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK_BLUE, rect, 2)

    # Top row squares
    for i, rect in enumerate(rects[15:]):
        color = BABY_BLUE if i % 2 == 1 else DARK_BLUE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, DARK_BLUE, rect, 2)

    # Corner squares in FOREST_GREEN
    pygame.draw.rect(screen, FOREST_GREEN, rects[0])  # GO square
    pygame.draw.rect(screen, FOREST_GREEN, rects[8])  # Right bottom corner
    pygame.draw.rect(screen, FOREST_GREEN, rects[15])  # Top right corner
    pygame.draw.rect(screen, FOREST_GREEN, (200, 30, 120, 120))  # Top left corner
    
    # Re-draw borders for corner squares
    pygame.draw.rect(screen, DARK_BLUE, rects[0], 2)  # GO square border
    pygame.draw.rect(screen, DARK_BLUE, rects[8], 2)  # Right bottom corner border
    pygame.draw.rect(screen, DARK_BLUE, rects[15], 2)  # Top right corner border
    pygame.draw.rect(screen, DARK_BLUE, (200, 30, 120, 120), 2)  # Top left corner border

    # Player list section with new colors
    pygame.draw.rect(screen, DARK_BLUE, (0, 30, 150, 20))
    draw_text('List of Players', text_font, white, 22, 30)
    pygame.draw.rect(screen, BABY_BLUE, (0, 50, 150, 70))

    draw_text('Player 1', text_font, DARK_BLUE, 10, 50)
    draw_text('Player 2', text_font, DARK_BLUE, 10, 65)
    draw_text('Player 3', text_font, DARK_BLUE, 10, 80)
    draw_text('Player 4 (Jail)', text_font, DARK_BLUE, 10, 95)

    # Leaderboard with new styling
    pygame.draw.rect(screen, DARK_BLUE, (0, 220, 150, 30))
    draw_text('LEADERBOARD', text_font, white, 10, 220)
    for i in range(4):
        pygame.draw.rect(screen, BABY_BLUE, (0, 237 + (i * 30), 150, 30))

    # Replace the old GO text with a styled button
    draw_rotated_button(screen, 'GO', (260, 560), 45, FOREST_GREEN, white)

    # Replace the chance text with a styled button
    draw_rotated_button(screen, '?', (400, 260), 45, SOFT_RED, white)

    # Update the community chest display
    chest = pygame.image.load("chest.png").convert_alpha()
    chest2 = pygame.transform.scale(chest, (80, 80))
    chest_button = draw_rotated_button(screen, 'CHEST', (600, 430), 45, GOLD, DARK_BLUE)
    
    # Rotate and display chest image on top of the button
    rotated_chest = pygame.transform.rotate(chest2, 45)
    rotated_rect = rotated_chest.get_rect(center=(600, 430))
    screen.blit(rotated_chest, rotated_rect.topleft)

    # Add dice to center
    dice = pygame.image.load("dice.png").convert_alpha()
    dice2 = pygame.transform.scale(dice, (80, 80))
    dice2.set_colorkey(white)
    screen.blit(dice2, (450, 300))

    # Bank section
    pygame.draw.rect(screen, DARK_BLUE, (830, 400, 150, 50))
    draw_text('BANK', text_font, white, 875, 420)
    pygame.draw.rect(screen, BABY_BLUE, (830, 450, 150, 180))
    draw_text('Total Balance', text_font, DARK_BLUE, 850, 460)
    draw_text('Player Balance', text_font, DARK_BLUE, 850, 490)

    # Property info section
    pygame.draw.rect(screen, DARK_BLUE, (850, 200, 130, 20))
    draw_text('Property', text_font, white, 880, 200)
    pygame.draw.rect(screen, BABY_BLUE, (850, 200, 130, 150))
    draw_text('Cost', text_font, DARK_BLUE, 860, 230)
    draw_text('Owner', text_font, DARK_BLUE, 860, 250)
    draw_text('Mortgage', text_font, DARK_BLUE, 860, 270)
    draw_text('Name', text_font, DARK_BLUE, 860, 290)
    draw_text('Houses', text_font, DARK_BLUE, 860, 310)

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()    
    
