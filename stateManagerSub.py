from cutterFraction import CutterFraction
import colors
import pygame
from drawText import draw_text
import numpy as np

class StateManagerSub:
    def __init__(self,cuttingType,screen):

        self.MULT = 1
        self.DIV = 2
        self.SUB = 3
        self.operation_type = self.SUB

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

        self.DONE = 4
        self.MOVING = 5 # for debuging
        ##self.THROWINGAWAY = 6

        self.currentState = self.CUTTINGVERTICALLY

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None
        self.trashCan = None

        self.screen = screen
        self.WIDTH = 700
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        self.rectsData = None
        self.hasInvertedRectData = False

    def getOperationType(self):
        return self.operation_type

    def update(self, cutter):
        # manager is cuttingvertically, wait for cutter class to be waiting so it can proceed
        if self.currentState == self.CUTTINGVERTICALLY:
            if cutter.getState() == "Waiting":
                self.currentState = self.SHADINGVERTICALLY

        # manager is now shading vertically, now can shade current rects
        elif self.currentState == self.SHADINGVERTICALLY:
            self.shadeVertical()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.CUTTINGHORIZONTALLY 
                cutter.setStateCutHorizontal()

        # manager now cutting horizontally, let cutter do work
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            if cutter.getState() == "Waiting":
                self.currentState = self.SHADINGHORIZONTALLY

        # manager now shading horizontally
        elif self.currentState == self.SHADINGHORIZONTALLY:
            if self.hasInvertedRectData == False:
                self.invertRectData()   #use tab for this
                self.hasInvertedRectData = True #use tab for this
            self.shadeHorizontal()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.MOVING

        elif self.currentState == self.MOVING:
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.DONE
                ##self.currentState = self.THROWINGAWAY
        ##elif self.currentState == self.THROWINGAWAY:
        ##        if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
        ##            self.currentState = self.DONE
        


    def draw(self):
        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.SHADINGHORIZONTALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to moving', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MOVING:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Finish', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        ##elif self.currentState == self.THROWINGAWAY:
        ##    pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
        ##    draw_text('Finish', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))


    def getCurrentState(self):
        if self.currentState == self.CUTTINGVERTICALLY:
            return "Cutting Vertically"
        elif self.currentState == self.SHADINGVERTICALLY:
            return "Shading Vertically"
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            return "Cutting Horizontally"
        elif self.currentState == self.SHADINGHORIZONTALLY:
            return "Shading Horizontally"
        elif self.currentState == self.DONE:
            return "Finished"
        elif self.currentState == self.MOVING:
            return "Moving"
        ##elif self.currentState == self.THROWINGAWAY:
        ##    return "Throwing Away"

    def shadeVertical(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True:
                    if rect.isShaded == False:
                        #rect.drawLines(self.colorPicker.myColor, 0)
                        #0 = Vertical, set an internal rect variable to 1
                        #   #rect.changeColor(self.colorPicker.myColor)
                        rect.changeColorHatch(self.colorPicker.myColor)
                        rect.isShadedV = True
                        rect.isShaded = True
                    elif rect.isShaded == True:
                        rect.changeColorHatch(colors.WHITE)
                        rect.isShadedV = False
                        rect.isShaded = False
    # needed for horiozntal shading. gets transpose of rectsData
    def invertRectData(self):
        self.rectsData = np.array(self.rectsData).T.tolist()

    # loop through all drawablesController rectangles. If its colliding with mouse and mouse released then
    # loop through each rectangle in eac row of rects data. If any rectangle in that row is selected, changle all colors
    # of rects in that row
    def shadeHorizontal(self):
        for rect in self.drawablesController.rectangles:
            if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True and self.mouse.leftMouseReleasedThisFrame:
                for row in self.rectsData:
                    for r in row:
                        if r == rect:
                            for r1 in row:
                                self.colorPicker.enabled = False
                                if r1.isShadedB == True or r1.isShadedH == True: # its already been shaded by user, let them go back
                                    if r1.isShadedB == True:
                                        r1.isShadedB = False
                                        r1.changeColorHatch(self.colorPicker.verticalColor)
                                    elif r1.isShadedH == True:
                                        r1.isShadedH = False
                                        r1.changeColorHatch(colors.WHITE)

                                elif r1.colorHatch == self.colorPicker.verticalColor:
                                    #r1.isShadedH = True
                                    r1.isShadedV = False
                                    r1.isShadedB = True
                                    r1.changeColorHatch(self.colorPicker.getBlendedColor())
                                    #rect.drawVLines(self.colorPicker.myColor)
                                    #1 = Horizontal, set an internal rect variable to 2
                                    #if two then (?)
                                    ##r1.changeColor(self.colorPicker.getBlendedColor())
                                elif r1.colorHatch == colors.WHITE:
                                    r1.isShadedH = True
                                    r1.changeColorHatch(self.colorPicker.myColor)
                                    ##r1.changeColor(self.colorPicker.myColor)

    def get_answer(self):
        numerator = 0
        denominator = 0
        for rect in self.drawablesController.rectangles:
            denominator += 1
            if rect.isTrash == False and rect.isShadedV == True:
            ##if rect.isShadedB == True:
                numerator += 1
            #   #if rect.color == self.colorPicker.getBlendedColor():
                #   #numerator += 1
        return (numerator, denominator)




    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c
    def setTrashCan(self, v):
        self.trashCan = v
