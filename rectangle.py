import pygame as pg
import colors
from cutmarker import CutMarker
from mouseHolder import MouseHandler
from guideline import GuideLine
from bgSquare import BgSquare
from pointCollider import PointCollider
from stateManager import manager
from cutterCutmarkers import CutterCutmarkers
from cutterVariable import CutterVariable
from cutterFraction import CutterFraction
import random

class Rectangle:
    def __init__(self, xx, yy, w, h, screen,drawablesController,isOriginalSquare, mouse,stateManager, ownerID):
        # the xPosition and yPosition refer to the middle point of the rectangle
        # include a origin point
        self.xPosition = xx
        self.yPosition = yy
        self.width = w
        self.height = h
        self.screen = screen
        self.drawablesController = drawablesController
        self.drawablesController.rectangles.append(self)
        self.xOrigin = xx
        self.yOrigin = yy
        self.address = self
        self.willBeDivided = True
        self.myPointCollider = None

        # Keeps track of which original rectangle it is a part of for shading in division
        # 0 if original test rect, 1 for first (left) rectangle, 2 for second (right), doesn't apply to multiplication
        self.ownerID = ownerID
        
        self.stateManager = stateManager

        #mouse var needed to pass to cutting
        self.mouse = mouse

        # these member variables may be useful for rectangle collisions
        self.topLeftX = int(self.xPosition - self.width / 2)
        self.topLeftY = int(self.yPosition - self.height / 2)
        self.bottomRightX = int(self.xPosition + self.width / 2)
        self.bottomRightY = int(self.yPosition + self.height / 2)
        self.topRightX = self.topLeftX + self.width
        self.bottomLeftX = self.bottomRightX - self.width

        # boolean var to decide if rectangle should be subdivided when all cutmarkers removed
        self.isOriginalSquare = isOriginalSquare

        # vars used to cut up rectangles if is original square
        self.numberHorizontalRects = -1
        self.numberVerticalRects = -1

        # show random color to display cutting working
        if self.isOriginalSquare == True:
            self.color = colors.WHITE
        else:
            # possColors = (colors.GREEN,colors.RED,colors.DARKBLUE)
            self.color = colors.WHITE
        self.isShaded = False # boolean used for toggling off/on shading
        # booleans used for cross-hatch shading
        self.isShadedV = False 
        self.isShadedH = False
        self.isShadedB = False
        self.colorHatch = colors.WHITE

        self.vColor = None # for subtraction right now
        self.hColor = None # just for subtr right now

        self.isTrash = False
        self.isMarked = False

        # draw outer guidelines and bg square only if rectangle is original square
        if self.isOriginalSquare == True:
            GuideLine(self.topLeftX,self.topLeftY,"vertical",self,self.screen,self.drawablesController, True)
            GuideLine(self.topLeftX,self.topLeftY,"horizontal",self,self.screen,self.drawablesController, True)
            GuideLine(self.topLeftX + self.width,self.topLeftY,"vertical",self,self.screen,self.drawablesController, True)
            GuideLine(self.topLeftX,self.topLeftY + self.height,"horizontal",self,self.screen,self.drawablesController, True)
            BgSquare(self.topLeftX,self.topLeftY,self.width,self.height,self.screen,self.drawablesController)

        # cutting behavior
        self.myCutter = None
        if self.isOriginalSquare == True:
            if self.stateManager.cuttingType == self.stateManager.VARCUTTING:
                self.myCutter = CutterVariable(self)
            elif self.stateManager.cuttingType == self.stateManager.CMCUTTING:
                self.myCutter = CutterCutmarkers(self)
            elif self.stateManager.cuttingType == self.stateManager.FRACTIONCUTTING:
                self.myCutter = CutterFraction(self)


    def update(self, mouse):

        # if is orig square update cutter and check if time to cut/movestate
        if self.isOriginalSquare == True:
            self.myCutter.update(mouse)

            #if len(self.drawablesController.cutmarkers) == 0:
            if self.myCutter.isReadyForSubdivide == True:
                self.finalCut()

        if self.stateManager.getCurrentState() == "Moving":

            if self.stateManager.operation_type == 4:       #Addition
                if self.isOriginalSquare == False and (self.ownerID != 3 and self.ownerID != 4):
                    if self.isShadedV is True:
                        if mouse.isClick == True and self.isCollidingWithPoint(mouse.mx,mouse.my) == True and mouse.whoisHeld == None and self.stateManager.getCurrentState() == "Moving":
                                mouse.whoisHeld = self
                                if self.myPointCollider != None:
                                    self.myPointCollider.isOccupied = False
                            # mouse release so remove self as being held
                        if mouse.isClick == False and mouse.whoisHeld == self:
                            self.putDownAdd(mouse)
                            # self is being dragged so move it around
                        if mouse.whoisHeld == self:
                            self.updatePosition(mouse.mx,mouse.my)

            if self.stateManager.operation_type == 2:       #Division
                    #collision checking with mouse, also check if square belongs to right side original rectangle (don't want these moved)
                    ##if self.isOriginalSquare == False and self.ownerID != 2 and (self.colorHatch != colors.WHITE or self.color != colors.WHITE):
                if self.isOriginalSquare == False and self.colorHatch != colors.WHITE and (self.ownerID != 2 and self.ownerID != 3):
                        # mouse is holding no one and clicking, set self as being held
                        if self.isShadedB is True or self.isShadedH is True:
                            if mouse.isClick == True and self.isCollidingWithPoint(mouse.mx,mouse.my) == True and mouse.whoisHeld == None and self.stateManager.getCurrentState() == "Moving":
                                mouse.whoisHeld = self
                                if self.myPointCollider != None:
                                    self.myPointCollider.isOccupied = False
                            # mouse release so remove self as being held
                            if mouse.isClick == False and mouse.whoisHeld == self:
                                self.putDownDiv(mouse)
                            # self is being dragged so move it around
                            if mouse.whoisHeld == self:
                                self.updatePosition(mouse.mx,mouse.my)
                else:
                #collision checking with mouse, also check if square belongs to right side original rectangle (don't want these moved)
                    if self.isOriginalSquare == False and self.ownerID != 2 and self.ownerID != 3 and(self.colorHatch != colors.WHITE or self.color != colors.WHITE):
                    ##if self.isOriginalSquare == False and (self.colorHatch != colors.WHITE or self.color != colors.WHITE):
                        # mouse is holding no one and clicking, set self as being held
                        if mouse.isClick == True and self.isCollidingWithPoint(mouse.mx,mouse.my) == True and mouse.whoisHeld == None and self.stateManager.getCurrentState() == "Moving":
                            mouse.whoisHeld = self
                            if self.myPointCollider != None:
                                self.myPointCollider.isOccupied = False
                        # mouse release so remove self as being held
                        if mouse.isClick == False and mouse.whoisHeld == self:
                            self.putDownDiv(mouse)
                        # self is being dragged so move it around
                        if mouse.whoisHeld == self:
                            self.updatePosition(mouse.mx,mouse.my)

    def updatePosition(self,xx,yy):
        self.xPosition = xx
        self.yPosition = yy
        self.topLeftX = (self.xPosition - self.width / 2)
        self.topLeftY = (self.yPosition - self.height / 2)                    
        self.bottomRightX = (self.xPosition + self.width / 2)
        self.bottomRightY = (self.yPosition + self.height / 2)

    def rotatePosition(self,xx,yy):
        newW = self.height
        newH = self.width
        self.width = newW
        self.height = newH
        self.xPosition = xx
        self.yPosition = yy
        self.topLeftX = (self.xPosition - self.width / 2)
        self.topLeftY = (self.yPosition - self.height / 2)                    
        self.bottomRightX = (self.xPosition + self.width / 2)
        self.bottomRightY = (self.yPosition + self.height / 2)

            
    def isCollidingWithPoint(self,xx, yy):
        if (xx > self.topLeftX and xx < self.bottomRightX and yy > self.topLeftY and yy < self.bottomRightY):
            return True
        else:
            return False

    def isCollidingWithTrash(self):
        topLX = 0
        topLY = 500
        botRX = 250
        botRY = 700
        if (self.topLeftX >= topLX and self.topLeftY >= topLY and self.bottomRightX <= botRX and self.bottomRightY <= botRY) and self:
            return True
        else:
            return False

        ##if (xx > self.topLeftX and xx < self.bottomRightX and yy > self.topLeftY and yy < self.bottomRightY):
        ##    return True
        ##else:
        ##    return False

    def putDownAdd(self,mouse):
        mouse.whoisHeld = None
        replaced = None
        ogColor = colors.WHITE
        for pc in self.drawablesController.pointColliders:
            if self.isCollidingWithPoint(pc.x,pc.y):
                # do not allow rects to be dragged onto empty(grey spaces) here by checking if the pc is not occupied
                if pc.isOccupied == False:
                    self.updatePosition(self.xOrigin, self.yOrigin)
                    return
 
                if pc.isOccupied and pc.valid:
                    for rect in self.drawablesController.rectangles:
                        if rect.myPointCollider is not None:
                            if rect.myPointCollider.x == pc.x and rect.myPointCollider.y == pc.y:
                                # #for allow rects to be dragged onto white squares
                                # if (rect.color == colors.WHITE or rect.ownerID == 1 or rect.isOriginalSquare):
                                # if (rect.color == colors.WHITE and rect.colorHatch == colors.BLACK) or rect.ownerID == 1 or rect.isOriginalSquare:
                                if (rect.color != colors.WHITE or rect.ownerID == 1 or rect.ownerID == 2 or rect.isOriginalSquare):
                                    self.updatePosition(self.xOrigin, self.yOrigin)
                                    return
                                else:
                                    if rect.color != colors.WHITE:
                                        ogColor = rect.color
                                    replaced = rect
                else:
                    if self.xOrigin == pc.x and self.yOrigin == pc.y:
                        self.updatePosition(self.xOrigin, self.yOrigin)
                        return
                # check to see if the spot occupied has matching height and width 
                # or check to see if the height of rect1 matches the width of rect2 and the width of rect1 matches the height of rect2
                # if neither statement is true, call snapback to the origin
                if (self.width - pc.width <= 1 and self.width - pc.width >= -1 and self.height - pc.height <= 1 and self.height - pc.height >= -1):
                    #deal with rounding errors
                    self.updatePosition(pc.x,pc.y)
                    self.xOrigin = pc.x
                    self.yOrigin = pc.y
                    pc.isOccupied = True
                    self.myPointCollider = pc

                    if self.stateManager.movedBefore == False:
                        self.ownerID = 3
                    else:
                        self.ownerID = 4
                    ##Can we change this?
                    if replaced:
                        self.drawablesController.pointColliders.remove(replaced.myPointCollider)
                        self.drawablesController.rectangles.remove(replaced)
                    return
                elif (self.width - pc.height <= 1 and self.width - pc.height >= -1 and self.height - pc.width <= 1 and self.height - pc.width >= -1):
                    #need to work on rotate
                    self.xOrigin = pc.x
                    self.yOrigin = pc.y
                    self.rotatePosition(pc.x,pc.y)
                    pc.isOccupied = True
                    self.myPointCollider = pc

                    if self.stateManager.movedBefore == False:
                        self.ownerID = 3
                    else:
                        self.ownerID = 4
                    ##Can we change this?
                    if replaced:
                        self.drawablesController.pointColliders.remove(replaced.myPointCollider)
                        self.drawablesController.rectangles.remove(replaced)
                    return
                else:
                    pass
        self.updatePosition(self.xOrigin, self.yOrigin)
            

    def putDownDiv(self,mouse):
        mouse.whoisHeld = None
        replaced = None
        ogColor = colors.WHITE
        for pc in self.drawablesController.pointColliders:
            if self.isCollidingWithPoint(pc.x,pc.y):
                # do not allow rects to be dragged onto empty(grey spaces) here by checking if the pc is not occupied
                if pc.isOccupied == False:
                    self.updatePosition(self.xOrigin, self.yOrigin)
                    return
 
                if pc.isOccupied and pc.valid:
                    for rect in self.drawablesController.rectangles:
                        if rect.myPointCollider is not None:
                            if rect.myPointCollider.x == pc.x and rect.myPointCollider.y == pc.y:
                                # #for not allow rects to be dragged onto white squares
                                # if (rect.color == colors.WHITE or rect.ownerID == 1 or rect.isOriginalSquare):
                                # if (rect.color == colors.WHITE and rect.colorHatch == colors.BLACK) or rect.ownerID == 1 or rect.isOriginalSquare:
                                if (rect.color == colors.WHITE or rect.ownerID == 1 or rect.isOriginalSquare):
                                    self.updatePosition(self.xOrigin, self.yOrigin)
                                    return
                                else:
                                    if rect.color != colors.WHITE:
                                        ogColor = rect.color
                                    replaced = rect
                else:
                    if self.xOrigin == pc.x and self.yOrigin == pc.y:
                        self.updatePosition(self.xOrigin, self.yOrigin)
                        return
                # check to see if the spot occupied has matching height and width 
                # or check to see if the height of rect1 matches the width of rect2 and the width of rect1 matches the height of rect2
                # if neither statement is true, call snapback to the origin
                if (self.width - pc.width <= 1 and self.width - pc.width >= -1 and self.height - pc.height <= 1 and self.height - pc.height >= -1):
                    #deal with rounding errors
                    self.updatePosition(pc.x,pc.y)
                    self.xOrigin = pc.x
                    self.yOrigin = pc.y
                    pc.isOccupied = True
                    self.myPointCollider = pc
                    self.changeColorHatch(colors.BLACK)
                    if self.color != colors.WHITE or self.color != ogColor:
                        self.color = ogColor
                    self.stateManager.invertRectData()
                    self.isShadedH = True
                    self.isShadedB = True
                    self.ownerID = 2
                    if replaced:
                        self.drawablesController.pointColliders.remove(replaced.myPointCollider)
                        self.drawablesController.rectangles.remove(replaced)
                    return
                elif (self.width - pc.height <= 1 and self.width - pc.height >= -1 and self.height - pc.width <= 1 and self.height - pc.width >= -1):
                    #need to work on rotate
                    self.xOrigin = pc.x
                    self.yOrigin = pc.y
                    self.rotatePosition(pc.x,pc.y)
                    pc.isOccupied = True
                    self.myPointCollider = pc
                    self.changeColorHatch(colors.BLACK)
                    if self.color != colors.WHITE or self.color != ogColor:
                        self.color = ogColor
                    self.stateManager.invertRectData()
                    self.isShadedH = True
                    self.isShadedB = True
                    self.ownerID = 2
                    if replaced:
                        self.drawablesController.pointColliders.remove(replaced.myPointCollider)
                        self.drawablesController.rectangles.remove(replaced)
                    return
                else:
                    pass
        self.updatePosition(self.xOrigin, self.yOrigin)
        

    def draw(self):
        pg.draw.rect(self.screen, self.color, [self.topLeftX,self.topLeftY,self.width,self.height],0)

        if self.stateManager.operation_type == 2: # subtraction
            if self.isMarked == True:
                self.drawMark()

        if self.stateManager.operation_type == 1: # multiplication
            isShadedLeftToRight = self.isShadedV # adapter variable
            isShadedRightToLeft = self.isShadedH # adapter variable
            if self.isShadedB == True:
                #SHADE TOP-BOTTOM 
                currentY = self.topLeftY
                while (currentY < self.bottomRightY):
                    newX, newY = self.getLineLengthLeftToRight(self.topLeftX,currentY)
                    pg.draw.line(self.screen, self.colorHatch, [self.topLeftX,currentY], [newX, newY], 6)
                    currentY += 25
                #SHADE LEFT-RIGHT
                currentX = self.topLeftX
                while (currentX < self.bottomRightX):
                    newX, newY = self.getLineLengthLeftToRight(currentX,self.topLeftY)
                    pg.draw.line(self.screen, self.colorHatch, [currentX,self.topLeftY], [newX, newY], 6)
                    currentX += 25
                #SHADE TOP-BOTTOM 
                currentY = self.topLeftY
                while (currentY < self.bottomRightY):
                    newX, newY = self.getLineLengthRightToLeft(self.bottomRightX,currentY)
                    pg.draw.line(self.screen, self.colorHatch, [self.bottomRightX,currentY], [newX, newY], 6)
                    currentY += 25
                #SHADE LEFT-RIGHT
                currentX = self.bottomRightX
                while (currentX > self.topLeftX):
                    newX, newY = self.getLineLengthRightToLeft(currentX,self.topLeftY)
                    pg.draw.line(self.screen, self.colorHatch, [currentX,self.topLeftY], [newX, newY], 6)
                    currentX -= 25
                
            #SHADING LEFT TO RIGHT
            elif isShadedLeftToRight == True:
                #SHADE TOP-BOTTOM 
                currentY = self.topLeftY
                while (currentY < self.bottomRightY):
                    newX, newY = self.getLineLengthLeftToRight(self.topLeftX,currentY)
                    pg.draw.line(self.screen, self.colorHatch, [self.topLeftX,currentY], [newX, newY], 6)
                    currentY += 25
                #SHADE LEFT-RIGHT
                currentX = self.topLeftX
                while (currentX < self.bottomRightX):
                    newX, newY = self.getLineLengthLeftToRight(currentX,self.topLeftY)
                    pg.draw.line(self.screen, self.colorHatch, [currentX,self.topLeftY], [newX, newY], 6)
                    currentX += 25
            #SHADING RIGHT TO LEFT
            elif isShadedRightToLeft == True:
                #SHADE TOP-BOTTOM 
                currentY = self.topLeftY
                while (currentY < self.bottomRightY):
                    newX, newY = self.getLineLengthRightToLeft(self.bottomRightX,currentY)
                    pg.draw.line(self.screen, self.colorHatch, [self.bottomRightX,currentY], [newX, newY], 6)
                    currentY += 25
                #SHADE LEFT-RIGHT
                currentX = self.bottomRightX
                while (currentX > self.topLeftX):
                    newX, newY = self.getLineLengthRightToLeft(currentX,self.topLeftY)
                    pg.draw.line(self.screen, self.colorHatch, [currentX,self.topLeftY], [newX, newY], 6)
                    currentX -= 25
                

                # pg.draw.line(self.screen, self.colorHatch, [self.topRightX,self.topLeftY], [self.topRightX - 30, self.topLeftY + 30], 4)

    def getLineLengthLeftToRight(self,xStart, yStart):
        x = xStart
        y = yStart
        while (x < self.bottomRightX and y < self.bottomRightY):
            x += 1
            y += 1
        return x,y

    def getLineLengthRightToLeft(self,xStart,yStart):
        x = xStart
        y = yStart
        while (x > self.topLeftX and y < self.bottomRightY):
            x -= 1
            y += 1
        return x,y


    def getCutter(self):
        return self.myCutter

    def setupCutting(self, numberDivisionsX, numberDivisionsY):
       self.myCutter.setupCutting(numberDivisionsX,numberDivisionsY)

    def cutSquareVertical(self):
        xLength = self.width / self.numberHorizontalRects
        yLength = self.height
        xOffset = xLength / 2
        yOffset = yLength / 2
        for i in range(0,self.numberHorizontalRects):
            r = None
            if self.willBeDivided == True:
                if self.ownerID == 1:
                    r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(0 * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 1)
                if self.ownerID == 2:
                    r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(0 * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 2)
                if self.ownerID == 3:
                    r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(0 * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 3)
                if self.ownerID == 4:
                    r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(0 * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 4)
            pc = PointCollider(int(i * xLength + self.topLeftX + xOffset),int(0 * yLength + self.topLeftY + yOffset),self.willBeDivided,xLength,yLength, False)
            # self.drawablesController.pointColliders.append(pc)
            if r != None:
                r.myPointCollider = pc

    def cutSquareHorizontal(self):
        pass
        
    #----------WARNING----------------
    #----anticipated pointcollider bugs here----
    def finalCut(self):
        #first create a copy of drawables controller list-these rects must be deleted at end of funct (vertical rects)
        copyList = list()
        for r in self.drawablesController.rectangles:
            if r.ownerID == self.ownerID:
                copyList.append(r)
        #remove self from copy list b/c we dont want to use it for collision checking for shaded value
        copyList.remove(self)

        xLength = self.width / self.numberHorizontalRects
        yLength = self.height / self.numberVerticalRects
        xOffset = xLength / 2
        yOffset = yLength / 2

        rectsData = list() # used by state manager for horizontal shading, list of lists->each row of rects is list
        for i in range(0,self.numberHorizontalRects):
            rectsRow = list() # each row will be 1 element in rectsData
            for j in range(0,self.numberVerticalRects):
                r = None
                if self.willBeDivided == True:
                    if self.ownerID == 1:
                        r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 1)
                        rectsRow.append(r)
                    elif self.ownerID == 2:
                        r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 2)
                        rectsRow.append(r)
                    elif self.ownerID == 3:
                        r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 3)
                        rectsRow.append(r)
                    elif self.ownerID == 4:
                        r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False,self.mouse,self.stateManager, 4)
                        rectsRow.append(r)
                    # see if theres already a rectangle in r's new spot, if there is-> shade it to that rectangles color
                    if self.getRectCollider(copyList, int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset)) != None:
                        # rC is prexisting vertical rectangle
                        rC = self.getRectCollider(copyList, int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset))
                        if self.drawablesController.pointColliders.count(rC.myPointCollider) > 0:
                            self.drawablesController.pointColliders.remove(rC.myPointCollider)
                        if rC.isShaded == True or rC.isShadedV == True:
                            r.isShaded = True
                            r.isShadedV = True
                            r.changeColorHatch(rC.colorHatch)
                            r.changeColor(rC.color)
                            r.vColor = rC.vColor
                pc = PointCollider(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),self.willBeDivided,xLength,yLength, True)
                self.drawablesController.pointColliders.append(pc)
                if r != None:
                    r.myPointCollider = pc
                    pc.isOccupied = True
            rectsData.append(rectsRow) # append row of rectangles to rectsData since out of j loop
        self.stateManager.rectsData = rectsData
        # remove all of the vertical rectangles from drawables controller rects list
        for r1 in copyList:
            for r2 in self.drawablesController.rectangles:
                if r1 == r2:
                    self.drawablesController.rectangles.remove(r1)
        # finally remove original rect from list
        if self.drawablesController.pointColliders.count(self.myPointCollider) > 0:
            self.drawablesController.pointColliders.remove(self.myPointCollider)
        self.drawablesController.rectangles.remove(self)

    def getRectCollider(self, li, xx, yy):
        for rect in li:
            if (xx > rect.topLeftX and xx < rect.bottomRightX and yy > rect.topLeftY and yy < rect.bottomRightY):
                return rect
        return None

    def setWillBeDivided(self,willDivide):
        self.willBeDivided = willDivide

    def changeColor(self, color):
        self.color = color

    def changeColorHatch(self, color):
        self.colorHatch = color

    def setMark(self, mark):
        self.isMarked = mark

    def getMark(self):
        return self.isMarked



    def drawMark(self):
        #Left part of 'X'
        Offset = 5
        LtopXstart = self.topLeftX + Offset
        LtopYstart = self.topLeftY + Offset
        LbotXend = self.bottomRightX - Offset
        LbotYend = self.bottomRightY - Offset
        pg.draw.line(self.screen, colors.BLACK, [LtopXstart,LtopYstart], [LbotXend, LbotYend], 4)

        #Right part of 'X'
        RtopXstart = self.topRightX - Offset
        RtopYstart = self.topLeftY + Offset
        RbotXend = self.bottomLeftX + Offset
        RbotYend = self.bottomRightY - Offset
        pg.draw.line(self.screen, colors.BLACK, [RtopXstart,RtopYstart], [RbotXend, RbotYend], 4)

    def drawVLines(self, color):
        if color != colors.WHITE:
            #xAdder = (int)(self.width / 3)
            for i in range(1,20):
                #iterator = (int)(self.width * (1/i))
                partition = i / 20
                drawertopXstart = self.topLeftX * (1 - partition) + self.bottomRightX * partition
                drawertopYstart = self.topLeftY
                drawerbotXend = drawertopXstart
                drawerbotYend = self.bottomRightY
                pg.draw.line(self.screen, color, [drawertopXstart,drawertopYstart], [drawerbotXend, drawerbotYend], 1)

    def drawHLines(self, color): 
        if color != colors.WHITE:
            # yAdder = (int)(self.height / 3)
            for j in range(1,20):
                partition = j / 20
                drawertopXstart = self.topLeftX 
                drawertopYstart = self.topLeftY * (1 - partition) + self.bottomRightY * partition
                drawerbotXend = self.bottomRightX 
                drawerbotYend = drawertopYstart
                pg.draw.line(self.screen, color, [drawertopXstart,drawertopYstart], [drawerbotXend, drawerbotYend], 1) 
    
    def drawBLines(self, color):
        if color != colors.WHITE:
            for i in range(1,20):
                #iterator = (int)(self.width * (1/i))
                partition = i / 20
                drawertopXstart = self.topLeftX * (1 - partition) + self.bottomRightX * partition
                drawertopYstart = self.topLeftY
                drawerbotXend = drawertopXstart
                drawerbotYend = self.bottomRightY
                pg.draw.line(self.screen, color, [drawertopXstart,drawertopYstart], [drawerbotXend, drawerbotYend], 1)
                drawertopXstart = self.topLeftX 
                drawertopYstart = self.topLeftY * (1 - partition) + self.bottomRightY * partition
                drawerbotXend = self.bottomRightX 
                drawerbotYend = drawertopYstart
                pg.draw.line(self.screen, color, [drawertopXstart,drawertopYstart], [drawerbotXend, drawerbotYend], 2) 

    def drawVLinesSub(self, color):
        for i in range(1,20):
            #iterator = (int)(self.width * (1/i))
            partition = i / 20
            drawertopXstart = self.topLeftX * (1 - partition) + self.bottomRightX * partition
            drawertopYstart = self.topLeftY
            drawerbotXend = drawertopXstart
            drawerbotYend = self.bottomRightY
            pg.draw.line(self.screen, color, [drawertopXstart,drawertopYstart], [drawerbotXend, drawerbotYend], 1)

    def drawHLinesSub(self, color): 
        for j in range(1,20):
            partition = j / 20
            drawertopXstart = self.topLeftX 
            drawertopYstart = self.topLeftY * (1 - partition) + self.bottomRightY * partition
            drawerbotXend = self.bottomRightX 
            drawerbotYend = drawertopYstart
            pg.draw.line(self.screen, color, [drawertopXstart,drawertopYstart], [drawerbotXend, drawerbotYend], 1) 

