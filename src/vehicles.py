import pathfinder
import utils

class MovementProcessor:
    def __init__(self,vehicle,world):
        self._vehicle = vehicle
        self._world = world
        self._moveProgress = 0
        self._path = None
        self._target = None
             
    def removeTarget(self,target):
        self._vehicle.removeTarget(target)
    
    def setTarget(self, target,save=True):
        self._target = target
        if save:
            if not target in self._vehicle._targets:
                self._vehicle._targets.append(target)
        self._updatePath()

    def updateDirection(self):
        if self._path is None:
            return
        other = self._world.getTile(self._path[0][0], self._path[0][1])
        newDirection = utils.relativeSide(self._vehicle, other)
        if newDirection is not None:
            self._vehicle._direction = newDirection

    def canMove(self):
        if self._target is not None and self._path is None:
            self.updateTarget()
        if self._path is None:
            return False
        if self._world.vehicles.getVehicle(self._path[0][0], self._path[0][1]) is not None and self._path[0] != None:
            self._updatePath()
            return False
        nextTile = self._world.getTile(self._path[0][0], self._path[0][1])
        reservedTo = nextTile._reservedTo
        if reservedTo is not None:
            return reservedTo == self._vehicle
        if reservedTo is None:
            nextTile._reservedTo = self._vehicle
            return True
        return False

    def _updatePath(self):
        x, y = self._vehicle.x, self._vehicle.y
        if x == self._target[0] and y == self._target[1]:
            self.removeTarget(self._target)
            self._path = None
            self._world.roads.cleanReservationsFrom(self)
            return
        if self._target is None:
            self._path = None
            self._world.roads.cleanReservationsFrom(self)
            return

        xt, yt = self._target[0], self._target[1]
        self._path = pathfinder.findPath(self._world, x, y, xt, yt)
    
    def updateTarget(self,add_road = False):
        if len(self._vehicle._targets) > 0:
            for target in self._vehicle._targets:
                self._target = target
                self._updatePath()
                if self._path is not None:
                    return 
        if add_road:
            target = self._world.roads.randomReachableRoad(self._vehicle.x, self._vehicle.y)
            if target is not None:
                self.setTarget((target.x,target.y),False)

    def move(self):
        if self._target is None:
            return
        if self._path is None:
            self._updatePath()
        if self._moveProgress >= 100:
            self._moveProgress = 0
            tile = self._world.getTile(self._vehicle.x, self._vehicle.y)
            tile._reservedTo = None
            self._vehicle.x, self._vehicle.y = self._path[0]
            self._updatePath()
        if self.canMove():
            self._moveProgress += self._vehicle._speed

    def update(self):
        self.updateDirection()
        if self._target is not None:
            self.move()
    

class Vehicle:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self._direction = "up"
        self._world = world
        self._speed = 4
        self._movementProcessor = MovementProcessor(self,world)
        self._moveProgress = 0
        self._path = None
        self._targets = []
        self._target = None
        self._packageTarget = None
        self._inventory = []

    def moveProgress(self):
        return self._movementProcessor._moveProgress

    def addTarget(self, target):
        if target not in self._targets:
            self._targets.append(target)

    def setTarget(self, target,save=True):
        self._movementProcessor.setTarget(target,save)

    def removeTarget(self, target):
        if target in self._targets:
            self._targets.remove(target)
        if self._movementProcessor._target == target:
            self._movementProcessor.updateTarget()
        
    def update(self):
        self._movementProcessor.update()
        
class Vehicles:
    def __init__(self, world):
        self._world = world
        self._vehicles = []

    def all(self):
        return self._vehicles

    def newVehicle(self, x, y):
        vehicle = Vehicle(x, y, self._world)
        self._vehicles.append(vehicle)
        return vehicle

    def hasStoppedVehicle(self, x, y):
        for vehicle in self._vehicles:
            if vehicle.x == x and vehicle.y == y and vehicle._moveProgress == 0:
                return True
        return False

    def getVehicle(self, x, y):
        for vehicle in self._vehicles:
            if vehicle.x == x and vehicle.y == y:
                return vehicle
        return None

    def update(self):
        for vehicle in self._vehicles:
            vehicle.update()
