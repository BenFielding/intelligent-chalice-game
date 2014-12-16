try:
    import pygame
    import sys
    import random
    from fighter import Fighter
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Enemy(Fighter):
    """An enemy character, inherits from Fighter
    Returns: An enemy object
    Functions: update, calcNewPos
    Attributes: """

    def __init__(self, name, imagelist, *groups):
        super(Enemy, self).__init__(name, imagelist, *groups)
        x = random.randint(0, 23)
        y = random.randint(0, 23)
        self.location = {'x': x, 'y': y}
        self.rect = self.rect.move(x*32, y*32)

    def randommove(self):
        directionlist = ['up', 'down', 'left', 'right', 'none']
        direction = random.choice(directionlist)
        if direction == 'none':
            self.moving = False
        else:
            self.direction = direction
            self.moving = True