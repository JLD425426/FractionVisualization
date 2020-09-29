import colors
import pygame as pg

class GuideLine():
    def __init__(self, xStart, yStart, _type, myRect, screen, drawablesController):
        self.xStart = xStart
        self.yStart = yStart
        self.type = _type
        self.myRect = myRect
        self.screen = screen
        self.drawablesController = drawablesController
        self.drawablesController.guidelines.append(self)

    def draw(self):
        if self.type == "vertical":
            pg.draw.line(self.screen,colors.BLACK, [self.xStart, self.yStart], [self.xStart, self.yStart + self.myRect.height], 5)
        elif self.type == "horizontal":
            pg.draw.line(self.screen,colors.BLACK, [self.xStart, self.yStart], [self.xStart + self.myRect.width, self.yStart], 5)
