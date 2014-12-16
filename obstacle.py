try:
    import sys
    import random
    from block import Block
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Obstacle(Block):
    """An obstacle, inherits from block
    Returns: An obstacle object
    Function:
    Attributes:"""

    def __init__(self, imagelist, *groups):
        super(Obstacle, self).__init__(imagelist, *groups)
        x = random.randint(0, 23)
        y = random.randint(0, 23)
        self.location = {'x': x, 'y': y}
        self.rect = self.rect.move(x*32, y*32)
        self.hp = random.randint(1, 10)
        self.update()

    def update(self):
        if self.hp > 5:
            self.image = self.imagelist['strong']
        else:
            self.image = self.imagelist['weak']