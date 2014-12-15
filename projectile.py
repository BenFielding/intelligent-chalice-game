try:
    import pygame
    import sys
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Projectile(pygame.sprite.Sprite):
    """The base class for all projectiles
    Returns: A projectile object
    Functions:
    Attributes:"""

    def __init__(self, image, rect, direction):
        super(Projectile, self).__init__(self)
        self.image = pygame.transform.scale(image, (16, 16))
        self.rect = rect.inflate(-16, -16)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.direction = direction
        # self.location = (0, 0)

    def update(self,  magnitude):
        newpos = self.calcnewpos(self.rect, self.direction, magnitude)
        self.rect = newpos

    def calcnewpos(self, rect, direction, magnitude):
        if direction == 'up':
            # move up
            return rect.move(0, -magnitude)
        elif direction == 'down':
            # move down
            return rect.move(0, +magnitude)
        elif direction == 'left':
            # move left
            return rect.move(-magnitude, 0)
        elif direction == 'right':
            # move right
            return rect.move(+magnitude, 0)