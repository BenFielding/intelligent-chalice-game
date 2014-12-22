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

    def __init__(self, imagelist, name, screenwidth, screenheight, *groups):
        super(Obstacle, self).__init__(imagelist, screenwidth, screenheight, *groups)
        self.strength = None
        self.name = name
        self.hp = random.randint(1, self.strongmax)
        self.weakmax = self.strongmax/2
        self.update()

    def update(self):
        """
        Check hitpoints and set strength and image based on basic rule.
        """
        if self.hp > self.weakmax:
            self.strength = 'strong'
            self.image = self.imagelist['strong']
        else:
            self.strength = 'weak'
            self.image = self.imagelist['weak']


class Crate(Obstacle):

    def __init__(self, imagelist, name, screenwidth, screenheight, *groups):
        self.strongmax = 10
        super(Crate, self).__init__(imagelist, name, screenwidth, screenheight, *groups)


class Rock(Obstacle):

    def __init__(self, imagelist, name, screenwidth, screenheight, *groups):
        self.strongmax = 20
        super(Rock, self).__init__(imagelist, name, screenwidth, screenheight, *groups)