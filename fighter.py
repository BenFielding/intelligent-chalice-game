try:
    import pygame
    import sys
    from block import Block
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Fighter(Block):
    """The base class for all fighters
    Returns: A fighter object
    Functions: update, calcNewPos
    Attributes:"""

    def __init__(self, name, imagelist, colour, screenwidth, screenheight, *groups):
        super(Fighter, self).__init__(imagelist, screenwidth, screenheight, *groups)
        self.name = name
        self.direction = 'down'
        self.image = self.imagelist[self.direction]
        self.moving = False
        self.attacking = False
        self.points = 0
        self.colour = colour

    def update(self, magnitude, obstaclelist):
        """
        Attempt movement in direction, of magnitude.
        If blocked by obstacle in obstaclelist, return False else return True.

        :param magnitude: (int) magnitude of movement
        :param obstaclelist: (pygame.sprite.Group()) List of obstacle to block movement
        :return: (bool) Success of movement
        """
        if self.moving:
            oldpos = self.rect
            newpos = self.calcnewpos(magnitude)
            self.rect = newpos
            if len(pygame.sprite.spritecollide(self, obstaclelist, False, pygame.sprite.collide_circle)) > 1:
                self.rect = oldpos
                success = False
            else:
                success = True
            self.rect.clamp_ip(self.area)
            self.location = {'x': self.rect.x/32, 'y': self.rect.y/32}
            return success

    def calcnewpos(self, magnitude):
        """
        Calculate a new position based on direction and magnitude of movement

        :param magnitude: (int) Magnitude of movement
        :return: (pygame.Rect) New location after movement
        """
        self.image = self.imagelist[self.direction]
        if self.direction == 'up':
            # move up
            return self.rect.move(0, -(magnitude*32))
        elif self.direction == 'down':
            # move down
            return self.rect.move(0, +(magnitude*32))
        elif self.direction == 'left':
            # move left
            return self.rect.move(-(magnitude*32), 0)
        elif self.direction == 'right':
            # move right
            return self.rect.move(+(magnitude*32), 0)