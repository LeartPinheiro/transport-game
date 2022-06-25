import utils
import roads
import tile

class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.resetGrid()
        self.roads = roads.Roads(self)

    def resetGrid(self):
        self.roads = roads.Roads(self)
    
    def allObjects(self):
        return self.roads.all()

    def getTile(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        for obj in self.allObjects():
            if obj.x == x and obj.y == y:
                return obj
        return tile.Tile(x,y)

    def isValid(self,x,y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def update(self):
        self.roads.update()

