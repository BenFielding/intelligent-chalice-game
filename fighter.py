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

    def __init__(self, name, imagefile, *groups):
        super(Fighter, self).__init__(imagefile, *groups)
        self.name = name
        self.direction = 'down'
        self.image = self.imagelist[self.direction]
        self.moving = False

    def update(self, magnitude, obstaclelist):
        if self.moving:
            oldpos = self.rect
            newpos = self.calcnewpos(self.rect, self.direction, magnitude)
            self.rect = newpos
            if pygame.sprite.spritecollide(self, obstaclelist, False, pygame.sprite.collide_circle):
                self.rect = oldpos
            self.rect.clamp_ip(self.area)
            self.location = {'x': self.rect.x/32, 'y': self.rect.y/32}

    def calcnewpos(self, rect, direction, magnitude):
        self.image = self.imagelist[direction]
        if direction == 'up':
            # move up
            return rect.move(0, -(magnitude*32))
        elif direction == 'down':
            # move down
            return rect.move(0, +(magnitude*32))
        elif direction == 'left':
            # move left
            return rect.move(-(magnitude*32), 0)
        elif direction == 'right':
            # move right
            return rect.move(+(magnitude*32), 0)