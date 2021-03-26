import pygame as pg
import colors
from drawText import draw_textLeftToRight

class StatesTabMult:
  def __init__(self,screen,WIDTH,HEIGHT,operation):
    self.screen = screen
    self.screenWidth = WIDTH
    self.screenHeight = HEIGHT
    self.operation = operation

    self.MULTIPLICATION = 0
    self.ADDITION = 1
    self.SUBTRACTION = 2
    self.DIVISION = 3
    self.TEST = 4

    self.xStart = 8
    self.yStart = 64
    self.selectionBoxWidth = 64
    self.selectionBoxHeight = 64
    self.selectionBoxMargin = 4

    # THIS IS VARIABLE USED TO HANDLE MULTIPLE DIFFERENT STATE TAB UNITS FOR 1 OPERATION,
    # id = 0 -> first state tab, id = 1 -> second state tab, ect...
    self.selectionBoxGroupListIndex = 0
    
    #List of list of selection boxes
    self.selectionBoxesGroupList = list()
    #Create the list of selection boxes that each represent 1 state, SelectionBox class at end of file
    self.selectionBoxes0 = list()
    self.selectionBoxes1 = list()
    self.selectionBoxes2 = list()
    self.selectionBoxes3 = list()
    self.selectionBoxes4 = list()

    if self.operation == self.TEST:
      yy = self.yStart
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutVertical.png',"Cut Vertically","Cutting Vertically"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutHorizontal.png',"Cut Horizontally","Cutting Horizontally"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/palleteIcon.png',"Shade Rectangles","Shading"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer","Submitting Answer"))
      # finally append to master list
      self.selectionBoxesGroupList.append(self.selectionBoxes0) # DONT FORGET TO APPEND LIST TO LIST OF LISTS

    #MULTIPLICATION CASE
    elif self.operation == self.MULTIPLICATION:
      #CREATE LIST OF SELECTION BOXES0 FOR MULTX
      self.xStart = 790
      self.yStart = 256
      yy = self.yStart
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutVertical.png',"Cut Vertically","Cutting Vertically"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutHorizontal.png',"Cut Horizontally","Cutting Horizontally"))
      # yy += self.selectionBoxHeight + self.selectionBoxMargin
      # self.selectionBoxes.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/palleteIcon.png',"Shade Rectangles","Shading"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer","Submitting Answer"))

      self.selectionBoxesGroupList.append(self.selectionBoxes0) # DONT FORGET TO APPEND LIST TO LIST OF LISTS
    
      #CREATE LIST OF SELECTIONBOXES1 FOR MULTX
      self.xStart = 790
      self.yStart = 256
      yy = self.yStart
      self.selectionBoxes1.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/palleteIcon.png',"Shade Rectangles","Shading Vertically"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes1.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer","Submitting Answer"))

      self.selectionBoxesGroupList.append(self.selectionBoxes1) # DONT FORGET TO APPEND LIST TO LIST OF LISTS

      #CREATE LIST OF SELECTIONBOXES2 FOR MULTX
      self.xStart = 790
      self.yStart = 256
      yy = self.yStart
      self.selectionBoxes2.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutHorizontal.png',"Cut Horizontally","Cutting Horizontally"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes2.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer","Submitting Answer"))

      self.selectionBoxesGroupList.append(self.selectionBoxes2) # DONT FORGET TO APPEND LIST TO LIST OF LISTS

      #CREATE LIST OF SELECTIONBOXES3 FOR MULTX
      self.xStart = 790
      self.yStart = 256
      yy = self.yStart
      self.selectionBoxes3.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/palleteIcon.png',"Shade Rectangles","Shading Horizontally"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes3.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer","Submitting Answer"))

      self.selectionBoxesGroupList.append(self.selectionBoxes3) # DONT FORGET TO APPEND LIST TO LIST OF LISTS

      
      #CREATE LIST OF SELECTIONBOXES4 FOR MULTX, User coming from shading horizontally, still needs to cut vertically
      self.xStart = 790
      self.yStart = 256
      yy = self.yStart
      self.selectionBoxes0.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/cutVertical.png',"Cut Vertically","Cutting Vertically"))
      yy += self.selectionBoxHeight + self.selectionBoxMargin
      self.selectionBoxes4.append(SelectionBox(self.xStart,yy,self.selectionBoxWidth,self.selectionBoxHeight,screen,'assets/submitAnswerIcon.png',"Submit Answer","Submitting Answer"))

      self.selectionBoxesGroupList.append(self.selectionBoxes4) # DONT FORGET TO APPEND LIST TO LIST OF LISTS



    # These next few lines are for setting up guidetext if user hovers over icon for long enough so as to clarify what
    # button does
    self.guideTimerSet = False
    self.sBselected = None
    self.guideTimer = 0
    self.buttonClarifyText = ""
    self.buttonClarifyTextX = self.xStart + 70
    self.buttonClarifyTextY = self.yStart

    #This is what state manager pulls from to get state
    self.state = None
    #This will get set by state manager as true when state manager is done and interface will dissapear
    self.isStateManagerDone = False
    

  def update(self,mouseX,mouseY,leftMouseReleasedThisFrame):
    if self.isStateManagerDone == False:
      #Manager user input on selection boxes, get what state they are in
      currentList = self.selectionBoxesGroupList[self.selectionBoxGroupListIndex]
      for sB in currentList:
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
          #they hover and click on selection box so its the new state
          if leftMouseReleasedThisFrame:
              self.state = sB.state
              sB.isSelected = True
              for otherB in currentList:
                if otherB != sB:
                  otherB.isSelected = False
        elif self.sBselected == sB:
          self.guideTimerSet = False
          self.sBselected = None
          self.guideTimer = 0
          self.buttonClarifyText = ""

  def clearSelected(self):
    for sbG in self.selectionBoxesGroupList:
      for sb in sbG:
        sb.isSelected = False
        self.state = "Waiting"

  def draw(self):
    
    if self.isStateManagerDone == False:
      currentList = self.selectionBoxesGroupList[self.selectionBoxGroupListIndex]
      for sB in currentList:
        sB.draw()
      if self.buttonClarifyText != "":
        draw_textLeftToRight(self.buttonClarifyText, pg.font.SysFont('Arial', 24), (0,0,0), self.screen, self.buttonClarifyTextX, self.buttonClarifyTextY + 20)



class SelectionBox:
  def __init__(self,xx,yy,stateBoxWidth, stateBoxHeight,screen,iconURL,buttonClarifyText,state):
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
    self.state = state

  def draw(self):
    if self.isSelected == False:
      pg.draw.rect(self.screen,colors.STATESTABUNSELECTED,[self.xx,self.yy,self.width,self.height],0)
    elif self.isSelected == True:
      pg.draw.rect(self.screen,colors.STATESTABSELECTED,[self.xx,self.yy,self.width,self.height],0)
    if self.iconURL != None:
      self.screen.blit(self.icon,(self.xx + 8,self.yy + 8)) 