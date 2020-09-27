import pygame as pg
import colors
import math

class CutMarker:
    def __init__(self, xx, yy, rad, screen, myRect):
        # the rectangles x and y position denote its top left coordinate
        self.xPosition = xx
        self.yPosition = yy
        self.radius = rad
        self.screen = screen
        self.color = colors.DARKBLUE
        self.myRect = myRect
        self.isTouchingMouse = False

    def update(self):
        mousePos = pg.mouse.get_pos()
        distToMouse = math.sqrt((self.xPosition - mousePos[0])**2 + (self.yPosition-mousePos[1])**2)
        if distToMouse < self.radius:
            self.isTouchingMouse = True
        else:
            self.isTouchingMouse = False



    def draw(self):
        pg.draw.circle(self.screen, self.color, (self.xPosition,self.yPosition), self.radius)
        if (self.isTouchingMouse == True):
            pg.draw.line(self.screen,colors.DARKBLUE, [self.xPosition, self.yPosition], [self.xPosition, self.yPosition + self.myRect.height], 5)