import pygame as pg
import colors
import math

from guideline import GuideLine

class CutMarker:
    def __init__(self, xx, yy, screen, myRect,_type,drawablesController):
        # the rectangles x and y position denote its top left coordinate
        self.xPosition = xx
        self.yPosition = yy
        self.radius = 8
        self.screen = screen
        self.color = colors.DARKBLUE
        self.myRect = myRect
        self.isTouchingMouse = False
        self.type = _type
        self.drawablesController = drawablesController
        self.drawablesController.cutmarkers.append(self)

    def update(self, isClick):
        # decide if close enough to mouse to draw guiding line or not
        mousePos = pg.mouse.get_pos()
        distToMouse = math.sqrt((self.xPosition - mousePos[0])**2 + (self.yPosition-mousePos[1])**2)
        if distToMouse < self.radius:
            self.isTouchingMouse = True
        else:
            self.isTouchingMouse = False

        if distToMouse < self.radius and isClick == True:
            gl = GuideLine(self.xPosition,self.yPosition,self.type,self.myRect,self.screen,self.drawablesController)
            self.drawablesController.cutmarkers.remove(self)


    def draw(self):
        pg.draw.circle(self.screen, self.color, (self.xPosition,self.yPosition), self.radius)
        if (self.isTouchingMouse == True):
            if self.type == "vertical":
                pg.draw.line(self.screen,colors.DARKBLUE, [self.xPosition, self.yPosition], [self.xPosition, self.yPosition + self.myRect.height], 5)
            elif self.type == "horizontal":
                pg.draw.line(self.screen,colors.DARKBLUE, [self.xPosition, self.yPosition], [self.xPosition + self.myRect.width, self.yPosition], 5)