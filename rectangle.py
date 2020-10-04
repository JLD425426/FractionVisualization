import pygame as pg
import colors
from cutmarker import CutMarker
from mouseHolder import MouseHandler
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
        self.xCurrent = xx
        self.yCurrent = yy
        self.rectHeld = False
        self.rectHeld2 = False

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
            possColors = (colors.GREEN,colors.RED,colors.WHITE,colors.DARKBLUE)
            self.color = random.choice(possColors)

    def update(self, click, mx, my):

        # if conditions pass, main square is ready to be cut up so cut it
        if self.isOriginalSquare == True:
            if len(self.drawablesController.cutmarkers) == 0:
                self.cutSquare()

        #collision checking with mouse
        
        if self.isOriginalSquare == False:
            self.rectisHeld(mx, my, click) 
            if self.rectHeld:
                if click != True and self.rectHeld2 == True:
                    self.xPosition = mx
                    self.yPosition = my
                    self.xCurrent = self.xPosition
                    self.yCurrent = self.yPosition
                    self.topLeftX = (self.xPosition - self.width / 2)
                    self.topLeftY = (self.yPosition - self.height / 2)                    
                    self.bottomRightX = (self.xPosition + self.width / 2)
                    self.bottomRightY = (self.yPosition + self.height / 2)

    def rectisHeld(self, mx, my, click):
        if click:
            if self.rectHeld:
                self.rectHeld2 = True
            else:
                if(mx > self.topLeftX and mx < self.bottomRightX and my > self.topLeftY and my < self.bottomRightY):
                    self.rectHeld = True
        #else:
         #   self.rectHeld = False

    def putDown(self):
        self.xPosition = self.xCurrent
        self.yPosition = self.yCurrent
        self.topLeftX = (self.xPosition - self.width / 2)
        self.topLeftY = (self.yPosition - self.height / 2)                    
        self.bottomRightX = (self.xPosition + self.width / 2)
        self.bottomRightY = (self.yPosition + self.height / 2)

    

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
                r = Rectangle(int(i * xLength + self.topLeftX + xOffset),int(j * yLength + self.topLeftY + yOffset),int(xLength),int(yLength),self.screen,self.drawablesController,False)
                self.drawablesController.rectangles.append(r)
        self.drawablesController.rectangles.remove(self)

            
        

        


