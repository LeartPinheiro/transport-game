from utils import *
import random


class Truck:
    def __init__(self,x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1
        self.move = 100
        self.path = []

    def setPath(self,path):
        self.path = path

class Place:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.resetGrid()
        self.vehicles = []

    def tileModel(self,x,y):
        return {"x": x, "y": y,"type": 0,"connections": [],
                    "state": 0, "permissions": [],"obj": None}

    def resetGrid(self):
        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                self.grid[x].append(self.tileModel(x,y))

    def getTile(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.grid[x][y]

    def connectTile(self,tile, side):
        target = self.getTile(tile["x"] + sides[side][0], tile["y"] + sides[side][1])
        if target is not None:
            if tile["type"] == 0:
                tile["type"] = 1
            if not side in tile["connections"]:
                tile["connections"].append(side)
                self.connectTile(target, reverseSide(side))
            return True
        else:
            return False

    def deleteTile(self,tile):
        for side in sides:
            target = self.getTile(tile["x"] + sides[side][0], tile["y"] + sides[side][1])
            if target is not None:
                reversedDir = reverseSide(side)
                if reversedDir in target["connections"]:
                    target["connections"].remove(reversedDir)
                    self.manageTile(target)
        x,y = tile["x"], tile["y"]
        self.grid[x][y] = self.tileModel(x,y)

    def isConnected(self,tile1,tile2):
        side = self.relativeSide(tile1, tile2)
        if side is None:
            return False
        side2 = reverseSide(side)
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

    def addPlace(self,x,y):
        if self.getTile(x,y)["type"] == 0:
            self.getTile(x,y)["type"] = 2
            self.grid[x][y]["obj"] = Place(x,y)
    
    def haveVehicle(self,x,y):
        for vehicle in self.vehicles:
            if vehicle.x == x and vehicle.y == y:
                return True
        return False

    def isReserved(self,x,y):
        return self.getTile(x,y)["state"] == 1

    def isPassable(self,x,y):
        pass

    def isRoad(self,x,y):
        return self.getTile(x,y)["type"] == 1

    def addVehicle(self,x,y,direction):
        if not self.haveVehicle(x,y):
            if self.isRoad(x,y):
                self.vehicles.append(Truck(x,y,direction))
    
    def removeVehicle(self,x,y):
        for vehicle in self.vehicles:
            if vehicle.x == x and vehicle.y == y:
                self.vehicles.remove(vehicle)
                return True

    def update(self):
        for vehicle in self.vehicles:
            self.moveVehicle(vehicle)

    def pickRandomRoad(self):
        roads = []
        for x in range(self.width):
            for y in range(self.height):
                if self.isRoad(x,y):
                    roads.append((x,y))
        if len(roads) == 0:
            return None
        return random.choice(roads)

    def pickRandomPlace(self):
        places = []
        for x in range(self.width):
            for y in range(self.height):
                if self.getTile(x,y)["type"] == 2:
                    places.append((x,y))
        if len(places) == 0:
            return None
        return random.choice(places)

    def updateVehicleDirection(self,vehicle):
        if len(vehicle.path) == 0:
            return
        newDirection = relativeSide(self.getTile(vehicle.x,vehicle.y), self.getTile(vehicle.path[0][0],vehicle.path[0][1]))
        if newDirection is not None:
            vehicle.direction = newDirection

    def moveVehicle(self,vehicle):
        if len(vehicle.path) == 0:
            return
        if vehicle.move <= 0:
            vehicle.move = 100
            vehicle.x, vehicle.y = vehicle.path[0]
            vehicle.path.pop(0)
            return 
        vehicle.move -= vehicle.speed
        self.updateVehicleDirection(vehicle)
        