import random
import os
import pygame
pygame.init()

screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.


gridWidth = 10
gridHeight = 10
tileWidth = 64


def newGrid():
    grid = []
    for x in range(gridWidth):
        grid.append([])
        for y in range(gridHeight):
            grid[x].append({"x": x, "y": y,"type": 0,"connections": []})
    return grid

grid = newGrid()

spriteCache = {}

sideCods = {
    "left":[-1, 0],
    "right":[1, 0],
    "up":[0, -1],
    "down":[0, 1]
}
lastTile = None

def getTile(x, y):
    if x < 0 or x >= gridWidth or y < 0 or y >= gridHeight:
        return None
    return grid[x][y]

def loadSprite(name):
    if name in spriteCache:
        return spriteCache[name]
    else:
        sprite = pygame.image.load("images/" + name + ".png")
        spriteCache[name] = sprite
        return sprite

def getTileSprite(tile):
    if tile["type"] == 0:
        return loadSprite("empty")
    elif tile["type"] == 1:
        return loadSprite(getRoadSprite(tile["connections"]))

def allImagesNames():
    return [f.replace('.png', '').split(' ') for f in os.listdir("images") if f.endswith(".png")]

def getRoadSprite(sides):
    return ' '.join(sorted(sides))

#draw grid with a border on tiles
def drawGrid():
    for x in range(gridWidth):
        for y in range(gridHeight):
            tile = getTile(x, y)
            sprite = getTileSprite(tile)
            screen.blit(sprite, (x * tileWidth, y * tileWidth))
    drawTilesBorders()

def drawTilesBorders():
    for x in range(gridWidth):
        pygame.draw.line(screen, (0, 0, 0), (x * tileWidth, 0), (x * tileWidth, 720), 1)
        for y in range(gridHeight):
            pygame.draw.line(screen, (0, 0, 0), (0, y * tileWidth), (720, y * tileWidth), 1)
            


def mouseToGrid(mouseX, mouseY):
    return (mouseX // tileWidth, mouseY // tileWidth)

def connectTile(tile, side):
    global sideCods
    target = getTile(tile["x"] + sideCods[side][0], tile["y"] + sideCods[side][1])
    if target is not None:
        if tile["type"] == 0:
            tile["type"] = 1
        if not side in tile["connections"]:
            tile["connections"].append(side)
            connectTile(target, reverseSide(side))
        return True
    else:
        return False

def deleteRoad(tile):
    tile["type"] = 0
    tile["connections"] = []
    for side in sideCods:
        target = getTile(tile["x"] + sideCods[side][0], tile["y"] + sideCods[side][1])
        if target is not None:
            reversedDir = reverseSide(side)
            if reversedDir in target["connections"]:
                target["connections"].remove(reversedDir)
                manageTile(target)

def mouseDelete(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = getTile(x, y)
    if tile is not None:
        deleteRoad(tile)

def reverseSide(side):
    if side == "left":
        return "right"
    elif side == "right":
        return "left"
    elif side == "up":
        return "down"
    elif side == "down":
        return "up"


def isConnected(tile1,tile2):
    side = relativeSide(tile1, tile2)
    if side is None:
        return False
    side2 = reverseSide(side)
    if side in tile1["connections"] and side2 in tile2["connections"]:
        return True


def relativeSide(tile1, tile2):
    for side in sideCods:
        if tile1["x"] + sideCods[side][0] == tile2["x"] and tile1["y"] + sideCods[side][1] == tile2["y"]:
            return side
    return None

def manageTile(tile):
    if tile["type"] == 0:
        return
    if len(tile["connections"]) == 0:
        tile["type"] = 0
        tile["connections"] = []

def mouseDown(event):
    if event.button == 1:
        mouseLeftDown(event)
    elif event.button == 3:
        mouseRightDown(event)

def mouseLeftDown(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = getTile(x, y)
    if tile is not None:
        global lastTile
        lastTile = tile

def mouseLeftUp(event):
    global lastTile
    lastTile = None

def mouseRightDown(event):
    mouseDelete(event)


def mouseRoad(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = getTile(x, y)
    tileExists = tile is not None
    global lastTile
    lastTileExists = lastTile is not None
    if tileExists and lastTileExists and tile != lastTile:
        side = relativeSide(lastTile, tile)
        if side is not None:
            connectTile(lastTile, side)
    lastTile = tile

def mouseMove(event):
    if event.buttons[0] == 1:
        mouseRoad(event)
    elif event.buttons[2] == 1:
        mouseDelete(event)
    
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown(event)
        if event.type == pygame.MOUSEBUTTONUP:
            mouseLeftUp(event)
        if event.type == pygame.MOUSEMOTION:
            mouseMove(event)
        #if press A
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                #print grid
                for x in range(gridWidth):
                    line = ""
                    for y in range(gridHeight):
                        line += str(grid[x][y]["type"]) + " "
                    print(line)
                    

    screen.fill((0, 0, 0))
    drawGrid()
    pygame.display.flip()
    




   

    

    
    




