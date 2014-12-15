try:
    import pygame
    import sys
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Block(pygame.sprite.Sprite):
    """The base class for all entities
    Returns: An entity object
    Functions:
    Attributes:"""

    def __init__(self, imagefile, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load(imagefile)
        if self.image.get_alpha() is None:
            self.image = self.image.convert()
        else:
            self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.location = {0, 0}
        self.radius = 8