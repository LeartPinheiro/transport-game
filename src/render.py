import pygame
import os

pygame.init()

screenWidth = 720
screenHeight = 720

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
FPS = 60 

originalTileWidth = 64
car_sprite_divider = [2.2,1.2]
tilesZooms = [24,32,48,64,96,128]
imagesFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images')) + "/"

class Render:
    def __init__(self,world):
        self.world = world
        self.zoom = 2
        self.spriteCache = {}
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()

    def zoomIn(self):
        if self.zoom < len(tilesZooms) - 1:
            self.zoom += 1
        
    def zoomOut(self):
        if self.zoom > 0:
            self.zoom -= 1

    def update(self):
        self.draw()

    def screenToWorld(self,x,y):
        return (x//self.zoomedTileWidth(), y//self.zoomedTileWidth())

    def zoomedTileWidth(self):
        return tilesZooms[self.zoom]

    def loadSprite(self,name):
        if name in self.spriteCache:
            return self.spriteCache[name]
        else:
            sprite = pygame.image.load(imagesFolder + name + ".png")
            self.spriteCache[name] = sprite
            return sprite

    def zoomedTile(self,sprite):
        width = self.zoomedTileWidth()
        return pygame.transform.scale(sprite, (width, width))

    def getRoadSprite(self,sides):
        return ' '.join(sorted(sides))

    def getTileSprite(self,x,y):
        tile = self.world.getTile(x,y)
        if tile is None:
            return
        tileType = tile.type
        if tileType is "empty":
            return self.zoomedTile(self.loadSprite("empty"))
        elif tileType is "road":
            spriteName = self.getRoadSprite(tile.getSidesConnected())
            sprite = self.loadSprite("roads/" + spriteName)
            return self.zoomedTile(sprite)

    def drawTile(self,x,y):
        sprite = self.getTileSprite(x,y)
        if sprite is None:
            return
        self.screen.blit(sprite, (x*self.zoomedTileWidth(), y*self.zoomedTileWidth()))

    def drawTiles(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.drawTile(x,y)

    def draw(self):
        self.screen.fill((0,0,0))
        self.drawTiles()
        pygame.display.flip()
        self.clock.tick(FPS)

    def update(self):
        self.draw()

    

