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

    def __init__(self, name, imagelist, screenwidth, screenheight, *groups):
        super(Enemy, self).__init__(name, imagelist, screenwidth, screenheight, *groups)
        self.path = None
        self.direction = None
        self.moving = True

    def update(self, magnitude, obstaclelist):
        if not self.attacking:
            self.direction = self.path.get()
        self.attacking = not super(Enemy, self).update(magnitude, obstaclelist)