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
from stateManagerDiv import StateManagerDiv
from stateManagerSub import StateManagerSub
from fractionHandler import Fraction
from colorpicker import ColorPicker
from problemDisplay import ProblemDisplay
from problemGenerator import ProblemGenerator
from trashCan import TrashCan

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
background_img = pygame.image.load("assets/yellow_background.jpg")

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
# problemGenerator declared globally so user can either:
# 1)restart session but keep same problem
# 2)restart session but get new problem
problemGenerator = ProblemGenerator() 

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
        """
        if cuttingType_button.collidepoint((m1x,m1y)):
            if click:
                if program_CuttingType == FRACTIONCUTTING:
                    program_CuttingType = VARCUTTING
                elif program_CuttingType == VARCUTTING:
                    program_CuttingType = CMCUTTING
                elif program_CuttingType == CMCUTTING:
                    program_CuttingType = FRACTIONCUTTING
        """
        if operationType_button.collidepoint((m1x,m1y)):
            if click:
                if program_OperationType == MULTIPLICATION:
                    program_OperationType = SUBTRACTION
                #elif program_OperationType == ADDITION:
                    #program_OperationType = SUBTRACTION
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
        """
        if program_CuttingType == CMCUTTING:
            draw_text('Cut with cutmarkers', button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))
        elif program_CuttingType == VARCUTTING:
            draw_text('Variable cutting',button_font, (0,0,0), screen, WIDTH/2, int((HEIGHT/3)+85))
        """
        if program_CuttingType == FRACTIONCUTTING:
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

    # init objects every state will have
    mouse = MouseHandler()
    drawablesController = DrawablesController()
    colorPicker = None
    trashCan = None

    # create state manager depending on operation type selected in menu:
    if program_OperationType == MULTIPLICATION:
        stateManager = StateManagerMult(program_CuttingType,screen)
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller
        testRectangle = Rectangle(WIDTH/2,HEIGHT/2,350,350,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call

        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)

    elif program_OperationType == ADDITION:
        #stateManager = StateManagerAdd(program_CuttingType,screen)
        pass

    elif program_OperationType == SUBTRACTION:
        stateManager = StateManagerSub(program_CuttingType,screen)
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller

        testRectangle = Rectangle(WIDTH/2,HEIGHT/2,350,350,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call

        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        trashCan = TrashCan(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)
        stateManager.setTrashCan(trashCan)

    elif program_OperationType == DIVISION:
        stateManager = StateManagerDiv(program_CuttingType,screen)
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller

        testRectangle = Rectangle(WIDTH-500,HEIGHT/2-30,280, 280,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call
        testRectangle2 = Rectangle(WIDTH-150,HEIGHT/2-30,280,280,screen,drawablesController,True,mouse,stateManager, 2)
        cutter2 = testRectangle2.getCutter() # need to get cutter here for draw call

        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)

    # init problemDisplay here, every operation will have
    problemDisplay = ProblemDisplay(screen,WIDTH,HEIGHT,stateManager,program_OperationType)
    # set up problemGenerator here because it needs to know problemDisplay
    problemGenerator.setProblemDisplay(problemDisplay)
    problemGenerator.setOperationType(program_OperationType)
    if problemGenerator.needsNewProblem == True:
        problemGenerator.getProblem()
        problemGenerator.needsNewProblem = False
    else:
        problemGenerator.resetCurrentProblem()

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
        if program_OperationType == MULTIPLICATION:
            stateManager.update(testRectangle.myCutter)
        elif program_OperationType == DIVISION:
            stateManager.update(testRectangle.myCutter, testRectangle2.myCutter)
        elif program_OperationType == SUBTRACTION:
            stateManager.update(testRectangle.myCutter)
            if TrashCan != None:
                trashCan.update()
        else:
            stateManager.update(testRectangle.myCutter)
        
        for rect in drawablesController.rectangles:
            rect.update(mouse)
        for cm in drawablesController.cutmarkers:
            cm.update(mouse.isClick)
        if colorPicker != None:
            colorPicker.update()
        
        
        # ---------UPDATE END----------------------------------
        # ---------DRAW BEGIN--------------------------------
        # Menu button and logic to go back to main screen and get new problem
        menu_button = pygame.Rect(WIDTH-100, 0, 100, 50)
        if menu_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                problemGenerator.needsNewProblem = True
                main_menu()

        restart_button = pygame.Rect(WIDTH-220, 0, 100, 50)
        if restart_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                main_prog()
        
        newProblem_button = pygame.Rect(WIDTH - 370, 0 , 130, 50)
        if newProblem_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                problemGenerator.needsNewProblem = True
                main_prog()
        
        # drawing here
        screen.fill(colors.BGCOLOR) #fill screen bg   

        # Drawing menu button
        pygame.draw.rect(screen, (8, 41, 255), menu_button)
        draw_text('Main Menu', button_font, (0,0,0), screen, WIDTH-50, 25)
        pygame.draw.rect(screen, (8, 41, 255), restart_button)
        draw_text('Restart', button_font, (0,0,0), screen, WIDTH-170, 25)
        pygame.draw.rect(screen, (8, 41, 255), newProblem_button) # for new prob button
        draw_text('New Problem', button_font, (0,0,0), screen, WIDTH-305, 25) # for new prob button
        state_message = "Current state: " + stateManager.getCurrentState()
        draw_text(state_message, button_font, (0,0,0), screen, 160, 25)


        tempRectList = list()
        for bgS in drawablesController.bgSquares:
            bgS.draw()
        for rect in drawablesController.rectangles:
            #
            #move to rectangle class
            if rect.ownerID == 2:
                rect.draw()
                if rect.isShadedV == True and rect.isShadedH != True:
                    rect.drawVLines(rect.colorHatch)
                if rect.isShadedH == True and rect.isShadedV != True:
                    rect.drawHLines(rect.colorHatch)
                if rect.isShadedB:
                    rect.drawBLines(rect.colorHatch)
            else:
                tempRectList.append(rect)
        for trect in tempRectList:
            trect.draw()
            if trect.isShadedV == True and trect.isShadedH != True:
                trect.drawVLines(trect.colorHatch)
            if trect.isShadedH == True and trect.isShadedV != True:
                trect.drawHLines(trect.colorHatch)
            if trect.isShadedB:
                trect.drawBLines(trect.colorHatch)
        for gl in drawablesController.guidelines:
            gl.draw()
        for cm in drawablesController.cutmarkers:
            cm.draw()
        if mouse.whoisHeld != None:
            mouse.whoisHeld.draw()
        cutter.draw()
        if program_OperationType == DIVISION:
            cutter2.draw()
        stateManager.draw()
        if colorPicker != None:
            colorPicker.draw()
        if trashCan != None:
            trashCan.draw()
        problemDisplay.draw()
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