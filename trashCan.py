import pygame as pg
from rectangle import Rectangle
import math
import colors
from resourcePath import resource_path

class TrashCan:
    def __init__(self, screen, screenW, screenH, mouse, statemanager, drawablesController):
        self.screen = screen
        self.SCREENWIDTH = screenW
        self.SCREENHEIGHT = screenH
        self.mouse = mouse
        self.stateManager = statemanager
        self.drawablesController = drawablesController
        
        self.trash = pg.image.load(resource_path('assets/trashbin.png'))
        self.trash.set_colorkey((255,255,255))
        #self.hide = pg.image.load('assets/stealth.png')
        #self.hide.set_colorkey((255,255,255))
        #self.bin.set_colorkey((0,0,0))
        self.enabled = False

    def setEnable(self, value):
        self.enabled = value

    def update(self):
        if self.stateManager.getCurrentState() == "Moving" or self.stateManager.getCurrentState() == "Finished":
            self.setEnable(True)

    def draw(self):
        if self.enabled == True:
            if self.stateManager.getCurrentState() == "Moving" or self.stateManager.getCurrentState() == "Finished":
                #self.screen.blit(self.hide, (528,self.SCREENHEIGHT-200))
                self.screen.blit(self.trash,(2,self.SCREENHEIGHT-200))
                pg.draw.rect(self.screen, colors.BGCOLOR, [self.SCREENWIDTH-172,self.SCREENHEIGHT-200,250,250],0)