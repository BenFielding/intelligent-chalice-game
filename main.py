#!/usr/bin/python

try:
    import pygame
    import sys
    from pygame.locals import *
    from block import Block
    from fighter import Fighter
    from enemy import Enemy
    from player import Player
    from projectile import Projectile
    from obstacle import Obstacle
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


def createobstacle():
    obstacle = Obstacle('/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate.png')
    if not pygame.sprite.spritecollide(obstacle, blocklist, False, pygame.sprite.collide_circle):
        obstaclelist.add(obstacle)
        blocklist.add(obstacle)
    else:
        obstacle.kill()
        createobstacle()


def createenemy(imagefile):
    enemy = Enemy(imagefile)
    if not pygame.sprite.spritecollide(enemy, blocklist, False, pygame.sprite.collide_circle):
        fighterlist.add(enemy)
        blocklist.add(enemy)
    else:
        enemy.kill()
        createenemy()
    return enemy


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((768, 768))
    pygame.display.set_caption('Artificial intelligence assignment')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialise sprite groups
    # List of all active blocks
    global blocklist
    blocklist = pygame.sprite.Group()

    # List of all active fighters
    global fighterlist
    fighterlist = pygame.sprite.Group()

    # List of all active projectiles
    global projectilelist
    projectilelist = pygame.sprite.Group()

    # List of all active obstacles
    global obstaclelist
    obstaclelist = pygame.sprite.Group()

    # Initialise obstacles
    for i in range(0, 50):
        createobstacle()

    # Initialise players
    global player1
    player1 = Player('/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter.png', fighterlist, blocklist)

    # Initialise enemies
    # TODO: Use OCEAN model for enemies
    global enemyaggressive
    enemyaggressive = createenemy('/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter.png')

    # Blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Event loop
    while True:
        clock.tick(10)
        for fighter in fighterlist:
            screen.blit(background, fighter.rect, fighter.rect)
        for projectile in projectilelist:
            screen.blit(background, projectile.rect, projectile.rect)
        for obstacle in obstaclelist:
            screen.blit(background, obstacle.rect, obstacle.rect)

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

        enemyaggressive.randommove()

        fighterlist.update(1, obstaclelist)
        projectilelist.update(32)

        blocklist.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()