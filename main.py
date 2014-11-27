#!/usr/bin/python

try:
    import pygame, sys, math
    from pygame.locals import *
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Fighter(pygame.sprite.Sprite):
    """The base class for all fighters
    Returns: A fighter object
    Functions: update, calcNewPos
    Attributes: area, vector"""

    def __init__(self, imagefile, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagefile)
        if self.image.get_alpha() is None:
            self.image = self.image.convert()
        else:
            self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self, direction):
        newpos = self.calcnewpos(self.rect, direction)
        self.rect = newpos

    def calcnewpos(self, rect, direction):
        if direction == 'up':
            # move up
            return rect.move(0, -16)
        elif direction == 'down':
            # move down
            return rect.move(0, +16)
        elif direction == 'left':
            # move left
            return rect.move(-16, 0)
        elif direction == 'right':
            # move right
            return rect.move(+16, 0)


class Player(Fighter):
    """A Player character, inherits from Fighter
    Returns: A player object
    Functions: update, calcNewPos
    Attributes: """


class Enemy(Fighter):
    """An enemy character, inherits from Fighter
    Returns: An enemy object
    Functions: update, calcNewPos
    Attributes: """






def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Artificial intelligence assignment')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialise players
    global player1
    player1 = Player('/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter.png', 0, 0)

    # Initialise sprites
    playersprite = pygame.sprite.RenderPlain(player1)

    # Blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Event loop
    while True:
        clock.tick(30)

        screen.blit(background, player1.rect, player1.rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    player1.update('up')
                elif event.key == K_s:
                    player1.update('down')
                elif event.key == K_a:
                    player1.update('left')
                elif event.key == K_d:
                    player1.update('right')


        playersprite.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()