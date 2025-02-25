import pygame
import random

pygame.init()
screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption('Property Tycoon')
#font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0) 
red=(255,0,0)
white = (255, 255, 255)
#creating variables to represent colour code
font = pygame.font.Font('freesansbold.ttf', 24)
text_font = pygame.font.SysFont('Arial', 15)
big_font = pygame.font.Font(None, 80)
def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))
#creates a variable to set font size and function to make texts

rects = [
    pygame.Rect(200, 30, 120, 120),
    pygame.Rect(200, 150, 120, 60),
    pygame.Rect(200, 210, 120, 60),
    pygame.Rect(200, 270, 120, 60),
    pygame.Rect(200, 330, 120, 60),
    pygame.Rect(200, 390, 120, 60),
    pygame.Rect(200, 450, 120, 60),
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
#coordinates and sizes for the board

class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (200, 40))

    def draw(self):
            pygame.draw.rect(screen, 'Light gray', self.button, 0, 5)
            pygame.draw.rect(screen, 'dark gray', self.button, 5, 5)
            text = font.render(self.text, True, 'black')
            screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False
    
    
#Button class

def draw_main_menu():
    pygame.draw.rect(screen, 'gray', [50, 50, 1100, 700])
    command = 0
    start_button = Button('Play game', (470, 250))
    start_button.draw()
    enter_name = Button('Enter names', (470, 300))
    enter_name.draw()
    if enter_name.check_clicked():
        command = 4
    if start_button.check_clicked():
         command = 5
    return command


    # menu_btn = pygame.draw.rect(screen, 'light gray', [230, 450, 260, 40], 0, 5)
    # pygame.draw.rect(screen, 'dark gray', [230, 450, 260, 40], 5, 5)
    # text = font.render('Main Menu', True, 'black')
    # screen.blit(text, (245, 457))
    # if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
    #     menu = True
    # else:
    #     menu = False
    # return menu 

def draw_game():
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

    # dice = pygame.image.load("dice.png").convert_alpha()
    # dice2 = pygame.transform.scale(dice, (80, 80))
    # dice2.set_colorkey(white) #scales the image
    # screen.blit(dice2, (450, 300))

    # angle = 45  # Change this to rotate to a different angle
    # rotated_chest = pygame.transform.rotate(chest2, angle)
    # rotated_rect = rotated_chest.get_rect(center=(600, 430))  # Adjust position
    # screen.blit(rotated_chest, rotated_rect.topleft)



    for rect in rects:
        pygame.draw.rect(screen, black, rect, 2)
    #draws out the board

    pygame.draw.rect(screen, black, (830, 400, 150, 50), 2)
    draw_text('BANK', text_font, black, 875, 420)
    pygame.draw.rect(screen, black, (830, 450, 150, 180), 2)
    draw_text('Total Balance', text_font, black, 850, 460)
    draw_text('Player Balance', text_font, black, 850, 490)
    #bank

    pygame.draw.rect(screen, black, (850, 200, 130, 20), 2)
    draw_text('Property', text_font, black, 880, 200)
    pygame.draw.rect(screen, black, (850, 200, 130, 150), 2)
    draw_text('Cost', text_font, black, 860, 230)
    draw_text('Owner', text_font, black, 860, 250)
    draw_text('Mortgage', text_font, black, 860, 270)
    draw_text('Name', text_font, black, 860, 290)
    draw_text('Houses', text_font, black, 860, 310)

    command = 0
    #pop up screen
    # menu_btn = pygame.draw.rect(screen, 'light gray', [120, 350, 260, 40], 0, 5)
    # pygame.draw.rect(screen, 'dark gray', [120, 350, 260, 40], 5, 5)
    # text = font.render('Exit Menu', True, 'black')
    # screen.blit(text, (135, 357))
    # if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
    #     menu = False
    # else:
    #     menu = True
    # return menu 
    pygame.draw.rect(screen, 'black', [1000, 300, 200, 200])
    menu_btn = Button('Exit Menu', (1000, 300))
    menu_btn.draw()
    if menu_btn.check_clicked():
         command = 5
    return command

def dice():
    x,y=450, 300
    r= random.randint(1, 6)
    pygame.draw.rect(screen,(255,0,0),(x,y,100,100))
    if r==1:
        pygame.draw.circle(screen,black,(x+50,y+50),10) 
    elif r==2:
        pygame.draw.circle(screen,black,(x+30,y+30),10)
        pygame.draw.circle(screen,black,(x+70,y+70),10)
    elif r==3:
        pygame.draw.circle(screen,black,(x+30,y+30),10)
        pygame.draw.circle(screen,black,(x+50,y+50),10)
        pygame.draw.circle(screen,black,(x+70,y+70),10)

    elif r==4:
        pygame.draw.circle(screen,black,(x+30,y+30),10)
        pygame.draw.circle(screen,black,(x+70,y+30),10)
        pygame.draw.circle(screen,black,(x+30,y+70),10) 
        pygame.draw.circle(screen,black,(x+70,y+70),10)
    elif r==5:
        pygame.draw.circle(screen,black,(x+30,y+30),10)
        pygame.draw.circle(screen,black,(x+70,y+30),10)
        pygame.draw.circle(screen,black,(x+50,y+50),10) 
        pygame.draw.circle(screen,black,(x+30,y+70),10)
        pygame.draw.circle(screen,black,(x+70,y+70),10)
    elif r==6:
        pygame.draw.circle(screen,black,(x+30,y+25),10) 
        pygame.draw.circle(screen,black,(x+70,y+25),10)
        pygame.draw.circle(screen,black,(x+70,y+75),10) 
        pygame.draw.circle(screen,black,(x+30,y+50),10)
        pygame.draw.circle(screen,black,(x+70,y+50),10)
        pygame.draw.circle(screen,black,(x+30,y+75),10)   



menu_command = 0
main_menu = None
show_text = False #New variable to track if text should be displayed

players = []
input_active = False
input_text = ""

#main game loop
run = True
while run:
    # timer.tick(fps)
    screen.fill('white')
    timer.tick(fps)
    if main_menu:
        menu_command = draw_game()
        if menu_command == 5:
             main_menu = False
             show_text = False
        
                
    else:
        menu_command = draw_main_menu()
        if menu_command == 5:
             main_menu = True
             show_text = False
        elif menu_command == 4: #Enter Names button is clicked
             input_active = True 
             input_text = "" #Input text
             show_text = True

    if show_text: #This only appears as long as the button you pressed was the "Enter names button"
        text = font.render('Enter your name', True, 'black')
        screen.blit(text, (100, 200))
        
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:
                if input_text.strip():  # Add only non-empty names
                    players.append(input_text)
                input_active = False  # Disable input mode
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode 
        if event.type == pygame.QUIT:
            run = False
        if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    dice()
                    pygame.display.update()
    
    if input_active and show_text: # The input box dissapears if you pressed any other buttons
        input_rect = pygame.Rect(50, 100, 200, 32) #Size of the name input box
        pygame.draw.rect(screen, black, input_rect, 2)
        input_surface = font.render(input_text, True, black)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

    # Display player names
    y_offset = 150 # distance of input away from hte input box
    for player in players:
        name_surface = font.render(player, True, black)
        screen.blit(name_surface, (50, y_offset))
        y_offset += 30 #distance between the name inputs

    pygame.display.flip()
pygame.quit()    
