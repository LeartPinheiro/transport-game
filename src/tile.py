
class Tile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = 'empty'
        self.tags = []

    def getTags(self):
        return self.tags

    def addTag(self,tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def removeTag(self,tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def hasTag(self,tag):
        return tag in self.tags

    def __str__(self) -> str:
        return f'Tile({self.x},{self.y})'