sides = {
    "left": [-1, 0],
    "right": [1, 0],
    "up": [0, -1],
    "down": [0, 1]
}

directionsToSide = {
    1: "left",
    2: "right",
    3: "up",
    4: "down"
}

sideToDirection = {
    "left": 1,
    "right": 2,
    "up": 3,
    "down": 4
}


def getOppositeSide(side):
    if side == "left":
        return "right"
    elif side == "right":
        return "left"
    elif side == "up":
        return "down"
    elif side == "down":
        return "up"


def relativeSide(tile1, tile2):
    for side in sides:
        if tile1.x + sides[side][0] == tile2.x and tile1.y + sides[side][1] == tile2.y:
            return side
    return None
