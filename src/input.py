import utils

class Input:
    def __init__(self,pygame,world,render):
        self.pygame = pygame
        self.world = world
        self.render = render
        self.lastTile = None
        self.mouse = (0,0)

    def screenToWorld(self,x,y):
        return self.render.screenToWorld(x,y)

    def mouseLeftDown(self,event):
        x, y = self.screenToWorld(event.pos[0], event.pos[1])
        tile = self.world.getTile(x, y)
        if tile is not None:
            self.lastTile = tile

    
    def mouseRightDown(self,event):
        self.mouseRoadDelete(event)

    def mouseLeftUp(self,event):
        self.lastTile = None

    def mouseDown(self,event):
        if event.button == 1:
            self.mouseLeftDown(event)
        elif event.button == 3:
            self.mouseRightDown(event)

    def mouseMove(self,event):
        self.mouse = event.pos
        if event.buttons[0] == 1:
            self.mouseRoad(event)
        elif event.buttons[2] == 1:
            self.mouseRoadDelete(event)

    def mouseRoad(self,event):
        x, y = self.screenToWorld(event.pos[0], event.pos[1])
        tile = self.world.getTile(x, y)
        tileExists = tile is not None
        lastTileExists = self.lastTile is not None
        if tileExists and lastTileExists and tile != self.lastTile:
            side = utils.relativeSide(self.lastTile, tile)
            if side is not None:
                self.world.roads.connectLocalities(self.lastTile.x, self.lastTile.y, tile.x, tile.y)
        self.lastTile = tile

    def mouseRoadDelete(self,event):
        x, y = self.screenToWorld(event.pos[0], event.pos[1])
        road = self.world.roads.getRoad(x, y)
        if road is not None:
            self.world.roads.deleteRoad(road)
            print(self.world.roads.all())

    def keyDown(self,event):
        if event.key == self.pygame.K_ESCAPE:
            self.pygame.quit()
            quit()
        if event.key == self.pygame.K_r:
            print(self.world.roads.all())
        if event.key == self.pygame.K_UP:
            self.render.zoomIn()
        if event.key == self.pygame.K_DOWN:
            self.render.zoomOut()
        if event.key == self.pygame.K_g:
            self.render.showGridLines = not self.render.showGridLines
        if event.key == self.pygame.K_p:
            self.render.showPaths = not self.render.showPaths
        if event.key == self.pygame.K_t:
            self.test()

    def update(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.pygame.quit()
                quit()
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                self.mouseDown(event)
            if event.type == self.pygame.MOUSEBUTTONUP:
                self.mouseLeftUp(event)
            if event.type == self.pygame.MOUSEMOTION:
                self.mouseMove(event)
            if event.type == self.pygame.KEYDOWN:
                self.keyDown(event)
            if event.type == self.pygame.KEYUP:
                #self.keyUp(event)
                pass

    def test(self):
        x,y = self.screenToWorld(self.mouse[0],self.mouse[1])
        self.world.vehicles.newVehicle(x,y)
        index = len(self.world.vehicles.all()) - 1
        self.world.vehicles._vehicles[index]._target = (9 - index ,9 - index)
