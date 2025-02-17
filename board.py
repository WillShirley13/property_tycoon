import pygame


pygame.init()
screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption('Property Tycoon')
#font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0) 
white = (255, 255, 255)
#creating variables to represent colour code

text_font = pygame.font.SysFont('Arial', 15)
big_font = pygame.font.Font(None, 80)
def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))
#creates a variable to set font size and function to make texts

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
    screen.fill('white')

    pygame.draw.rect(screen, black, (0, 30, 150, 20), 2)
    draw_text('List of Players', text_font, black, 22, 30)
    pygame.draw.rect(screen, black, (0, 50, 150, 70), 2)

    draw_text('Player 1', text_font, black, 10, 50)
    draw_text('Player 2', text_font, black, 10, 65)
    draw_text('Player 3', text_font, black, 10, 80)
    draw_text('Player 4 (Jail)', text_font, black, 10, 95)
    #List of players table

    draw_text('LEADERBOARD', text_font, black, 10, 220)
    pygame.draw.rect(screen, black, (0, 237, 150, 30), 2)
    pygame.draw.rect(screen, black, (0, 267, 150, 30), 2)
    pygame.draw.rect(screen, black, (0, 297, 150, 30), 2)
    pygame.draw.rect(screen, black, (0, 327, 150, 30), 2)
    #Leaderboard

    pygame.draw.rect(screen, black, (0, 500, 150, 30), 2)
    draw_text('Current Player', text_font, black, 22, 505)
    pygame.draw.rect(screen, black, (0, 530, 150, 100), 2)
    draw_text('Money', text_font, black, 10, 535)
    draw_text('Properties', text_font, black, 10, 555)
    #Current Player Table

    pygame.draw.rect(screen, black, (200, 30, 120, 120), 2)
    pygame.draw.rect(screen, black, (200, 150, 120, 60), 2)
    pygame.draw.rect(screen, black, (200, 210, 120, 60), 2)
    pygame.draw.rect(screen, black, (200, 270, 120, 60), 2)
    pygame.draw.rect(screen, black, (200, 330, 120, 60), 2)
    pygame.draw.rect(screen, black, (200, 390, 120, 60), 2)
    pygame.draw.rect(screen, black, (200, 450, 120, 60), 2)

    rect_surface = pygame.Surface((130, 80), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 0, 0))  
    pygame.draw.rect(rect_surface, black, (0, 0, 130, 80), 2)
    angle = 45 
    rotated_surface = pygame.transform.rotate(rect_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(400, 250))
    screen.blit(rotated_surface, rotated_rect.topleft)

    text_surface = big_font.render('?', True, black)
    rotated_text = pygame.transform.rotate(text_surface, 45)
    text_rect = rotated_text.get_rect(center=(400, 260))
    screen.blit(rotated_text, text_rect.topleft)
    #Chance



    text_surface = big_font.render('GO', True, black)
    rotated_text = pygame.transform.rotate(text_surface, 45)
    text_rect = rotated_text.get_rect(center=(260, 560))
    screen.blit(rotated_text, text_rect.topleft)
    #Big GO sign

    rect_surface = pygame.Surface((130, 80), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 0, 0))  
    pygame.draw.rect(rect_surface, black, (0, 0, 130, 80), 2)
    angle = 45
    rotated_surface = pygame.transform.rotate(rect_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(600, 430))
    screen.blit(rotated_surface, rotated_rect.topleft)

    chest = pygame.image.load("chest.png").convert_alpha()
    chest2 = pygame.transform.scale(chest, (80, 80)) #scales the image
    #chest2.set_colorkey(white)
    angle = 45  # Change this to rotate to a different angle
    rotated_chest = pygame.transform.rotate(chest2, angle)
    rotated_rect = rotated_chest.get_rect(center=(600, 430))  # Adjust position
    screen.blit(rotated_chest, rotated_rect.topleft)
    #community chest

    dice = pygame.image.load("dice.png").convert_alpha()
    dice2 = pygame.transform.scale(dice, (80, 80))
    dice2.set_colorkey(white) #scales the image
    screen.blit(dice2, (450, 300))

    # angle = 45  # Change this to rotate to a different angle
    # rotated_chest = pygame.transform.rotate(chest2, angle)
    # rotated_rect = rotated_chest.get_rect(center=(600, 430))  # Adjust position
    # screen.blit(rotated_chest, rotated_rect.topleft)



    for rect in rects:
        pygame.draw.rect(screen, black, rect, 2)

    pygame.draw.rect(screen, black, (830, 400, 150, 50), 2)
    draw_text('BANK', text_font, black, 875, 420)
    pygame.draw.rect(screen, black, (830, 450, 150, 180), 2)
    draw_text('Total Balance', text_font, black, 850, 460)
    draw_text('Player Balance', text_font, black, 850, 490)

    pygame.draw.rect(screen, black, (850, 200, 130, 20), 2)
    draw_text('Property', text_font, black, 880, 200)
    pygame.draw.rect(screen, black, (850, 200, 130, 150), 2)
    draw_text('Cost', text_font, black, 860, 230)
    draw_text('Owner', text_font, black, 860, 250)
    draw_text('Mortgage', text_font, black, 860, 270)
    draw_text('Name', text_font, black, 860, 290)
    draw_text('Houses', text_font, black, 860, 310)


    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()    
    
    


    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()    
