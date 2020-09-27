import pygame as pg
import colors
from cutmarker import CutMarker

class Rectangle:
    def __init__(self, xx, yy, w, h, screen):
        # the rectangles x and y position denote its top left coordinate
        self.xPosition = xx
        self.yPosition = yy
        self.width = w
        self.height = h
        self.screen = screen
        self.color = colors.WHITE

    def draw(self):
        pg.draw.rect(self.screen, self.color, [self.xPosition,self.yPosition,self.width,self.height],0)

    def createCutMarkers(self, numberDivisions):
        xLength = self.width
        xSpacing = xLength / numberDivisions
        CutMarkers = list()
        for i in range(1,numberDivisions):
            CutMarkers.append(CutMarker(int(i * xSpacing + self.xPosition),self.yPosition, 7, self.screen, self,))
        return CutMarkers
            
        

        


