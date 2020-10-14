import pygame
import colors
from drawText import draw_text
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker
from drawablesController import DrawablesController
from mouseHolder import MouseHandler
from stateManager import manager

pygame.init()

# Define dimensions for window
WIDTH, HEIGHT = 700, 700

# define window
screenDimensions = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("425 Project")

# Create fonts for interface
title_font = pygame.font.SysFont(None, 60)
button_font = pygame.font.SysFont(None, 25)
message_font = pygame.font.SysFont(None, 32)

# define bool to decide when program ends
isProgramRunning = True

# clock controls framerate of program
clock = pygame.time.Clock()
fps = 60

# Load image in for background
background_img = pygame.image.load("yellow_background.jpg")

# Create state manager
stateManager = manager("Cutting")

# create bool to decide when mouse is clicked
check = False

# Function runs the main menu 
def main_menu():

    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    while True:

        # Main event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = True
 
        screen.fill((255, 245, 112))        # Fill background
        screen.blit(background_img, (0, 100))
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position
        title_bar = pygame.Rect(0, 0, 695, 100)

        # Create start and quit buttons with rect
        start_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/4), 200, 50)
        quit_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/3), 200, 50)
        cuttingType_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/3)+ 60, 200, 50)

        # Check if mouse is on a button when clicked
        if start_button.collidepoint((m1x, m1y)):   # Calls main program if start is selected
            if click:
                main_prog()
        if quit_button.collidepoint((m1x, m1y)):    # Quits game on quit button click
            if click:
                quit_message()
        if cuttingType_button.collidepoint((m1x,m1y)):
            if click:
                if stateManager.cuttingType == stateManager.VARCUTTING:
                    stateManager.cuttingType = stateManager.CMCUTTING
                elif stateManager.cuttingType == stateManager.CMCUTTING:
                    stateManager.cuttingType = stateManager.VARCUTTING

        # Drawing the buttons and text for menu
        pygame.draw.rect(screen, (245, 222, 47), title_bar)
        pygame.draw.rect(screen, (0, 0, 0), title_bar, 7)
        draw_text('Main Menu', title_font, (8, 41, 255), screen, int(WIDTH/2), int(HEIGHT/12))
        pygame.draw.rect(screen, (8, 41, 255), start_button)
        draw_text('Start', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/4)+25))
        pygame.draw.rect(screen, (8, 41, 255), quit_button)
        draw_text('Quit', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+25))
        pygame.draw.rect(screen, (8, 41, 255), cuttingType_button)
        if stateManager.cuttingType == stateManager.CMCUTTING:
            draw_text('Cut with cutmarkers', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))
        elif stateManager.cuttingType == stateManager.VARCUTTING:
            draw_text('Variable cutting',button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))

        click = False
        pygame.display.update()
        clock.tick(60)
 
# Displays "are you sure you want to quit" message and gets click response
def quit_message():
    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    while True:
 
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position

        # Create pop up window
        pop_up = pygame.Rect(100, 50, 500, 500)

        # Create yes and no buttons with rect
        yes_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/3), 200, 50)
        no_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/2), 200, 50)

        # Check if mouse is on a button when clicked
        if no_button.collidepoint((m1x, m1y)):   # Calls main program if start is selected
            if click:
                main_menu()
        if yes_button.collidepoint((m1x, m1y)):    # Quits game on quit button click
            if click:
                pygame.quit()
        
        # Drawing the buttons and text for pop-up
        pygame.draw.rect(screen, (255, 255, 255), pop_up)
        draw_text('Are you sure you would like to quit?', message_font, (0,0,0), screen, WIDTH/2, HEIGHT/5)
        pygame.draw.rect(screen, (8, 41, 255), yes_button)
        draw_text('Yes', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+25))
        pygame.draw.rect(screen, (8, 41, 255), no_button)
        draw_text('No', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/2)+25))

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
    
    # create drawable object lists
    mouse = MouseHandler()
    drawablesController = DrawablesController()
    testRectangle = Rectangle(200,350,250,250,screen,drawablesController,True,mouse,stateManager)
    testRectangle2 = Rectangle(500,350,250,250,screen,drawablesController,True,mouse,stateManager)
    testRectangle2.setWillBeDivided(False)
    testRectangle.setupCutting(2,2)
    testRectangle2.setupCutting(2,2)

    isProgramRunning = True
    check = False
    click = False       # To check if Main Menu button is clicked
    # main loop
    while isProgramRunning:
        # main event loop -- user keyboard/mouse input here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isProgramRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    check = True
                    click = True
                    if mouse.isHeld == False:
                        mouse.setHeld(True)
                    else:
                        mouse.setHeld(False)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse.leftMouseReleasedThisFrame = True
                    check = False
                    #setClick(check)
                    click = False
                    #hold = False

        # update all objects
        mouse.update(check)
        for rect in drawablesController.rectangles:
            rect.update(mouse, stateManager)
        for cm in drawablesController.cutmarkers:
            cm.update(mouse.isClick)
    
        # UPDATE END
        # DRAW BEGIN

        # Menu button and logic to go back to main screen
        menu_button = pygame.Rect(WIDTH-100, 0, 100, 50)
        if menu_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                main_menu()

        # drawing here
        screen.fill(colors.GREY) #fill screen bg   

        # Drawing menu button
        pygame.draw.rect(screen, (8, 41, 255), menu_button)
        draw_text('Main Menu', button_font, (0,0,0), screen, WIDTH-50, 25)
        state_message = "Current state: " + stateManager.currentState
        draw_text(state_message, button_font, (0,0,0), screen, 100, 25)

        for bgS in drawablesController.bgSquares:
            bgS.draw()
        for rect in drawablesController.rectangles:
            rect.draw() 
        for cm in drawablesController.cutmarkers:
            cm.draw()
        for gl in drawablesController.guidelines:
            gl.draw()
        if mouse.whoisHeld != None:
            mouse.whoisHeld.draw()

        #this update must be after drawing b/c logic in cutterVariable draw()--will try to fix later so it can go with rest of updates
        mouse.leftMouseReleasedThisFrame = False
        # DRAW END

        #update screen and set framerate
        pygame.display.flip()
        clock.tick(fps)

    #end of main loop
    pygame.quit()

# Call main menu
main_menu()