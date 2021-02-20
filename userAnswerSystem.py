import colors
import pygame as pg
from drawText import draw_text
from fractionHandler import Fraction

class UserAnswerSystem:

  def __init__(self,screen,stateManager,WIDTH, HEIGHT,problemDisplay):
    self.screen = screen
    self.stateManager = stateManager
    self.WIDTH = WIDTH
    self.HEIGHT = HEIGHT
    self.problemDisplay = problemDisplay

    # set which operation is happening here
    self.MULT = 1
    self.DIV = 2
    self.SUB = 3
    self.operation_type = None
    if stateManager.operation_type == self.MULT:
      self.operation_type = self.MULT
    elif stateManager.operation_type == self.DIV:
      self.operation_type = self.DIV
    elif stateManager.operation_type == self.SUB:
      self.operation_type = self.SUB

    # for numerator and denom values
    self.numeratorValue = 0
    self.denominatorValue = 0
    self.numberFont = pg.font.SysFont('Arial', 64)
    self.selectionIndex = -1 # 0-> numerator # 1-> denom

    # for user input
    self.mX = 0     
    self.mY = 0

    #for blinking
    self.blinkClock = 0      

    #-----------------------------------------------------
    #---------------MULTX/SUB BUTTON PLACEMENTS-----------
    #-----------------------------------------------------
    if self.operation_type == self.MULT or self.operation_type == self.SUB:
      # for "Enter Answer Here Text"
      self.enterAnswerHere_font = pg.font.SysFont('Arial', 36)
      self.startY = int(self.HEIGHT / 2) - 150
      self.startX = self.WIDTH - 210
      self.feedbackTextX = self.startX
      self.feedbackTextY = self.startY

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

      #for blinkyline
      self.blinkyYoffset = 80
      self.blinkyXOffset1 = 20
      self.blinkyXOffset2 = 80

      #for sprites
      self.spriteXOffset = 150
      self.spriteYOffset = 80
    
    #----------------------------------------------------
    #---------------DIVISION BUTTON PLACEMENTS-----------
    #----------------------------------------------------
    elif self.operation_type == self.DIV:
      # for "Enter Answer Here Text"
      self.enterAnswerHere_font = pg.font.SysFont('Arial', 30)
      self.startY = self.HEIGHT - 150
      self.startX = int(self.WIDTH/2) - 180
      self.feedbackTextX = int(self.WIDTH/2)
      self.feedbackTextY = self.HEIGHT - 30

      # for numerator rect
      self.numberRectWidth = 75
      self.numberRectHeight = 75
      self.numeratorRectX = int(self.WIDTH/2) - int(self.numberRectWidth/2)
      self.numeratorRectY = self.HEIGHT - 225
      self.numeratorRect = pg.Rect(self.numeratorRectX,self.numeratorRectY,self.numberRectWidth,self.numberRectHeight)

      # for line dividing numer and denom
      self.divideLineY = self.numeratorRectY + self.numberRectHeight + 5
      self.divideLineStartX = self.numeratorRectX - 20
      self.divideLineEndX = self.numeratorRectX + self.numberRectWidth + 20

      # for denominator rect
      self.denomRectX = self.numeratorRectX
      self.denomRectY = self.numeratorRectY + 85
      self.denomRect = pg.Rect(self.denomRectX,self.denomRectY,self.numberRectWidth,self.numberRectHeight)

      #for blinkyline
      self.blinkyYoffset = 70
      self.blinkyXOffset1 = 15
      self.blinkyXOffset2 = 60

      #for sprites
      self.spriteXOffset = 130
      self.spriteYOffset = 50

    self.hasCheckedAnswer = False # for making sure answer checked exactly one time
    self.hasCorrectAnswer = False
    self.hasReducedAnswer = False
    self.checkmark = pg.image.load('assets/checkmark.png')
    self.x = pg.image.load('assets/x.png')




  def update(self,click,keyDown):

    if self.stateManager.getCurrentState() == "Submitting Answer":
      self.mX, self.mY = pg.mouse.get_pos()   # Get mouse position 

      self.interpretInput(keyDown)

      if self.numeratorRect.collidepoint(self.mX,self.mY):
        if click:
          self.selectionIndex = 0
          self.blinkClock = 0
      if self.denomRect.collidepoint(self.mX,self.mY):
        if click:
          self.selectionIndex = 1
          self.blinkClock = 0

      # tick blinking clock and reset it as needed
      if self.selectionIndex != -1:
        self.blinkClock +=1
      if self.blinkClock >= 60:
        self.blinkClock = 0
    
    elif self.stateManager.getCurrentState() == "Finished":
      if self.hasCheckedAnswer == False:
        self.validateAnswer()
        self.hasCheckedAnswer = True


  def draw(self):

    # draw fraction if state mgr in submitting answer or finished state AND its subtraction or multx
    if (self.stateManager.getCurrentState() == "Submitting Answer" or self.stateManager.getCurrentState() == "Finished"):
      pg.draw.rect(self.screen,colors.WHITE,self.numeratorRect) #draw numerator box
      pg.draw.rect(self.screen,colors.WHITE,self.denomRect) #draw denominator box
      draw_text(str(self.numeratorValue),self.numberFont,colors.BLACK,self.screen,self.numeratorRectX + int(self.numberRectWidth/2),self.numeratorRectY + int(self.numberRectHeight/2)) #draw numerator value
      draw_text(str(self.denominatorValue),self.numberFont,colors.BLACK,self.screen,self.denomRectX + int(self.numberRectWidth/2),self.denomRectY + int(self.numberRectHeight/2)) #draw denominator value
      pg.draw.line(self.screen,(0,0,0), [self.divideLineStartX, self.divideLineY], [self.divideLineEndX,self.divideLineY], 5) # draw dividing line

    # only draw blinky blink if if answer is in process of submitting answer, not in finished state, no div
    if (self.stateManager.getCurrentState() == "Submitting Answer"):
      draw_text('Enter Answer Here:', self.enterAnswerHere_font, (0,0,0), self.screen, self.startX, self.startY)
      if self.selectionIndex == 0 and self.blinkClock >= 30: # numerator selected
        pg.draw.line(self.screen,(0,0,0), [self.numeratorRectX + self.blinkyXOffset1, self.numeratorRectY + self.blinkyYoffset], [self.numeratorRectX + self.blinkyXOffset2,self.numeratorRectY + self.blinkyYoffset], 5)
      elif self.selectionIndex == 1 and self.blinkClock >= 30: #denom selected
        pg.draw.line(self.screen,(0,0,0), [self.denomRectX + self.blinkyXOffset1, self.denomRectY + self.blinkyYoffset], [self.denomRectX + self.blinkyXOffset2,self.denomRectY + self.blinkyYoffset], 5)

    # FOR MULTX AND SUBTRACTION:
    # if (self.operation_type == self.MULT or self.operation_type == self.SUB):
    if (self.stateManager.getCurrentState() == "Finished"):
      if self.hasCorrectAnswer == True and self.hasReducedAnswer == True:
        draw_text('Great Job!', self.enterAnswerHere_font, (0,0,0), self.screen, self.feedbackTextX, self.feedbackTextY)
        self.screen.blit(self.checkmark,(self.numeratorRectX + self.spriteXOffset,self.numeratorRectY + self.spriteYOffset))
      elif self.hasCorrectAnswer == True:
        draw_text('Correct, but can be reduced.', self.enterAnswerHere_font, (0,0,0), self.screen, self.feedbackTextX, self.feedbackTextY)
        self.screen.blit(self.checkmark,(self.numeratorRectX + self.spriteXOffset,self.numeratorRectY + self.spriteYOffset))
      else:
        draw_text('Try Again', self.enterAnswerHere_font, (0,0,0), self.screen, self.feedbackTextX, self.feedbackTextY)
        self.screen.blit(self.x,(self.numeratorRectX + self.spriteXOffset,self.numeratorRectY + self.spriteYOffset))
      draw_text('Your Visual Answer:', self.enterAnswerHere_font, (0,0,0), self.screen, int(self.WIDTH/2), 35)


  def interpretInput(self,keyDown):
    if keyDown == None:
      return
    elif keyDown == "Backspace": # reduce number
      if self.selectionIndex == 0: #numer selected
        if self.numeratorValue < 10:
          self.numeratorValue = 0
        else: # numer >= 10
          self.numeratorValue = int(self.numeratorValue / 10)
      elif self.selectionIndex == 1: #denom selected
        if self.denominatorValue < 10:
          self.denominatorValue = 0
        else: # denom >= 10
          self.denominatorValue = int(self.denominatorValue / 10)

    else: #keyDown is a number then
      if self.selectionIndex == 0: #numerator selected
        if self.numeratorValue == 0: # then numerator goes from 0->keydown
          self.numeratorValue = int(keyDown)
        elif self.numeratorValue < 10: #one digit in numerator value
          self.numeratorValue = self.numeratorValue * 10 + int(keyDown)

      elif self.selectionIndex == 1: #denom selected
        if self.denominatorValue == 0: # then denominator goes from 0->keydown
          self.denominatorValue = int(keyDown)
        elif self.denominatorValue < 10: #one digit in denom value
          self.denominatorValue = self.denominatorValue * 10 + int(keyDown)

  def validateAnswer(self):
    #multx validation
    numAnswer = self.problemDisplay.numeratorAnswer
    denAnswer = self.problemDisplay.denominatorAnswer
    realAnswerFraction = Fraction(numAnswer,denAnswer)
    # print("num answer: " + str(numAnswer))
    # print("den answer: " + str(denAnswer))

    # testF = Fraction(numAnswer,denAnswer)
    # print("numerator unred: " + str(testF.numerator) + " denom unred: " + str(testF.denominator))
    # while(testF.canReduce()):
    #   testF.finalReduce()
    # print("numerator red: " + str(testF.numerator) + " denom red: " + str(testF.denominator))

    # check for a zero answer problem
    if numAnswer == self.numeratorValue == 0:
      self.hasCorrectAnswer = True
      self.hasReducedAnswer = True
      return
    # check to see if user entered unreduced fraction, if they did-give them credit (for now)
    if numAnswer == self.numeratorValue and denAnswer == self.denominatorValue:
      self.hasCorrectAnswer = True
      if realAnswerFraction.canReduce() == False:
        self.hasReducedAnswer = True
      else:
        self.hasReducedAnswer = False
      return
    # check if real answer can be reduced, and if so, reduce it then check against user answer to see if they got correct
    # reduced answer
    if realAnswerFraction.canReduce():
      while (realAnswerFraction.canReduce()):
        realAnswerFraction .finalReduce()
      if realAnswerFraction.numerator == self.numeratorValue and realAnswerFraction.denominator == self.denominatorValue:
        self.hasCorrectAnswer = True
        self.hasReducedAnswer = True
        return
    