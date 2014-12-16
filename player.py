try:
    import sys
    import random
    from fighter import Fighter
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Player(Fighter):
    """A Player character, inherits from Fighter
    Returns: A player object
    Functions: update, calcNewPos
    Attributes: """

    def __init__(self, name, imagelist, *groups):
        super(Player, self).__init__(name, imagelist, *groups)
        x = random.randint(0, 23)
        y = random.randint(0, 23)
        self.location = {'x': x, 'y': y}
        self.rect = self.rect.move(x*32, y*32)