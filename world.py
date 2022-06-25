from utils import *
import pathfinder
import random
import roads

class Truck:
    def __init__(self,x,y,direction,world):
        self.x = x
        self.y = y
        self.direction = direction
        self.world = world
        self.speed = 4
        self.moving = 100
        self.path = None
        self.target = None
        self.inventory = []
        self.packageTarget = None

    def setTarget(self,target):
        self.target = target
        self.updatePath()
    
    def update(self):
        if self.target is not None:
            self.move()

    def canMove(self):
        if self.path is None:
            return False
        nextTile = self.world.getTile(self.path[0][0],self.path[0][1])
        reservedTo = nextTile["reservedTo"]
        if reservedTo is not None:
            return reservedTo == self
        if reservedTo is None:
            nextTile["reservedTo"] = self
            return True
        return False
        
    def updatePath(self):
        if self.x == self.target[0] and self.y == self.target[1]:
            self.target = None
            self.path = None
            return
        if self.target is None:
            self.path = None
            return
        self.path = self.world.getPath(self.x,self.y,self.target[0],self.target[1])

    def move(self):
        if self.target is None:
            return
        if self.path is None:
            self.updatePath()
        if self.moving <= 0:
            self.moving = 100
            tile = self.world.getTile(self.x,self.y)
            tile["reservedTo"] = None
            self.x, self.y = self.path[0]
            self.updatePath()
        if self.canMove():
            self.moving -= self.speed
        self.world.updateVehicleDirection(self)
                



class Tile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = "empty"



class Building:
    def __init__(self,x,y):
        self.x = x
        self.y = y


class Garage:
    def __init__(self,x,y,inventary,world):
        self.x = x
        self.y = y
        self.vehicles = [Truck(x,y,"up",world) for i in range(inventary)]   
    
    def pickVehicle(self):
        vehicle = random.choice(self.vehicles)
        self.vehicles.remove(vehicle)
        return vehicle
    
    def addVehicle(self,vehicle):
        self.vehicles.append(vehicle)
    
    def removeVehicle(self,vehicle):
        self.vehicles.remove(vehicle)

class package:
    def __init__(self,location,target):
        self.location = location
        self.location.inventory.append(self)
        self.target = target
    
    def move(self,location):
        self.location.inventory.remove(self)
        self.location = location
        self.location.inventory.append(self)

class Logistics:
    def __init__(self,world):
        self.world = world
        self.packages = []
        self.timer = 10000

    def addPackage(self,location,target):
        self.packages.append(package(location,target))
    
    def updateTimer(self):
        self.timer -= 1
        if self.timer <= 0:
            self.timer = 10000
            self.addPackage(random.choice(self.world.garages),random.choice(self.world.garages))

    def update():
        pass
        
class Tile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = "empty"

class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.resetGrid()
        self.roads = roads.Roads(self)
        self.vehicles = []
        self.garages = []
        self.buildings = []

    def resetGrid(self):
        self.roads = roads.Roads(self)
        self.vehicles = []
        self.garages = []
        self.buildings = []
    
    def allTilesObjects(self):
        pass


    def getTile(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return Tile(x,y)

    def getGrid(self):
        grid = []
        for x in range(self.width):
            grid.append([])
            for y in range(self.height):
                grid[x].append(self.getTile(x,y))
        return grid

    def deleteTile(self,tile):
        for side in sides:
            target = self.getTile(tile["x"] + sides[side][0], tile["y"] + sides[side][1])
            if target is not None:
                reversedDir = getOppositeSide(side)
                if reversedDir in target["connections"]:
                    target["connections"].remove(reversedDir)
                    self.manageTile(target)
        x,y = tile["x"], tile["y"]
        self.grid[x][y] = self.tileModel(x,y)

    def isConnected(self,tile1,tile2):
        if not self.isValid(tile1["x"],tile1["y"]) or not self.isValid(tile2["x"],tile2["y"]):
            return False
        side = relativeSide(tile1, tile2)
        if side is None:
            return False
        side2 = getOppositeSide(side)
        if side in tile1["connections"] and side2 in tile2["connections"]:
            return True

    def manageTile(self,tile):
        if tile["type"] == 0:
            return
        self.manageRoadTile(tile)
        
    def manageRoadTile(self,tile):
        if len(tile["connections"]) == 0 and tile["type"] == 1:
            tile["type"] = 0
            tile["connections"] = []

    def addBuilding(self,x,y):
        if self.getTile(x,y)["type"] == 0:
            self.getTile(x,y)["type"] = 2
            self.grid[x][y]["obj"] = Building(x,y)

    def addGarage(self,x,y):
        if self.getTile(x,y)["type"] == 0:
            self.getTile(x,y)["type"] = 3
            self.grid[x][y]["obj"] = Garage(x,y,2,self)
    
    def haveVehicle(self,x,y):
        for vehicle in self.vehicles:
            if vehicle.x == x and vehicle.y == y:
                return True
        return False

    def isValid(self,x,y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def isReserved(self,x,y):
        return self.getTile(x,y)["reservedTo"] is not None

    def hasParkedVehicle(self,x,y):
        if not self.isValid(x,y):
            return False
        if not self.haveVehicle(x,y):
            return False
        for vehicle in self.vehicles:
            if vehicle.x == x and vehicle.y == y:
                parked = vehicle.moving is 100
                if parked:
                    return True
        return False


    def isPassable(self,x,y):
        return self.isRoad(x,y)
            
    def isRoad(self,x,y):
        if not self.isValid(x,y):
            return False
        return self.getTile(x,y)["type"] == 1

    def createVehicle(self,x,y,direction):
        if not self.haveVehicle(x,y):
            if self.isRoad(x,y) or self.isGarage(x,y):
                vehicle = Truck(x,y,direction,self)
                self.vehicles.append(vehicle)
                return vehicle
        return None

    def isGarage(self,x,y):
        if not self.isValid(x,y):
            return False
        return self.getTile(x,y)["type"] == 3

    def addVehicle(self,vehicle):
        self.vehicles.append(vehicle)
    
    def deleteVehicle(self,x,y):
        for vehicle in self.vehicles:
            if vehicle.x == x and vehicle.y == y:
                self.vehicles.remove(vehicle)
                return vehicle
        return None
    
    def removeVehicle(self,vehicle):
        self.vehicles.remove(vehicle)

    def update(self):
        for vehicle in self.vehicles:
            vehicle.update()
    
    def pickRandomEmpty(self):
        return self.pickRandomCoordsByType(0)

    def pickRandomRoad(self):
        return self.pickRandomCoordsByType(1)

    def pickRandomBuilding(self):
        return self.pickRandomCoordsByType(2)

    def pickRandomGarage(self):
        return self.pickRandomCoordsByType(3)


    def pickRandomCoordsByType(self,type):
        places = []
        for x in range(self.width):
            for y in range(self.height):
                if self.getTile(x,y)["type"] == type:
                    places.append((x,y))
        if len(places) == 0:
            return None
        return random.choice(places)

    def updateVehicleDirection(self,vehicle):
        if vehicle.path is None:
            return
        newDirection = relativeSide(self.getTile(vehicle.x,vehicle.y), self.getTile(vehicle.path[0][0],vehicle.path[0][1]))
        if newDirection is not None:
            vehicle.direction = newDirection

    def getPath(self,x,y,targetX,targetY):
        if not self.isValid(x,y) or not self.isValid(targetX,targetY):
            return None
        return pathfinder.findPath(self,x,y,targetX,targetY)

    