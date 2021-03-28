import pygame as pg
import colors
from guideline import GuideLine
from drawText import draw_text
class CutterFraction:
    def __init__(self,myRect):
        self.myRect = myRect
        self.mouse = myRect.mouse
        #bounding box class used for collision, class below CutterFraction
        self.myBoundingBox = BoundingBox(myRect.topLeftX,myRect.bottomRightX,myRect.topLeftY - 20,myRect.bottomRightY)

        #when isReadyForSubdivide == True, rectangle cuts in its update loop
        self.isReadyForSubdivide = False

        #Cutter state mgmt
        self.CUTTINGVERTICAL = 1
        self.CUTTINGHORIZONTAL = 2
        self.WAITING = 0
        self.FINALCUT = 4
        self.DONE = 3
        self.state = self.CUTTINGVERTICAL


        # CutterFraction will set myRect's numberHorizontalRects and numberVerticalRects based on 
        # verticalGuidelinesCount and horizontalGuidelninesCunt
        self.isShowingVerticalGuidelines = False
        self.verticalGuidelinesCount = 0
        self.isShowingHorizontalGuidelines = False
        self.horizontalGuidelinesCount = 0

        #SET UP FRACTION CUTS
        self.maxDivisions = 6 # This is how many possible divisions rect can be cut by
        self.dstForCutInit = 5 # how far away mouse can be to pick up cut, requires fine tuning

        # For state manager that can jump between states
        self.verticalDone = 0
        self.horizontalDone = 0

        # For subtraction to guarantee a cutter does not cut more than twice
        self.cutsMade = 0


        #init vertical cuts
        self.verticalCuts = list()
        #init horizontal cuts
        # most of horizontal cut init done in function initHorizontalCuts called when leaving
        # CUTTINGVERTICAL state b/c we dont want to show till then
        self.horizontalCuts = list()
        self.setStateCutVertical()

        # if operation is multx then start cutter out as waiting instead of vertical cutting
        if self.myRect.stateManager.operation_type == self.myRect.stateManager.MULT or self.myRect.stateManager.operation_type == self.myRect.stateManager.SUB:
            self.setStateWaiting()

        #For drawing font
        self.message_font = pg.font.SysFont('Arial', 32)
        self.message_fontL = pg.font.SysFont('Arial', 42)
        self.message_fontS = pg.font.SysFont('Arial', 22)
        
    def getState(self):
        if self.state == self.CUTTINGVERTICAL:
            return "Cutting Vertical"
        elif self.state == self.CUTTINGHORIZONTAL:
            return "Cutting Horizontal"
        elif self.state == self.WAITING:
            return "Waiting"
        elif self.state == self.DONE:
            return "Done"
        elif self.state == self.FINALCUT:
            return "Final Cut"

    def setStateWaiting(self):
        self.state = self.WAITING

    def setStateDone(self):
        self.state = self.DONE

    def setStateCutVertical(self):
        self.initVerticalCuts()
        self.state = self.CUTTINGVERTICAL

    def setStateCutHorizontal(self):
        self.initHorizontalCuts()
        self.state = self.CUTTINGHORIZONTAL

    def setupCutting(self, numberDivisionsX, numberDivisionsY):
        # dont need anything here for this cutting behavior
        pass

    def update(self, mouse):
        if self.myRect.stateManager.operation_type == self.myRect.stateManager.TEST or self.myRect.stateManager.operation_type == self.myRect.stateManager.MULT:
            # ENTRY STATE: VERTICAL CUTTING
            if self.state == self.CUTTINGVERTICAL:
                if self.myBoundingBox.isPointColliding(self.mouse.mx,self.mouse.my):
                    for fc in self.verticalCuts:
                        if abs(fc.xPos - self.mouse.mx) < self.dstForCutInit:
                            self.isShowingVerticalGuidelines = True
                            self.verticalGuidelinesCount = fc.numberCuts
                            # if mouse released and mouse.x close to fraction cut x, call cleanup/divide routines, change state
                            if self.mouse.leftMouseReleasedThisFrame == True: 
                                self.divideVertical()
                                self.isShowingVerticalGuidelines = False
                                self.cleanupCuts(self.verticalCuts)
                                # self.initHorizontalCuts()
                                # self.state = self.CUTTINGHORIZONTAL
                                self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
                                self.myRect.cutSquareVertical()
                                self.state = self.WAITING 
                                if self.horizontalDone == 1:
                                    self.state = self.FINALCUT
                                self.verticalDone = 1
                                return
            # 2ND STATE: HORIZONTAL CUTTING
            elif self.state == self.CUTTINGHORIZONTAL:
                if self.myBoundingBox.isPointColliding(self.mouse.mx,self.mouse.my):
                    for fc in self.horizontalCuts:
                        if abs(fc.yPos - self.mouse.my) < self.dstForCutInit:
                            self.isShowingHorizontalGuidelines = True
                            self.horizontalGuidelinesCount = fc.numberCuts
                            # if mouse release and mouse.y close to fraction cut y, call cleanup/divide routine, enter final state
                            if self.mouse.leftMouseReleasedThisFrame == True:
                                self.divideHorizontal()
                                self.isShowingHorizontalGuidelines = False
                                self.cleanupCuts(self.horizontalCuts)

                                self.myRect.numberVerticalRects = self.horizontalGuidelinesCount
                                self.myRect.cutSquareHorizontal()

                                self.state = self.WAITING
                                if self.verticalDone == 1:
                                    self.state = self.FINALCUT
                                self.horizontalDone = 1
                                return

            # FINAL STATE: SET UP MY RECT FOR SUBDIVIDE
            elif self.state == self.FINALCUT:
                #not sure why these next 2 lines have to be flipped but they do need to be to work properly
                self.myRect.numberVerticalRects = self.horizontalGuidelinesCount
                self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
                self.isReadyForSubdivide = True
                self.state = self.WAITING
            elif self.state == self.WAITING:
                #do nothing waiting for next instruction
                pass
        
        if self.myRect.stateManager.operation_type == self.myRect.stateManager.SUB:
            if self.state == self.CUTTINGVERTICAL:
                if self.myBoundingBox.isPointColliding(self.mouse.mx,self.mouse.my):
                    for fc in self.verticalCuts:
                        if abs(fc.xPos - self.mouse.mx) < self.dstForCutInit:
                            self.isShowingVerticalGuidelines = True
                            self.verticalGuidelinesCount = fc.numberCuts
                            # if mouse released and mouse.x close to fraction cut x, call cleanup/divide routines, change state
                            if self.mouse.leftMouseReleasedThisFrame == True: 
                                self.divideVertical()
                                self.isShowingVerticalGuidelines = False
                                self.cleanupCuts(self.verticalCuts)
                                # self.initHorizontalCuts()
                                # self.state = self.CUTTINGHORIZONTAL
                                self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
                                self.myRect.cutSquareVertical()
                                self.state = self.DONE
                                if self.cutsMade == 2:
                                    self.state = self.FINALCUT
                                else:
                                    self.cutsMade += 1        
                                return
            # 2ND STATE: HORIZONTAL CUTTING
            elif self.state == self.CUTTINGHORIZONTAL:
                if self.myBoundingBox.isPointColliding(self.mouse.mx,self.mouse.my):
                    for fc in self.horizontalCuts:
                        if abs(fc.yPos - self.mouse.my) < self.dstForCutInit:
                            self.isShowingHorizontalGuidelines = True
                            self.horizontalGuidelinesCount = fc.numberCuts
                            # if mouse release and mouse.y close to fraction cut y, call cleanup/divide routine, enter final state
                            if self.mouse.leftMouseReleasedThisFrame == True:
                                self.divideHorizontal()
                                self.isShowingHorizontalGuidelines = False
                                self.cleanupCuts(self.horizontalCuts)

                                self.myRect.numberVerticalRects = self.horizontalGuidelinesCount
                                self.myRect.cutSquareHorizontal()

                                self.state = self.DONE
                                if self.cutsMade == 2:
                                    self.state = self.FINALCUT
                                else:
                                    self.cutsMade += 1 
                                return

            # FINAL STATE: SET UP MY RECT FOR SUBDIVIDE
            elif self.state == self.FINALCUT:
                #not sure why these next 2 lines have to be flipped but they do need to be to work properly
                self.myRect.numberVerticalRects = self.horizontalGuidelinesCount
                self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
                self.isReadyForSubdivide = True
                self.state = self.WAITING
            elif self.state == self.WAITING:
                #do nothing waiting for next instruction
                pass

        else:   # IF ANY OTHER STATE BUT MULT
            # ENTRY STATE: VERTICAL CUTTING
            if self.state == self.CUTTINGVERTICAL:
                if self.myBoundingBox.isPointColliding(self.mouse.mx,self.mouse.my):
                    for fc in self.verticalCuts:
                        if abs(fc.xPos - self.mouse.mx) < self.dstForCutInit:
                            self.isShowingVerticalGuidelines = True
                            self.verticalGuidelinesCount = fc.numberCuts
                            # if mouse released and mouse.x close to fraction cut x, call cleanup/divide routines, change state
                            if self.mouse.leftMouseReleasedThisFrame == True: 
                                self.divideVertical()
                                self.isShowingVerticalGuidelines = False
                                self.cleanupCuts(self.verticalCuts)
                                # self.initHorizontalCuts()
                                # self.state = self.CUTTINGHORIZONTAL
                                self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
                                self.myRect.cutSquareVertical()
                                self.state = self.WAITING         
                else:
                    self.isShowingVerticalGuidelines = False
            # 2ND STATE: HORIZONTAL CUTTING
            elif self.state == self.CUTTINGHORIZONTAL:
                if self.myBoundingBox.isPointColliding(self.mouse.mx,self.mouse.my):
                    for fc in self.horizontalCuts:
                        if abs(fc.yPos - self.mouse.my) < self.dstForCutInit:
                            self.isShowingHorizontalGuidelines = True
                            self.horizontalGuidelinesCount = fc.numberCuts
                            # if mouse release and mouse.y close to fraction cut y, call cleanup/divide routine, enter final state
                            if self.mouse.leftMouseReleasedThisFrame == True:
                                self.divideHorizontal()
                                self.isShowingHorizontalGuidelines = False
                                self.cleanupCuts(self.horizontalCuts)
                                self.state = self.FINALCUT
                else:
                    self.isShowingHorizontalGuidelines = False
            # FINAL STATE: SET UP MY RECT FOR SUBDIVIDE
            elif self.state == self.FINALCUT:
                #not sure why these next 2 lines have to be flipped but they do need to be to work properly
                self.myRect.numberVerticalRects = self.horizontalGuidelinesCount
                self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
                self.isReadyForSubdivide = True
                self.state = self.WAITING
            elif self.state == self.WAITING:
                #do nothing waiting for next instruction
                pass

    def draw(self):
        # DISPLAY TEMPORARY VERTICAL BLUE GUIDELINES IF MOUSE X CLOSE TO FRACTION CUT X AND Draw text
        if self.isShowingVerticalGuidelines == True and (self.myRect.stateManager.getCurrentState() == "Cutting Vertically" or self.myRect.stateManager.getCurrentState() == "Cutting Vertically 1"  or self.myRect.stateManager.getCurrentState() == "Cutting Vertically 2" or self.myRect.stateManager.getCurrentState() == "Cutting Vertically 3" or self.myRect.stateManager.getCurrentState() == "Cutting Round 1" or self.myRect.stateManager.getCurrentState() == "Cutting Round 2"):
            #draw_text("YOOO",self.message_font,colors.BLACK,self.myRect.screen,200,200)
            xLength = self.myRect.width
            xSpacing = xLength / self.verticalGuidelinesCount
            for i in range(1,self.verticalGuidelinesCount):
                xPosition = int(xSpacing * i + self.myRect.topLeftX)
                pg.draw.line(self.myRect.screen,colors.DARKBLUE, [xPosition, self.myRect.topLeftY], [xPosition,self.myRect.bottomRightY], 5)
            # draw fraction text
            for i in range(0, self.verticalGuidelinesCount):
                xPosition = int(xSpacing * i + self.myRect.topLeftX)
                xOffset = int(10 + (self.myRect.width/(self.verticalGuidelinesCount+1)*.5))
                yOffset = -20
                #       #draw_text("1/" + str(self.verticalGuidelinesCount),self.message_font,colors.BLACK,self.myRect.screen,xPosition + xOffset,self.myRect.topLeftY + yOffset)
                draw_text("1",self.message_fontS,colors.BLACK,self.myRect.screen,xPosition + xOffset,self.myRect.topLeftY + yOffset - 20)
                pg.draw.line(self.myRect.screen,colors.BLACK,[xPosition + xOffset - 10,self.myRect.topLeftY + yOffset - 10],[xPosition + xOffset + 10,self.myRect.topLeftY + yOffset - 10], 2)
                draw_text(str(self.verticalGuidelinesCount),self.message_fontS,colors.BLACK,self.myRect.screen,xPosition + xOffset,self.myRect.topLeftY + yOffset)
            
        # DISPLAY TEMPORARY HORIZONTAL BLUE GUIDELINES IF MOUSE Y CLOSE TO FRACTION CUT Y and draw txt
        if self.isShowingHorizontalGuidelines == True and (self.myRect.stateManager.getCurrentState() == "Cutting Horizontally" or self.myRect.stateManager.getCurrentState() == "Cutting Horizontally 1"  or self.myRect.stateManager.getCurrentState() == "Cutting Horizontally 2" or self.myRect.stateManager.getCurrentState() == "Cutting Horizontally 3" or self.myRect.stateManager.getCurrentState() == "Cutting Round 1" or self.myRect.stateManager.getCurrentState() == "Cutting Round 2"):
            yLength = self.myRect.height
            ySpacing = yLength / self.horizontalGuidelinesCount
            for i in range(1, self.horizontalGuidelinesCount):
                yPosition = int(ySpacing * i + self.myRect.topLeftY)
                pg.draw.line(self.myRect.screen,colors.DARKBLUE, [self.myRect.topLeftX, yPosition], [self.myRect.bottomRightX,yPosition], 5)
            for i in range(0, self.horizontalGuidelinesCount):
                yPosition = int(ySpacing * i + self.myRect.topLeftY)
                yOffset = int(10 + (self.myRect.height/(self.horizontalGuidelinesCount+1)*.5))
                xOffset = -25
                #   #draw_text("1/" + str(self.horizontalGuidelinesCount),self.message_font,colors.BLACK,self.myRect.screen,self.myRect.topLeftX + xOffset,yPosition + yOffset)
                draw_text("1",self.message_fontS,colors.BLACK,self.myRect.screen,self.myRect.topLeftX + xOffset,yPosition + yOffset - 30)
                pg.draw.line(self.myRect.screen,colors.BLACK,[self.myRect.topLeftX + xOffset - 10,yPosition + yOffset - 15],[self.myRect.topLeftX + xOffset + 10,yPosition + yOffset - 15], 2)
                draw_text(str(self.horizontalGuidelinesCount),self.message_fontS,colors.BLACK,self.myRect.screen,self.myRect.topLeftX + xOffset,yPosition + yOffset)

    def autoCut(self, hCuts, vCuts):
        self.verticalGuidelinesCount = vCuts
        xLength = self.myRect.width
        xSpacing = xLength / self.verticalGuidelinesCount
        for i in range(1,self.verticalGuidelinesCount):
            xPosition = int(xSpacing * i + self.myRect.topLeftX)
            gl = GuideLine(xPosition,self.myRect.topLeftY,"vertical",self.myRect,self.myRect.screen,self.myRect.drawablesController,True)
        self.myRect.numberHorizontalRects = self.verticalGuidelinesCount
        self.myRect.cutSquareVertical()
        
        self.horizontalGuidelinesCount = hCuts
        yLength = self.myRect.height
        ySpacing = yLength / self.horizontalGuidelinesCount
        for i in range(1,self.horizontalGuidelinesCount):
            yPosition = int(ySpacing * i + self.myRect.topLeftY)
            gl = GuideLine(self.myRect.topLeftX,yPosition,"horizontal",self.myRect,self.myRect.screen,self.myRect.drawablesController,True)
        self.myRect.numberVerticalRects = self.horizontalGuidelinesCount
        self.myRect.finalCut()


    # divides OG rectangle with permanant black vertical guidelines
    def divideVertical(self):
        xLength = self.myRect.width
        xSpacing = xLength / self.verticalGuidelinesCount
        for i in range(1,self.verticalGuidelinesCount):
            xPosition = int(xSpacing * i + self.myRect.topLeftX)
            gl = GuideLine(xPosition,self.myRect.topLeftY,"vertical",self.myRect,self.myRect.screen,self.myRect.drawablesController,True)

    # divide OG rectangle with permenant black horizontal guidelines
    def divideHorizontal(self):
        yLength = self.myRect.height
        ySpacing = yLength / self.horizontalGuidelinesCount
        for i in range(1,self.horizontalGuidelinesCount):
            yPosition = int(ySpacing * i + self.myRect.topLeftY)
            gl = GuideLine(self.myRect.topLeftX,yPosition,"horizontal",self.myRect,self.myRect.screen,self.myRect.drawablesController,True)

    #loop through either self.horizontalCuts or self.verticalCuts and remove them from drawablesController list
    def cleanupCuts(self, li):
        for cut in li:
            for cm in self.myRect.drawablesController.cutmarkers:
                if cut == cm:
                    self.myRect.drawablesController.cutmarkers.remove(cut)

    def initHorizontalCuts(self):
        #init horizontal cuts
        for x in range(2, self.maxDivisions+1):
            yPos = int((self.myRect.height * (1/x)) + self.myRect.topLeftY)
            numberCuts = x
            self.horizontalCuts.append(FractionCut(self.myRect.topLeftX,yPos,numberCuts,str(numberCuts),self.myRect))
        
    def initVerticalCuts(self):
        for x in range(2,self.maxDivisions+1):
            xPos = int((self.myRect.width * (1/x)) + self.myRect.topLeftX)
            numberCuts = x
            self.verticalCuts.append(FractionCut(xPos,self.myRect.topLeftY,numberCuts,str(numberCuts),self.myRect))


class BoundingBox:
    def __init__(self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax

    def isPointColliding(self, px, py):
        if px > self.xMin and px < self.xMax and py > self.yMin and py < self.yMax:
            return True
        else:
            return False

class FractionCut:
    def __init__(self, xx, yy, numberCuts, label, myRect):
        self.xPos = xx
        self.yPos = yy
        self.numberCuts = numberCuts
        self.label = label
        self.myRect = myRect
        self.drawablesController = myRect.drawablesController
        self.drawablesController.cutmarkers.append(self)

        self.color = colors.BLUE
        self.radius = 7

    def update(self,isClick):
        pass
    def draw(self):
        # not sure if he wants outside indicators to show or not--uncomment to show
        #pg.draw.circle(self.myRect.screen, self.color, (self.xPos,self.yPos), self.radius)
        pass