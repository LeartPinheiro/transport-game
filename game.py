import random
import os
import pygame
import world as wd
from utils import *
pygame.init()

screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.


gridWidth = 10
gridHeight = 10
tileWidth = 64

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
            tile = world.getTile(x, y)
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


def mouseDelete(event):
    x, y = mouseToGrid(event.pos[0], event.pos[1])
    tile = world.getTile(x, y)
    if tile is not None:
        world.deleteRoad(tile)

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
    lastTile = None

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
                world.connectTile(world.getTile(0, 0), "right")

    screen.fill((0, 0, 0))
    drawGrid()
    pygame.display.flip()
    




   

    

    
    




