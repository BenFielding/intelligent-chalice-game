try:
    import pygame
    import sys
    import random
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Block(pygame.sprite.Sprite):
    """The base class for all entities
    Returns: An entity object
    Functions:
    Attributes:"""

    def __init__(self, imagelist, screenwidth, screenheight, *groups):
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
        x = random.randint(0, (screenwidth/self.rect.width) - 1)
        y = random.randint(0, (screenheight/self.rect.height) - 1)
        self.location = {'x': x, 'y': y}
        self.rect = self.rect.move(x*32, y*32)
        self.radius = 8