import pygame 


class MouseHandler:
    def __init__(self):
        # make a class to interact with rectangles and the screen
        self.mx , self.my = pygame.mouse.get_pos()
        self.isClick = False
        self.isHeld = False
        self.manyDrag = 0
        self.whoisHeld = None
    
    def setClick(self, check):
        self.isClick = check
    
    def setHeld(self, check):
        self.isHeld = check

    def getX(self):
        return self.mx

    def getY(self):
        return self.my     

    def getDrag(self):
        return self.manyDrag   

    def isClicked(self):
        return self.isClick

    def isHeld(self):
        return self.isHeld

    def update(self, check):
        self.mx, self.my = pygame.mouse.get_pos()
        self.setClick(check)

    def whoHold(self, address):
        self.whoisHeld = address

    def muchDrag(self, check):
        if check:
            self.manyDrag = 1
        else:
            self.manyDrag = 0






