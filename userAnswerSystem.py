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
    self.ADD = 4
    self.operation_type = None
    if stateManager.operation_type == self.MULT:
      self.operation_type = self.MULT
    elif stateManager.operation_type == self.DIV:
      self.operation_type = self.DIV
    elif stateManager.operation_type == self.SUB:
      self.operation_type = self.SUB
    elif stateManager.operation_type == self.ADD:
      self.operation_type = self.ADD

    # for numerator and denom values
    self.numeratorValue = None
    self.denominatorValue = None
    self.wholeValue = None
    self.numberFont = pg.font.SysFont('Arial', 64)
    self.operation_font = pg.font.SysFont('Arial', 60)
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
      self.startX = int(self.WIDTH/2) - 260
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

      # for whole rect
      self.wholeRectX = self.numeratorRectX - 98
      self.wholeRectY = self.numeratorRectY + int(self.numberRectHeight / 2)
      self.wholeRect = pg.Rect(self.wholeRectX,self.wholeRectY,self.numberRectWidth,self.numberRectHeight)

      #for blinkyline
      self.blinkyYoffset = 70
      self.blinkyXOffset1 = 15
      self.blinkyXOffset2 = 60

      #for sprites
      self.spriteXOffset = 130
      self.spriteYOffset = 50

    #----------------------------------------------------
    #---------------ADDITION BUTTON PLACEMENTS-----------
    #----------------------------------------------------
    elif self.operation_type == self.ADD:
      # for "Enter Answer Here Text"
      self.enterAnswerHere_font = pg.font.SysFont('Arial', 30)
      self.startY = self.HEIGHT - 410
      self.startX = int(self.WIDTH/2) + 100
      self.feedbackTextX = int(self.WIDTH/2) + 95 
      self.feedbackTextY = self.HEIGHT - 200

      # for numerator rect
      self.numberRectWidth = 75
      self.numberRectHeight = 75
      self.numeratorRectX = int(self.WIDTH/2) - int(self.numberRectWidth/2) + 100
      self.numeratorRectY = self.HEIGHT - 390
      self.numeratorRect = pg.Rect(self.numeratorRectX,self.numeratorRectY,self.numberRectWidth,self.numberRectHeight)

      # for line dividing numer and denom
      self.divideLineY = self.numeratorRectY + self.numberRectHeight + 5
      self.divideLineStartX = self.numeratorRectX - 20
      self.divideLineEndX = self.numeratorRectX + self.numberRectWidth + 20

      # for denominator rect
      self.denomRectX = self.numeratorRectX
      self.denomRectY = self.numeratorRectY + 85
      self.denomRect = pg.Rect(self.denomRectX,self.denomRectY,self.numberRectWidth,self.numberRectHeight)

      # for whole rect
      self.wholeRectX = self.numeratorRectX - 98
      self.wholeRectY = self.numeratorRectY + int(self.numberRectHeight / 2)
      self.wholeRect = pg.Rect(self.wholeRectX,self.wholeRectY,self.numberRectWidth,self.numberRectHeight)

      #for blinkyline
      self.blinkyYoffset = 70
      self.blinkyXOffset1 = 15
      self.blinkyXOffset2 = 60

      #for sprites
      self.spriteXOffset = 120
      self.spriteYOffset = 40

    self.hasCheckedAnswer = False # for making sure answer checked exactly one time
    self.hasCorrectAnswer = False
    self.hasReducedAnswer = False
    self.checkmark = pg.image.load('assets/checkmark.png')
    self.x = pg.image.load('assets/x.png')




  def update(self,click,keyDown):

    # allow/dont allow for answer submission for multx and sub
    if (self.operation_type == self.SUB or self.operation_type == self.MULT):
      if (self.numeratorValue != None and self.denominatorValue != None):
        self.stateManager.userAnswerSystemReadyForSubmission = True
      else:
        self.stateManager.userAnswerSystemReadyForSubmission = False
    # allow/donnt allow for answer subbmission for div and add
    if (self.operation_type == self.ADD or self.operation_type == self.DIV):
      if (self.numeratorValue != None and self.denominatorValue != None or self.wholeValue != None):
        self.stateManager.userAnswerSystemReadyForSubmission = True
      else:
        self.stateManager.userAnswerSystemReadyForSubmission = False


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
      if self.operation_type == self.DIV or self.operation_type == self.ADD:
        if self.wholeRect.collidepoint(self.mX,self.mY):
          if click:
            self.selectionIndex = 2
            self.blinkClock = 0

      # tick blinking clock and reset it as needed
      if self.selectionIndex != -1:
        self.blinkClock +=1
      if self.blinkClock >= 60:
        self.blinkClock = 0
    
    elif self.stateManager.getCurrentState() == "Finished":
      if self.hasCheckedAnswer == False:
        if self.operation_type == self.MULT or self.operation_type == self.SUB:
          self.validateAnswerNoWhole(self.numeratorValue)
          self.hasCheckedAnswer = True
        elif self.operation_type == self.ADD or self.operation_type == self.DIV:
          self.validateAnswerWhole()
          self.hasCheckedAnswer = True
          


  def draw(self):


    # draw fraction if state mgr in submitting answer or finished state AND its subtraction or multx
    if (self.stateManager.getCurrentState() == "Submitting Answer" or self.stateManager.getCurrentState() == "Finished"):
      if self.stateManager.getCurrentState() == "Submitting Answer":
        pg.draw.rect(self.screen,colors.WHITE,self.numeratorRect) #draw numerator box
        pg.draw.rect(self.screen,colors.WHITE,self.denomRect) #draw denominator box
      if self.numeratorValue != None:
        draw_text(str(self.numeratorValue),self.numberFont,colors.BLACK,self.screen,self.numeratorRectX + int(self.numberRectWidth/2),self.numeratorRectY + int(self.numberRectHeight/2)) #draw numerator value
      if self.denominatorValue != None:
        draw_text(str(self.denominatorValue),self.numberFont,colors.BLACK,self.screen,self.denomRectX + int(self.numberRectWidth/2),self.denomRectY + int(self.numberRectHeight/2)) #draw denominator value
      pg.draw.line(self.screen,(0,0,0), [self.divideLineStartX, self.divideLineY], [self.divideLineEndX,self.divideLineY], 5) # draw dividing line

      # special cases for addition and div ---> draw whole rect
      if self.operation_type == self.ADD or self.operation_type == self.DIV:
        if self.stateManager.getCurrentState() == "Submitting Answer":
          pg.draw.rect(self.screen,colors.WHITE,self.wholeRect)
        if self.wholeValue != None:
          draw_text(str(self.wholeValue),self.numberFont,colors.BLACK,self.screen,self.wholeRectX + int(self.numberRectWidth/2),self.wholeRectY + int(self.numberRectHeight/2)) #draw wole value


    # only draw blinky blink if if answer is in process of submitting answer, not in finished state, no div
    if (self.stateManager.getCurrentState() == "Submitting Answer"):
      draw_text('Enter Answer Here:', self.enterAnswerHere_font, (0,0,0), self.screen, self.startX, self.startY)
      if self.selectionIndex == 0 and self.blinkClock >= 30: # numerator selected
        pg.draw.line(self.screen,(0,0,0), [self.numeratorRectX + self.blinkyXOffset1, self.numeratorRectY + self.blinkyYoffset], [self.numeratorRectX + self.blinkyXOffset2,self.numeratorRectY + self.blinkyYoffset], 5)
      elif self.selectionIndex == 1 and self.blinkClock >= 30: #denom selected
        pg.draw.line(self.screen,(0,0,0), [self.denomRectX + self.blinkyXOffset1, self.denomRectY + self.blinkyYoffset], [self.denomRectX + self.blinkyXOffset2,self.denomRectY + self.blinkyYoffset], 5)
      elif self.selectionIndex == 2 and self.blinkClock >= 30: #denom selected
        pg.draw.line(self.screen,(0,0,0), [self.wholeRectX + self.blinkyXOffset1, self.wholeRectY + self.blinkyYoffset], [self.wholeRectX + self.blinkyXOffset2,self.wholeRectY + self.blinkyYoffset], 5)

    # FOR MULTX AND SUBTRACTION:
    # if (self.operation_type == self.MULT or self.operation_type == self.SUB):
    if (self.stateManager.getCurrentState() == "Finished"):
      if self.hasCorrectAnswer == True and self.hasReducedAnswer == True:
        draw_text('Great Job!', self.enterAnswerHere_font, (0,0,0), self.screen, self.feedbackTextX, self.feedbackTextY)
        self.screen.blit(self.checkmark,(self.numeratorRectX + self.spriteXOffset,self.numeratorRectY + self.spriteYOffset))
      elif self.hasCorrectAnswer == True:
        draw_text('Correct, but can be simplified.', self.enterAnswerHere_font, (0,0,0), self.screen, self.feedbackTextX, self.feedbackTextY)
        self.screen.blit(self.checkmark,(self.numeratorRectX + self.spriteXOffset,self.numeratorRectY + self.spriteYOffset))
      else:
        draw_text('Press Restart to try again', self.enterAnswerHere_font, (0,0,0), self.screen, self.feedbackTextX, self.feedbackTextY)
        self.screen.blit(self.x,(self.numeratorRectX + self.spriteXOffset,self.numeratorRectY + self.spriteYOffset))

      if self.operation_type != self.ADD:
        draw_text('Your Visual Answer:', self.enterAnswerHere_font, (0,0,0), self.screen, int(self.WIDTH/2), 35)
      else:
        draw_text('Your Visual Answer:', self.enterAnswerHere_font, (0,0,0), self.screen, int(self.WIDTH/2) - 275, 50)


    # drawing the addition and equals sign
    if self.operation_type == self.ADD:
      draw_text('+', self.operation_font, (0,0,0), self.screen, 200 , 386)

      if self.stateManager.getCurrentState() == "Submitting Answer" or self.stateManager.getCurrentState() == "Finished":
        draw_text('=', self.operation_font, (0,0,0), self.screen, 545 , 386)
      else:
        draw_text('=', self.operation_font, (0,0,0), self.screen, 690 , 386)


  def interpretInput(self,keyDown):
    if keyDown == None:
      return
    
    elif keyDown == "Backspace": # reduce number
      if self.selectionIndex == 0: #numer selected
        if self.numeratorValue == None:
          pass
        elif self.numeratorValue < 10:
          self.numeratorValue = None
        else: # numer >= 10
          self.numeratorValue = int(self.numeratorValue / 10)
      elif self.selectionIndex == 1: #denom selected
        if self.denominatorValue == None:
          pass
        elif self.denominatorValue < 10:
          self.denominatorValue = None
        else: # denom >= 10
          self.denominatorValue = int(self.denominatorValue / 10)
      elif self.selectionIndex == 2: #whole selected
        if self.wholeValue == None:
          pass
        elif self.wholeValue < 10:
          self.wholeValue = None
        else: # whole >= 10
          self.wholeValue = int(self.wholeValue / 10)

    else: #keyDown is a number then
      if self.selectionIndex == 0: #numerator selected
        if self.numeratorValue == 0 or self.numeratorValue == None: # then numerator goes from 0->keydown
          self.numeratorValue = int(keyDown)
        elif self.numeratorValue < 10: #one digit in numerator value
          self.numeratorValue = self.numeratorValue * 10 + int(keyDown)

      elif self.selectionIndex == 1: #denom selected
        if self.denominatorValue == 0 or self.denominatorValue == None: # then denominator goes from 0->keydown
          self.denominatorValue = int(keyDown)
        elif self.denominatorValue < 10: #one digit in denom value
          self.denominatorValue = self.denominatorValue * 10 + int(keyDown)

      elif self.selectionIndex == 2: #whole selected
        if self.wholeValue == 0 or self.wholeValue == None: # then whole goes from 0->keydown
          self.wholeValue = int(keyDown)
        elif self.wholeValue < 10: #one digit in denom value
          self.wholeValue = self.wholeValue * 10 + int(keyDown)

  def validateAnswerNoWhole(self,numToUse):
    #multx validation
    numAnswer = self.problemDisplay.numeratorAnswer
    denAnswer = self.problemDisplay.denominatorAnswer
    realAnswerFraction = Fraction(numAnswer,denAnswer)

    # check for a zero answer problem
    if numAnswer == numToUse == 0:
      self.hasCorrectAnswer = True
      self.hasReducedAnswer = True
      return
    # check to see if user entered unreduced fraction, if they did-give them credit (for now)
    if numAnswer == numToUse and denAnswer == self.denominatorValue:
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
      if realAnswerFraction.numerator == numToUse and realAnswerFraction.denominator == self.denominatorValue:
        self.hasCorrectAnswer = True
        self.hasReducedAnswer = True
        return
    # 
    userAnswerFraction = Fraction(numToUse,self.denominatorValue)
    if (userAnswerFraction.canReduce()):
      while (userAnswerFraction.canReduce()):
        userAnswerFraction.finalReduce()
    if realAnswerFraction.numerator == userAnswerFraction.numerator and realAnswerFraction.denominator == userAnswerFraction.denominator:
      self.hasCorrectAnswer = True
      self.hasReducedAnswer = False
      return
  
  def validateAnswerWhole(self):
    #first handle case where user has no whole value
    if self.wholeValue == None:
      self.validateAnswerNoWhole(self.numeratorValue)
      return

    #handle case where user only enters whole value
    if self.wholeValue != None and self.numeratorValue == None and self.denominatorValue == None:
      if self.problemDisplay.numeratorAnswer / self.problemDisplay.denominatorAnswer == self.wholeValue:
        self.hasCorrectAnswer = True
        self.hasReducedAnswer = True
        return
      else: #they got it wrong
        self.hasCorrectAnswer = False
        return
    #handle case where user enters both whole # and fraction
    if self.wholeValue != None and self.numeratorValue != None and self.denominatorValue != None:
      wholeNumeratorValue = self.numeratorValue + (self.wholeValue * self.denominatorValue)
      self.validateAnswerNoWhole(wholeNumeratorValue)
      return

    