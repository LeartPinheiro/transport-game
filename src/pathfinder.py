import utils


def isInList(list, x, y):
    for item in list:
        if item[0] == x and item[1] == y:
            return True
    return False


def getPath(current):
    path = []
    while current[3] is not None:
        path.append((current[0], current[1]))
        current = current[3]
    # reverse the path
    path.reverse()
    return path


def findPath(world, startX, startY, targetX, targetY):
    openList = []
    closedList = []
    openList.append((startX, startY, 0, None))
    while len(openList) > 0:
        openList.sort(key=lambda x: x[2])
        current = openList.pop(0)
        closedList.append(current)
        if current[0] == targetX and current[1] == targetY:
            return getPath(current)
        for side in utils.sides:
            x = current[0] + utils.sides[side][0]
            y = current[1] + utils.sides[side][1]
            tile1 = world.getTile(current[0], current[1])
            tile2 = world.getTile(x, y)
            if world.isPassable(x, y) and tile1.hasTag("connectable"):
                if not world.vehicles.hasStoppedVehicle(x, y) and tile1.isConnectedTo(tile2):
                    if not isInList(openList, x, y) and not isInList(closedList, x, y):
                        cost = current[2] + 1
                        openList.append((x, y, cost, current))
    return None
