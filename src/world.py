import utils
import roads
import vehicles
import tile
import pathfinder

class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.resetGrid()
        self.roads = roads.Roads(self)
        self.vehicles = vehicles.Vehicles(self)

    def resetGrid(self):
        self.roads = roads.Roads(self)
    
    def allTilesObjects(self):
        return self.roads.all()

    def getTile(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        for obj in self.allTilesObjects():
            if obj.x == x and obj.y == y:
                return obj
        return tile.Tile(x,y)

    def isValid(self,x,y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def isPassable(self,x,y):
        if not self.isValid(x,y):
            return False
        return self.getTile(x,y).hasTag("passable")
    
    def getPath(self,x,y,xt,yt):
        return pathfinder.findPath(self,x,y,xt,yt)

    def update(self):
        self.roads.update()
        self.vehicles.update()

    

