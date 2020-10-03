import pygame
# from pygame_widgets import Slider
import colors
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker
from drawablesController import DrawablesController

pygame.init()

mx, my = 0, 0
WIDTH, HEIGHT = 700, 700
# define window
screenDimensions = (WIDTH, HEIGHT)
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

# Create fonts for interface
title_font = pygame.font.SysFont(None, 60)
button_font = pygame.font.SysFont(None, 25)

# Function to create and draw text object
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Function runs the main menu 
def main_menu():
    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    while True:
 
        screen.fill((255, 245, 112))        # Fill background
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position
        title_bar = pygame.Rect(0, 0, 700, 100)

        # Create start and quit buttons with rect
        start_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/4), 200, 50)
        quit_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/3), 200, 50)

        # Check if mouse is on a button when clicked
        if start_button.collidepoint((m1x, m1y)):   # Calls main program if start is selected
            if click:
                main_prog()
        if quit_button.collidepoint((m1x, m1y)):    # Quits game on quit button click
            if click:
                pygame.quit()
        
        # Drawing the buttons and text for menu
        pygame.draw.rect(screen, (245, 222, 47), title_bar)
        draw_text('Main Menu', title_font, (8, 41, 255), screen, int(WIDTH/2), int(HEIGHT/12))
        pygame.draw.rect(screen, (8, 41, 255), start_button)
        draw_text('Start', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/4)+25))
        pygame.draw.rect(screen, (8, 41, 255), quit_button)
        draw_text('Quit', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+25))

        # Main event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(60)
 


def main_prog():
    mx = 0      # Get error if you don't set value for mx and my here
    my = 0      # Maybe pass as parameter for main_prog()
    # create clicking tracker
    click = False
    # Bool to decide when program ends
    isProgramRunning = True

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
        for rect in drawablesController.rectangles:
            rect.update(click,mx,my)
        for cm in drawablesController.cutmarkers:
            cm.update(click)

        # Menu button and logic to go back to main screen
        menu_button = pygame.Rect(WIDTH-100, 0, 100, 50)
        if menu_button.collidepoint((mx, my)):
            if click:
                main_menu()
        
        # drawing here
        screen.fill(colors.GREY) #fill screen bg    

        # Drawing menu button
        pygame.draw.rect(screen, (8, 41, 255), menu_button)
        draw_text('Main Menu', button_font, (0,0,0), screen, WIDTH-50, 25)

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

# Call main menu
main_menu()