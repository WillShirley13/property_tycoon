import pygame

def draw_board(screen):
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # Board dimensions for a larger screen
    BOARD_SIZE = 720  # Reduced board size
    CORNER_SIZE = 72  # Size of corner spaces (square)
    SPACE_HEIGHT = 72  # Height of spaces on top/bottom
    SIDE_HEIGHT = 64  # Height of spaces on left/right sides
    GAP = 2  # Small gap between spaces
    
    # Calculate the width of non-corner spaces to fit 9 spaces on top/bottom
    SPACE_WIDTH = (BOARD_SIZE - 2 * CORNER_SIZE) / 9
    
    # Center the board on the screen
    START_X = (1280 - BOARD_SIZE) // 2
    START_Y = (768 - BOARD_SIZE) // 2
    
    # Draw the outer border of the board
    pygame.draw.rect(screen, BLACK, (START_X, START_Y, BOARD_SIZE, BOARD_SIZE), 2)
    
    # Draw corner spaces
    # Bottom-left corner (GO)
    pygame.draw.rect(screen, BLACK, 
                    (START_X, START_Y + BOARD_SIZE - CORNER_SIZE, CORNER_SIZE, CORNER_SIZE), 2)
    # Bottom-right corner (Go To Jail)
    pygame.draw.rect(screen, BLACK, 
                    (START_X + BOARD_SIZE - CORNER_SIZE, START_Y + BOARD_SIZE - CORNER_SIZE, CORNER_SIZE, CORNER_SIZE), 2)
    # Top-right corner (Free Parking)
    pygame.draw.rect(screen, BLACK, 
                    (START_X + BOARD_SIZE - CORNER_SIZE, START_Y, CORNER_SIZE, CORNER_SIZE), 2)
    # Top-left corner (Jail)
    pygame.draw.rect(screen, BLACK, 
                    (START_X, START_Y, CORNER_SIZE, CORNER_SIZE), 2)
    
    # Draw bottom row spaces (excluding corners)
    for i in range(9):
        pygame.draw.rect(screen, BLACK, 
                      (START_X + CORNER_SIZE + i * SPACE_WIDTH + GAP, 
                       START_Y + BOARD_SIZE - SPACE_HEIGHT, 
                       SPACE_WIDTH - GAP, SPACE_HEIGHT - GAP), 2)
    
    # Draw top row spaces (excluding corners)
    for i in range(9):
        pygame.draw.rect(screen, BLACK, 
                      (START_X + CORNER_SIZE + i * SPACE_WIDTH + GAP, 
                       START_Y, 
                       SPACE_WIDTH - GAP, SPACE_HEIGHT - GAP), 2)
    
    # Draw left column spaces (excluding corners)
    for i in range(9):
        pygame.draw.rect(screen, BLACK, 
                      (START_X, 
                       START_Y + CORNER_SIZE + i * SIDE_HEIGHT + GAP, 
                       CORNER_SIZE - GAP, SIDE_HEIGHT - GAP), 2)
    
    # Draw right column spaces (excluding corners)
    for i in range(9):
        pygame.draw.rect(screen, BLACK, 
                      (START_X + BOARD_SIZE - CORNER_SIZE, 
                       START_Y + CORNER_SIZE + i * SIDE_HEIGHT + GAP, 
                       CORNER_SIZE - GAP, SIDE_HEIGHT - GAP), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 768))
    pygame.display.set_caption("Monopoly Board")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        draw_board(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
