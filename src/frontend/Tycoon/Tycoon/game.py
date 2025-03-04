#Where game is run
import pygame
import random
import dice
import menu

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
#creates a variable to set font size and function to make texts

rolled_number = None #Stores the last drawn dice
    
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
        menu_command = menu.draw_game()
        if menu_command == 5: 
             main_menu = False
             show_text = False
             rolled_number = None #Dice dissapears when exit menu is clicked
        
                
    else:
        menu_command = menu.draw_main_menu() 
        if menu_command == 5: #Start game is pressed
             main_menu = True
             show_text = False
        elif menu_command == 4: #Enter Names button is clicked, show_text will be true and displays certain stuff
             input_active = True 
             input_text = "" #Input text
             show_text = True

    if show_text: #This only appears as long as the button you pressed was the "Enter names button"
        text = font.render('Enter your name', True, 'black')
        screen.blit(text, (300, 100))

    if rolled_number is not None: #Draw the last rolled dice (if any)
        dice.draw_dice(rolled_number)

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
                    rolled_number = random.randint(1, 6) # Roll new dice
                    if not main_menu: #Dice will not display if you're in the main menu
                        rolled_number = None 
                    
        #pygame.display.update()
        #timer.tick(60)

    if input_active and show_text: # The input box dissapears if you pressed any other buttons
        input_rect = pygame.Rect(50, 100, 200, 32) #Size of the name input box
        pygame.draw.rect(screen, black, input_rect, 2)
        input_surface = font.render(input_text, True, black)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

    if show_text:     # Display player names
        y_offset = 150 # distance of input away from hte input box
        for player in players:
            name_surface = font.render(player, True, black)
            screen.blit(name_surface, (50, y_offset))
            y_offset += 30 #distance between the name inputs

    pygame.display.flip()
pygame.quit()    