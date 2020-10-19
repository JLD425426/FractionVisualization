import pygame as pg
import colors
from guideline import GuideLine
from drawText import draw_text

# define cuttervariable states
CUTTINGVERTICAL = 0
CUTTINGHORIZONTAL = 1
TRYSUBDIVIDE = 2

class CutterVariable:
    def __init__(self, myRect):
        self.myRect = myRect
        self.screen = myRect.screen
        # var used to decide if myRect ready for subdivide
        self.isReadyForSubdivide = False

        self.state = CUTTINGVERTICAL

        self.numberHorizontalRects = 1
        self.numberVerticalRects = 1

        self.buttonPressed = False

        self.guidelines = list()

        self.button_font = pg.font.SysFont('Arial', 25)

        self.lastLine = None
        self.lineList = list()


    def setupCutting(self, numberDivisionsX, numberDivisionsY):
        pass

    def update(self):
        if self.state == CUTTINGVERTICAL and self.myRect.isCollidingWithPoint(self.myRect.mouse.mx,self.myRect.mouse.my) and self.myRect.mouse.leftMouseReleasedThisFrame == True:
            gl = GuideLine(self.myRect.mouse.mx,self.myRect.topLeftY,"vertical",self.myRect,self.screen,self.myRect.drawablesController, False)
            self.guidelines.append(gl)
            self.numberHorizontalRects += 1
            self.lastLine = (gl, "vertical")
            self.lineList.append(self.lastLine)

        elif self.state == CUTTINGHORIZONTAL and self.myRect.isCollidingWithPoint(self.myRect.mouse.mx,self.myRect.mouse.my) and self.myRect.mouse.leftMouseReleasedThisFrame == True:
            gl = GuideLine(self.myRect.topLeftX,self.myRect.mouse.my,"horizontal",self.myRect,self.screen,self.myRect.drawablesController, False)
            self.guidelines.append(gl)
            self.numberVerticalRects += 1
            self.lastLine = (gl, "horizontal")
            self.lineList.append(self.lastLine)

        if self.state == CUTTINGVERTICAL and self.buttonPressed == True:
            self.state = CUTTINGHORIZONTAL
            self.buttonPressed = False    
        
        if self.state == CUTTINGHORIZONTAL and self.buttonPressed == True:
            self.state = TRYSUBDIVIDE
            self.buttonPressed = False

        if self.state == TRYSUBDIVIDE:
            #first remove guidelines
            for gl in self.guidelines:
                for glInDc in self.myRect.drawablesController.guidelines:
                    if gl == glInDc:
                        self.myRect.drawablesController.guidelines.remove(glInDc)
            #next re-add guidelines in right places
            self.redrawguidelines()
            self.myRect.numberVerticalRects = self.numberVerticalRects
            self.myRect.numberHorizontalRects = self.numberHorizontalRects
            self.isReadyForSubdivide = True

    def draw(self):
        if self.state == CUTTINGVERTICAL or self.state == CUTTINGHORIZONTAL:
            cutButton = pg.Rect(self.myRect.topLeftX, self.myRect.topLeftY-100, 140, 80)
            if cutButton.collidepoint((self.myRect.mouse.mx, self.myRect.mouse.my)):
                if self.myRect.mouse.leftMouseReleasedThisFrame:
                    self.buttonPressed = True
            # Drawing menu button
            pg.draw.rect(self.screen, (8, 41, 255), cutButton)
            if self.state == CUTTINGVERTICAL:
                draw_text("Cut Horizontal", self.button_font, (0,0,0),self.screen, self.myRect.topLeftX+70, self.myRect.topLeftY-60)
            elif self.state == CUTTINGHORIZONTAL:
                draw_text("Finalize Cuts", self.button_font, (0,0,0),self.screen, self.myRect.topLeftX+70, self.myRect.topLeftY-60)

        if self.state == CUTTINGVERTICAL and self.myRect.isCollidingWithPoint(self.myRect.mouse.mx,self.myRect.mouse.my):
            pg.draw.line(self.screen,colors.DARKBLUE, [self.myRect.mouse.mx, self.myRect.topLeftY], [self.myRect.mouse.mx, self.myRect.bottomRightY], 5)
        elif self.state == CUTTINGHORIZONTAL and self.myRect.isCollidingWithPoint(self.myRect.mouse.mx,self.myRect.mouse.my):
            pg.draw.line(self.screen,colors.DARKBLUE, [self.myRect.topLeftX, self.myRect.mouse.my], [self.myRect.bottomRightX, self.myRect.mouse.my], 5)

    def redrawguidelines(self):
        numberDivisionsX = self.numberHorizontalRects
        numberDivisionsY = self.numberVerticalRects

        xLength = self.myRect.width
        xSpacing = xLength / numberDivisionsX
        for i in range(1,numberDivisionsX):
            gl = GuideLine(int(i * xSpacing + self.myRect.topLeftX),self.myRect.topLeftY,"vertical",self.myRect,self.screen,self.myRect.drawablesController, True)

        yLength = self.myRect.height
        ySpacing = yLength / numberDivisionsY
        for i in range(1,numberDivisionsY):
            gl = GuideLine(self.myRect.topLeftX,int(i * ySpacing + self.myRect.topLeftY),"horizontal",self.myRect,self.screen,self.myRect.drawablesController, True)

    def deleteLastLine(self):
        for line in self.myRect.drawablesController.guidelines:
            if line == self.lastLine[0]:
                if self.lastLine[0].isOriginal == False:
                    self.myRect.drawablesController.guidelines.remove(line)
                    if self.lastLine[1] == "horizontal":
                        self.numberVerticalRects -= 1
                    else:
                        self.numberHorizontalRects -= 1
