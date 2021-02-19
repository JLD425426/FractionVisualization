import colors
import pygame as pg
from drawText import draw_text

class UserAnswerSystem:

  def __init__(self,screen,stateManager,WIDTH, HEIGHT):
    self.screen = screen
    self.stateManager = stateManager
    self.WIDTH = WIDTH
    self.HEIGHT = HEIGHT

    # for "Enter Answer Here Text"
    self.enterAnswerHere_font = pg.font.SysFont('Arial', 36)
    self.startY = int(self.HEIGHT / 2) - 150
    self.startX = self.WIDTH - 210

    # for numerator rect
    self.numberRectWidth = 100
    self.numberRectHeight = 100
    self.numeratorRectX = self.startX - int(self.numberRectWidth/2)
    self.numeratorRectY = self.startY + 30
    self.numeratorRect = pg.Rect(self.numeratorRectX,self.numeratorRectY,self.numberRectWidth,self.numberRectHeight)

    # for line dividing numer and denom
    self.divideLineY = self.numeratorRectY + self.numberRectHeight + 8
    self.divideLineStartX = self.numeratorRectX - 20
    self.divideLineEndX = self.numeratorRectX + self.numberRectWidth + 20

    # for denominator rect
    self.denomRectX = self.numeratorRectX
    self.denomRectY = self.numeratorRectY + 118
    self.denomRect = pg.Rect(self.denomRectX,self.denomRectY,self.numberRectWidth,self.numberRectHeight)



  def update(self):
    if self.stateManager.getCurrentState() == "Submitting Answer":
      pass

  def draw(self):
    if self.stateManager.getCurrentState() == "Submitting Answer":
      draw_text('Enter Answer Here:', self.enterAnswerHere_font, (0,0,0), self.screen, self.startX, self.startY)
      pg.draw.rect(self.screen,colors.WHITE,self.numeratorRect) #draw numerator box
      pg.draw.line(self.screen,(0,0,0), [self.divideLineStartX, self.divideLineY], [self.divideLineEndX,self.divideLineY], 5) # draw dividing line
      pg.draw.rect(self.screen,colors.WHITE,self.denomRect) #draw numerator box

