import pygame
import colors
import math
from drawText import draw_text
from rectangle import Rectangle
from pygame.locals import *
from cutmarker import CutMarker
from drawablesController import DrawablesController
from mouseHolder import MouseHandler
from stateManager import manager
from stateManagerMult import StateManagerMult
from stateManagerTest import StateManagerTest
from stateManagerDiv import StateManagerDiv
from stateManagerSub import StateManagerSub
from stateManagerSubNewCuts import StateManagerSubNewCuts
from stateManagerAdd import StateManagerAdd
from fractionHandler import Fraction
from colorpicker import ColorPicker
from problemDisplay import ProblemDisplay
from problemGenerator import ProblemGenerator
from trashCan import TrashCan
from problemValidation import isValidProblem
from userAnswerSystem import UserAnswerSystem
from statesTab import StatesTab
from stateManagerMultNew import StateManagerMultNew
from statesTabMult import StatesTabMult

pygame.init()

# Define dimensions for window
WIDTH, HEIGHT = 1200, 700

# define window
screenDimensions = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("425 Project")

# Create fonts for interface
title_font = pygame.font.SysFont('Arial', 60)
button_font = pygame.font.SysFont('Arial', 25)
smallButton_font = pygame.font.SysFont('Arial',20)
message_font = pygame.font.SysFont('Arial', 32)
message_font_s = pygame.font.SysFont('Arial', 30)

# define bool to decide when program ends
isProgramRunning = True

# clock controls framerate of program
clock = pygame.time.Clock()
fps = 60

# Load image in for background
# background_img = pygame.image.load("assets/yellow_background.jpg")
background_img = pygame.image.load("assets/testBG1.png")

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
TEST = 4
program_OperationType = DIVISION
# problemGenerator declared globally so user can either:
# 1)restart session but keep same problem
# 2)restart session but get new problem
problemGenerator = ProblemGenerator() 

# declare program creation type as global var, set to enum of either random problem
RANDOMPROBLEM = 0
USERPROBLEM = 1
program_problemCreationType = RANDOMPROBLEM


