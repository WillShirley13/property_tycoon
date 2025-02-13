import pygame

pygame.init()
WIDTH = 1300
HEIGHT = 680
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Property Tycoon')
#font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0) #creating a variable to represent colour code

text_font = pygame.font.SysFont('Arial', 20)
def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))
#main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    pygame.draw.rect(screen, black, (0, 0, 100, 100), 1)
    pygame.draw.rect(screen, black, (0, 100,100, 80 ), 1)
    pygame.draw.rect(screen, black, (0, 180,100, 80 ), 1)
    pygame.draw.rect(screen, black, (0, 260,100, 80 ), 1)
    pygame.draw.rect(screen, black, (0, 340,100, 80 ), 1)
    pygame.draw.rect(screen, black, (0, 420,100, 80 ), 1)
    pygame.draw.rect(screen, black, (0, 500,100, 80 ), 1)
 

    pygame.draw.rect(screen, black, (0, 580,100, 100 ), 1)
    pygame.draw.rect(screen, black, (100, 580,80, 100 ), 1)
    pygame.draw.rect(screen, black, (180, 580,80, 100 ), 1)
    pygame.draw.rect(screen, black, (260, 580,80, 100 ), 1)
    pygame.draw.rect(screen, black, (340, 580,80, 100 ), 1)
    pygame.draw.rect(screen, black, (420, 580,80, 100 ), 1)
    pygame.draw.rect(screen, black, (500, 580,80, 100 ), 1)

    pygame.draw.rect(screen, black, (580, 580,100, 100 ), 1)
    pygame.draw.rect(screen, black, (580, 500, 100, 80 ), 1)
    pygame.draw.rect(screen, black, (580, 420, 100, 80 ), 1)
    pygame.draw.rect(screen, black, (580, 340, 100, 80 ), 1)
    pygame.draw.rect(screen, black, (580, 260, 100, 80 ), 1)
    pygame.draw.rect(screen, black, (580, 180, 100, 80 ), 1)
    pygame.draw.rect(screen, black, (580, 100, 100, 80 ), 1)

    pygame.draw.rect(screen, black, (580, 0, 100, 100 ), 1)
    pygame.draw.rect(screen, black, (500, 0, 80, 100 ), 1)
    pygame.draw.rect(screen, black, (420, 0, 80, 100 ), 1)
    pygame.draw.rect(screen, black, (340, 0, 80, 100 ), 1)
    pygame.draw.rect(screen, black, (260, 0, 80, 100 ), 1)
    pygame.draw.rect(screen, black, (180, 0, 80, 100 ), 1)
    pygame.draw.rect(screen, black, (100, 0, 80, 100 ), 1)

    pygame.draw.rect(screen, black, (800, 0, 400, 200 ), 1)
    draw_text('Players', text_font, black, 945, 0)
    draw_text('Player 1: $1500', text_font, black, 850, 50)


    pygame.draw.rect(screen, black, (800, 400, 400, 200 ), 1)
    draw_text('Properties', text_font, black, 945, 400)

    
    


    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()    