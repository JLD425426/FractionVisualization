import pygame as pg
import colors
from cutmarker import CutMarker

class Rectangle:
    def __init__(self, xx, yy, w, h, screen):
        # the rectangles x and y position denote its top left coordinate
        # the rectangles x + width and y + height position denote its top right coordinate
        self.xPosition = xx
        self.yPosition = yy
        self.width = w
        self.height = h
        self.screen = screen
        self.color = colors.WHITE

    def draw(self):
        pg.draw.rect(self.screen, self.color, [self.xPosition,self.yPosition,self.width,self.height],0)

    def createCutMarkers(self, numberDivisionsX, numberDivisionsY):
        xLength = self.width
        xSpacing = xLength / numberDivisionsX
        CutMarkers = list()
        for i in range(1,numberDivisionsX):
            CutMarkers.append(CutMarker(int(i * xSpacing + self.xPosition),self.yPosition, self.screen, self,"vertical"))

        yLength = self.height
        ySpacing = yLength / numberDivisionsY
        for i in range(1,numberDivisionsY):
            CutMarkers.append(CutMarker(self.xPosition,int(i * ySpacing + self.yPosition),self.screen,self,"horizontal"))
        return CutMarkers
            
        

        


