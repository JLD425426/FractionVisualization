import pygame
import colors
from rectangle import Rectangle
from pygame.locals import *

pygame.init()

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

# create clicking tracker
click = False

# main loop
while isProgramRunning:
    # main event loop -- user keyboard/mouse input here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isProgramRunning = False
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True    
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click = False



    
    # main logic here

    # drawing here
    screen.fill(colors.GREY) #fill screen bg    
    testRectangle.draw()
    # if user clicks outside of rectangle, display red
    # if user hovers inside of rectangle, display green
    if click: 
        if mx <= 175 or my <=175:
            screen.fill(colors.RED) 
        if mx >= 525 or my >= 525:
            screen.fill(colors.RED) 
    else:
        if mx >= 175 and my >= 175:
            if mx <= 525 and my <= 525:
                screen.fill(colors.GREEN)     


    # pygame.draw.line(screen,GREEN, [0, 0], [100, 100], 5) !This function may be useful for dividing up rectangle with line

    #update screen and set framerate
    pygame.display.flip()
    clock.tick(fps)

#end of main loop
pygame.quit()

