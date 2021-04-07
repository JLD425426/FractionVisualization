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
        self.CUTTINGVERTICAL = 0
        self.CUTTINGHORIZONTAL = 1
        self.WAITING = 2
        self.FINALCUT = 3
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

        # For undoing cuts
        self.verticalCutList = list()
        self.horizontalCutList = list()

        #init vertical cuts
        self.verticalCuts = list()
        self.horizontalCuts = list()
        self.setStateCutVertical()

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
        elif self.state == self.FINALCUT:
            return "Final Cut"

    def setStateWaiting(self):
        self.state = self.WAITING

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
                            if self.myRect.stateManager.operation_type == self.myRect.stateManager.DIV or self.myRect.stateManager.operation_type == self.myRect.stateManager.MULT or self.myRect.stateManager.operation_type == self.myRect.stateManager.SUB:
                                self.state = self.WAITING
                            else:
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
        if self.isShowingVerticalGuidelines == True:
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
        if self.isShowingHorizontalGuidelines == True:
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
            self.verticalCutList.append(gl)

    # divide OG rectangle with permenant black horizontal guidelines
    def divideHorizontal(self):
        yLength = self.myRect.height
        ySpacing = yLength / self.horizontalGuidelinesCount
        for i in range(1,self.horizontalGuidelinesCount):
            yPosition = int(ySpacing * i + self.myRect.topLeftY)
            gl = GuideLine(self.myRect.topLeftX,yPosition,"horizontal",self.myRect,self.myRect.screen,self.myRect.drawablesController,True)
            self.horizontalCutList.append(gl)
    #loop through either self.horizontalCuts or self.verticalCuts and remove them from drawablesController list
    def cleanupCuts(self, li):
        for cut in li:
            for cm in self.myRect.drawablesController.cutmarkers:
                if cut == cm:
                    self.myRect.drawablesController.cutmarkers.remove(cut)

    def initHorizontalCuts(self):
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