import pygame
import random

screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption('Property tycoon')
#font = pygame.font.Font('freesansbold.ttf', 30)
timer = pygame.time.Clock()
fps = 60
black = (0, 0, 0) 
red= (255,0,0)
white = (255, 255, 255)

def draw_dice(r):
    """Draw the dice with the given number."""
    x, y = 470, 300  # Dice position

    pygame.draw.rect(screen, red, (x, y, 100, 100))
    
    dots = {
        1: [(x + 50, y + 50)],
        2: [(x + 30, y + 30), (x + 70, y + 70)],
        3: [(x + 30, y + 30), (x + 50, y + 50), (x + 70, y + 70)],
        4: [(x + 30, y + 30), (x + 70, y + 30), (x + 30, y + 70), (x + 70, y + 70)],
        5: [(x + 30, y + 30), (x + 70, y + 30), (x + 50, y + 50), (x + 30, y + 70), (x + 70, y + 70)],
        6: [(x + 30, y + 25), (x + 70, y + 25), (x + 30, y + 50), (x + 70, y + 50), (x + 30, y + 75), (x + 70, y + 75)]
    }

    for dot in dots[r]:
        pygame.draw.circle(screen, black, dot, 10)