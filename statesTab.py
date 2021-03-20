import pygame as pg
import colors
from drawText import draw_textLeftToRight

class StatesTab:
  def __init__(self,screen,WIDTH,HEIGHT,operation):
    self.screen = screen
    self.screenWidth = WIDTH
    self.screenHeight = HEIGHT
    self.operation = operation

    self.MULTIPLICATION = 0
    self.ADDITION = 1
    self.SUBTRACTION = 2
    self.DIVISION = 3

    self.xStart = 8
    self.yStart = 64
    self.selectionBoxWidth = 64
    self.selectionBoxHeight = 64
    self.selectionBoxMargin = 4
    
    self.selectionBoxes = list()
    if self.operation == self.MULTIPLICATION:
      yy = self.yStart
      self.selectionBoxes.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutVertical.png',"Cut Vertically"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutHorizontal.png',"Cut Horizontally"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/palleteIcon.png',"Shade Rectangles"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer"))

    self.guideTimerSet = False
    self.sBselected = None
    self.guideTimer = 0
    self.buttonClarifyText = ""
    self.buttonClarifyTextX = self.xStart + 70
    self.buttonClarifyTextY = self.yStart
    

  def update(self,mouseX,mouseY,leftMouseReleasedThisFrame):
    for sB in self.selectionBoxes:
      xx = sB.xx
      yy = sB.yy
      sB_button = pg.Rect(xx, yy, self.selectionBoxWidth, self.selectionBoxHeight)
      if sB_button.collidepoint((mouseX, mouseY)):
        if self.guideTimerSet == False and (self.sBselected == None or self.sBselected != sB):
          self.guideTimerSet = True
          self.sBselected = sB
          self.guideTimer = 0
        if self.guideTimerSet == True and self.sBselected == sB:
          self.guideTimer += 1
        if self.guideTimer >= 60:
          # print("ALARM " + str(self.guideTimer))
          self.buttonClarifyText = sB.buttonClarifyText
          self.buttonClarifyTextY = sB.yy

        if leftMouseReleasedThisFrame:
            sB.isSelected = True
            for otherB in self.selectionBoxes:
              if otherB != sB:
                otherB.isSelected = False
      elif self.sBselected == sB:
        self.guideTimerSet = False
        self.sBselected = None
        self.guideTimer = 0
        self.buttonClarifyText = ""

  def draw(self):
    for sB in self.selectionBoxes:
      sB.draw()
    if self.buttonClarifyText != "":
      draw_textLeftToRight(self.buttonClarifyText, pg.font.SysFont('Arial', 24), (0,0,0), self.screen, self.buttonClarifyTextX, self.buttonClarifyTextY + 20)



class SelectionBox:
  def __init__(self,xx,yy,stateBoxWidth, stateBoxHeight,screen,iconURL,buttonClarifyText):
    self.xx = xx
    self.yy = yy
    self.width = stateBoxWidth
    self.height = stateBoxHeight
    self.screen = screen
    self.isSelected = False
    self.iconURL = iconURL
    if self.iconURL != None:
      self.icon = pg.image.load(self.iconURL)
    self.buttonClarifyText = buttonClarifyText

  def draw(self):
    if self.isSelected == False:
      pg.draw.rect(self.screen,colors.STATESTABUNSELECTED,[self.xx,self.yy,self.width,self.height],0)
    elif self.isSelected == True:
      pg.draw.rect(self.screen,colors.STATESTABSELECTED,[self.xx,self.yy,self.width,self.height],0)
    if self.iconURL != None:
      self.screen.blit(self.icon,(self.xx + 8,self.yy + 8)) 