import pygame as pg
import colors
from cutmarker import CutMarker
from mouseHolder import MouseHandler
from guideline import GuideLine
from bgSquare import BgSquare
from pointCollider import PointCollider
import random

class Rectangle:
    def __init__(self, xx, yy, w, h, screen,drawablesController,isOriginalSquare):
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

        # these 4 member variables may be useful for rectangle collisions
        self.topLeftX = int(self.xPosition - self.width / 2)
        self.topLeftY = int(self.yPosition - self.height / 2)
        self.bottomRightX = int(self.xPosition + self.width / 2)
        self.bottomRightY = int(self.yPosition + self.height / 2)

        # boolean var to decide if rectangle should be subdivided when all cutmarkers removed
        self.isOriginalSquare = isOriginalSquare

        # vars used to cut up rectangles if is original square
        self.numberHorizontalRects = -1
        self.numberVerticalRects = -1

        
        # show random color to display cutting working
        if self.isOriginalSquare == True:
            self.color = colors.WHITE
        else:
            possColors = (colors.GREEN,colors.RED,colors.DARKBLUE)
            self.color = random.choice(possColors)

        # draw outer guidelines and bg square only if rectangle is original square
        if self.isOriginalSquare == True:
            GuideLine(self.topLeftX,self.topLeftY,"vertical",self,self.screen,self.drawablesController)
            GuideLine(self.topLeftX,self.topLeftY,"horizontal",self,self.screen,self.drawablesController)
            GuideLine(self.topLeftX + self.width,self.topLeftY,"vertical",self,self.screen,self.drawablesController)
            GuideLine(self.topLeftX,self.topLeftY + self.height,"horizontal",self,self.screen,self.drawablesController)
            BgSquare(self.topLeftX,self.topLeftY,self.width,self.height,self.screen,self.drawablesController)


    def update(self, mouse):

        # if conditions pass, main square is ready to be cut up so cut it
        if self.isOriginalSquare == True:
            if len(self.drawablesController.cutmarkers) == 0:
                self.cutSquare()

        #collision checking with mouse
        if self.isOriginalSquare == False:
            # mouse is holding noone and clicking, set self as being held
            if mouse.isClick == True and self.isCollidingWithPoint(mouse.mx,mouse.my) == True and mouse.whoisHeld == None:
                mouse.whoisHeld = self
                if self.myPointCollider != None:
                    self.myPointCollider.isOccupied = False
            # mouse release so remove self as being held
            if mouse.isClick == False and mouse.whoisHeld == self:
                self.putDown(mouse)
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

            
    def isCollidingWithPoint(self,xx, yy):
        if (xx > self.topLeftX and xx < self.bottomRightX and yy > self.topLeftY and yy < self.bottomRightY):
            return True
        else:
            return False

    def putDown(self,mouse):
        mouse.whoisHeld = None

        for pc in self.drawablesController.pointColliders:
            if self.isCollidingWithPoint(pc.x,pc.y) and pc.isOccupied == False:
                self.updatePosition(pc.x,pc.y)
                self.xOrigin = pc.x
                self.yOrigin = pc.y
                pc.isOccupied = True
                self.myPointCollider = pc
                return
        self.updatePosition(self.xOrigin,self.yOrigin)


    def draw(self):
        pg.draw.rect(self.screen, self.color, [self.topLeftX,self.topLeftY,self.width,self.height],0)

    def createCutMarkers(self, numberDivisionsX, numberDivisionsY):
        self.numberHorizontalRects = numberDivisionsX
        self.numberVerticalRects = numberDivisionsY

        xLength = self.width
        xSpacing = xLength / numberDivisionsX
        CutMarkers = list()
        for i in range(1,numberDivisionsX):
            cm = CutMarker(int(i * xSpacing + self.topLeftX),self.topLeftY, self.screen, self,"vertical",self.drawablesController)

        yLength = self.height
        ySpacing = yLength / numberDivisionsY
        for i in range(1,numberDivisionsY):
            cm = CutMarker(self.topLeftX,int(i * ySpacing + self.topLeftY),self.screen,self,"horizontal",self.drawablesController)

    def cutSquare(self):
        xLength = self.width / self.numberHorizontalRects
        yLength = self.height / self.numberVerticalRects
        xOffset = xLength / 2
        yOffset = yLength / 2
        for i in range(0,self.numberHorizontalRects):
            for j in range(0,self.numberVerticalRects):
                r = None
                if self.willBeDivided == True:
                    r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False)
                    self.drawablesController.rectangles.append(r)
                pc = PointCollider(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),self.willBeDivided)
                self.drawablesController.pointColliders.append(pc)
                if r != None:
                    r.myPointCollider = pc
                    pc.isOccupied = True
        self.drawablesController.rectangles.remove(self)

    def setWillBeDivided(self,willDivide):
        self.willBeDivided = willDivide
            
        

        


