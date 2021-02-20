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
        self.ANSWERSUBMISSION = 7
        ##self.THROWINGAWAY = 6

        self.currentState = self.CUTTINGVERTICALLY

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None
        self.trashCan = None

        self.screen = screen
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)
        ##self.pop_up = pygame.Rect(int(self.WIDTH/3), 120, 500, 500)
        ##self.message_font_s = pygame.font.SysFont('Arial', 30)
        ##self.timer = 0
        ##self.error_detect = False

        self.submitAnswerButtonX = int(self.WIDTH -310)
        self.submitAnswerButtonY = int(self.HEIGHT/2 + 110)
        self.submitAnswerButton = pygame.Rect(self.submitAnswerButtonX, self.submitAnswerButtonY, 200, 50)

        self.rectsData = None
        self.hasInvertedRectData = False

        self.vColor = colors.WHITE
        self.hColor = colors.WHITE

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
                ##self.error_detect = True
                

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
                sCount = 0
                for rect in self.drawablesController.rectangles:
                    if rect.isShadedH == True:
                        sCount += 1
                if sCount != 0:
                    ##self.error_detect = False
                    self.currentState = self.MOVING
                ##self.error_detect = True
                

        elif self.currentState == self.MOVING:
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                tCount = 0
                for rect in self.drawablesController.rectangles:
                    if rect.isTrash == True:
                        tCount += 1
                if tCount != 0:        
                    self.currentState = self.ANSWERSUBMISSION
                ##self.currentState = self.THROWINGAWAY
        ##elif self.currentState == self.THROWINGAWAY:
        ##        if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
        ##            self.currentState = self.DONE
                # manager is in answer submission state, wait for user to press submit answer button to proceed
        elif self.currentState == self.ANSWERSUBMISSION:
            if self.submitAnswerButton.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                # self.currentState = self.DONE
                self.currentState = self.DONE
        


    def draw(self):
        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
            ##if self.error_detect == True:
            ##    while (self.timer <= 300):
            ##        pygame.draw.rect(self.screen, (255, 255, 255), self.pop_up)
            ##        draw_text('Shading Vert', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))

        elif self.currentState == self.SHADINGHORIZONTALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to moving', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MOVING:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to answer submission', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.ANSWERSUBMISSION:
            pygame.draw.rect(self.screen, (8, 41, 255), self.submitAnswerButton)
            draw_text('Submit Answer', self.button_font, (0,0,0), self.screen, self.submitAnswerButtonX + 100, self.submitAnswerButtonY + 25)
        ##elif self.currentState == self.THROWINGAWAY:
        ##    pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
        ##    draw_text('Finish', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))

    ###THis does nothing!TO be fixed
    def drawError(self):
        while (timer <= 300):
            pygame.draw.rect(self.screen, (255, 255, 255), self.pop_up)
            if self.currentState == self.SHADINGVERTICALLY:
                draw_text('Shading Vert', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))
            elif self.currentState == self.SHADINGHORIZONTALLY:
                draw_text('Are you sure you would like to quit?', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))
            elif self.currentState == self.MOVING:       
                draw_text('Are you sure you would like to quit?', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))
            timer += 1
    ##DISREGARD
        

    def getCurrentState(self):
        if self.currentState == self.CUTTINGVERTICALLY:
            return "Cutting Vertically"
        elif self.currentState == self.SHADINGVERTICALLY:
            return "Shading Vertically"
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            return "Cutting Horizontally"
        elif self.currentState == self.SHADINGHORIZONTALLY:
            return "Shading Horizontally"
        elif self.currentState == self.MOVING:
            return "Moving"
        elif self.currentState == self.DONE:
            return "Finished"
        elif self.currentState == self.ANSWERSUBMISSION:
            return "Submitting Answer"
        ##elif self.currentState == self.THROWINGAWAY:
        ##    return "Throwing Away"

    def shadeVertical(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True:
                    if rect.isShadedV == False:
                        rect.isShadedV = True
                        rect.vColor = self.colorPicker.myColor
                        for r in self.drawablesController.rectangles:
                            if r.isShadedV == True:
                                r.vColor = self.colorPicker.myColor
                                self.vColor = self.colorPicker.myColor
                    elif rect.isShadedV == True:
                        rect.isShadedV = False
    # needed for horiozntal shading. gets transpose of rectsData
    def invertRectData(self):
        self.rectsData = np.array(self.rectsData).T.tolist()

    # loop through all drawablesController rectangles. If its colliding with mouse and mouse released then
    # loop through each rectangle in eac row of rects data. If any rectangle in that row is selected, changle all colors
    # of rects in that row
    def shadeHorizontal(self):
        self.hColor = self.colorPicker.myColor
        for rect in self.drawablesController.rectangles:
            if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True and self.mouse.leftMouseReleasedThisFrame:
                for row in self.rectsData:
                    for r in row:
                        if r == rect:
                            for r1 in row:
                                self.colorPicker.enabled = False
                                if (r1.isShadedV == False and r1.isShadedH == False and r1.isShadedB == False) or r1.isShadedV == True: # horizontal line not shaded, make white rects shaded horizontally and vertically shaded rects shaded both ways
                                    if r1.isShadedV == True: # for vertically shaded rects
                                        r1.isShadedV = False
                                        r1.isShadedH = False
                                        r1.isShadedB = True
                                        r1.hColor = self.colorPicker.myColor
                                    else: # for white rects
                                        r1.isShadedV = False
                                        r1.isShadedH = True
                                        r1.isShadedB = False
                                        r1.hColor = self.colorPicker.myColor
                                elif r1.isShadedH == True or r1.isShadedB == True: #undo shading here
                                    if r1.isShadedB == True:
                                        r1.isShadedV = True
                                        r1.isShadedH = False
                                        r1.isShadedB = False
                                    elif r1.isShadedH == True:
                                        r1.isShadedV = False
                                        r1.isShadedH = False
                                        r1.isShadedB = False



    def get_answerDenom(self):
        denominator = 0
        for rect in self.drawablesController.rectangles:
            denominator += 1
        return denominator

    def get_answerNumer(self):
        numerator = 0
        for rect in self.drawablesController.rectangles:
            if rect.isTrash == False and (rect.isShadedV == True or rect.isShadedB == True):
                numerator += 1
        return numerator




    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c
    def setTrashCan(self, v):
        self.trashCan = v
