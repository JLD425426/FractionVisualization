import pygame
import colors
from drawText import draw_text
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker
from drawablesController import DrawablesController
from mouseHolder import MouseHandler
from stateManager import manager
from stateManagerMult import StateManagerMult
from fractionHandler import Fraction


pygame.init()

# Define dimensions for window
WIDTH, HEIGHT = 700, 700

# define window
screenDimensions = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("425 Project")

# Create fonts for interface
title_font = pygame.font.SysFont('Arial', 60)
button_font = pygame.font.SysFont('Arial', 25)
message_font = pygame.font.SysFont('Arial', 32)

# define bool to decide when program ends
isProgramRunning = True

# clock controls framerate of program
clock = pygame.time.Clock()
fps = 60

# Load image in for background
background_img = pygame.image.load("yellow_background.jpg")

# Create state manager
stateManager = manager("cutting")

# create bool to decide when mouse is clicked
check = False

# constants for deciding cutting type and state manager type
FRACTIONCUTTING = 0
VARCUTTING = 1
CMCUTTING = 2
program_CuttingType = FRACTIONCUTTING

MULTIPLICATION = 0
ADDITION = 1
SUBTRACTION = 2
DIVISION = 3
program_OperationType = MULTIPLICATION

# Function runs the main menu 
def main_menu():

    global program_CuttingType
    global program_OperationType

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
        operationType_button = pygame.Rect(int((WIDTH/2))-100, int(HEIGHT/3)+ 120, 200, 50)

        # Check if mouse is on a button when clicked
        if start_button.collidepoint((m1x, m1y)):   # Calls main program if start is selected
            if click:
                main_prog()
        if quit_button.collidepoint((m1x, m1y)):    # Quits game on quit button click
            if click:
                quit_message()
        if cuttingType_button.collidepoint((m1x,m1y)):
            if click:
                if program_CuttingType == FRACTIONCUTTING:
                    program_CuttingType = VARCUTTING
                elif program_CuttingType == VARCUTTING:
                    program_CuttingType = CMCUTTING
                elif program_CuttingType == CMCUTTING:
                    program_CuttingType = FRACTIONCUTTING
        if operationType_button.collidepoint((m1x,m1y)):
            if click:
                if program_OperationType == MULTIPLICATION:
                    program_OperationType = ADDITION
                elif program_OperationType == ADDITION:
                    program_OperationType = SUBTRACTION
                elif program_OperationType == SUBTRACTION:
                    program_OperationType = DIVISION
                elif program_OperationType == DIVISION:
                    program_OperationType = MULTIPLICATION

        # Drawing the buttons and text for menu
        pygame.draw.rect(screen, (245, 222, 47), title_bar)
        pygame.draw.rect(screen, (0, 0, 0), title_bar, 7)
        draw_text('Main Menu', title_font, (8, 41, 255), screen, int(WIDTH/2), int(HEIGHT/12))
        pygame.draw.rect(screen, (8, 41, 255), start_button)
        draw_text('Start', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/4)+25))
        pygame.draw.rect(screen, (8, 41, 255), quit_button)
        draw_text('Quit', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+25))
        pygame.draw.rect(screen, (8, 41, 255), cuttingType_button)

        if program_CuttingType == CMCUTTING:
            draw_text('Cut with cutmarkers', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))
        elif program_CuttingType == VARCUTTING:
            draw_text('Variable cutting',button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))
        elif program_CuttingType == FRACTIONCUTTING:
            draw_text('Fraction cutting',button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))
        pygame.draw.rect(screen, (8, 41, 255), operationType_button)

        if program_OperationType == MULTIPLICATION:
            draw_text('Multiplication', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+145))
        elif program_OperationType == ADDITION:
            draw_text('Addition', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+145)) 
        elif program_OperationType == SUBTRACTION:
            draw_text('Subtraction', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+145)) 
        elif program_OperationType == DIVISION:
            draw_text('Division', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+145)) 

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
        draw_text('Are you sure you would like to quit?', message_font, (0,0,0), screen, 350, 140)
        pygame.draw.rect(screen, (8, 41, 255), yes_button)
        draw_text('Yes', button_font, (0,0,0), screen, 350, 258)
        pygame.draw.rect(screen, (8, 41, 255), no_button)
        draw_text('No', button_font, (0,0,0), screen, 350, 375)

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

    # create state manager depending on operation type selected in menu:
    if program_OperationType == MULTIPLICATION:
        stateManager = StateManagerMult(program_CuttingType,screen)
    elif program_OperationType == ADDITION:
        #stateManager = StateManagerAdd(program_CuttingType,screen)
        pass
    elif program_OperationType == SUBTRACTION:
        #stateManager = StateManagerSub(program_CuttingType,screen)
        pass
    elif program_OperationType == DIVISION:
        #stateManager = StateManagerDiv(program_CuttingType,screen)
        pass

    # create drawable object lists
    mouse = MouseHandler()
    stateManager.setMouse(mouse) # link state manager and mouse
    drawablesController = DrawablesController()
    stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller
    testRectangle = Rectangle(WIDTH/2,HEIGHT/2,350,350,screen,drawablesController,True,mouse,stateManager)
    cutter = testRectangle.getCutter() # need to get cutter here for draw call

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

        #---------UPDATE BEGIN-------UPDATE ALL OBJECTS
        mouse.update(check)
        stateManager.update(testRectangle.myCutter)
        
        for rect in drawablesController.rectangles:
            rect.update(mouse)
        for cm in drawablesController.cutmarkers:
            cm.update(mouse.isClick)
        
        
        # ---------UPDATE END----------------------------------
        # ---------DRAW BEGIN--------------------------------
        # Menu button and logic to go back to main screen
        menu_button = pygame.Rect(WIDTH-100, 0, 100, 50)
        if menu_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                main_menu()

        restart_button = pygame.Rect(WIDTH-250, 0, 100, 50)
        if restart_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                main_prog()
        
        # drawing here
        screen.fill(colors.GREY) #fill screen bg   

        # Drawing menu button
        pygame.draw.rect(screen, (8, 41, 255), menu_button)
        draw_text('Main Menu', button_font, (0,0,0), screen, WIDTH-50, 25)
        pygame.draw.rect(screen, (8, 41, 255), restart_button)
        draw_text('Restart', button_font, (0,0,0), screen, WIDTH-200, 25)
        state_message = "Current state: " + stateManager.getCurrentState()
        draw_text(state_message, button_font, (0,0,0), screen, 200, 25)
        
        if(stateManager.getCurrentState() == "Finished"):
            numerator, denominator = stateManager.get_answer()
            userAnswer = Fraction(numerator, denominator)
            canreduce = userAnswer.canReduce()
            #answer1 = userAnswer.ftoString()
            if canreduce == True:
                userAnswerReduced = Fraction(userAnswer.getNum(), userAnswer.getDenom())
                userAnswerReduced.finalReduce()
                #answer2 = userAnswerReduced.ftoString()
                draw_text(str(userAnswer.getNum()), button_font, (0,0,0), screen, WIDTH-437, HEIGHT-620)
                draw_text('---', button_font, (0,0,0), screen, WIDTH-437, HEIGHT-600)
                draw_text(str(userAnswer.getDenom()), button_font, (0,0,0), screen, WIDTH-437, HEIGHT-580)
                draw_text('=', button_font, (0,0,0), screen, WIDTH-350, HEIGHT-600)
                draw_text(str(userAnswerReduced.getNum()), button_font, (0,0,0), screen, WIDTH-263, HEIGHT-620)
                draw_text('---', button_font, (0,0,0), screen, WIDTH-262, HEIGHT-600)
                draw_text(str(userAnswerReduced.getDenom()), button_font, (0,0,0), screen, WIDTH-263, HEIGHT-580)
            else:
                draw_text(str(userAnswer.getNum()), button_font, (0,0,0), screen, WIDTH-350, HEIGHT-620)
                draw_text('---', button_font, (0,0,0), screen, WIDTH-350, HEIGHT-600)
                draw_text(str(userAnswer.getDenom()), button_font, (0,0,0), screen, WIDTH-350, HEIGHT-580)



            #nSimp, dSimp = 0, 0
            #if numerator % 3 == 0 and denominator % 3 == 0:
            #    nSimp = int(numerator/3)
            #    dSimp = int(denominator/3)
            #    while nSimp % 3 == 0 and dSimp % 3 == 0:
            #        nSimp = int(nSimp/3)
            #        dSimp = int(dSimp/3)
            #if numerator % 2 == 0 and denominator % 2 == 0:
            #    nSimp = int(numerator/2)
            #    dSimp = int(denominator/2)
            #    while nSimp % 2 == 0 and dSimp % 2 == 0:
            #        nSimp = int(nSimp/2)
            #        dSimp = int(dSimp/2)
            #if nSimp != 0:
            #    answer = "Final answer (double-shaded region): " + str(numerator) + " / " + str(denominator) + " = " + str(nSimp) + " / " + str(dSimp)
            #else:
            #    answer = "Final answer (double-shaded region): " + str(numerator) + " / " + str(denominator)
            #draw_text(answer, button_font, (0,0,0), screen, WIDTH-350, HEIGHT-550)

        for bgS in drawablesController.bgSquares:
            bgS.draw()
        for rect in drawablesController.rectangles:
            rect.draw() 
        for gl in drawablesController.guidelines:
            gl.draw()
        for cm in drawablesController.cutmarkers:
            cm.draw()
        if mouse.whoisHeld != None:
            mouse.whoisHeld.draw()
        cutter.draw()
        stateManager.draw()
        #-----------------------------DRAW END---------------------------------------
        mouse.leftMouseReleasedThisFrame = False
        #update screen and set framerate
        pygame.display.flip()
        clock.tick(fps)

    #end of main loop
    pygame.quit()

# Call main menu
main_menu()

pygame.quit()