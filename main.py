import pygame
import colors
from drawText import draw_text
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker
from drawablesController import DrawablesController
from mouseHolder import MouseHandler

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

# create drawable object lists
rectangles = list()
cutMarkers = list()
guideLines = list()
bgSquares = list()
drawablesController = DrawablesController(rectangles, cutMarkers, guideLines, bgSquares)
testRectangle = Rectangle(350,350,350,350,screen,drawablesController,True)
testRectangle.createCutMarkers(3,4)
mouse = MouseHandler()

# create bool to decide when mouse is clicked
check = False

# Function runs the main menu 
def main_menu():
    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    while True:
 
        screen.fill((255, 245, 112))        # Fill background
        screen.blit(background_img, (0, 100))
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position
        title_bar = pygame.Rect(0, 0, 695, 100)

        # Create start and quit buttons with rect
        start_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/4), 200, 50)
        quit_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/3), 200, 50)

        # Check if mouse is on a button when clicked
        if start_button.collidepoint((m1x, m1y)):   # Calls main program if start is selected
            if click:
                main_prog()
        if quit_button.collidepoint((m1x, m1y)):    # Quits game on quit button click
            if click:
                quit_message()
        
        # Drawing the buttons and text for menu
        pygame.draw.rect(screen, (245, 222, 47), title_bar)
        pygame.draw.rect(screen, (0, 0, 0), title_bar, 7)
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
    isProgramRunning = True
    check = False
    click = False       # To check if Main Menu button is clicked
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
                    click = True
                    if mouse.isHeld == False:
                        mouse.setHeld(True)
                    else:
                        mouse.setHeld(False)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    check = False
                    #setClick(check)
                    click = False
                    #hold = False
        
            ###        
    
        # main logic here
        for rect in drawablesController.rectangles:
            rect.update(mouse.isClick,mouse.mx,mouse.my,mouse.isHeld)
        for cm in drawablesController.cutmarkers:
            cm.update(mouse.isClick)

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