# Function runs the main menu 
def main_menu():

    global program_CuttingType
    global program_OperationType
    global program_problemCreationType

    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    isProgramRunning = True

    #for button states
    isDivHover = isDivClicked = isMultHover = isMultClicked = isSubHover = isSubClicked = isTestHover = isTestClicked = False
    isAddHover = isAddClicked = False
    if program_OperationType == MULTIPLICATION:
        isMultClicked = True
    elif program_OperationType == DIVISION:
        isDivClicked = True
    elif program_OperationType == SUBTRACTION:
        isSubClicked = True
    elif program_OperationType == ADDITION:
        isAddClicked = True
    elif program_OperationType == TEST:
         isTestClicked = True

    isRandomHover = isRandomClicked = isUserHover = isUserClicked = False
    if program_problemCreationType == RANDOMPROBLEM:
        isRandomClicked = True
    elif program_problemCreationType == USERPROBLEM:
        isUserClicked = True

    isHoverStart = False
    isHoverQuit = False

    while isProgramRunning:

        # Main event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                isProgramRunning = False
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isProgramRunning = False
                    break
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        screen.fill((255, 245, 112))        # Fill background
        # screen.blit(background_img, (int((WIDTH-864)/2), 0))
        screen.blit(background_img,(0,0))
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position
        title_bar = pygame.Rect(0, 0, 1200, 100)

        startY = 164
        operationButtonsY = startY + 40
        operationButtonWidth = 200
        operationButtonHeight = 50
        operationButtonXBuffer = 10


        multiplicationButtonX = int(WIDTH/2 - operationButtonWidth - operationButtonXBuffer)
        multiplicationButton = pygame.Rect(multiplicationButtonX,operationButtonsY,operationButtonWidth,operationButtonHeight)
        divisionButtonX = int(WIDTH/2 + operationButtonXBuffer)
        divisionButton = pygame.Rect(divisionButtonX,operationButtonsY,operationButtonWidth,operationButtonHeight)
        subtractionButtonX = multiplicationButtonX - operationButtonWidth - operationButtonXBuffer * 2
        subtractionButton = pygame.Rect(subtractionButtonX,operationButtonsY,operationButtonWidth,operationButtonHeight)
        additionButtonX = int(WIDTH/2 + operationButtonXBuffer) + operationButtonWidth + operationButtonXBuffer * 2
        additionButton = pygame.Rect(additionButtonX,operationButtonsY,operationButtonWidth,operationButtonHeight)
        testButtonX = int(WIDTH/2 + operationButtonXBuffer) + operationButtonWidth * 2 + operationButtonXBuffer * 2
        testButton = pygame.Rect(testButtonX,operationButtonsY,operationButtonWidth,operationButtonHeight)

        problemTypeY = operationButtonsY + 100
        problemButtonsY = problemTypeY + 40
        problemButtonWidth = 200
        problemButtonHeight = 50
        problemButtonXBuffer = 10
        randomProblemButtonX = int(WIDTH/2 - problemButtonWidth - problemButtonXBuffer)
        randomProblemButton = pygame.Rect(randomProblemButtonX,problemButtonsY,problemButtonWidth,problemButtonHeight)
        userProblemButtonX = int(WIDTH/2 + problemButtonXBuffer)
        userProblemButton = pygame.Rect(userProblemButtonX,problemButtonsY,problemButtonWidth,problemButtonHeight)

        startQuitButtonY = problemButtonsY + 140
        startQuitButtonWidth = 250
        startQuitButtonHeight = 80
        startQuitButtonXBuffer = 40
        startButtonX = int(WIDTH/2 + startQuitButtonXBuffer)
        startButton = pygame.Rect(startButtonX,startQuitButtonY,startQuitButtonWidth,startQuitButtonHeight)
        quitButtonX = int(WIDTH/2 - startQuitButtonWidth - startQuitButtonXBuffer)
        quitButton = pygame.Rect(quitButtonX,startQuitButtonY,startQuitButtonWidth,startQuitButtonHeight)

        if (multiplicationButton.collidepoint((m1x,m1y))):
            isMultHover = True
            if click:
                isMultClicked = True
                isDivClicked = False
                isSubClicked = False
                isAddClicked = False
                isTestClicked = False
                program_OperationType = MULTIPLICATION
        else:
            isMultHover = False
        if (divisionButton.collidepoint((m1x,m1y))):
            isDivHover = True
            if click:
                isDivClicked = True
                isMultClicked = False
                isSubClicked = False
                isAddClicked = False
                isTestClicked = False
                program_OperationType = DIVISION
        else:
            isDivHover = False
        if (subtractionButton.collidepoint((m1x,m1y))):
            isSubHover = True
            if click:
                isSubClicked = True
                isMultClicked = False
                isDivClicked = False
                isAddClicked = False
                isTestClicked = False
                program_OperationType = SUBTRACTION
        else:
            isSubHover = False
        if (additionButton.collidepoint((m1x,m1y))):
            isAddHover = True
            if click:
                isAddClicked = True
                isMultClicked = False
                isSubClicked = False
                isDivClicked = False
                isTestClicked = False
                program_OperationType = ADDITION
        else:
            isAddHover = False

        if (randomProblemButton.collidepoint((m1x,m1y))):
            isRandomHover = True
            if click:
                isRandomClicked =True
                isUserClicked = False
                program_problemCreationType = RANDOMPROBLEM
        else:
            isRandomHover = False

        if (testButton.collidepoint((m1x,m1y))):
            isTestHover = True
            if click:
                isAddClicked = False
                isMultClicked = False
                isSubClicked = False
                isDivClicked = False
                isTestClicked = True
                program_OperationType = TEST
        else:
            isTestHover = False

        if (userProblemButton.collidepoint((m1x,m1y))):
            isUserHover = True
            if click:
                isUserClicked =True
                isRandomClicked = False
                program_problemCreationType = USERPROBLEM
        else:
            isUserHover = False

        if (startButton.collidepoint((m1x,m1y))):
            isStartHover = True
            if click:
                if program_problemCreationType == RANDOMPROBLEM:
                    problemGenerator.setProblemCreationType(RANDOMPROBLEM)
                    main_prog()
                elif program_problemCreationType == USERPROBLEM:
                    createUserProblem()
        else:
            isStartHover = False

        if (quitButton.collidepoint((m1x,m1y))):
            isQuitHover = True
            if click:
                quit_message()
        else:
            isQuitHover = False

        # Drawing the buttons and text for menu
        pygame.draw.rect(screen, colors.TITLEBAR, title_bar)
        pygame.draw.rect(screen, (0, 0, 0), title_bar, 7)
        draw_text('Main Menu', title_font, (0,0,0), screen, int(WIDTH/2), int(HEIGHT/12))

        draw_text('Operation', pygame.font.SysFont('Arial', 48), (0,0,0), screen, WIDTH/2, startY) 
        #draw operation buttons and their tet
        if (isMultClicked == False and isMultHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, multiplicationButton)
        elif (isMultClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, multiplicationButton)
        elif (isMultHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, multiplicationButton)
        draw_text("Multiplication",button_font,(0,0,0),screen, multiplicationButtonX + int(operationButtonWidth/2), operationButtonsY+int(operationButtonHeight/2))

        if (isDivClicked == False and isDivHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, divisionButton)
        elif (isDivClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, divisionButton)
        elif (isDivHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, divisionButton)
        draw_text("Division",button_font,(0,0,0),screen, divisionButtonX + int(operationButtonWidth/2), operationButtonsY+int(operationButtonHeight/2))

        if (isSubClicked == False and isSubHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, subtractionButton)
        elif (isSubClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, subtractionButton)
        elif (isSubHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, subtractionButton)
        draw_text("Subtraction",button_font,(0,0,0),screen, subtractionButtonX + int(operationButtonWidth/2), operationButtonsY+int(operationButtonHeight/2))

        if (isAddClicked == False and isAddHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, additionButton)
        elif (isAddClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, additionButton)
        elif (isAddHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, additionButton)
        draw_text("Addition",button_font,(0,0,0),screen, additionButtonX + int(operationButtonWidth/2), operationButtonsY+int(operationButtonHeight/2))

        draw_text('Problem Type', pygame.font.SysFont('Arial', 48), (0,0,0), screen, WIDTH/2, problemTypeY) 

        if(isTestClicked == False and isTestHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, testButton)
        elif (isTestClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, testButton)
        elif (isAddHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, testButton)
        draw_text("Test",button_font,(0,0,0),screen, testButtonX + int(operationButtonWidth/2), operationButtonsY+int(operationButtonHeight/2))

        if (isRandomClicked == False and isRandomHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, randomProblemButton)
        elif (isRandomClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, randomProblemButton)
        elif (isRandomHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, randomProblemButton)
        draw_text("Random",button_font,(0,0,0),screen, randomProblemButtonX + int(problemButtonWidth/2), problemButtonsY+int(problemButtonHeight/2))
        if (isUserClicked == False and isUserHover == False):
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, userProblemButton)
        elif (isUserClicked == True):
            pygame.draw.rect(screen, colors.BUTTONCLICKED, userProblemButton)
        elif (isUserHover == True):
            pygame.draw.rect(screen, colors.BUTTONHOVER, userProblemButton)
        draw_text("Create Your Own",button_font,(0,0,0),screen, userProblemButtonX + int(problemButtonWidth/2), problemButtonsY+int(problemButtonHeight/2))
        
        if isStartHover == False:
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, startButton)
        else:
            pygame.draw.rect(screen, colors.BUTTONHOVER, startButton)
        draw_text("Start",pygame.font.SysFont('Arial', 40),(0,0,0),screen, startButtonX + int(startQuitButtonWidth/2), startQuitButtonY+int(startQuitButtonHeight/2))
        if isQuitHover == False:
            pygame.draw.rect(screen, colors.BUTTONSTANDARD, quitButton)
        else:
            pygame.draw.rect(screen, colors.BUTTONHOVER, quitButton)
        draw_text("Quit",pygame.font.SysFont('Arial', 40),(0,0,0),screen, quitButtonX + int(startQuitButtonWidth/2), startQuitButtonY+int(startQuitButtonHeight/2))



        click = False
        pygame.display.update()
        clock.tick(60)
 
    pygame.quit()
