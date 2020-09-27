import pygame
import colors
from rectangle import Rectangle
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

# main loop
while isProgramRunning:
    # main event loop -- user keyboard/mouse input here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isProgramRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left mouse button click
                print("left mouse")
    
    # main logic here
    for cm in cutMarkers:
        cm.update()

    # drawing here
    screen.fill(colors.GREY) #fill screen bg

    testRectangle.draw()
    for cm in cutMarkers:
        cm.draw()

    # pygame.draw.line(screen,GREEN, [0, 0], [100, 100], 5) !This function may be useful for dividing up rectangle with line

    #update screen and set framerate
    pygame.display.flip()
    clock.tick(fps)

#end of main loop
pygame.quit()

