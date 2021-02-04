from cutterFraction import CutterFraction
import colors
import pygame
from drawText import draw_text
import numpy as np

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

        self.currentState = self.CUTTINGVERTICALLY

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None

        self.screen = screen
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        # Need actual CPU answer to check if > 1
        self.cpuDenomAns = 0
        self.cpuNumerAns = 0

        # For get answer function
        self.numShadedRightRects = 0

        self.rectsData = None
        self.hasInvertedRectData = False

    
    def getOperationType(self):
        return self.operation_type
        

    def update(self, cutter, cutter2, cutter3):
        # manager is cuttingvertically, wait for cutter class to be waiting so it can proceed
        if self.currentState == self.CUTTINGVERTICALLY:
            if cutter3 is None:
                if cutter.getState() == "Waiting" and cutter2.getState() == "Waiting":
                    self.currentState = self.SHADINGVERTICALLY
            else:
                if cutter.getState() == "Waiting" and cutter2.getState() == "Waiting" and cutter3.getState() == "Waiting":
                    self.currentState = self.SHADINGVERTICALLY

        # manager is now shading vertically, now can shade current rects
        elif self.currentState == self.SHADINGVERTICALLY:
            self.shadeVertical()
            self.shadeVertical2()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.CUTTINGHORIZONTALLY
                cutter.setStateCutHorizontal()
                cutter2.setStateCutHorizontal()
                if cutter3 is not None:
                    cutter3.setStateCutHorizontal()

        # manager now cutting horizontally, let cutter do work
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            if cutter3 is None:
                if cutter.getState() == "Waiting" and cutter2.getState() == "Waiting":
                    self.currentState = self.GETTINGDENOMINATOR
            else: 
                if cutter.getState() == "Waiting" and cutter2.getState() == "Waiting" and cutter3.getState() == "Waiting":
                    self.currentState = self.GETTINGDENOMINATOR

        elif self.currentState == self.GETTINGDENOMINATOR:
            self.getDenominator()

            ##################################################
            # Add in third rectangle here if answer is > 1   #
            ##################################################
            self.currentState = self.MOVING

        elif self.currentState == self.MOVING:
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.DONE


    def draw(self):
        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MOVING:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Finish!', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))

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


    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c
