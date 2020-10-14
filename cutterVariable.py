import pygame as pg
import colors
from guideline import GuideLine

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


    def setupCutting(self, numberDivisionsX, numberDivisionsY):
        pass

    def update(self):
        if self.state == CUTTINGVERTICAL and self.myRect.isCollidingWithPoint(self.myRect.mouse.mx,self.myRect.mouse.my) and self.myRect.mouse.leftMouseReleasedThisFrame == True:
            gl = GuideLine(self.myRect.mouse.mx,self.myRect.topLeftY,"vertical",self.myRect,self.screen,self.myRect.drawablesController)
            self.guidelines.append(gl)
            self.numberHorizontalRects += 1
        elif self.state == CUTTINGHORIZONTAL and self.myRect.isCollidingWithPoint(self.myRect.mouse.mx,self.myRect.mouse.my) and self.myRect.mouse.leftMouseReleasedThisFrame == True:
            gl = GuideLine(self.myRect.topLeftX,self.myRect.mouse.my,"horizontal",self.myRect,self.screen,self.myRect.drawablesController)
            self.guidelines.append(gl)
            self.numberVerticalRects += 1

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
            cutButton = pg.Rect(self.myRect.topLeftX, self.myRect.topLeftY-100, 80, 80)
            if cutButton.collidepoint((self.myRect.mouse.mx, self.myRect.mouse.my)):
                if self.myRect.mouse.leftMouseReleasedThisFrame:
                    self.buttonPressed = True
            # Drawing menu button
            pg.draw.rect(self.screen, (8, 41, 255), cutButton)

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
            gl = GuideLine(int(i * xSpacing + self.myRect.topLeftX),self.myRect.topLeftY,"vertical",self.myRect,self.screen,self.myRect.drawablesController)

        yLength = self.myRect.height
        ySpacing = yLength / numberDivisionsY
        for i in range(1,numberDivisionsY):
            gl = GuideLine(self.myRect.topLeftX,int(i * ySpacing + self.myRect.topLeftY),"horizontal",self.myRect,self.screen,self.myRect.drawablesController)
