import pathfinder
import utils

class Vehicle:
    def __init__(self,x,y,world):
        self.x = x
        self.y = y
        self._direction = "up"
        self._world = world
        self._speed = 4
        self._moveNeeded = 100
        self._path = None
        self._target = None
        self._packageTarget = None
        self._inventory = []

    def moveNeeded(self):
        return self._moveNeeded

    def setTarget(self,target):
        self._target = target
        self.updatePath()
    
    def updateDirection(self):
        if self._path is None:
            return
        other = self._world.getTile(self._path[0][0],self._path[0][1])
        newDirection = utils.relativeSide(self,other)
        if newDirection is not None:
            self._direction = newDirection

    def update(self):
        self.updateDirection()
        if self._target is not None:
            self.move()

    def canMove(self):
        if self._path is None:
            return False
        nextTile = self._world.getTile(self._path[0][0],self._path[0][1])
        reservedTo = nextTile._reservedTo
        if reservedTo is not None:
            return reservedTo == self
        if reservedTo is None:
            nextTile._reservedTo = self
            return True
        return False
        
    def updatePath(self):
        if self.x == self._target[0] and self.y == self._target[1]:
            self._target = None
            self._path = None
            return
        if self._target is None:
            self._path = None
            return
        x,y = self.x,self.y
        xt,yt = self._target[0],self._target[1]
        self._path = pathfinder.findPath(self._world,x,y,xt,yt)


    def move(self):
        if self._target is None:
            return
        if self._path is None:
            self.updatePath()
        if self._moveNeeded <= 0:
            self._moveNeeded = 100
            tile = self._world.getTile(self.x,self.y)
            tile._reservedTo = None
            self.x, self.y = self._path[0]
            self.updatePath()
        if self.canMove():
            self._moveNeeded -= self._speed

        
class Vehicles:
    def __init__(self,world):
        self._world = world
        self._vehicles = []

    def all(self):
        return self._vehicles

    def newVehicle(self,x,y):
        vehicle = Vehicle(x,y,self._world)
        self._vehicles.append(vehicle)
        return vehicle

    def hasStoppedVehicle(self,x,y):
        for vehicle in self._vehicles:
            if vehicle.x == x and vehicle.y == y and vehicle._moveNeeded == 100:
                return True
        return False
                
    def getVehicle(self,x,y):
        for vehicle in self._vehicles:
            if vehicle.x == x and vehicle.y == y:
                return vehicle
        return None

    def update(self):
        for vehicle in self._vehicles:
            vehicle.update()



    

    
        