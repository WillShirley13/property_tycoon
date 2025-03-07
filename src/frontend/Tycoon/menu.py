#Contains the function that draws out the menu, main game, the button class and other property boxes
import pygame
import board

pygame.init()
screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption('Property tycoon')
#font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0) 
red= (255,0,0)
white = (255, 255, 255)
#creating variables to represent colour code
font = pygame.font.Font('freesansbold.ttf', 24)
text_font = pygame.font.SysFont('Arial', 15)
big_font = pygame.font.Font(None, 80)
def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))


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
    rotated_rect = rotated_surface.get_rect(center=(400, 200))
    screen.blit(rotated_surface, rotated_rect.topleft)
    #rectangle box for Chance

    text_surface = big_font.render('?', True, black)
    rotated_text = pygame.transform.rotate(text_surface, 45)
    text_rect = rotated_text.get_rect(center=(400, 200))
    screen.blit(rotated_text, text_rect.topleft)
    # #Chance

    text_surface = big_font.render('GO', True, black)
    rotated_text = pygame.transform.rotate(text_surface, 45)
    text_rect = rotated_text.get_rect(center=(260, 600))
    screen.blit(rotated_text, text_rect.topleft)
    # #Big GO sign

    rect_surface = pygame.Surface((130, 80), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 0, 0))  
    pygame.draw.rect(rect_surface, black, (0, 0, 130, 80), 2)
    angle = 45
    rotated_surface = pygame.transform.rotate(rect_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(650, 450))
    screen.blit(rotated_surface, rotated_rect.topleft)
    # #Rectangle box for the chest

    chest = pygame.image.load("chest.png").convert_alpha()
    chest2 = pygame.transform.scale(chest, (80, 80)) #scales the image
    chest2.set_colorkey(white)
    angle = 45  # Change this to rotate to a different angle
    rotated_chest = pygame.transform.rotate(chest2, angle)
    rotated_rect = rotated_chest.get_rect(center=(650, 450))  # Adjust position
    screen.blit(rotated_chest, rotated_rect.topleft)
    # #community chest

    board.makeBoard() #Draws the main board

    pygame.draw.rect(screen, black, (980, 400, 150, 50), 2)
    draw_text('BANK', text_font, black, 1025, 420)
    pygame.draw.rect(screen, black, (980, 450, 150, 180), 2)
    draw_text('Total Balance', text_font, black, 1000, 460)
    draw_text('Player Balance', text_font, black, 1000, 490)

    #bank

    pygame.draw.rect(screen, black, (1000, 200, 130, 20), 2)
    draw_text('Property', text_font, black, 1030, 200)
    pygame.draw.rect(screen, black, (1000, 200, 130, 150), 2)
    draw_text('Cost', text_font, black, 1010, 230)
    draw_text('Owner', text_font, black, 1010, 250)
    draw_text('Mortgage', text_font, black, 1010, 270)
    draw_text('Name', text_font, black, 1010, 290)
    draw_text('Houses', text_font, black, 1010, 310)
    #property table

    command = 0
    #pygame.draw.rect(screen, 'black', [1000, 300, 100, 100])
    menu_btn = Button('Exit Menu', (1070, 30))
    menu_btn.draw()
    if menu_btn.check_clicked():
         command = 5
    return command
