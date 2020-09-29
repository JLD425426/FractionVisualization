import pygame as pg
import colors
from cutmarker import CutMarker

class Rectangle:
    def __init__(self, xx, yy, w, h, screen):
        # the xPosition and yPosition refer to the middle point of the rectangle
        self.xPosition = xx
        self.yPosition = yy
        self.width = w
        self.height = h
        self.screen = screen

        # these 4 member variables may be useful for rectangle collisions
        self.topLeftX = int(self.xPosition - self.width / 2)
        self.topLeftY = int(self.yPosition - self.height / 2)
        self.bottomRightX = int(self.xPosition + self.width / 2)
        self.bottomRightY = int(self.yPosition + self.height / 2)

        self.color = colors.WHITE

    def draw(self):
        # pg.draw.rect(self.screen, self.color, [self.xPosition,self.yPosition,self.width,self.height],0)
        pg.draw.rect(self.screen, self.color, [self.topLeftX,self.topLeftY,self.width,self.height],0)

    def createCutMarkers(self, numberDivisionsX, numberDivisionsY):
        xLength = self.width
        xSpacing = xLength / numberDivisionsX
        CutMarkers = list()
        for i in range(1,numberDivisionsX):
            CutMarkers.append(CutMarker(int(i * xSpacing + self.topLeftX),self.topLeftY, self.screen, self,"vertical"))

        yLength = self.height
        ySpacing = yLength / numberDivisionsY
        for i in range(1,numberDivisionsY):
            CutMarkers.append(CutMarker(self.topLeftX,int(i * ySpacing + self.topLeftY),self.screen,self,"horizontal"))
        return CutMarkers
            
        

        


