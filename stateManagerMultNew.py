from cutterFraction import CutterFraction
import colors
import pygame
from drawText import draw_text
import numpy as np
from statesTab import StatesTab

class StateManagerMultNew:
    def __init__(self,cuttingType,screen,statesTab):

        self.MULT = 1
        self.DIV = 2
        self.SUB = 3
        self.ADD = 4
        self.TEST = 5
        self.operation_type = self.MULT

        #define cutting types
        self.FRACTIONCUTTING = 0
        self.VARCUTTING = 1
        self.CMCUTTING = 2
        self.cuttingType = cuttingType

        #SET statesTab
        self.statesTab = statesTab

        #define states
        self.CUTTINGVERTICALLY = 0
        self.SHADINGVERTICALLY = 1
        self.CUTTINGHORIZONTALLY = 2
        self.SHADINGHORIZONTALLY = 3
        self.FINALIZECUTS = 8
        self.WAITING = 9
        self.CHECKCUTS = 12

        self.DONE = 4
        self.MOVING = 5 # for debuging
        self.ANSWERSUBMISSION = 6

        self.currentState = self.WAITING 

        self.drawablesController = None
        self.mouse = None
        self.colorPicker = None

        self.borderLeft = 0
        self.borderTop = 0

        self.lastCuts = -1
        self.rectsHolder = list()

        self.screen = screen
        self.WIDTH = 1200
        self.HEIGHT = 700
        self.proceed_button = pygame.Rect(int((self.WIDTH/2)-150), int(self.HEIGHT/2+180), 300, 50)
        self.submitAnswerButtonX = int(self.WIDTH -310)
        self.submitAnswerButtonY = int(self.HEIGHT/2 + 110)
        self.submitAnswerButton = pygame.Rect(self.submitAnswerButtonX, self.submitAnswerButtonY, 200, 50)
        self.button_font = pygame.font.SysFont('Arial', 25)

        self.rectsData = None
        self.hasInvertedRectData = False

        self.userAnswerSystemReadyForSubmission = False

        self.hasCutHorizontally = False
        self.hasCutVertically = False
        self.hasCutVerticallyFirst = False

    def getOperationType(self):
        return self.operation_type

    def update(self, cutter):

        if self.currentState == self.CUTTINGHORIZONTALLY:
            if cutter.horizontalDone != 1:
                cutter.setStateCutHorizontal()
            else:
                self.statesTab.selectionBoxGroupListIndex = 3
                # print("done cutting vertically")
                #self.currentState = self.WAITING
                self.statesTab.clearSelected()
                self.hasCutHorizontally = True
                # Hold the rects here for undoing second set of cuts
                if self.hasCutVertically is True:
                    for rect in self.drawablesController.rectangles:
                        if rect.ownerID == 1:
                            self.rectsHolder.append(rect)
                self.lastCuts = 1   # 1 to indicate the last cut made was horizontal
                self.currentState = self.CHECKCUTS
                return

        elif self.currentState == self.CHECKCUTS:
            if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                if self.hasCutVertically is True and self.hasCutHorizontally is True:
                    cutter.state = cutter.FINALCUT
                self.currentState = self.WAITING

        if self.currentState == self.CUTTINGVERTICALLY:
            if cutter.verticalDone != 1:
                cutter.setStateCutVertical()
            else:
                if self.hasCutHorizontally == False:
                    self.hasCutVerticallyFirst = True
                self.statesTab.selectionBoxGroupListIndex = 1
                # print("done cutting vertically")
                #self.currentState = self.WAITING
                self.statesTab.clearSelected()
                self.hasCutVertically = True
                # Hold the rects here for undoing second set of cuts
                if self.hasCutHorizontally is True:
                    for rect in self.drawablesController.rectangles:
                        if rect.ownerID == 1:
                            self.rectsHolder.append(rect)
                self.lastCuts = 0   # 0 to indicate the last cut made was vertical
                self.currentState = self.CHECKCUTS
                return

        if self.currentState == self.SHADINGHORIZONTALLY:
            if self.hasInvertedRectData == False:
                self.invertRectData()   #use tab for this
                self.hasInvertedRectData = True #use tab for this
            if self.hasCutVertically == True: # user already cut vertically so use regular shading function
                self.shadeHorizontal()
            else:
                self.shadeHorizontalNew() # user has only cut horizontally, shade normally

            if self.hasCutVertically == False:
                if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                    sCount = 0
                    for rect in self.drawablesController.rectangles:
                        if rect.isShadedH == True:
                            sCount += 1
                    if sCount != 0:
                        self.statesTab.selectionBoxGroupListIndex = 4
                        self.currentState = self.WAITING
                        self.statesTab.clearSelected()
                        return



        # manager is now shading vertically, now can shade current rects
        if self.currentState == self.SHADINGVERTICALLY:
            if self.hasCutHorizontally == False: # user hasnt cut horizontally yet so regular shade function
                self.shadeVertical()
            else:
                self.shadeVerticalNew() # user has cut horizontally so use new funct
            if self.hasCutHorizontally == False:
                if self.proceed_button.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                    #if there is nothing shaded, display a quick window telling the user to shade vertically, 
                    #if there are shaded rectangles, continue as normal
                    #Display that halts the state continuation will appear for 4 Seconds
                    sCount = 0
                    for rect in self.drawablesController.rectangles:
                        if rect.isShadedV == True:
                            sCount += 1
                    if sCount != 0:
                        self.statesTab.selectionBoxGroupListIndex = 2
                        self.currentState = self.WAITING
                        self.statesTab.clearSelected()
                        return

        self.setBorderPos()

        if self.currentState == self.ANSWERSUBMISSION and self.userAnswerSystemReadyForSubmission == True:
            if self.submitAnswerButton.collidepoint((self.mouse.mx, self.mouse.my)) and self.mouse.leftMouseReleasedThisFrame:
                self.currentState = self.DONE
                self.statesTab.isStateManagerDone = True

        # get state from states tab every frame
        if self.currentState != self.DONE:
            self.getStateFromStatesTab()


    def draw(self):
        if self.currentState == self.CHECKCUTS:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        if self.currentState == self.SHADINGVERTICALLY and self.hasCutHorizontally == False:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting horizontally', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.SHADINGHORIZONTALLY and self.hasCutVertically == False:
            pygame.draw.rect(self.screen, (8, 41, 255), self.proceed_button)
            draw_text('Proceed to cutting vertically', self.button_font, (0,0,0), self.screen, self.WIDTH/2, int((self.HEIGHT/2+180)+25))
        elif self.currentState == self.ANSWERSUBMISSION:
            pygame.draw.rect(self.screen, (8, 41, 255), self.submitAnswerButton)
            draw_text('Submit Answer', self.button_font, (0,0,0), self.screen, self.submitAnswerButtonX + 100, self.submitAnswerButtonY + 25)


    def getCurrentState(self):
        if self.currentState == self.CUTTINGVERTICALLY:
            return "Cutting Vertically"
        elif self.currentState == self.SHADINGVERTICALLY:
            return "Shading Vertically"
        elif self.currentState == self.CHECKCUTS:
            return "Checking Cuts"
        elif self.currentState == self.CUTTINGHORIZONTALLY:
            return "Cutting Horizontally"
        elif self.currentState == self.SHADINGHORIZONTALLY:
            return "Shading Horizontally"
        elif self.currentState == self.DONE:
            return "Finished"
        elif self.currentState == self.MOVING:
            return "Moving"
        elif self.currentState == self.ANSWERSUBMISSION:
            return "Submitting Answer"
        elif self.currentState == self.FINALIZECUTS:
            return "Finalizing Cuts"
        elif self.currentState == None or self.currentState == self.WAITING:
          return "Waiting"

    def getStateFromStatesTab(self):
      if self.statesTab.state == "Cutting Vertically":
        self.currentState = self.CUTTINGVERTICALLY
      elif self.statesTab.state == "Cutting Horizontally":
        self.currentState = self.CUTTINGHORIZONTALLY
      elif self.statesTab.state == "Shading":
        self.currentState = self.SHADINGVERTICALLY
      elif self.statesTab.state == "Shading Vertically":
          self.currentState = self.SHADINGVERTICALLY
      elif self.statesTab.state == "Shading Horizontally":
          self.currentState = self.SHADINGHORIZONTALLY
      elif self.statesTab.state == "Submitting Answer":
        self.currentState = self.ANSWERSUBMISSION
      

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
                        #   #rect.changeColor(colors.WHITE)
                        #rect.changeColorHatch(self.colorPicker.myColor)
                        rect.changeColorHatch(colors.WHITE)
                        rect.isShadedV = False
                        rect.isShaded = False
    # needed for horiozntal shading. gets transpose of rectsData
    def invertRectData(self):
        self.rectsData = np.array(self.rectsData).T.tolist()

    def shadeHorizontalNew(self):
        if self.mouse.leftMouseReleasedThisFrame == True:
            for rect in self.drawablesController.rectangles:
                if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True:
                    if rect.isShaded == False:
                        #rect.drawLines(self.colorPicker.myColor, 0)
                        #0 = Vertical, set an internal rect variable to 1
                        #   #rect.changeColor(self.colorPicker.myColor)
                        rect.changeColorHatch(self.colorPicker.myColor)
                        rect.isShadedH = True
                        rect.isShaded = True
                    elif rect.isShaded == True:
                        #   #rect.changeColor(colors.WHITE)
                        #rect.changeColorHatch(self.colorPicker.myColor)
                        rect.changeColorHatch(colors.WHITE)
                        rect.isShadedH = False
                        rect.isShaded = False

    # loop through all drawablesController rectangles. If its colliding with mouse and mouse released then
    # loop through each rectangle in eac row of rects data. If any rectangle in that row is selected, changle all colors
    # of rects in that row
    def shadeHorizontal(self):
        for rect in self.drawablesController.rectangles:
            if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True and self.mouse.leftMouseReleasedThisFrame:
                for row in self.rectsData:
                    for r in row:
                        if r == rect:
                            self.colorPicker.enabled = False
                            for r1 in row:
                                if r1.isShadedB == True or r1.isShadedH == True: # its already been shaded by user, let them go back
                                    if r1.isShadedB == True:
                                        r1.isShadedB = False
                                        r1.changeColorHatch(self.colorPicker.verticalColor)
                                    elif r1.isShadedH == True:
                                        r1.isShadedH = False
                                        r1.changeColorHatch(colors.WHITE)

                                elif r1.colorHatch == self.colorPicker.verticalColor:
                                    #r1.isShadedH = True
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
    def shadeVerticalNew(self):
        for rect in self.drawablesController.rectangles:
            if rect.isCollidingWithPoint(self.mouse.mx, self.mouse.my) == True and self.mouse.leftMouseReleasedThisFrame:
                for row in self.rectsData:
                    for r in row:
                        if r == rect:
                            self.colorPicker.enabled = False
                            for r1 in row:
                                if r1.isShadedB == True or r1.isShadedV == True: # its already been shaded by user, let them go back
                                    if r1.isShadedB == True:
                                        r1.isShadedB = False
                                        r1.changeColorHatch(self.colorPicker.verticalColor)
                                    elif r1.isShadedV == True:
                                        r1.isShadedV = False
                                        r1.changeColorHatch(colors.WHITE)

                                elif r1.colorHatch == self.colorPicker.verticalColor:
                                    #r1.isShadedH = True
                                    r1.isShadedB = True
                                    r1.changeColorHatch(self.colorPicker.getBlendedColor())
                                    #rect.drawVLines(self.colorPicker.myColor)
                                    #1 = Horizontal, set an internal rect variable to 2
                                    #if two then (?)
                                    ##r1.changeColor(self.colorPicker.getBlendedColor())
                                elif r1.colorHatch == colors.WHITE:
                                    r1.isShadedV = True
                                    r1.changeColorHatch(self.colorPicker.myColor)
                                    ##r1.changeColor(self.colorPicker.myColor)

    def get_answer(self):
        numerator = 0
        denominator = 0
        for rect in self.drawablesController.rectangles:
            denominator += 1
            if rect.isShadedB == True:
                numerator += 1
            #   #if rect.color == self.colorPicker.getBlendedColor():
                #   #numerator += 1
        return (numerator, denominator)

    def get_answerDenom(self):
        denominator = 0
        for rect in self.drawablesController.rectangles:
            denominator += 1
        return denominator

    def get_answerNumer(self):
        numerator = 0
        for rect in self.drawablesController.rectangles:
            if rect.isShadedB == True:
                numerator += 1
        return numerator

    def undoCutsVert(self, cutter):
        if self.hasCutHorizontally is True:
            for rect in self.rectsHolder:
                if rect.isOriginalSquare is False:
                    self.drawablesController.rectangles.append(rect)
            self.rectsHolder.clear()
        else:
            for rect in self.drawablesController.rectangles:
                if rect.isOriginalSquare is False:
                    self.drawablesController.rectangles.remove(rect)
        for gl in self.drawablesController.guidelines:
            for gl2 in cutter.verticalCutList:
                if gl is gl2:
                    self.drawablesController.guidelines.remove(gl)
        cutter.verticalCuts.clear()
        # cutter.isShowingVerticalGuidelines = True
        cutter.setStateCutVertical()
        self.hasCutVertically = False
        cutter.verticalDone = 0
        self.currentState = self.CUTTINGVERTICALLY

    def undoCutsHoriz(self, cutter):
        if self.hasCutVertically is True:
            for rect in self.rectsHolder:
                if rect.isOriginalSquare is False:
                    self.drawablesController.rectangles.append(rect)
            self.rectsHolder.clear()
        else:
            for rect in self.drawablesController.rectangles:
                if rect.isOriginalSquare is False:
                        self.drawablesController.rectangles.remove(rect)
        for gl in self.drawablesController.guidelines:
            for gl2 in cutter.horizontalCutList:
                if gl is gl2:
                    self.drawablesController.guidelines.remove(gl)
        cutter.horizontalCuts.clear()
        cutter.setStateCutHorizontal()
        cutter.horizontalDone = 0
        self.hasCutHorizontally = False
        # cutter.isShowingHorizontalGuidelines = True
        self.currentState = self.CUTTINGHORIZONTALLY



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