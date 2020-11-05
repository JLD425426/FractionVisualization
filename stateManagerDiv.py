from cutterFraction import CutterFraction
import colors
import pygame
from drawText import draw_text
import numpy as np

class StateManagerDiv:
    def __init__(self,cuttingType,screen):

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

        # States for a second rectangle?
        self.CUTTINGVERTICALLY2 = 6
        self.SHADINGVERTICALLY2 = 7
        self.CUTTINGHORIZONTALLY2 = 8
        self.SHADINGHORIZONTALLY2 = 9

        # Other states
        self.DONE = 4
        self.MOVING = 5 # for debuging

        self.currentState = self.CUTTINGVERTICALLY

        self.drawablesController = None
        self.mouse = None

        self.screen = screen
        self.WIDTH = 700
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        self.rectsData = None
        self.hasInvertedRectData = False
        self.colorPicker = None


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
                self.invertRectData()
                self.hasInvertedRectData = True
            self.shadeHorizontal()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.DONE

    def draw(self):
        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.SHADINGHORIZONTALLY:
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
        elif self.currentState == self.DONE:
            return "Finished"
        elif self.currentState == self.MOVING:
            return "Moving"

    def shadeVertical(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True:
                    if rect.isShaded == False:
                        rect.changeColor(colors.RED)
                        rect.isShaded = True
                    elif rect.isShaded == True:
                        rect.changeColor(colors.WHITE)
                        rect.isShaded = False
    def invertRectData(self):
        self.rectsData = np.array(self.rectsData).T.tolist()

    def shadeHorizontal(self):
        for rect in self.drawablesController.rectangles:
            if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True and self.mouse.leftMouseReleasedThisFrame:
                for row in self.rectsData:
                    for r in row:
                        if r == rect:
                            for r1 in row:
                                if r1.color == colors.RED:
                                    r1.changeColor(colors.ORANGE)
                                elif r1.color == colors.WHITE:
                                    r1.changeColor(colors.YELLOW)

    def get_answer(self):
        numerator = 0
        denominator = 0
        for rect in self.drawablesController.rectangles:
            denominator += 1
            if rect.color == colors.ORANGE:
                numerator += 1
        return (numerator, denominator)



    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c
