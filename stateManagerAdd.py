from fractionHandler import Fraction
from cutterFraction import CutterFraction
from rectangle import Rectangle
import colors
import pygame
from drawText import draw_text
import numpy as np

# Define dimensions for window
WIDTH, HEIGHT = 1200, 700

class StateManagerAdd:
    def __init__(self,cuttingType,screen):

        self.MULT = 1
        self.DIV = 2
        self.SUB = 3
        self.ADD = 4
        self.TEST = 5
        self.operation_type = self.ADD
        #define cutting types
        self.FRACTIONCUTTING = 0
        self.VARCUTTING = 1
        self.CMCUTTING = 2
        self.cuttingType = cuttingType

        #define states
        self.CUTTINGVERTICALLY1 = 0     # Cutting left two boxes vertically
        self.SHADINGVERTICALLY = 1     # Shading left two boxes vertically
        self.CUTTINGHORIZONTALLY1 = 2   # Cutting left two boxes horizontally
        self.CUTTINGVERTICALLY2 = 4     # Cutting right box vertically
        self.CUTTINGHORIZONTALLY2 = 5   # Cutting right box horizontally
        


        # Other states
        self.MOVING = 6
        self.GETTINGDENOMINATOR = 3
        self.CUTTINGVERTICALLY3 = 7     # Cutting 2nd right box vertically
        self.CUTTINGHORIZONTALLY3 = 8   # Cutting 2nd right box horizontally
        self.MOVING2 = 9
        self.ANSWERSUBMISSION = 10
        self.DONE = 11

        self.currentState = self.CUTTINGVERTICALLY1

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None

        self.screen = screen
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/1.72)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        self.submitAnswerButtonX = int(self.WIDTH/2 - 100) + 100
        self.submitAnswerButtonY = int(self.HEIGHT - 220)
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

        self.movedBefore = False

        # For border to highlight current sections
        self.border1Top = 0
        self.border1Left = 0
        self.border2Top = 0
        self.border2Left = 0

        # For checking if gold border is needed for rect 4
        self.twoWholes = False

        self.userAnswerSystemReadyForSubmission = False

        self.statesTab = None

    def getOperationType(self):
        return self.operation_type
        
    def update(self, cutter1, cutter2, cutter3, cutter4):
        # We only want to cut the left two rectangles here
        if self.currentState == self.CUTTINGVERTICALLY1:
            cutter3.setStateWaiting()
            cutter4.setStateWaiting()
            if cutter1.getState() == "Waiting" and cutter2.getState() == "Waiting":
                    self.currentState = self.SHADINGVERTICALLY
        # manager is now shading vertically, now can shade current rects
        elif self.currentState == self.SHADINGVERTICALLY:
            self.shadeVertical()
            self.shadeVertical2()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                #if there is nothing shaded, display a quick window telling the user to shade vertically, 
                #if there are shaded rectangles, continue as normal
                #Display that halts the state continuation will appear for 4 Seconds
                sCountR1 = 0
                sCountR2 = 0
                for rect in self.drawablesController.rectangles:
                    if rect.isShadedV == True:
                        if rect.ownerID == 1:
                            sCountR1 += 1
                        elif rect.ownerID == 2:
                            sCountR2 += 1
                    
                if sCountR1 != 0 and sCountR2 != 0:
                    ##self.error_detect = False
                    self.currentState = self.CUTTINGHORIZONTALLY1
                    cutter1.setStateCutHorizontal()
                    cutter2.setStateCutHorizontal()
                ##self.error_detect = True
                # manager now cutting horizontally, let cutter do work        
        elif self.currentState == self.CUTTINGHORIZONTALLY1:
            if cutter1.getState() == "Waiting" and cutter2.getState() == "Waiting":
                    cutter3.setStateCutVertical()
                    ####cutter4.setStateCutVertical()
                    self.currentState = self.CUTTINGVERTICALLY2
        elif self.currentState == self.CUTTINGVERTICALLY2 and self.movedBefore == True:
            if cutter4.getState() == "Waiting":
                    cutter4.setStateCutHorizontal()
                    self.currentState = self.CUTTINGHORIZONTALLY2
                    ####cutter4.setStateCutHorizontal()
        elif self.currentState == self.CUTTINGHORIZONTALLY2 and self.movedBefore == True:
            if cutter4.getState() == "Waiting": ####and cutter4.getState() == "Waiting":
                self.currentState = self.GETTINGDENOMINATOR        
        elif self.currentState == self.CUTTINGVERTICALLY2 and self.movedBefore == False:
            if cutter3.getState() == "Waiting":
                    cutter3.setStateCutHorizontal()
                    self.currentState = self.CUTTINGHORIZONTALLY2
                    ####cutter4.setStateCutHorizontal()
        elif self.currentState == self.CUTTINGHORIZONTALLY2 and self.movedBefore == False:
            if cutter3.getState() == "Waiting": ####and cutter4.getState() == "Waiting":
                self.currentState = self.GETTINGDENOMINATOR
        elif self.currentState == self.GETTINGDENOMINATOR:
            self.getDenominator()
            self.setBorder1Pos()
            self.setBorder2Pos()
            self.currentState = self.MOVING
        elif self.currentState == self.MOVING and self.movedBefore == False:
            ##IDEA: Create a method to check when both input rectangles have finished drag and drop, 
            ##IDEA cont: THEN display the Answer submission button
            
            if self.is_filled(3) == True and self.shadedRectsRemaining() is True:
                cutter4.setStateCutVertical()
                self.twoWholes = True
                self.currentState = self.CUTTINGVERTICALLY3
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.ANSWERSUBMISSION
        elif self.currentState == self.CUTTINGVERTICALLY3:
            self.movedBefore = True
            if cutter4.getState() == "Waiting":
                cutter4.setStateCutHorizontal()
                self.currentState = self.CUTTINGHORIZONTALLY3
        elif self.currentState == self.CUTTINGHORIZONTALLY3:
            if cutter4.getState() == "Waiting":
                self.currentState = self.MOVING
        elif self.currentState == self.MOVING and self.movedBefore == True:
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.ANSWERSUBMISSION
        elif self.currentState == self.ANSWERSUBMISSION and self.userAnswerSystemReadyForSubmission == True:
            if self.submitAnswerButton.collidepoint(self.mouse.mx,self.mouse.my) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.DONE
                



    def draw(self):
        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/1.72, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MOVING or self.currentState == self.MOVING2:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to answer submission', self.button_font, (0,0,0), self.screen, self.WIDTH/1.72, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.ANSWERSUBMISSION:
            pygame.draw.rect(self.screen, (8, 41, 255), self.submitAnswerButton)
            draw_text('Submit Answer', self.button_font, (0,0,0), self.screen, self.submitAnswerButtonX + 100, self.submitAnswerButtonY + 25)


    def getCurrentState(self):
        if self.currentState == self.CUTTINGVERTICALLY1:
            return "Cutting Vertically 1"
        elif self.currentState == self.SHADINGVERTICALLY:
            return "Shading Vertically"
        elif self.currentState == self.CUTTINGHORIZONTALLY1:
            return "Cutting Horizontally 1"
        elif self.currentState == self.CUTTINGVERTICALLY2:
            return "Cutting Vertically 2"
        elif self.currentState == self.CUTTINGHORIZONTALLY2:
            return "Cutting Horizontally 2"
        elif self.currentState == self.GETTINGDENOMINATOR:
            return "Calculating/Loading"
        elif self.currentState == self.DONE:
            return "Finished"
        elif self.currentState == self.MOVING:
            return "Moving"
        elif self.currentState == self.CUTTINGVERTICALLY3:
            return "Cutting Vertically 3"
        elif self.currentState == self.CUTTINGHORIZONTALLY3:
            return "Cutting Horizontally 3"
        elif self.currentState == self.MOVING and self.movedBefore == True:
            return "Moving2"
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


    def getDenominator(self):
        count = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 1:
                if rect.color != colors.WHITE:
                    count += 1
        self.numShadedRightRects = count

    def get_answerDenom(self):
        numRectsShadedThird = 0
        numRectsShadedFourth = 0
        totalRectsThird = 0
        totalRectsFourth = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 3:
                totalRectsThird += 1
                if rect.color != colors.WHITE:
                    numRectsShadedThird += 1
            if rect.ownerID == 4:
                totalRectsFourth += 1
                if rect.color != colors.WHITE:
                    numRectsShadedFourth += 1
        
        f1 = Fraction(numRectsShadedThird,totalRectsThird)
        f2 = Fraction(numRectsShadedFourth,totalRectsFourth)
        sumN, sumD = f1.fAdd(f2.numerator,f2.denominator)
        return sumD

    def get_answerNumer(self):
        numRectsShadedThird = 0
        numRectsShadedFourth = 0
        totalRectsThird = 0
        totalRectsFourth = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 3:
                totalRectsThird += 1
                if rect.color != colors.WHITE:
                    numRectsShadedThird += 1
            if rect.ownerID == 4:
                totalRectsFourth += 1
                if rect.color != colors.WHITE:
                    numRectsShadedFourth += 1
        
        f1 = Fraction(numRectsShadedThird,totalRectsThird)
        f2 = Fraction(numRectsShadedFourth,totalRectsFourth)
        sumN, sumD = f1.fAdd(f2.numerator,f2.denominator)
        return sumN

    def is_filled(self, Rectid):
        numRectsTotal = 0
        numRectsFilled = 0
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == Rectid:
                numRectsTotal += 1
                if rect.color != colors.WHITE:
                    numRectsFilled += 1
        if numRectsFilled == numRectsTotal and numRectsTotal != 0:
            return True
        return False
        
    def setBorder1Pos(self):
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 3:
                self.border1Left = rect.xPosition - (rect.width/2)
                self.border1Top = rect.yPosition - (rect.height/2)
                return
    
    def setBorder2Pos(self):
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 4:
                self.border2Left = rect.xPosition - (rect.width/2)
                self.border2Top = rect.yPosition - (rect.height/2)
                return

    def shadedRectsRemaining(self):
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 1 or rect.ownerID == 2:
                if rect.isShaded:
                    return True
        return False

    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c

