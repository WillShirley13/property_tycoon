import pygame
import random

rects = [
    pygame.Rect(200, 0, 100, 100, ),
    pygame.Rect(200, 100, 100, 50),
    pygame.Rect(200, 150, 100, 50),
    pygame.Rect(200, 200, 100, 50),
    pygame.Rect(200, 250, 100, 50),
    pygame.Rect(200, 300, 100, 50),
    pygame.Rect(200, 350, 100, 50),
    pygame.Rect(200, 400, 100, 50),
    pygame.Rect(200, 450, 100, 50),
    pygame.Rect(200, 500, 100, 50),
    #top left to bottom

    pygame.Rect(200, 550, 100, 100),
    pygame.Rect(300, 550, 50, 100),
    pygame.Rect(350, 550, 50, 100),
    pygame.Rect(400, 550, 50, 100),
    pygame.Rect(450, 550, 50, 100),
    pygame.Rect(500, 550, 50, 100),
    pygame.Rect(550, 550, 50, 100),
    pygame.Rect(600, 550, 50, 100),
    pygame.Rect(650, 550, 50, 100),
    pygame.Rect(700, 550, 50, 100),
    pygame.Rect(750, 550, 100, 100),
    # #Bottom left to right

    pygame.Rect(750, 500, 100, 50),
    pygame.Rect(750, 450, 100, 50),
    pygame.Rect(750, 400, 100, 50),
    pygame.Rect(750, 350, 100, 50),
    pygame.Rect(750, 300, 100, 50),
    pygame.Rect(750, 250, 100, 50),
    pygame.Rect(750, 200, 100, 50),
    pygame.Rect(750, 150, 100, 50),
    pygame.Rect(750, 100, 100, 50),
    pygame.Rect(750, 0, 100, 100),
    # #Bottom right to top
    
    pygame.Rect(700, 0, 50, 100),
    pygame.Rect(650, 0, 50, 100),
    pygame.Rect(600, 0, 50, 100),
    pygame.Rect(550, 0, 50, 100),
    pygame.Rect(500, 0, 50, 100),
    pygame.Rect(450, 0, 50, 100),
    pygame.Rect(400, 0, 50, 100),
    pygame.Rect(350, 0, 50, 100),
    pygame.Rect(300, 0, 50, 100),

]
#coordinates and sizes for the board
screen = pygame.display.set_mode([1280, 720])
black = (0, 0, 0)

# middle_coords = [rect.center for rect in rects]

# # Display the middle coordinates
# for idx, coord in enumerate(middle_coords):
#     print(f"Rectangle {idx + 1} center: {coord}") (Finds coordinates of each rectangles)

# Rectangle 1 center: (250, 50)
# Rectangle 2 center: (250, 125)
# Rectangle 3 center: (250, 175)
# Rectangle 4 center: (250, 225)
# Rectangle 5 center: (250, 275)
# Rectangle 6 center: (250, 325)
# Rectangle 7 center: (250, 375)
# Rectangle 8 center: (250, 425)
# Rectangle 9 center: (250, 475)
# Rectangle 10 center: (250, 525)
# Rectangle 11 center: (250, 600)
# Rectangle 12 center: (325, 600)
# Rectangle 13 center: (375, 600)
# Rectangle 14 center: (425, 600)
# Rectangle 15 center: (475, 600)
# Rectangle 16 center: (525, 600)
# Rectangle 17 center: (575, 600)
# Rectangle 18 center: (625, 600)
# Rectangle 19 center: (675, 600)
# Rectangle 20 center: (725, 600)
# Rectangle 21 center: (800, 600)
# Rectangle 22 center: (800, 525)
# Rectangle 23 center: (800, 475)
# Rectangle 24 center: (800, 425)
# Rectangle 25 center: (800, 375)
# Rectangle 26 center: (800, 325)
# Rectangle 27 center: (800, 275)
# Rectangle 28 center: (800, 225)
# Rectangle 29 center: (800, 175)
# Rectangle 30 center: (800, 125)
# Rectangle 31 center: (800, 50)
# Rectangle 32 center: (725, 50)
# Rectangle 33 center: (675, 50)
# Rectangle 34 center: (625, 50)
# Rectangle 35 center: (575, 50)
# Rectangle 36 center: (525, 50)
# Rectangle 37 center: (475, 50)
# Rectangle 38 center: (425, 50)
# Rectangle 39 center: (375, 50)
# Rectangle 40 center: (325, 50)


def makeBoard():
    for rect in rects:
        pygame.draw.rect(screen, black, rect, 2)
    #draws out the board
