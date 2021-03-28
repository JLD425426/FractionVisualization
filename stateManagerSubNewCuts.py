from cutterFraction import CutterFraction
import colors
import pygame
from drawText import draw_text
import numpy as np
from statesTab import StatesTab

##We do not use the statesTab, as I am trying to manipulate the cutterFraction more
##statesTab is set to None

class StateManagerSubNewCuts:
    def __init__(self,cuttingType,screen,statesTab):

        self.MULT = 1
        self.DIV = 2
        self.SUB = 3
        self.ADD = 4
        self.TEST = 5
        self.operation_type = self.SUB

        #define cutting types
        self.FRACTIONCUTTING = 0
        self.VARCUTTING = 1
        self.CMCUTTING = 2
        self.cuttingType = cuttingType

        self.statesTab = statesTab

        #define states
        self.CUTTINGFIRST = 0
        self.SHADINGVERTICALLY = 1
        self.CUTTINGSECOND = 2
        self.SHADINGHORIZONTALLY = 9 #Throwaway value for now
        self.MARKING = 3
        self.DONE = 4
        self.MOVING = 5 # for debuging
        self.ANSWERSUBMISSION = 7
        ##self.THROWINGAWAY = 6

        self.currentState = self.CUTTINGFIRST

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None
        self.trashCan = None

        

        self.screen = screen
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        self.selectionBoxWidth = 64
        self.selectionBoxHeight = 64

        #TODO: Add hover and selected buttons to the options
        #TODO: Figure out cut bug

        self.vButton1x = (int)(self.WIDTH/8)
        self.vButton1y = self.HEIGHT/2 - 160
        self.vButton1 = pygame.Rect(self.vButton1x, self.vButton1y, self.selectionBoxWidth, self.selectionBoxHeight)

        self.vButton2x = (int)(self.WIDTH/2) - 48
        self.vButton2y = self.HEIGHT/2 - 160
        self.vButton2 = pygame.Rect(self.vButton2x, self.vButton2y, self.selectionBoxWidth, self.selectionBoxHeight)

        self.hButton1x = (int)(self.WIDTH/8) 
        self.hButton1y = self.HEIGHT/2 - 90
        self.hButton1 = pygame.Rect(self.hButton1x, self.hButton1y, self.selectionBoxWidth, self.selectionBoxHeight)

        self.hButton2x = (int)(self.WIDTH/2) - 48
        self.hButton2y = self.HEIGHT/2 - 90
        self.hButton2 = pygame.Rect(self.hButton2x, self.hButton2y, self.selectionBoxWidth, self.selectionBoxHeight)

        self.dButton1x = (int)(self.WIDTH/8)
        self.dButton1y =  self.HEIGHT/2 - 20
        self.dButton1 = pygame.Rect(self.dButton1x, self.dButton1y, self.selectionBoxWidth, self.selectionBoxHeight)

        self.dButton2x = (int)(self.WIDTH/2) - 48
        self.dButton2y =  self.HEIGHT/2 - 20
        self.dButton2 = pygame.Rect(self.dButton2x, self.dButton2y, self.selectionBoxWidth, self.selectionBoxHeight)

        
        ##self.pop_up = pygame.Rect(int(self.WIDTH/3), 120, 500, 500)
        ##self.message_font_s = pygame.font.SysFont('Arial', 30)
        ##self.timer = 0
        ##self.error_detect = False

        self.submitAnswerButtonX = int(self.WIDTH/2 - 100)
        self.submitAnswerButtonY = int(self.HEIGHT - 60)
        self.submitAnswerButton = pygame.Rect(self.submitAnswerButtonX, self.submitAnswerButtonY, 200, 50)

        self.rectsData = None
        self.hasInvertedRectData = False

        # For border to highlight current section
        self.borderSet = 0
        self.borderTop = 0
        self.borderLeft = 0

        self.vColor = colors.WHITE
        self.hColor = colors.WHITE

        self.userAnswerSystemReadyForSubmission = False

    def getOperationType(self):
        return self.operation_type

    def update(self, cutter, cutter2):
        # manager is cuttingvertically, wait for cutter class to be waiting so it can proceed
        if self.currentState == self.CUTTINGFIRST:

            #Rect 1 buttons
            if self.vButton1.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter.getState() == "Waiting":
                cutter.setStateCutVertical()
            if self.hButton1.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter.getState() == "Waiting":
                cutter.setStateCutHorizontal()    
            #Rect 2 buttons    
            if self.vButton2.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter2.getState() == "Waiting":
                cutter2.setStateCutVertical()   
            if self.hButton2.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter2.getState() == "Waiting":
                cutter2.setStateCutHorizontal()     

            if cutter.getState() == "Done" and cutter2.getState() == "Done":
                self.setBorderPos()
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
                    self.currentState = self.CUTTINGSECOND
                    cutter.setStateWaiting()
                    cutter2.setStateWaiting()
                ##self.error_detect = True

        # manager now cutting horizontally, let cutter do work
        elif self.currentState == self.CUTTINGSECOND:
            #Rect 1 buttons
            if self.vButton1.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter.getState() == "Waiting":
                cutter.setStateCutVertical()
            if self.hButton1.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter.getState() == "Waiting":
                cutter.setStateCutHorizontal()    
            if self.dButton1.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter.getState() == "Waiting":
                cutter.cutsMade += 1
                cutter.setStateDone()
            #Rect 2 buttons    
            if self.vButton2.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter2.getState() == "Waiting":
                cutter2.setStateCutVertical()   
            if self.hButton2.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter2.getState() == "Waiting":
                cutter2.setStateCutHorizontal()
            if self.dButton2.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame and cutter2.getState() == "Waiting":
                cutter2.cutsMade += 1
                cutter2.setStateDone()

            if cutter.getState() == "Done" and cutter2.getState() == "Done":
                #self.currentState = self.SHADINGHORIZONTALLY
                
                self.currentState = self.MARKING

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

        elif self.currentState == self.MARKING:
            self.markRects()
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                mCount = 0 
                tCount = 0
                #if the amount of marked rectangles is less than the number of colored rectangles on the right rectangle
                #"Block" the user's button press
                #for rect in self.drawablesController.rectangles:
                #    if rect.ownerID == 2 and rect.color != colors.WHITE:
                #        tCount += 1
                #      if rect.isMarked == True:
                #            mCount += 1
                #if mCount == tCount:
                self.get_answerNumer()
                self.get_answerDenom()
                self.currentState = self.ANSWERSUBMISSION
                        



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
        elif self.currentState == self.ANSWERSUBMISSION and self.userAnswerSystemReadyForSubmission == True:
            if self.submitAnswerButton.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                # self.currentState = self.DONE
                self.currentState = self.DONE
        


    def draw(self):
        
        if self.currentState == self.CUTTINGFIRST:
            #Rect 1
            pygame.draw.rect(self.screen, (8, 41, 255), self.vButton1)
            pygame.draw.rect(self.screen, (8, 41, 255), self.hButton1)
            #REct 2
            pygame.draw.rect(self.screen, (8, 41, 255), self.vButton2)
            pygame.draw.rect(self.screen, (8, 41, 255), self.hButton2)

        if self.currentState == self.SHADINGVERTICALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting 2', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
            ##if self.error_detect == True:
            ##    while (self.timer <= 300):
            ##        pygame.draw.rect(self.screen, (255, 255, 255), self.pop_up)
            ##        draw_text('Shading Vert', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))

        if self.currentState == self.CUTTINGSECOND:
            #Rect 1
            pygame.draw.rect(self.screen, (8, 41, 255), self.vButton1)
            pygame.draw.rect(self.screen, (8, 41, 255), self.hButton1)
            pygame.draw.rect(self.screen, (8, 41, 255), self.dButton1)
            #REct 2
            pygame.draw.rect(self.screen, (8, 41, 255), self.vButton2)
            pygame.draw.rect(self.screen, (8, 41, 255), self.hButton2)
            pygame.draw.rect(self.screen, (8, 41, 255), self.dButton2)

        elif self.currentState == self.SHADINGHORIZONTALLY:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to marking', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MOVING:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to answer submission', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.MARKING:
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
                draw_text('Shading', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))
            elif self.currentState == self.SHADINGHORIZONTALLY:
                draw_text('Are you sure you would like to quit?', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))
            elif self.currentState == self.MOVING:       
                draw_text('Are you sure you would like to quit?', self.message_font_s, (0,0,0), self.screen, (int)(self.WIDTH/2), (self.HEIGHT-560))
            timer += 1
    ##DISREGARD
        

    def getCurrentState(self):
        if self.currentState == self.CUTTINGFIRST:
            return "Cutting Round 1"
        elif self.currentState == self.SHADINGVERTICALLY:
            return "Shading"
        elif self.currentState == self.CUTTINGSECOND:
            return "Cutting Round 2"
        #elif self.currentState == self.SHADINGHORIZONTALLY:
        #    return "Shading Horizontally"
        elif self.currentState == self.MARKING:
            return "Marking"
        #elif self.currentState == self.MOVING:
        #    return "Moving"
        elif self.currentState == self.DONE:
           return "Finished"
        elif self.currentState == self.ANSWERSUBMISSION:
            return "Submitting Answer"
        ##elif self.currentState == self.THROWINGAWAY:
        ##    return "Throwing Away"

    def markRects(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True and rect.isShaded == True:
                    if rect.ownerID == 1:
                        if rect.getMark() == False:
                        #now find a shaded rectangle in the other rectangle and mark it at the same time, once we mark one rectangle we stop
                            for _r in self.drawablesController.rectangles:
                                if _r.ownerID == 2 and _r.isShaded == True and _r.getMark() == False:
                                    rwd = rect.width - _r.width
                                    rhd = rect.height - _r.height
                                    rowd = rect.width - _r.height
                                    rohd = rect.height - _r.width
                                    if ((rwd >= -1 and rwd <= 1) and (rhd >= -1 and rhd <= 1)) or ((rowd >= -1 and rowd <= 1) and (rohd >= -1 and rohd <= 1)):
                                        _r.setMark(True)
                                        rect.setMark(True)
                                        break



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
            if rect.ownerID == 1:
                denominator += 1
        return denominator

    def get_answerNumer(self):
        numerator = 0
        for rect in self.drawablesController.rectangles:
            ##if rect.isTrash == False and (rect.isShadedV == True or rect.isShadedB == True):
            ##    numerator += 1
            if rect.ownerID == 1 and rect.isMarked == False and rect.isShaded == True:
                numerator += 1
        return numerator

    def setBorderPos(self):
        for rect in self.drawablesController.rectangles:
            if rect.ownerID == 1:
                self.borderLeft = rect.xPosition - (rect.width/2)
                self.borderTop = rect.yPosition - (rect.height/2)
                return


    #Setter functions required b/c state manager instantiated 1st, cannot pass these vars into __init__
    def setDrawablesController(self, dC):
        self.drawablesController = dC
    def setMouse(self, m):
        self.mouse = m
    def setColorPicker(self, c):
        self.colorPicker = c
    def setTrashCan(self, v):
        self.trashCan = v
