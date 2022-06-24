import random
import os
import pygame
import world as wd
from utils import *
pygame.init()

screenWidth = 720
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.


gridWidth = 10
gridHeight = 10
originalTileWidth = 64
car_sprite_divider = [2.2,1.2]
tilesZooms = [24,32,48,64,96,128]
zoom = 2
world = wd.World(gridWidth, gridHeight)

spriteCache = {}

sideCods = {
    "left":[-1, 0],
    "right":[1, 0],
    "up":[0, -1],
    "down":[0, 1]
}
lastTile = None
    
def loadSprite(name):
    if name in spriteCache:
        return spriteCache[name]
    else:
        sprite = pygame.image.load("images/" + name + ".png")
        spriteCache[name] = sprite
        return sprite

def zoomedTileWidth():
    return tilesZooms[zoom]

def zoomedSprite(sprite):
    return pygame.transform.scale(sprite, (zoomedTileWidth(), zoomedTileWidth()))

def getGarageSprite(garage):
    count = len(garage.vehicles)
    spriteName = "garage" + str(count)
    return spriteName

#need to refactor this
def getTileSprite(tile):
    
    if tile["type"] == 0:
        return zoomedSprite(loadSprite("empty"))
    elif tile["type"] == 1:
        return zoomedSprite(loadSprite("roads/" + getRoadSprite(tile["connections"])))
    elif tile["type"] == 2:
        return zoomedSprite(loadSprite("place"))
    elif tile["type"] == 3:
        sprite = zoomedSprite(loadSprite("empty"))
        sprite.blit(zoomedSprite(loadSprite(getGarageSprite(tile["obj"]))), (0, 0))
        return sprite

def allImagesNames():
    return [f.replace('.png', '').split(' ') for f in os.listdir("images") if f.endswith(".png")]

def getRoadSprite(sides):
    return ' '.join(sorted(sides))

def drawGrid():
    for x in range(gridWidth):
        for y in range(gridHeight):
            tile = world.getTile(x, y)
            sprite = getTileSprite(tile)
            screen.blit(sprite, (x * zoomedTileWidth(), y * zoomedTileWidth()))
    drawTilesBorders()

def drawTilesBorders():
    for x in range(gridWidth):
        pygame.draw.line(screen, (0, 0, 0), (x * zoomedTileWidth(), 0), (x * zoomedTileWidth(), screenHeight))
        for y in range(gridHeight):
            pygame.draw.line(screen, (0, 0, 0), (0, y * zoomedTileWidth()), (screenWidth, y * zoomedTileWidth()))

def rotateSprite(sprite, side):
    if side == "left":
        return pygame.transform.rotate(sprite, 90)
    elif side == "right":
        return pygame.transform.rotate(sprite, -90)
    elif side == "up":
        return sprite
    elif side == "down":
        return pygame.transform.rotate(sprite, 180)

def getVehicleSprite(vehicle):
    direction = vehicle.direction
    sprite = loadSprite("truck")
    width = zoomedTileWidth() / car_sprite_divider[0]
    height = zoomedTileWidth() / car_sprite_divider[1]
    sprite = pygame.transform.scale(sprite, (width, height))
    return rotateSprite(sprite, direction)

def drawVehicle(vehicle):
    sprite = getVehicleSprite(vehicle)
    direction = vehicle.direction
    width = zoomedTileWidth() / car_sprite_divider[0]
    height = zoomedTileWidth() / car_sprite_divider[1]
    if direction == "left" or direction == "right":
        width = zoomedTileWidth() / car_sprite_divider[1]
        height = zoomedTileWidth() / car_sprite_divider[0]
    side = sideCods[direction]
    xa = side[0] * zoomedTileWidth() / 100 * (100 - vehicle.moving)
    ya = side[1] * zoomedTileWidth() / 100 * (100 - vehicle.moving)
    x = vehicle.x * zoomedTileWidth() + zoomedTileWidth() / 2 - width / 2 + xa
    y = vehicle.y * zoomedTileWidth() + zoomedTileWidth() / 2 - height / 2 + ya

    screen.blit(sprite, (x,y))
      
def drawVehicles():
    for vehicle in world.vehicles:
        drawVehicle(vehicle)

def draw():
    drawGrid()
    drawVehicles()

def mouseToGrid(mouseX, mouseY):
    return (mouseX // zoomedTileWidth(), mouseY // zoomedTileWidth())

def mouseDelete(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = world.getTile(x, y)
    if tile is not None:
        if tile["type"] == 1:
            world.deleteTile(tile)

def mouseDown(event):
    if event.button == 1:
        mouseLeftDown(event)
    elif event.button == 3:
        mouseRightDown(event)

def mouseLeftDown(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = world.getTile(x, y)
    if tile is not None:
        global lastTile
        lastTile = tile

def mouseLeftUp(event):
    global lastTile
    mouseAddPlace(event)
    lastTile = None

def mouseAddPlace(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = world.getTile(x, y)
    if tile is not None and lastTile is not None and tile == lastTile:
        #world.addGarage(x,y)
        pass

def mouseRightDown(event):
    mouseDelete(event)

def mouseRoad(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = world.getTile(x, y)
    tileExists = tile is not None
    global lastTile
    lastTileExists = lastTile is not None
    if tileExists and lastTileExists and tile != lastTile:
        side = relativeSide(lastTile, tile)
        if side is not None:
            world.connectTile(lastTile, side)
    lastTile = tile

def mouseMove(event):
    if event.buttons[0] == 1:
        mouseRoad(event)
    elif event.buttons[2] == 1:
        mouseDelete(event)

timer = 5000

def createUpdate():
    global timer
    timer -= 1000 / 60
    if timer <= 0:
        timer = 30000
        empty = world.pickRandomEmpty()
        if empty is not None:
            rand = random.randint(0,100)
            if rand < 30:
                world.addGarage(empty[0], empty[1])
            elif rand < 100:
                world.addBuilding(empty[0], empty[1])

def addFirstGrid():
    empty = world.pickRandomEmpty()
    if empty is not None:
        world.addGarage(empty[0], empty[1])
    empty = world.pickRandomEmpty()
    if empty is not None:
        world.addBuilding(empty[0], empty[1])
    if empty is not None:
        world.addBuilding(empty[0], empty[1])
addFirstGrid()

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
        if event.type == pygame.KEYDOWN:
            pass
    screen.fill((0, 0, 0))
    draw()
    world.update()
    createUpdate()
    pygame.display.flip()
    