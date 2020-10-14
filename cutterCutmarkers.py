from cutmarker import CutMarker

class CutterCutmarkers:
    def __init__(self,myRect):
        self.myRect = myRect
        self.numberHorizontalRects = -1
        self.numberVerticalRects = -1
        self.width = myRect.width
        self.height = myRect.height
        self.topLeftX = myRect.topLeftX
        self.topLeftY = myRect.topLeftY
        self.drawablesController = myRect.drawablesController
        self.screen = myRect.screen

        # var used to decide if myRect ready for subdivide
        self.isReadyForSubdivide = False


    def setupCutting(self, numberDivisionsX, numberDivisionsY):
        self.numberHorizontalRects = numberDivisionsX
        self.numberVerticalRects = numberDivisionsY
        self.myRect.numberHorizontalRects = numberDivisionsX
        self.myRect.numberVerticalRects = numberDivisionsY

        xLength = self.width
        xSpacing = xLength / numberDivisionsX
        CutMarkers = list()
        for i in range(1,numberDivisionsX):
            cm = CutMarker(int(i * xSpacing + self.topLeftX),self.topLeftY, self.screen, self,"vertical",self.drawablesController)

        yLength = self.height
        ySpacing = yLength / numberDivisionsY
        for i in range(1,numberDivisionsY):
            cm = CutMarker(self.topLeftX,int(i * ySpacing + self.topLeftY),self.screen,self,"horizontal",self.drawablesController)

    def update(self):
        if len(self.drawablesController.cutmarkers) == 0:
            self.isReadyForSubdivide = True

    def draw(self):
        pass
        

