from utils import *


class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.resetGrid()

    def resetGrid(self):
        self.grid = []
        for x in range(self.width):
            self.grid.append([])
            for y in range(self.height):
                self.grid[x].append({"x": x, "y": y,"type": 0,"connections": []})

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

    def deleteRoad(self,tile):
        tile["type"] = 0
        tile["connections"] = []
        for side in sides:
            target = self.getTile(tile["x"] + sides[side][0], tile["y"] + sides[side][1])
            if target is not None:
                reversedDir = reverseSide(side)
                if reversedDir in target["connections"]:
                    target["connections"].remove(reversedDir)
                    self.manageTile(target)

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
        if len(tile["connections"]) == 0:
            tile["type"] = 0
            tile["connections"] = []