import utils

class Connectable:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self._tags = ["connectable"]
        self._isPassable = False
        self._reservedTo = None
        self._sidesConnected = []

    def getTags(self):
        return self._tags

    def addTag(self,tag):
        if tag not in self._tags:
            self._tags.append(tag)

    def removeTag(self,tag):
        if tag in self._tags:
            self._tags.remove(tag)

    def hasTag(self,tag):
        return tag in self._tags

    def isConnectable(self):
        return self.hasTag("connectable")

    def isPassable(self):
        return self._isPassable
    
    def isReserved(self):
        return self._reservedTo is not None

    def isReservedTo(self,vehicle):
        return self._reservedTo is vehicle

    def setReservedTo(self,vehicle):
        self._reservedTo = vehicle

    def clearReservedTo(self):
        self._reservedTo = None
    
    def getSidesConnected(self):
        return self._sidesConnected
    
    def isConnectedTo(self,connectable):
        side1 = utils.getSide(self.x,self.y,connectable.x,connectable.y)
        side2 = utils.getSide(connectable.x,connectable.y,self.x,self.y)
        if side1 in self._sidesConnected and side2 in connectable.sidesConnected:
            return True
        return False
    
    def connectTo(self,connectable):
        if self.isConnectable() and connectable.isConnectable():
            side = utils.relativeSide(self,connectable)
            if side is not None:
                self.addSide(side)
                connectable.addSide(utils.getOppositeSide(side))
                return True
        return False

    def addSide(self,side):
        if side not in self._sidesConnected:
            self._sidesConnected.append(side)
            return True
        return False
    
    def removeSide(self,side):
        if side in self._sidesConnected:
            self._sidesConnected.remove(side)
            return True
        return False

    
