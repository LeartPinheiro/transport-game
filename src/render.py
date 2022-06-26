import pygame
import os
import utils

pygame.init()

screenWidth = 720
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
FPS = 60

originalTileWidth = 64
car_sprite_divider = [2.2, 1.2]
tilesZooms = [24, 32, 48, 64, 96, 128]
imagesFolder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'images')) + "/"


class Render:
    def __init__(self, world):
        self.world = world
        self.zoom = 2
        self.spriteCache = {}
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.showGridLines = False
        self.pathsToDraw = []
        self.showPaths = False

    def zoomIn(self):
        if self.zoom < len(tilesZooms) - 1:
            self.zoom += 1

    def zoomOut(self):
        if self.zoom > 0:
            self.zoom -= 1

    def update(self):
        self.draw()

    def screenToWorld(self, x, y):
        return (x//self.zoomedTileWidth(), y//self.zoomedTileWidth())

    def zoomedTileWidth(self):
        return tilesZooms[self.zoom]

    def loadSprite(self, name):
        if name in self.spriteCache:
            return self.spriteCache[name]
        else:
            sprite = pygame.image.load(imagesFolder + name + ".png")
            self.spriteCache[name] = sprite
            return sprite

    def zoomedTile(self, sprite):
        width = self.zoomedTileWidth()
        return pygame.transform.scale(sprite, (width, width))

    def rotateSprite(self, sprite, side):
        if side == "left":
            return pygame.transform.rotate(sprite, 90)
        elif side == "right":
            return pygame.transform.rotate(sprite, -90)
        elif side == "up":
            return sprite
        elif side == "down":
            return pygame.transform.rotate(sprite, 180)

    def getRoadSprite(self, sides):
        return ' '.join(sorted(sides))

    def getTileSprite(self, x, y):
        tile = self.world.getTile(x, y)
        if tile is None:
            return
        tileType = tile.type
        if tileType is "empty":
            return self.zoomedTile(self.loadSprite("empty"))
        elif tileType is "road":
            spriteName = self.getRoadSprite(tile.getSidesConnected())
            sprite = self.loadSprite("roads/" + spriteName)
            return self.zoomedTile(sprite)

    def drawTile(self, x, y):
        sprite = self.getTileSprite(x, y)
        if sprite is None:
            return
        self.screen.blit(
            sprite, (x*self.zoomedTileWidth(), y*self.zoomedTileWidth()))

    def drawTiles(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.drawTile(x, y)

    def drawGridLines(self):
        for x in range(self.world.width):
            start = (x*self.zoomedTileWidth(), 0)
            end = (x*self.zoomedTileWidth(), screenHeight)
            color = (0, 0, 0)
            pygame.draw.line(self.screen, color, start, end, 1)
            for y in range(self.world.height):
                start = (0, y*self.zoomedTileWidth())
                end = (screenWidth, y*self.zoomedTileWidth())
                color = (0, 0, 0)
                pygame.draw.line(self.screen, color, start, end, 1)

    def drawPath(self, path):
        for i in range(len(path) - 1):
            start = (path[i][0]*self.zoomedTileWidth() + self.zoomedTileWidth()/2,
                     path[i][1]*self.zoomedTileWidth() + self.zoomedTileWidth()/2)
            end = (path[i+1][0]*self.zoomedTileWidth() + self.zoomedTileWidth()/2,
                   path[i+1][1]*self.zoomedTileWidth() + self.zoomedTileWidth()/2)
            color = (0, 0, 0)
            pygame.draw.line(self.screen, color, start, end, 1)

    def getVehicleSprite(self, vehicle):
        direction = vehicle._direction
        sprite = self.loadSprite("truck")
        width = self.zoomedTileWidth() / car_sprite_divider[0]
        height = self.zoomedTileWidth() / car_sprite_divider[1]
        sprite = pygame.transform.scale(sprite, (width, height))
        return self.rotateSprite(sprite, direction)

    def drawVehicle(self, vehicle):
        sprite = self.getVehicleSprite(vehicle)
        direction = vehicle._direction
        width = self.zoomedTileWidth() / car_sprite_divider[0]
        height = self.zoomedTileWidth() / car_sprite_divider[1]
        if direction == "left" or direction == "right":
            width = self.zoomedTileWidth() / car_sprite_divider[1]
            height = self.zoomedTileWidth() / car_sprite_divider[0]
        side = utils.sides[direction]
        tileWid = self.zoomedTileWidth()
        xa = side[0] * tileWid / 100 * (vehicle.moveProgress())
        ya = side[1] * tileWid / 100 * (vehicle.moveProgress())
        x = vehicle.x * tileWid + tileWid / 2 - width / 2 + xa
        y = vehicle.y * tileWid + tileWid / 2 - height / 2 + ya
        screen.blit(sprite, (x, y))

    def drawVehicles(self):
        for vehicle in self.world.vehicles.all():
            tile = self.world.getTile(vehicle.x, vehicle.y)
            if tile is not None:
                if tile.type == "road" or vehicle.moveProgress() is not 100:
                    self.drawVehicle(vehicle)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.drawTiles()
        if self.showGridLines:
            self.drawGridLines()
        if self.showPaths:
            for path in self.pathsToDraw:
                self.drawPath(path)
        self.drawVehicles()
        pygame.display.flip()
        self.clock.tick(FPS)

    def update(self):
        self.draw()