# Displays "are you sure you want to quit" message and gets click response
def quit_message():
    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    isProgramRunning = True
    while isProgramRunning:
 
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position

        # Create pop up window
        pop_up = pygame.Rect(int(WIDTH/3), 120, 400, 350)

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
        draw_text('Are you sure you would like to quit?', message_font_s, (0,0,0), screen, (int)(WIDTH/2), (HEIGHT-560))
        pygame.draw.rect(screen, (8, 41, 255), yes_button)
        draw_text('Yes', button_font, (0,0,0), screen, (int)(WIDTH/2), (HEIGHT-442))
        pygame.draw.rect(screen, (8, 41, 255), no_button)
        draw_text('No', button_font, (0,0,0), screen, (int)(WIDTH/2), (HEIGHT-325))

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
    statesTab = None

    # create state manager depending on operation type selected in menu:
    if program_OperationType == MULTIPLICATION:
        statesTab = StatesTabMult(screen,WIDTH,HEIGHT,MULTIPLICATION)
        stateManager = StateManagerMultNew(program_CuttingType,screen,statesTab)
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller
        testRectangle = Rectangle(WIDTH/2,HEIGHT/2,350,350,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call

        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)

    elif program_OperationType == ADDITION:
        stateManager = StateManagerAdd(program_CuttingType,screen)
        stateManager.setMouse(mouse)    # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller

        # Create rectangles and their respective cutters
        testRectangle = Rectangle((int)(WIDTH/3),HEIGHT/3,270,270,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call
        testRectangle2 = Rectangle((int)(WIDTH/3),HEIGHT-(HEIGHT/4.5)+15,270,270,screen,drawablesController,True,mouse,stateManager, 2)
        cutter2 = testRectangle2.getCutter()
        testRectangle3 = Rectangle(WIDTH-(int)(WIDTH/5.7),HEIGHT/3,270,270,screen,drawablesController,True,mouse,stateManager, 3)
        cutter3 = testRectangle3.getCutter()
        testRectangle4 = Rectangle(WIDTH-(int)(WIDTH/5.7),HEIGHT-(HEIGHT/4.5)+15,270,270,screen,drawablesController,True,mouse,stateManager, 4)
        cutter4 = testRectangle4.getCutter()
        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)

    elif program_OperationType == SUBTRACTION:
        ##Old:
        #stateManager = StateManagerSub(program_CuttingType,screen)
        
        
        ##statesTab = StatesTabMult(screen,WIDTH,HEIGHT,SUBTRACTION)
        statesTab = None
        stateManager = StateManagerSubNewCuts(program_CuttingType,screen,statesTab)
        
        
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller

        testRectangle = Rectangle((int)((WIDTH/3)),HEIGHT/2-30,280, 280,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call
        testRectangle2 = Rectangle((int)((WIDTH/3)*2),HEIGHT/2-30,280,280,screen,drawablesController,True,mouse,stateManager, 2)
        cutter2 = testRectangle2.getCutter() # need to get cutter here for draw call

        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        trashCan = TrashCan(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)
        stateManager.setTrashCan(trashCan)

    elif program_OperationType == DIVISION:
        stateManager = StateManagerDiv(program_CuttingType,screen)
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller
        #testRectangle = Rectangle((int)((WIDTH/3)),HEIGHT/2-30,280, 280,screen,drawablesController,True,mouse,stateManager, 1)
        #cutter = testRectangle.getCutter() # need to get cutter here for draw call
        #testRectangle2 = Rectangle((int)((WIDTH/3)*2),HEIGHT/2-30,280,280,screen,drawablesController,True,mouse,stateManager, 2)
        #cutter2 = testRectangle2.getCutter() # need to get cutter here for draw call
        ##For 3 Squares, Use (int)(WIDTH/4), (int)((WIDTH/4)*2), etc.
        colorPicker = ColorPicker(screen,WIDTH,HEIGHT,mouse,stateManager,drawablesController)
        stateManager.setColorPicker(colorPicker)
        positionSet = 0

    elif program_OperationType == TEST:
        statesTab = StatesTab(screen,WIDTH,HEIGHT,program_OperationType)
        stateManager = StateManagerTest(program_CuttingType, screen, statesTab)
        stateManager.setMouse(mouse) # link state manager and mouse
        stateManager.setDrawablesController(drawablesController) # link state manager and drawables controller
        testRectangle = Rectangle(WIDTH/2,HEIGHT/2,350,350,screen,drawablesController,True,mouse,stateManager, 1)
        cutter = testRectangle.getCutter() # need to get cutter here for draw call
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

    # Creating division rectangles down here because we first need to know what the problem answer will be
    stateManager.cpuDenomAns = problemGenerator.problemDisplay.denominatorAnswer
    stateManager.cpuNumerAns = problemGenerator.problemDisplay.numeratorAnswer
    if program_OperationType == DIVISION:
        extraRect = False
        answerCeiling = math.ceil(problemGenerator.problemDisplay.numeratorAnswer/problemGenerator.problemDisplay.denominatorAnswer)
        fractionReciprocal = problemGenerator.problemDisplay.denominator2/problemGenerator.problemDisplay.numerator2
        if fractionReciprocal < answerCeiling:
            extraRect = True
        if extraRect is True:
                testRectangle = Rectangle((int)((WIDTH/4))-50,HEIGHT/2-30,280, 280,screen,drawablesController,True,mouse,stateManager, 1)
                cutter = testRectangle.getCutter() # need to get cutter here for draw call
                testRectangle2 = Rectangle((int)((WIDTH/4)*2),HEIGHT/2-30,280,280,screen,drawablesController,True,mouse,stateManager, 2)
                cutter2 = testRectangle2.getCutter() # need to get cutter here for draw call
                stateManager.hasThreeSquares = True
                #testRectangle3 = Rectangle((int)((WIDTH/4)*3)+50,HEIGHT/2-30,280,280,screen,drawablesController,True,mouse,stateManager, 3)
                #cutter3 = testRectangle3.getCutter() # need to get cutter here for draw call
        else:
                testRectangle = Rectangle((int)((WIDTH/3)),HEIGHT/2-30,280, 280,screen,drawablesController,True,mouse,stateManager, 1)
                cutter = testRectangle.getCutter() # need to get cutter here for draw call
                testRectangle2 = Rectangle((int)((WIDTH/3)*2),HEIGHT/2-30,280,280,screen,drawablesController,True,mouse,stateManager, 2)
                cutter2 = testRectangle2.getCutter() # need to get cutter here for draw call

    # bring in userAnswerSystem
    userAnswerSystem = UserAnswerSystem(screen, stateManager, WIDTH, HEIGHT,problemDisplay)

    isProgramRunning = True
    check = False
    click = False       # To check if Main Menu button is clicked
    keyDown = None # for passing information to userAnswerSystem
    # main loop
    while isProgramRunning:
        # main event loop -- user keyboard/mouse input here
        for event in pygame.event.get():
            if event.type == QUIT:
                isProgramRunning = False
                break
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
            if event.type == KEYDOWN:
                if event.key == pygame.K_1:
                    keyDown = "1"
                elif event.key == pygame.K_2:
                    keyDown = "2"
                elif event.key == pygame.K_3:
                    keyDown = "3"
                elif event.key == pygame.K_4:
                    keyDown = "4"
                elif event.key == pygame.K_5:
                    keyDown = "5"
                elif event.key == pygame.K_6:
                    keyDown = "6"
                elif event.key == pygame.K_7:
                    keyDown = "7"
                elif event.key == pygame.K_8:
                    keyDown = "8"
                elif event.key == pygame.K_9:
                    keyDown = "9"
                elif event.key == pygame.K_0:
                    keyDown = "0"
                elif event.key == pygame.K_BACKSPACE:
                    keyDown = "Backspace"


        #---------UPDATE BEGIN-------UPDATE ALL OBJECTS
        mouse.update(check)
        if program_OperationType == MULTIPLICATION:
            stateManager.update(testRectangle.myCutter)
        elif program_OperationType == DIVISION:
            if (stateManager.cpuNumerAns/stateManager.cpuDenomAns) > 2:
                stateManager.update(testRectangle.myCutter, testRectangle2.myCutter)
            else:
                stateManager.update(testRectangle.myCutter, testRectangle2.myCutter)
        elif program_OperationType == SUBTRACTION:
            stateManager.update(testRectangle.myCutter, testRectangle2.myCutter)
            if TrashCan != None:
                trashCan.update()
        elif program_OperationType == ADDITION:
            stateManager.update(testRectangle.myCutter, testRectangle2.myCutter, testRectangle3.myCutter, testRectangle4.myCutter)
        elif program_OperationType == TEST:
            stateManager.update(testRectangle.myCutter)
            statesTab.update(mouse.mx,mouse.my,mouse.leftMouseReleasedThisFrame)
            statesTab.draw()
        
        for rect in drawablesController.rectangles:
            rect.update(mouse)
        for cm in drawablesController.cutmarkers:
            cm.update(mouse.isClick)
        if colorPicker != None:
            colorPicker.update()

        if program_OperationType != TEST:
            userAnswerSystem.update(mouse.leftMouseReleasedThisFrame,keyDown)

        if program_OperationType == DIVISION:
            if stateManager.hasThreeSquares is True:
                if positionSet == 0:
                    secondLeft, secondTop = stateManager.getSecondBorderPos()
                    positionSet = 1
                borderTop, borderLeft, numBoundaries = stateManager.getBorderPos()
                borderHeight = testRectangle2.height
                borderWidth = (testRectangle2.width/problemGenerator.problemDisplay.denominator2)*problemGenerator.problemDisplay.numerator2
            else:
                numBoundaries = 0
                borderTop, borderLeft, numBoundaries = stateManager.getBorderPos()
                borderHeight = testRectangle2.height
                borderWidth = (testRectangle2.width/problemGenerator.problemDisplay.denominator2)*problemGenerator.problemDisplay.numerator2
        elif program_OperationType == ADDITION:
            border1Top, border1Left = stateManager.border1Top, stateManager.border1Left
            borderHeight, borderWidth = testRectangle3.height, testRectangle3.width
            if stateManager.twoWholes is True:
                border2Top, border2Left = stateManager.border2Top, stateManager.border2Left
        elif program_OperationType == MULTIPLICATION:
            borderTop, borderLeft = stateManager.borderTop, stateManager.borderLeft
            borderHeight, borderWidth = testRectangle.height, testRectangle.width
        elif program_OperationType == SUBTRACTION:
            borderTop, borderLeft = stateManager.borderTop, stateManager.borderLeft
            borderHeight, borderWidth = testRectangle.height, testRectangle.width
        if stateManager.statesTab != None:
            statesTab.update(mouse.mx,mouse.my,mouse.leftMouseReleasedThisFrame)

        # ---------UPDATE END----------------------------------
        # ---------DRAW BEGIN--------------------------------
        # Menu button and logic to go back to main screen and get new problem
        menu_button = pygame.Rect(WIDTH-100, 0, 100, 50)
        if menu_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                problemGenerator.needsNewProblem = True
                main_menu()
                isProgramRunning = False
                break

        restart_button = pygame.Rect(WIDTH-220, 0, 100, 50)
        if restart_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                main_prog()
                isProgramRunning = False
                break
        
        newProblem_button = pygame.Rect(WIDTH - 370, 0 , 130, 50)
        if newProblem_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                if problemGenerator.program_problemCreationType == problemGenerator.USERPROBLEM:
                    createUserProblem()
                problemGenerator.needsNewProblem = True
                main_prog()
                isProgramRunning = False
                break
        
        if program_OperationType == ADDITION:
            undoCut_button = pygame.Rect(WIDTH/3-testRectangle.width+5, HEIGHT/3, 130, 50)
            undoCut_button2 = pygame.Rect(WIDTH/3-testRectangle.width+5, HEIGHT/3*2+100, 130, 50)
            undoCut_button3 = pygame.Rect(WIDTH/3*2-75, HEIGHT/3*2+100, 130, 50)
            undoCut_button4 = pygame.Rect(WIDTH/3*2-75, HEIGHT/3, 130, 50)
            if undoCut_button.collidepoint((mouse.mx, mouse.my)):
                if click:
                    print("BUTTON WORKS")
            if undoCut_button2.collidepoint((mouse.mx, mouse.my)):
                if click:
                    print("BUTTON WORKS")
            if undoCut_button3.collidepoint((mouse.mx, mouse.my)):
                if click:
                    print("BUTTON WORKS")
            if undoCut_button4.collidepoint((mouse.mx, mouse.my)):
                if click:
                    print("BUTTON WORKS")

        elif program_OperationType == DIVISION:
            if stateManager.hasThreeSquares:
                undoCut_button = pygame.Rect(WIDTH/5 - 55, HEIGHT/2 + testRectangle.height/2 - 30 , 130, 50)
                undoCut_button2 = pygame.Rect(WIDTH/2-65, HEIGHT/2 + testRectangle.height/2 - 30 , 130, 50)
            else:
                undoCut_button = pygame.Rect(WIDTH/3 - 60, HEIGHT/2 + testRectangle.height/2 - 30 , 130, 50)
                undoCut_button2 = pygame.Rect(WIDTH/3*2 - 65, (HEIGHT/2 + testRectangle.height/2)-30, 130, 50)
            if undoCut_button.collidepoint((mouse.mx, mouse.my)):
                if click:
                        if stateManager.lastCuts == 0:
                            stateManager.undoCutsVert(1, cutter)
                        else:
                            stateManager.undoCutsHoriz(1, cutter)
            if undoCut_button2.collidepoint((mouse.mx, mouse.my)):
                if click:
                        if stateManager.lastCuts == 0:
                            stateManager.undoCutsVert(2, cutter2)
                        else:
                            stateManager.undoCutsHoriz(2, cutter2)
    
        elif program_OperationType == SUBTRACTION:
            undoCut_button = pygame.Rect(WIDTH/3 - 65, (HEIGHT/2 + testRectangle.height/2)-30 , 130, 50)
            undoCut_button2 = pygame.Rect(WIDTH/3*2 - 65, (HEIGHT/2 + testRectangle.height/2)-30, 130, 50)
            if undoCut_button.collidepoint((mouse.mx, mouse.my)):
                if click:
                    print("BUTTON WORKS")
        elif program_OperationType == MULTIPLICATION:
            undoCut_button = pygame.Rect(WIDTH/4, HEIGHT/2, 130, 50)
            if undoCut_button.collidepoint((mouse.mx, mouse.my)):
                if click:
                    if stateManager.lastCuts == 0:
                        stateManager.undoCutsVert(cutter)
                    else:
                        stateManager.undoCutsHoriz(cutter)

        
        # drawing here
        screen.fill(colors.BGCOLOR) #fill screen bg   


        # Drawing menu button
        pygame.draw.rect(screen, (8, 41, 255), menu_button)
        draw_text('Main Menu', button_font, (0,0,0), screen, WIDTH-50, 25)
        pygame.draw.rect(screen, (8, 41, 255), restart_button)
        draw_text('Restart', button_font, (0,0,0), screen, WIDTH-170, 25)
        pygame.draw.rect(screen, (8, 41, 255), newProblem_button) # for new prob button
        draw_text('New Problem', button_font, (0,0,0), screen, WIDTH-305, 25) # for new prob button

        # ALL LOGIC FOR DRAWING UNDO BUTTONS HERE
        if program_OperationType == ADDITION:
            if stateManager.currentState == stateManager.CUTTINGVERTICALLY1 or stateManager.currentState == stateManager.CUTTINGHORIZONTALLY1:
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button)
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button2)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3 - testRectangle.width/1.5-20, (HEIGHT/3)+25)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3 - testRectangle.width/1.5-20, (HEIGHT/3)*2+125)
            elif stateManager.currentState == stateManager.CUTTINGVERTICALLY2 or stateManager.currentState == stateManager.CUTTINGHORIZONTALLY2:
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button4)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3*2-10, (HEIGHT/3)+25)
            elif stateManager.currentState == stateManager.CUTTINGVERTICALLY3 or stateManager.currentState == stateManager.CUTTINGHORIZONTALLY3:
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button3)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3*2-10, (HEIGHT/3)*2+125)

        elif program_OperationType == DIVISION:
            if stateManager.currentState == stateManager.CHECKCUTS:
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button)
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button2)

                if stateManager.hasThreeSquares is True:
                    draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/4-55, (HEIGHT/2)+(testRectangle.height/2))
                    draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/4*2, (HEIGHT/2)+(testRectangle.height/2))
                else:
                    draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3, (HEIGHT/2)+(testRectangle.height/2))
                    draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3*2, (HEIGHT/2)+(testRectangle.height/2))
        elif program_OperationType == SUBTRACTION:
            
            if stateManager.currentState == stateManager.CUTTINGFIRST or stateManager.currentState == stateManager.CUTTINGSECOND:
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3, (HEIGHT/2)+(testRectangle.height/2)-5)
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button2)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/3*2, (HEIGHT/2)+(testRectangle.height/2)-5)
        else:
            if stateManager.currentState == stateManager.CHECKCUTS:
                pygame.draw.rect(screen, (8, 41, 255), undoCut_button)
                draw_text('Undo Cut', button_font, (0,0,0), screen, WIDTH/4 + 65, (HEIGHT/2)+25)


        if stateManager.getCurrentState() != "Finished":
            state_message = "Current state: " + stateManager.getCurrentState()
        else:
            state_message = ""
        draw_text(state_message, button_font, (0,0,0), screen, 160, 25)

        tempRectList = list()
        for bgS in drawablesController.bgSquares:
            bgS.draw()
        if program_OperationType == MULTIPLICATION:
            for rect in drawablesController.rectangles:
                rect.draw()
        if program_OperationType == SUBTRACTION:
            for rect in drawablesController.rectangles:
                rect.draw()
                if rect.isMarked == True:
                    rect.drawMark()
        if program_OperationType == TEST:
            for rect in drawablesController.rectangles:
                rect.draw()
        if program_OperationType != MULTIPLICATION and program_OperationType != SUBTRACTION:
            for rect in drawablesController.rectangles:
                #
                #move to rectangle class
                if rect.ownerID == 2:
                    rect.draw()
                    #if rect.isShadedV == True and rect.isShadedH != True:
                        #rect.drawVLines(rect.colorHatch)
                    #if rect.isShadedH == True and rect.isShadedV != True:
                        #rect.drawHLines(rect.colorHatch)
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
        
        cutter.draw()
        if program_OperationType == DIVISION or program_OperationType == SUBTRACTION:
            cutter2.draw()
            if stateManager.cpuNumerAns > stateManager.cpuDenomAns:
                pass
        if program_OperationType == ADDITION:
            cutter2.draw()
            cutter3.draw()
            cutter4.draw()
        stateManager.draw()
        if colorPicker != None:
            colorPicker.draw()
        #if trashCan != None:
        #    trashCan.draw()
        if program_OperationType != TEST:
            problemDisplay.draw()
            userAnswerSystem.draw()
        # DRAW BORDER HERE TO HIGHLIGHT CURRENT SECTION
        if program_OperationType == DIVISION:
            if stateManager.hasThreeSquares is True:
                if stateManager.currentState == stateManager.MOVING or stateManager.currentState == stateManager.ANSWERSUBMISSION or stateManager.currentState == stateManager.DONE:
                    pygame.draw.rect(screen, colors.YELLOW, (borderLeft, borderTop, borderWidth, borderHeight), 4)  # width = 4
                    pygame.draw.rect(screen, colors.YELLOW, (secondLeft, secondTop, borderWidth, borderHeight), 4)  # width = 4

            else:
                if stateManager.currentState == stateManager.MOVING or stateManager.currentState == stateManager.ANSWERSUBMISSION or stateManager.currentState == stateManager.DONE:
                    numBoundaries += 1
                    for i in range(numBoundaries):
                        if i < stateManager.answerCeiling:
                            pygame.draw.rect(screen, colors.YELLOW, (borderLeft-((i)*borderWidth), borderTop, borderWidth, borderHeight), 4)  # width = 4
        elif program_OperationType == ADDITION:
            if stateManager.currentState == stateManager.MOVING or stateManager.currentState == stateManager.ANSWERSUBMISSION or stateManager.currentState == stateManager.DONE or stateManager.currentState == stateManager.CUTTINGHORIZONTALLY3 or stateManager.currentState == stateManager.CUTTINGVERTICALLY3:
                pygame.draw.rect(screen, colors.YELLOW, (border1Left, border1Top, borderWidth, borderHeight), 4)
                if stateManager.twoWholes is True:
                    pygame.draw.rect(screen, colors.YELLOW, (border2Left, border2Top, borderWidth, borderHeight), 4)
        elif program_OperationType == MULTIPLICATION:
            if stateManager.currentState == stateManager.ANSWERSUBMISSION or stateManager.currentState == stateManager.DONE:
                pygame.draw.rect(screen, colors.YELLOW, (borderLeft, borderTop, borderWidth, borderHeight), 4)
        elif program_OperationType == SUBTRACTION:
            if stateManager.currentState == stateManager.ANSWERSUBMISSION or stateManager.currentState == stateManager.DONE:
                pygame.draw.rect(screen, colors.YELLOW, (borderLeft, borderTop, borderWidth, borderHeight), 4)
            
        if stateManager.statesTab != None:
            statesTab.draw()


        if mouse.whoisHeld != None:
            mouse.whoisHeld.draw()

        #-----------------------------DRAW END---------------------------------------
        mouse.leftMouseReleasedThisFrame = False
        keyDown = None
        #update screen and set framerate
        pygame.display.flip()
        clock.tick(fps)

    #end of main loop
    pygame.quit()

