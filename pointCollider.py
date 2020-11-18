class PointCollider:
    def __init__(self,xx,yy,isOccupied,width,height, valid):
        self.x = xx
        self.y = yy
        self.isOccupied = isOccupied
        self.width = width
        self.height = height
        self.valid = valid