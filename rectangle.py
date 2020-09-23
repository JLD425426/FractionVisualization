import pygame as pg

WHITE = ( 255, 255, 255)

class Rectangle:
    def __init__(self, xx, yy, w, h, screen):
        # the rectangles x and y position denote its top left coordinate
        self.xPosition = xx
        self.yPosition = yy
        self.width = w
        self.height = h
        self.screen = screen
        self.color = WHITE

    def draw(self):
        pg.draw.rect(self.screen, self.color, [self.xPosition,self.yPosition,self.width,self.height],0)


