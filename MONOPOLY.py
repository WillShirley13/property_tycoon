import pygame
import random
import time , os 
pygame.init()

screen = pygame.display.set_mode((500, 600))
font1 = pygame.font.SysFont("comicsans", 20)
font2 = pygame.font.SysFont("comicsans", 20)
#colours for dice
white=(225,255,255)
red=(255,0,0)
black=(0,0,0)
screen.fill(white)
pygame.display.update()
end= True
x,y=200,250

def dice():
    screen.fill(white)
    
    
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
        
end =True
while end ==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end= False
            if event.type== pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    dice()
                    pygame.display.update()
pygame.quit()
