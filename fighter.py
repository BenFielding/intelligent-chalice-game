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

    def __init__(self, name, imagelist, screenwidth, screenheight, *groups):
        super(Fighter, self).__init__(imagelist, screenwidth, screenheight, *groups)
        self.name = name
        self.direction = 'down'
        self.image = self.imagelist[self.direction]
        self.moving = False
        self.attacking = False

    def update(self, magnitude, obstaclelist):
        if self.moving:
            oldpos = self.rect
            newpos = self.calcnewpos(magnitude)
            self.rect = newpos
            if pygame.sprite.spritecollide(self, obstaclelist, False, pygame.sprite.collide_circle):
                self.rect = oldpos
                success = False
            else:
                success = True
            self.rect.clamp_ip(self.area)
            self.location = {'x': self.rect.x/32, 'y': self.rect.y/32}
            return success

    def calcnewpos(self, magnitude):
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