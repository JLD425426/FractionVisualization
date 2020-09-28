import pygame
import colors
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker

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
cutMarkers = testRectangle.createCutMarkers(6)

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
    for cm in cutMarkers:
        cm.update()

    # drawing here
    screen.fill(colors.GREY) #fill screen bg    
    testRectangle.draw()
    # if user clicks outside of rectangle fill screen red, inside fill screen green
    if click: 
        if mx <= 175 or my <=175: #outside rectangle
            screen.fill(colors.RED) 
        if mx >= 525 or my >= 525: #outside rectangle
            screen.fill(colors.RED) 
        elif mx >= 175 and my >= 175: #click inside rectangle
            if mx <= 525 and my <= 525:
                screen.fill(colors.GREEN)     

    for cm in cutMarkers:
        cm.draw()

    #update screen and set framerate
    pygame.display.flip()
    clock.tick(fps)

#end of main loop
pygame.quit()

