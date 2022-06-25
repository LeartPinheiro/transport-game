import utils
from connectable import Connectable


class Road(Connectable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "road"
        self.addTag("passable")


class Roads:
    def __init__(self, world):
        self._world = world
        self._roads = []

    def all(self):
        return self._roads

    def getRoad(self, x, y):
        for road in self._roads:
            if road.x == x and road.y == y:
                return road
        return None

    def __str__(self) -> str:
        return f'Road({self.x},{self.y})'

    def addRoad(self, x, y):
        empty = self._world.getTile(x, y).type == "empty"
        if self.getRoad(x, y) is not None:
            self.getRoad(x, y)
        if empty:
            road = Road(x, y)
            self._roads.append(road)
            return road
        return None

    def connectPlaces(self, loc1, loc2):
        if not loc1.hasTag("connectable") or not loc2.hasTag("connectable"):
            return False
        return loc1.connectTo(loc2)

    def connectLocalities(self, x, y, x2, y2):
        if not self._world.isValid(x, y) or not self._world.isValid(x2, y2):
            return False
        loc1 = self._world.getTile(x, y)
        loc2 = self._world.getTile(x2, y2)
        loc1 = self.addRoad(x, y) if loc1.type is 'empty' else loc1
        loc2 = self.addRoad(x2, y2) if loc2.type is 'empty' else loc2
        if loc1 is not None and loc2 is not None:
            self.connectPlaces(loc1, loc2)
            return True
        return False

    def NeededByaVehicle(self, road):
        if road is None:
            return False
        if road.isReserved() or self._world.vehicles.getVehicle(road.x, road.y) is not None:
            return True
        return False

    def neededByAnother(self, road):
        for side in road.getSidesConnected():
            road2 = self.getRoad(
                road.x + utils.sides[side][0], road.y + utils.sides[side][1])
            if road is not None:
                if self.NeededByaVehicle(road2):
                    if len(road2.getSidesConnected()) == 1:
                        return True
        return False

    def canBeDeleted(self, road):
        if road is None:
            return False
        if self.NeededByaVehicle(road):
            return False
        if self.neededByAnother(road):
            return False
        return True

    def deleteRoad(self, road):
        if not self.canBeDeleted(road):
            return False
        for side in road.getSidesConnected():
            road2 = self.getRoad(
                road.x + utils.sides[side][0], road.y + utils.sides[side][1])
            if road2 is not None:
                road2.removeSide(utils.getOppositeSide(side))
        self._roads.remove(road)
        self.deleteEmptyRoads()
        return True

    def deleteRoadAt(self, x, y):
        road = self.getRoad(x, y)
        if road is not None:
            self.deleteRoad(road)
            return True
        return False

    def deleteEmptyRoads(self):
        for road in self._roads:
            if len(road.getSidesConnected()) == 0:
                self.deleteRoad(road)

    def update(self):
        self.deleteEmptyRoads()
