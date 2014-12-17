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
        self.path = None
        self.direction = None
        self.attacking = False
        self.moving = True

    def attemptmove(self, magnitude, obstaclelist):
        if self.attacking:
            self.attacking = not self.update(magnitude, obstaclelist)
        else:
            self.direction = self.path.get()
            self.attacking = not self.update(magnitude, obstaclelist)
        return not self.attacking