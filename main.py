#!/usr/bin/python

try:
    import pygame
    import sys
    import math
    import random
    from pygame.locals import *
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Projectile(pygame.sprite.Sprite):
    """The base class for all projectiles
    Returns: A projectile object
    Functions:
    Attributes:"""

    def __init__(self, image, rect, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (16, 16))
        self.rect = rect.inflate(-16, -16)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.direction = direction

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


class Fighter(pygame.sprite.Sprite):
    """The base class for all fighters
    Returns: A fighter object
    Functions: update, calcNewPos
    Attributes:"""

    def __init__(self, imagefile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagefile)
        if self.image.get_alpha() is None:
            self.image = self.image.convert()
        else:
            self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.direction = 'none'

    def update(self, magnitude):
        if self.direction != 'none':
            newpos = self.calcnewpos(self.rect, self.direction, magnitude)
            self.rect = newpos
            self.rect.clamp_ip(self.area)

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

    def __init__(self, imagefile):
        Fighter.__init__(self, imagefile)
        self.direction = 'right'
        self.update(736)
        self.direction = 'none'

    def randommove(self):
        directionlist = ['up', 'down', 'left', 'right', 'none']
        self.direction = random.choice(directionlist)


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((768, 768))
    pygame.display.set_caption('Artificial intelligence assignment')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialise players
    global player1
    player1 = Player('/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter.png')

    # Initialise enemies
    global enemy1
    enemy1 = Enemy('/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter.png')

    # List of all active fighters
    fighterlist = pygame.sprite.Group()

    # Initialise sprites
    playersprite = pygame.sprite.RenderPlain(player1)
    fighterlist.add(playersprite)
    enemysprite = pygame.sprite.RenderPlain(enemy1)
    fighterlist.add(enemysprite)

    # List of all active projectiles
    projectilelist = pygame.sprite.Group()

    # Blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Event loop
    while True:
        clock.tick(30)

        for fighter in fighterlist:
            screen.blit(background, fighter.rect, fighter.rect)
        for projectile in projectilelist:
            screen.blit(background, projectile.rect, projectile.rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    player1.direction = 'up'
                elif event.key == K_s:
                    player1.direction = 'down'
                elif event.key == K_a:
                    player1.direction = 'left'
                elif event.key == K_d:
                    player1.direction = 'right'
                else:
                    if event.key == K_SPACE:
                        projectile = Projectile(player1.image, player1.rect, 'right')
                        projectilelist.add(projectile)
            elif event.type == KEYUP:
                if event.key == K_w and player1.direction == 'up':
                    player1.direction = 'none'
                elif event.key == K_s and player1.direction == 'down':
                    player1.direction = 'none'
                elif event.key == K_a and player1.direction == 'left':
                    player1.direction = 'none'
                elif event.key == K_d and player1.direction == 'right':
                    player1.direction = 'none'

        enemy1.randommove()

        fighterlist.update(16)
        projectilelist.update(32)

        fighterlist.draw(screen)
        projectilelist.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()