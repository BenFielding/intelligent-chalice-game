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

    def __init__(self, imagelist, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.imagelist = {}
        for key, imagefile in imagelist.iteritems():
            self.imagelist[key] = pygame.image.load(imagefile)
            if self.imagelist[key].get_alpha() is None:
                self.imagelist[key] = self.imagelist[key].convert()
            else:
                self.imagelist[key] = self.imagelist[key].convert_alpha()
        self.image = self.imagelist.itervalues().next()
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.location = {'x': 0, 'y': 0}
        self.radius = 8