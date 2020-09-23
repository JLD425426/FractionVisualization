import pygame
from rectangle import Rectangle

pygame.init()

# define colors !temporary here, at some point we will want to move these constants to another file
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
PURPLE = ( 227, 39, 211)
GREY = (136, 140, 139)

# define window
screenDimensions = (700, 700)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("425 Project")

# define bool to decide when program ends
isProgramRunning = True

# clock controls framerate of program
clock = pygame.time.Clock()
fps = 60

# create rectangle class
testRectangle = Rectangle(175,175,350,350,screen)

# main loop
while isProgramRunning:
    # main event loop -- user keyboard/mouse input here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isProgramRunning = False
    
    # main logic here

    # drawing here
    screen.fill(GREY) #clear screen to white

    testRectangle.draw()

    # pygame.draw.line(screen,GREEN, [0, 0], [100, 100], 5) !This function may be useful for dividing up rectangle with line

    #update screen and set framerate
    pygame.display.flip()
    clock.tick(fps)

#end of main loop
pygame.quit()

