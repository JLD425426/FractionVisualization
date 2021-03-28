import pygame as pg
import colors
import math

class ColorPicker:
    def __init__(self, screen, screenW, screenH, mouse,statemanager,drawablesController):
        self.screen = screen
        self.SCREENWIDTH = screenW
        self.SCREENHEIGHT = screenH
        self.mouse = mouse
        self.stateManager = statemanager
        self.drawablesController = drawablesController

        self.clickRadius = 20 #number of pixels away from colorBlot for change color to happen

        self.palette = pg.image.load('assets/palette.png')

        self.brushTip = pg.image.load('assets/brushTip.png')
        self.brushTip.set_colorkey((0,0,0))

        # create list of colorblots user will select to change color
        self.colorBlots = list()
        self.colorBlots.append(ColorBlot("Red",colors.RED,135,self.SCREENHEIGHT-150))
        self.colorBlots.append(ColorBlot("Orange",colors.ORANGE,57,self.SCREENHEIGHT-140))
        self.colorBlots.append(ColorBlot("Yellow",colors.YELLOW,38,self.SCREENHEIGHT-95))
        self.colorBlots.append(ColorBlot("Blue",colors.BLUE,71,self.SCREENHEIGHT-60))
        self.colorBlots.append(ColorBlot("Green",colors.GREEN,122,self.SCREENHEIGHT-75))
        self.colorBlots.append(ColorBlot("Purple",colors.PURPLE,179,self.SCREENHEIGHT-79))

        # init starting color
        self.myColor = colors.RED
        self.changeColor(self.myColor,self.myColor,False)

        # for state mgmt of colorpicker
        self.betweenShadingAlarm = False
        self.verticalColor = None
        self.enabled = True



    def update(self):
        if self.enabled == True: #only execute if color picker is enabled
            # shading vertically1
            if self.stateManager.operation_type != self.stateManager.MULT and self.stateManager.operation_type != self.stateManager.SUB:
                if self.stateManager.getCurrentState() == "Shading Vertically":
                    self.checkForColorChange()
                    self.betweenShadingAlarm = True
                
                # alarm between shading types so that this will if will execute exactly once
                if self.stateManager.getCurrentState() != "Shading Vertically" and self.betweenShadingAlarm == True:
                    self.verticalColor = self.myColor
                    self.primeHorizontalColors()
                    self.changeColor(self.myColor,self.colorBlots[0].color,True)
                    self.betweenShadingAlarm = False

                # shading horizontally
                if self.stateManager.getCurrentState() == "Shading Horizontally":
                    self.checkForColorChange()

            if self.stateManager.operation_type == self.stateManager.SUB:
                if self.stateManager.getCurrentState() == "Shading":
                    self.checkForColorChange()
                    self.betweenShadingAlarm = True
                    
            else: # For multx
                if self.stateManager.hasCutVerticallyFirst == True:
                    if self.stateManager.getCurrentState() == "Shading Vertically":
                        self.checkForColorChange()
                        self.betweenShadingAlarm = True
                    
                    # alarm between shading types so that this will if will execute exactly once
                    if self.stateManager.getCurrentState() != "Shading Vertically" and self.betweenShadingAlarm == True:
                        self.verticalColor = self.myColor
                        self.primeHorizontalColors()
                        self.changeColor(self.myColor,self.colorBlots[0].color,True)
                        self.betweenShadingAlarm = False

                    # shading horizontally
                    if self.stateManager.getCurrentState() == "Shading Horizontally":
                        self.checkForColorChange()

                else:
                    if self.stateManager.getCurrentState() == "Shading Horizontally":
                        self.checkForColorChange()
                        self.betweenShadingAlarm = True
                    
                    # alarm between shading types so that this will if will execute exactly once
                    if self.stateManager.getCurrentState() != "Shading Horizontally" and self.betweenShadingAlarm == True:
                        self.verticalColor = self.myColor
                        self.primeHorizontalColors()
                        self.changeColor(self.myColor,self.colorBlots[0].color,True)
                        self.betweenShadingAlarm = False

                    # shading horizontally
                    if self.stateManager.getCurrentState() == "Shading Vertically":
                        self.checkForColorChange()

        


    def draw(self):

        if self.enabled == True: # only draw if enabled
            if self.stateManager.getCurrentState() == "Shading Horizontally" or self.stateManager.getCurrentState() == "Shading Vertically" or self.stateManager.getCurrentState() == "Shading":
                self.screen.blit(self.brushTip,(10,self.SCREENHEIGHT-225)) # draw brushtip

                self.screen.blit(self.palette,(10,self.SCREENHEIGHT-225)) # draw palette base
                
                for cB in self.colorBlots: # draw all selectable color blots
                    self.screen.blit(cB.spr,(cB.x,cB.y))

    def checkForColorChange(self):
        # loops thru colorBlots and if close to mouse and click->set new color based on colorblot
        for cB in self.colorBlots:
            distToMouse = math.sqrt((cB.centerX - self.mouse.mx)**2 + (cB.centerY - self.mouse.my)**2)
            if distToMouse < self.clickRadius and self.mouse.leftMouseReleasedThisFrame:
                self.changeColor(self.myColor,cB.color,False)
                break

    def changeColor(self, oldColor,newColor,isPhaseChange):
        #loop through brush image pixels, if not black->make it new color
        for x in range(self.brushTip.get_width()):
            for y in range(self.brushTip.get_height()):
                color = self.brushTip.get_at((x,y))
                if color != (0, 0, 0, 255):
                    self.brushTip.set_at((x,y),(newColor[2],newColor[1],newColor[0],0))
        if isPhaseChange == False:
            for rect in self.drawablesController.rectangles:
                if self.stateManager.operation_type == self.stateManager.MULT or self.stateManager.operation_type == self.stateManager.SUB:
                    if rect.colorHatch == oldColor:
                        rect.colorHatch = newColor
                elif self.stateManager.operation_type == self.stateManager.DIV:
                    if rect.color == oldColor:
                        pass
                        # We don't want all other rect colors redrawn in this case, but we also want
                        #   all sub rects in the same rectangle to be the same color
                        # rect.color = newColor
        self.myColor = newColor
            

    # only allow 2 colorblots in colorblot list depending on vertical color
    def primeHorizontalColors(self):
        self.colorBlots.clear()
        xPos1 = 57
        yPos1 = self.SCREENHEIGHT-140
        xPos2 = 71
        yPos2 = self.SCREENHEIGHT-60
        if self.verticalColor == colors.RED:
            self.colorBlots.append(ColorBlot("Blue",colors.BLUE,xPos1,yPos1))
            self.colorBlots.append(ColorBlot("Yellow",colors.YELLOW,xPos2,yPos2))
        elif self.verticalColor == colors.ORANGE:
            self.colorBlots.append(ColorBlot("Purple",colors.PURPLE,xPos1,yPos1))
            self.colorBlots.append(ColorBlot("Green",colors.GREEN,xPos2,yPos2))
        elif self.verticalColor == colors.YELLOW:
            self.colorBlots.append(ColorBlot("Red",colors.RED,xPos1,yPos1))
            self.colorBlots.append(ColorBlot("Blue",colors.BLUE,xPos2,yPos2))
        elif self.verticalColor == colors.GREEN:
            self.colorBlots.append(ColorBlot("Orange",colors.ORANGE,xPos1,yPos1))
            self.colorBlots.append(ColorBlot("Purple",colors.PURPLE,xPos2,yPos2))
        elif self.verticalColor == colors.BLUE:
            self.colorBlots.append(ColorBlot("Red",colors.RED,xPos1,yPos1))
            self.colorBlots.append(ColorBlot("Yellow",colors.YELLOW,xPos2,yPos2))
        elif self.verticalColor == colors.PURPLE:
            self.colorBlots.append(ColorBlot("Orange",colors.ORANGE,xPos1,yPos1))
            self.colorBlots.append(ColorBlot("Green",colors.GREEN,xPos2,yPos2))

    def getBlendedColor(self):
        if self.verticalColor == colors.RED:
            if self.myColor == colors.BLUE: # red + blue -> purple
                return colors.PURPLE
            else: 
                return colors.ORANGE # red + yellow -> oj
        elif self.verticalColor == colors.ORANGE:
            if self.myColor == colors.PURPLE: # orange + purple -> red
                return colors.RED
            else: 
                return colors.YELLOW # orange + green -> yellow
        elif self.verticalColor == colors.YELLOW:
            if self.myColor == colors.RED:
                return colors.ORANGE # yellow + red -> oj
            else: 
                return colors.GREEN # yellow + blue -> green
        elif self.verticalColor == colors.GREEN:
            if self.myColor == colors.ORANGE:
                return colors.YELLOW # green + oj -> yellow
            else: 
                return colors.BLUE # green + purple -> blue
        elif self.verticalColor == colors.BLUE:
            if self.myColor == colors.YELLOW: # blue + yellow -> green
                return colors.GREEN
            else: 
                return colors.PURPLE # blue + red -> purple 
        elif self.verticalColor == colors.PURPLE:
            if self.myColor == colors.ORANGE:
                return colors.RED # purple + oj -> red
            else: 
                return colors.BLUE # purple + green -> blue


class ColorBlot:
    def __init__(self,name,col,x,y):
        self.spr = pg.image.load('assets/colorBlot.png')
        self.spr.set_colorkey((0,0,0)) # makes it so black pixels arent drawn
        self.color = col
        self.x = x
        self.y = y
        self.centerX = self.x + 20 # + 20 b/c image is 40 pixels wide
        self.centerY = self.y + 15 # + 15 b/c image is 30 pixels tall
        self.name = name

        # loop thru image pixels and if pixel isnt black make it appropriate color
        for x in range(self.spr.get_width()):
            for y in range(self.spr.get_height()):
                color = self.spr.get_at((x,y))
                if color != (0, 0, 0, 255):
                    self.spr.set_at((x,y),(self.color[2],self.color[1],self.color[0],0))




