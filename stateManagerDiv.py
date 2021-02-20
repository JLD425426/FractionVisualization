from cutterFraction import CutterFraction
from rectangle import Rectangle
import colors
import pygame
from drawText import draw_text
import numpy as np

# Define dimensions for window
WIDTH, HEIGHT = 1200, 700

class StateManagerDiv:
    def __init__(self,cuttingType,screen):

        self.MULT = 1
        self.DIV = 2
        self.SUB = 3
        self.operation_type = self.DIV
        #define cutting types
        self.FRACTIONCUTTING = 0
        self.VARCUTTING = 1
        self.CMCUTTING = 2
        self.cuttingType = cuttingType

        #define states
        self.CUTTINGVERTICALLY = 0
        self.SHADINGVERTICALLY = 1
        self.CUTTINGHORIZONTALLY = 2
        self.SHADINGHORIZONTALLY = 3

        # Other states
        self.DONE = 4
        self.MOVING = 5
        self.GETTINGDENOMINATOR = 6
        self.ANSWERSUBMISSION = 7

        self.currentState = self.CUTTINGVERTICALLY

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None

        self.screen = screen
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        self.submitAnswerButtonX = int(self.WIDTH/2 - 100)
        self.submitAnswerButtonY = int(self.HEIGHT - 60)
        self.submitAnswerButton = pygame.Rect(self.submitAnswerButtonX, self.submitAnswerButtonY, 200, 50)

        # Need actual CPU answer to check if > 1
        self.cpuDenomAns = 0
        self.cpuNumerAns = 0

        # For third rectangle to check if done auto cutting
        self.rectCreated = 0
        self.autoCutDone = 0

        # For get answer function
        self.numShadedRightRects = 0

        self.rectsData = None
        self.hasInvertedRectData = False

        # for if answer is between 1 and 2
        self.between = False
        # Checks if double shading has been done in the same rect
        self.doubleShaded = False
        # for setting third rect or not 
        self.hasThreeSquares = False
        # for making sure third square gets generated once
        self.hasCreatedThirdSquare = False


    
    def getOperationType(self):
        return self.operation_type
        

    def update(self, cutter, cutter2):
        # manager is cuttingvertically, wait for cutter class to be waiting so it can proceed
        if self.currentState == self.CUTTINGVERTICALLY:
                if cutter.getState() == "Waiting" and cutter2.getState() == "Waiting":
                    self.currentState = self.SHADINGVERTICALLY

        # manager is now shading vertically, now can shade current rects
        elif self.currentState == self.SHADINGVERTICALLY:
            self.shadeVertical()
            self.shadeVertical2()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                #if there is nothing shaded, display a quick window telling the user to shade vertically, 
                #if there are shaded rectangles, continue as normal
                #Display that halts the state continuation will appear for 4 Seconds
                sCount = 0
                for rect in self.drawablesController.rectangles:
                    if rect.isShadedV == True:
                        sCount += 1
                if sCount != 0:
                    ##self.error_detect = False
                    self.currentState = self.CUTTINGHORIZONTALLY
                    cutter.setStateCutHorizontal()
                    cutter2.setStateCutHorizontal()
                ##self.error_detect = True
                

        # manager now cutting horizontally, let cutter do work
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            if cutter.getState() == "Waiting" and cutter2.getState() == "Waiting":
                    self.currentState = self.GETTINGDENOMINATOR

        elif self.currentState == self.GETTINGDENOMINATOR:
            self.getDenominator()
            self.currentState = self.MOVING

        elif self.currentState == self.MOVING:
            if self.hasThreeSquares == True:
                if self.hasCreatedThirdSquare == False:
                    testRectangle3 = Rectangle((int)((WIDTH/4)*3)+50,HEIGHT/2-30,280,280,self.screen,self.drawablesController,True,self.mouse,self, 3)
                    cutter3 = testRectangle3.getCutter()
                    vCuts = cutter2.verticalGuidelinesCount
                    hCuts = cutter2.horizontalGuidelinesCount
                    cutter3.autoCut(hCuts, vCuts)
                    cutter3.state = cutter3.FINALCUT
                    for rect in self.drawablesController.rectangles:
                        if rect.ownerID == 3:
                            rect.changeColor(colors.WHITE)
                    self.rectCreated = 1
                    self.hasCreatedThirdSquare = True
                    self.auto_color_rect()
                    if self.cpuNumerAns/self.cpuDenomAns >= 2:
                        self.thirdShade()
            
            if self.between is True:
                if self.currentFilled() is True:
                    if self.doubleShaded is False:
                        self.secondShade()
                        self.doubleShaded = True


            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                sCount = 0
                for rect in self.drawablesController.rectangles:
                    if rect.isShadedB == True:
                        sCount += 1
                if sCount != 0:
                    ##self.error_detect = False
                    self.currentState = self.ANSWERSUBMISSION
                ##self.error_detect = True
                

        elif self.currentState == self.ANSWERSUBMISSION:
            if self.submitAnswerButton.collidepoint(self.mouse.mx,self.mouse.my) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.DONE


    def draw(self):
        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MOVING:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to answer submission', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.ANSWERSUBMISSION:
            pygame.draw.rect(self.screen, (8, 41, 255), self.submitAnswerButton)
            draw_text('Submit Answer', self.button_font, (0,0,0), self.screen, self.submitAnswerButtonX + 100, self.submitAnswerButtonY + 25)


    def getCurrentState(self):
        if self.currentState == self.CUTTINGVERTICALLY:
            return "Cutting Vertically"
        elif self.currentState == self.SHADINGVERTICALLY:
            return "Shading Vertically"
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            return "Cutting Horizontally"
        elif self.currentState == self.SHADINGHORIZONTALLY:
            return "Shading Horizontally"
        elif self.currentState == self.GETTINGDENOMINATOR:
            return "Calculating/Loading"
        elif self.currentState == self.DONE:
            return "Finished"
        elif self.currentState == self.MOVING:
            return "Moving"
        elif self.currentState == self.ANSWERSUBMISSION:
            return "Submitting Answer"

    def shadeVertical(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.ownerID == 1:
                    if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True:
                        if rect.isShaded == False:
                            #rect.drawLines(self.colorPicker.myColor, 0)
                            #0 = Vertical, set an internal rect variable to 1
                            #   #rect.changeColor(self.colorPicker.myColor)
                            rect.changeColor(self.colorPicker.myColor)
                            rect.isShadedV = True
                            rect.isShaded = True
                            #change all colors of shaded rects in corresponding square to new color
                            for _r in self.drawablesController.rectangles:
                                if _r.ownerID == 1 and _r.isShadedV == True:
                                    _r.changeColor(self.colorPicker.myColor)
                        elif rect.isShaded == True:
                            #   #rect.changeColor(colors.WHITE)
                            rect.changeColor(colors.WHITE)
                            rect.isShaded = False
                            rect.isShadedV = False

    def shadeVertical2(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.ownerID == 2:
                    if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True:
                        if rect.isShaded == False:
                            #rect.drawLines(self.colorPicker.myColor, 0)
                            #0 = Vertical, set an internal rect variable to 1
                            #   #rect.changeColor(self.colorPicker.myColor)
                            rect.changeColor(self.colorPicker.myColor)
                            rect.isShadedV = True
                            rect.isShaded = True
                            #change all colors of shaded rects in corresponding square to new color
                            for _r in self.drawablesController.rectangles:
                                if _r.ownerID == 2 and _r.isShadedV == True:
                                    _r.changeColor(self.colorPicker.myColor)
                        elif rect.isShaded == True:
                            #   #rect.changeColor(colors.WHITE)
                            rect.changeColor(colors.WHITE)
                            rect.isShaded = False
                            rect.isShadedV = False

    # needed for horizontal shading. gets transpose of rectsData
    def invertRectData(self):
        self.rectsData = np.array(self.rectsData).T.tolist()

    def getDenominator(self):
        count = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 2:
                if rect.color != colors.WHITE:
                    count += 1
        self.numShadedRightRects = count

    def get_answer(self):
        numerator = 0
        denominator = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 2 and rect.colorHatch != colors.WHITE:
                denominator += 1
                if rect.isShadedB == True:
                    numerator += 1
            #   #if rect.color == self.colorPicker.getBlendedColor():
                #   #numerator += 1
        return (numerator, self.numShadedRightRects)

    def get_answerDenom(self):
        return self.numShadedRightRects

    def get_answerNumer(self):
        numerator = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 2 and rect.colorHatch != colors.WHITE:
                if rect.isShadedB == True:
                    numerator += 1
        return numerator

    def auto_color_rect(self):
        twos, threes = [], []
        newColor = colors.WHITE
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 2:
                twos.append(rect)
            elif rect.ownerID == 3:
                threes.append(rect)
        for i in range(len(threes)):
            newColor = twos[i].color
            if twos[i].color != colors.WHITE and twos[i].color != colors.GREY:
                newColor = self.lighten(newColor)
            threes[i].color = newColor
            if threes[i].color != colors.WHITE:
                threes[i].isShaded = True

    def secondShade(self):
        twos = []
        newColor = colors.WHITE
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 2:
                twos.append(rect)
        total = len(twos)
        count = 0
        while count < total/2:
            if twos[count].isShaded:
                newColor = twos[count].color
                newColor = self.lighten(newColor)
                twos[total-count-1].color = newColor
                twos[total-count-1].isShaded = True
            count += 1
    
    def thirdShade(self):
        threes = []
        newColor = colors.WHITE
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 3:
                threes.append(rect)
        total = len(threes)
        count = 0
        while count < total/2:
            if threes[count].isShaded:
                newColor = threes[count].color
                newColor = self.lighten(newColor)
                threes[total-count-1].color = newColor
                threes[total-count-1].isShaded = True
            count += 1

    def lighten(self, color):
        if color == colors.RED:
            return colors.LIGHTRED
        if color == colors.BLUE:
            return colors.LIGHTBLUE
        if color == colors.YELLOW:
            return colors.LIGHTYELLOW
        if color == colors.ORANGE:
            return colors.LIGHTORANGE
        if color == colors.GREEN:
            return colors.LIGHTGREEN
        if color == colors.PURPLE:
            return colors.LIGHTPURPLE
        if color == colors.WHITE:
            return colors.WHITE
        else:
            return color

    def currentFilled(self):
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 2:
                if rect.isShaded:
                    if rect.isShadedB is False:
                        return False
        return True

    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c
