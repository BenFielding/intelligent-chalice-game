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

    def __init__(self, imagelist, name, *groups):
        super(Obstacle, self).__init__(imagelist, *groups)
        x = random.randint(0, 23)
        y = random.randint(0, 23)
        self.location = {'x': x, 'y': y}
        self.rect = self.rect.move(x*32, y*32)
        self.strength = None
        self.name = name
        if self.name == 'crate':
            self.strongmax = 10
        else:
            self.strongmax = 50
        self.hp = random.randint(1, self.strongmax)
        self.weakmax = self.strongmax/2
        self.update()

    def update(self):
        if self.hp > self.weakmax:
            self.strength = 'strong'
            self.image = self.imagelist['strong']
        else:
            self.strength = 'weak'
            self.image = self.imagelist['weak']