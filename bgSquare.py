import colors
import pygame as pg

class BgSquare:
    def __init__(self, topLeftX, topLeftY, width, height, screen, drawablesController):
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.width = width
        self.height = height
        self.screen = screen
        self.drawablesController = drawablesController
        self.color = colors.LIGHTGREY
        self.drawablesController.bgSquares.append(self)

    def draw(self):
        pg.draw.rect(self.screen, self.color, [self.topLeftX,self.topLeftY,self.width,self.height],0)
