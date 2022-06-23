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

def getTileSprite(tile):
    if tile["type"] == 0:
        return zoomedSprite(loadSprite("empty"))
    elif tile["type"] == 1:
        return zoomedSprite(loadSprite("roads/" + getRoadSprite(tile["connections"])))
    elif tile["type"] == 2:
        return zoomedSprite(loadSprite("place"))

def allImagesNames():
    return [f.replace('.png', '').split(' ') for f in os.listdir("images") if f.endswith(".png")]

def getRoadSprite(sides):
    return ' '.join(sorted(sides))

#draw grid with a border on tiles
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
        return pygame.transform.rotate(sprite, -90)
    elif side == "right":
        return pygame.transform.rotate(sprite, 90)
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
    side = sideCods[direction]
    xa = side[0] * zoomedTileWidth() / 100 * (100 - vehicle.move)
    ya = side[1] * zoomedTileWidth() / 100 * (100 - vehicle.move)
    x = vehicle.x * zoomedTileWidth() + zoomedTileWidth() / 2 - width / 2 + xa
    y = vehicle.y * zoomedTileWidth() + zoomedTileWidth() / 2 - height / 2 + ya
    screen.blit(sprite, (x,y))
    
            
def drawVehicles():
    for vehicle in world.vehicles:
        drawVehicle(vehicle)
        print("drawing vehicle")

def draw():
    drawGrid()
    drawVehicles()

def mouseToGrid(mouseX, mouseY):
    return (mouseX // zoomedTileWidth(), mouseY // zoomedTileWidth())

def mouseDelete(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = world.getTile(x, y)
    if tile is not None:
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
        world.addPlace(x,y)

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
            if event.key == pygame.K_a:
                world.connectTile(world.getTile(5, 5), "right")
            #right arrow key
            if event.key == pygame.K_UP:
                zoom += 1
                if zoom >= len(tilesZooms):
                    zoom = len(tilesZooms) - 1
            #left arrow key
            if event.key == pygame.K_DOWN:
                zoom -= 1
                if zoom < 0:
                    zoom = 0
            if event.key == pygame.K_r:
                world.addVehicle(0, 1, "up")
            if event.key == pygame.K_s:
                x = world.vehicles[0].x
                y = world.vehicles[0].y
                world.vehicles[0].setPath([[x, y + 1]])
    

    screen.fill((0, 0, 0))
    draw()
    world.update()
    pygame.display.flip()
    