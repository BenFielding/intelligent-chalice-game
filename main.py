#!/usr/bin/python

try:
    import pygame
    import sys
    from pygame.locals import *
    from block import Block
    from fighter import Fighter
    from enemy import Enemy
    from player import Player
    from obstacle import Obstacle
    from goal import Goal
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


def createobstacle():
    obstacleimagelist = {}
    obstacleimagelist['strong'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate_metal.png'
    obstacleimagelist['weak'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate_wood.png'
    obstacle = Obstacle(obstacleimagelist)
    if not pygame.sprite.spritecollide(obstacle, blocklist, False, pygame.sprite.collide_circle):
        obstaclelist.add(obstacle)
        blocklist.add(obstacle)
    else:
        obstacle.kill()
        createobstacle()


def createenemy(name, imagelist):
    enemy = Enemy(name, imagelist)
    if not pygame.sprite.spritecollide(enemy, blocklist, False, pygame.sprite.collide_circle):
        fighterlist.add(enemy)
        blocklist.add(enemy)
    else:
        enemy.kill()
        createenemy(name, imagelist)
    return enemy

def createplayer(name, imagelist):
    player = Player(name, imagelist)
    if not pygame.sprite.spritecollide(player, blocklist, False, pygame.sprite.collide_circle):
        fighterlist.add(player)
        blocklist.add(player)
    else:
        player.kill()
        createplayer(name, imagelist)
    return player

def creategoal():
    goalimagelist = {}
    goalimagelist['goal'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice.png'
    goal = Goal(goalimagelist)
    if not pygame.sprite.spritecollide(goal, blocklist, False, pygame.sprite.collide_circle):
        blocklist.add(goal)
    else:
        goal.kill()
        createenemy(goalimagelist)
    return goal


def attackobstacle(location, direction):
    objlocation = {'x': location['x'], 'y': location['y']}
    if direction == 'up':
        objlocation['y'] = location['y'] - 1
    elif direction == 'down':
        objlocation['y'] = location['y'] + 1
    elif direction == 'left':
        objlocation['x'] = location['x'] - 1
    elif direction == 'right':
        objlocation['x'] = location['x'] + 1

    foundobstacle = None
    for obstacle in obstaclelist:
        if obstacle.location == objlocation:
            foundobstacle = obstacle

    if foundobstacle:
        foundobstacle.hp -= 1
        if foundobstacle.hp <= 0:
            foundobstacle.kill()


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

    # TODO: Graph of all locations

    # Initialise goal
    goal = creategoal()

    # Initialise obstacles
    for i in range(0, 50):
        createobstacle()

    # Initialise players
    playerimagelist = {}
    playerimagelist['up'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_up.png'
    playerimagelist['down'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_down.png'
    playerimagelist['left'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_left.png'
    playerimagelist['right'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_right.png'
    player1 = createplayer('Player one', playerimagelist) # Player(playerimagelist, fighterlist, blocklist)

    # Initialise enemies
    # TODO: Use OCEAN model for enemies
    enemyimagelist = {}
    enemyimagelist['up'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_up.png'
    enemyimagelist['down'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_down.png'
    enemyimagelist['left'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_left.png'
    enemyimagelist['right'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_right.png'
    enemyaggressive = createenemy('Aggressive enemy', enemyimagelist)

    # Blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Event loop
    while True:
        clock.tick(5)
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
                    player1.moving = True
                elif event.key == K_s:
                    player1.direction = 'down'
                    player1.moving = True
                elif event.key == K_a:
                    player1.direction = 'left'
                    player1.moving = True
                elif event.key == K_d:
                    player1.direction = 'right'
                    player1.moving = True
                else:
                    if event.key == K_SPACE:
                        attackobstacle(player1.location, player1.direction)
            elif event.type == KEYUP:
                if event.key == K_w and player1.direction == 'up':
                    player1.moving = False
                elif event.key == K_s and player1.direction == 'down':
                    player1.moving = False
                elif event.key == K_a and player1.direction == 'left':
                    player1.moving = False
                elif event.key == K_d and player1.direction == 'right':
                    player1.moving = False

        enemyaggressive.randommove()

        fighterlist.update(1, obstaclelist)
        projectilelist.update(32)
        obstaclelist.update()

        blocklist.draw(screen)

        winner = pygame.sprite.spritecollide(goal, fighterlist, False, pygame.sprite.collide_circle)
        if winner:
            print "{0} has reached the chalice and won!".format(winner[0].name)
            sys.exit(0)

        pygame.display.flip()

if __name__ == '__main__':
    main()