#fuunction to control user creating their own problem
def createUserProblem():
    click = False
    m1x = 0      # Get error if you don't set value for mx and my here
    m1y = 0      # Maybe pass as parameter for main_prog()
    isProgramRunning = True
    global program_OperationType

    # operationSymbol is for drawing purposes in main loop
    operationSymbol = ""
    if program_OperationType == MULTIPLICATION:
        operationSymbol = "x"
    elif program_OperationType == SUBTRACTION:
        operationSymbol = "-"
    elif program_OperationType == DIVISION:
        operationSymbol = chr(247)
    elif program_OperationType == ADDITION:
        operationSymbol = "+"

    problemFont = pygame.font.SysFont('Arial', 64)
    errorFont = pygame.font.SysFont('Arial',20)

    #to ensure only 1 rect can be selected at once, string var, n1 n2 d1 d2
    selectedRect = ""
    selectionClock = 0 #for blinking to highlight to user which number is selected
    selectionIndex = -1
    #init numerator and denominator values as a list 
    #n1, d1, n2, d2
    fractionValues = [1,1,1,1]

    validationResult = ""

    while isProgramRunning:
        m1x, m1y = pygame.mouse.get_pos()   # Get mouse position     
        # Main event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                isProgramRunning = False
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_1 and selectionIndex != -1:
                    fractionValues[selectionIndex] = 1
                elif event.key == pygame.K_2 and selectionIndex != -1:
                    fractionValues[selectionIndex] = 2
                elif event.key == pygame.K_3 and selectionIndex != -1:
                    fractionValues[selectionIndex] = 3
                elif event.key == pygame.K_4 and selectionIndex != -1:
                    fractionValues[selectionIndex] = 4
                elif event.key == pygame.K_5 and selectionIndex != -1:
                    fractionValues[selectionIndex] = 5
                elif event.key == pygame.K_6 and selectionIndex != -1:
                    fractionValues[selectionIndex] = 6
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #-----------LOGIC-------------

        # Create back and start button rects
        backButtonX = 50
        backButtonY = HEIGHT - 100
        back_button = pygame.Rect(backButtonX, backButtonY, 200, 50)
        startButtonX = WIDTH - 250
        startButtonY = HEIGHT - 100
        start_button = pygame.Rect(startButtonX, startButtonY, 200, 50)
        # Create error msg rect
        errorRectX = WIDTH / 2
        errorRectY = HEIGHT - 100
        errorRectWidth = 600
        errorRectHeight = 50
        errorRect = pygame.Rect(int(errorRectX - errorRectWidth/2),errorRectY,errorRectWidth,errorRectHeight)
        #operation rect
        operationRectWidth = 100
        operationRectHeight = 100
        operationRectX = int(WIDTH / 2) - int(operationRectWidth / 2)
        operationRectY = int(HEIGHT / 2) - int(operationRectHeight / 2)
        operationRect = pygame.Rect(operationRectX,operationRectY,operationRectWidth,operationRectHeight)
        #create numerator and denmon rects
        boxWidth = 100
        boxHeight = 100
        numer1RectX = operationRectX - 100
        numer1RectY = operationRectY - 52
        numer1Rect = pygame.Rect(numer1RectX,numer1RectY,boxWidth,boxHeight)

        denom1RectX = numer1RectX
        denom1RectY = operationRectY + 52
        denom1Rect = pygame.Rect(denom1RectX,denom1RectY,boxWidth,boxHeight)

        numer2RectX = operationRectX + 100
        numer2RectY = numer1RectY
        numer2Rect = pygame.Rect(numer2RectX,numer2RectY,boxWidth,boxHeight)

        denom2RectX = numer2RectX
        denom2RectY = denom1RectY
        denom2Rect = pygame.Rect(numer2RectX,denom1RectY,boxWidth,boxHeight)


        # Check if mouse is on a button when clicked
        if back_button.collidepoint((m1x, m1y)):   # go back to main menu
            if click:
                main_menu()
                break
        if start_button.collidepoint((m1x, m1y)):    # begin main loop
            if click:
                validationResult = isValidProblem(fractionValues[0],fractionValues[1],fractionValues[2],fractionValues[3],program_OperationType)
                if validationResult == True: #the problem is good so start main loop
                    problemGenerator.setProblemCreationType(USERPROBLEM)
                    problemGenerator.fractionValues = fractionValues
                    problemGenerator.getProblemUserGen()
                    main_prog()
                    isProgramRunning = False
                    break
        # for selecting n1 n2 d1 d2
        if numer1Rect.collidepoint((m1x,m1y)):
            if click:
                selectedRect = "n1"
                selectionIndex = 0
                selectionClock = 30
        if numer2Rect.collidepoint((m1x,m1y)):
            if click:
                selectedRect = "n2"
                selectionIndex = 2
                selectionClock = 30
        if denom1Rect.collidepoint((m1x,m1y)):
            if click:
                selectedRect = "d1"
                selectionIndex = 1
                selectionClock = 30
        if denom2Rect.collidepoint((m1x,m1y)):
            if click:
                selectedRect = "d2"
                selectionIndex = 3
                selectionClock = 30
        
        # check for collisions with operationRect and set operation type accordingly
        if operationRect.collidepoint((m1x,m1y)):
            if click:
                if program_OperationType == MULTIPLICATION:
                    program_OperationType = SUBTRACTION
                    operationSymbol = "-"
                elif program_OperationType == SUBTRACTION:
                    program_OperationType = DIVISION
                    operationSymbol = chr(247)
                elif program_OperationType == DIVISION:
                    operationSymbol = "+"
                    program_OperationType = ADDITION
                elif program_OperationType == ADDITION:
                    operationSymbol = "x"
                    program_OperationType = MULTIPLICATION

        #----------- BEGIN DRAW, END LOGIC-------------------#
        # draw back and start buttons and corresponding text
        background_img = pygame.image.load("assets/testBG1.png")
        screen.blit(background_img, (0, 0))

        draw_text('Create Your Problem', title_font, (0,0,0), screen, int(WIDTH/2), int(HEIGHT/12))
        pygame.draw.rect(screen, (8, 41, 255), back_button)
        draw_text('Back', button_font, (0,0,0), screen, backButtonX + 100, backButtonY + 25)
        pygame.draw.rect(screen, (8, 41, 255), start_button)
        draw_text('Start', button_font, (0,0,0), screen, startButtonX + 100, startButtonY + 25)
        #draw error rect and validation errors
        pygame.draw.rect(screen,colors.TEXTBOX,errorRect)
        draw_text(validationResult,errorFont,(255,0,0),screen,errorRectX,errorRectY + 25)
        # draw operation rect
        pygame.draw.rect(screen,colors.TEXTBOX,operationRect)
        draw_text(operationSymbol, problemFont, (0,0,0), screen, operationRectX + 50, operationRectY + 50)

        # draw numerator and denominator rects
        pygame.draw.rect(screen,colors.TEXTBOX,numer1Rect)
        pygame.draw.rect(screen,colors.TEXTBOX,denom1Rect)
        pygame.draw.rect(screen,colors.TEXTBOX,numer2Rect)
        pygame.draw.rect(screen,colors.TEXTBOX,denom2Rect)
        # draw fraction divider to left and right of operationRect
        pygame.draw.line(screen,(0,0,0), [operationRectX - 100, operationRectY + int(operationRectHeight/2)], [operationRectX,operationRectY + int(operationRectHeight/2)], 5)
        pygame.draw.line(screen,(0,0,0), [operationRectX + 100, operationRectY + int(operationRectHeight/2)], [operationRectX + 200,operationRectY + int(operationRectHeight/2)], 5)

        if selectionClock > 30:
            # draw line to show user which numer/denom they are currently selecting
            if selectedRect == "n1":
                pygame.draw.line(screen,(0,0,0),[numer1RectX + 20,numer2RectY+80],[numer1RectX+80,numer2RectY+80],4)
            elif selectedRect == "n2":
                pygame.draw.line(screen,(0,0,0),[numer2RectX + 20,numer2RectY+80],[numer2RectX+80,numer2RectY+80],4)
            elif selectedRect == "d1":
                pygame.draw.line(screen,(0,0,0),[denom1RectX + 20,denom1RectY+80],[denom1RectX+80,denom1RectY+80],4)
            elif selectedRect == "d2":
                pygame.draw.line(screen,(0,0,0),[denom2RectX + 20,denom2RectY+80],[denom2RectX+80,denom2RectY+80],4)
        if selectionClock >= 60:
            selectionClock = 0

        # draw correct number text for each numerator and denominator
        #n1
        draw_text(str(fractionValues[0]), problemFont, (0,0,0), screen, numer1RectX+50, numer1RectY+50)
        #d1
        draw_text(str(fractionValues[1]), problemFont, (0,0,0), screen, denom1RectX+50, denom1RectY+50)
        #n2
        draw_text(str(fractionValues[2]), problemFont, (0,0,0), screen, numer2RectX+50, numer2RectY+50)
        #d2
        draw_text(str(fractionValues[3]), problemFont, (0,0,0), screen, denom2RectX+50, denom2RectY+50)

        # finally update screen and tick clock, reset click
        click = False
        pygame.display.update()
        selectionClock += 1
        clock.tick(60)
    pygame.quit()

# Call main menu
main_menu()

pygame.quit()