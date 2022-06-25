
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = 'empty'
        self._tags = []

    def getTags(self):
        return self._tags

    def addTag(self, tag):
        if tag not in self._tags:
            self._tags.append(tag)

    def removeTag(self, tag):
        if tag in self._tags:
            self._tags.remove(tag)

    def hasTag(self, tag):
        return tag in self._tags

    def __str__(self) -> str:
        return f'Tile({self.x},{self.y})'
