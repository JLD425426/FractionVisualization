import pygame
import colors
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker
from drawablesController import DrawablesController
from mouseHolder import MouseHandler

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

# create drawable object lists
rectangles = list()
cutMarkers = list()
guideLines = list()
drawablesController = DrawablesController(rectangles, cutMarkers, guideLines)
testRectangle = Rectangle(350,350,350,350,screen,drawablesController,True)
testRectangle.createCutMarkers(3,4)
mouse = MouseHandler()


# create bool to decide when mouse is clicked
check = False

# main loop
while isProgramRunning:
    # main event loop -- user keyboard/mouse input here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isProgramRunning = False
        ### replace with mouse class object setter
        mouse.update(check)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check = True
                if mouse.isHeld == False:
                    mouse.setHeld(True)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                check = False
                #setClick(check)
                #click = False
                #hold = False
        
        ###        
    
    # main logic here
    for rect in drawablesController.rectangles:
        rect.update(mouse.isClick,mouse.mx,mouse.my)
    for cm in drawablesController.cutmarkers:
        cm.update(mouse.isClick)

    # drawing here
    screen.fill(colors.GREY) #fill screen bg     

    for rect in drawablesController.rectangles:
        rect.draw() 
    for cm in drawablesController.cutmarkers:
        cm.draw()
    for gl in drawablesController.guidelines:
        gl.draw()

    # pygame.draw.rect(screen, colors.GREEN, [0,0,100,100],5)


    #update screen and set framerate
    pygame.display.flip()
    clock.tick(fps)

#end of main loop
pygame.quit()

