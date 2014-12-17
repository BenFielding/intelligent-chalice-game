#!/usr/bin/python

try:
    import pygame
    import sys
    import random
    from pygame.locals import *
    from Queue import *
    from block import Block
    from fighter import Fighter
    from enemy import Enemy
    from player import Player
    from obstacle import Obstacle
    from goal import Goal
    from astar import Astar
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


def createfighter(name, imagelist, fightertype = Player):
    fighter = fightertype(name, imagelist)
    if pygame.sprite.spritecollide(fighter, blocklist, False, pygame.sprite.collide_circle):
        fighter.kill()
        fighter = createfighter(name, imagelist, fightertype)
    fighterlist.add(fighter)
    blocklist.add(fighter)
    return fighter


def createobstacle():
    obstacleimagelistchoice = \
        {'crate': {'strong': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate_metal.png',
                   'weak': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate_wood.png'},
         'rock': {'strong': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/rock_strong.png',
                  'weak': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/rock_weak.png'}}
    obstacletype = random.choice(['crate', 'rock'])
    obstacle = Obstacle(obstacleimagelistchoice[obstacletype], obstacletype)
    if not pygame.sprite.spritecollide(obstacle, blocklist, False, pygame.sprite.collide_circle):
        obstaclelist.add(obstacle)
        blocklist.add(obstacle)
    else:
        obstacle.kill()
        createobstacle()


def creategoal():
    goalimagelist = {}
    goalimagelist['goal'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice.png'
    goal = Goal(goalimagelist)
    if not pygame.sprite.spritecollide(goal, blocklist, False, pygame.sprite.collide_circle):
        blocklist.add(goal)
    else:
        print 'Goal creation blocked!'
        goal.kill()
        goal = creategoal()
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

    # List of all active players
    global playerlist
    playerlist = pygame.sprite.Group()

    # List of all active enemies
    global enemylist
    enemylist = pygame.sprite.Group()

    # List of all active obstacles
    global obstaclelist
    obstaclelist = pygame.sprite.Group()

    # Initialise goal
    goal = creategoal()

    # Initialise obstacles
    for i in range(0, 100):
        createobstacle()

    imagedirectionlist = ['up', 'down', 'left', 'right']

    # Initialise players
    playerimagelist = {}
    for direction in imagedirectionlist:
        playerimagelist[direction] = \
            '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_{0}.png'.format(direction)
    player1 = createfighter('Player one', playerimagelist, Player)
    playerlist.add(player1)

    # Initialise enemies
    # TODO: Use OCEAN model for enemies?
    # enemycolourlist = ['red', 'yellow', 'pink', 'cyan']
    enemycolourlist = ['red']
    for enemycolour in enemycolourlist:
        enemyimagelist = {}
        for direction in imagedirectionlist:
            enemyimagelist[direction] = \
                '/home/ben/Documents/uni_git/artificial_intelligence/sprites/{0}_fighter_{1}.png'\
                .format(enemycolour, direction)
        enemy = createfighter('{0} enemy'.format(enemycolour), enemyimagelist, Enemy)
        enemylist.add(enemy)

    # Blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Initialise Astar
    for enemy in enemylist:
        enemy.path = Astar(obstaclelist, enemy, goal).traverse()

    # Initialise player controls
    directionqueue = LifoQueue()
    keyeventdict = {'up': False, 'down': False, 'left': False, 'right': False, 'space': False}

    # Event loop
    while True:
        clock.tick(5)
        for fighter in fighterlist:
            screen.blit(background, fighter.rect, fighter.rect)
        for obstacle in obstaclelist:
            screen.blit(background, obstacle.rect, obstacle.rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    keyeventdict['up'] = True
                    directionqueue.put('up')
                    player1.direction = 'up'
                    player1.moving = True
                elif event.key == K_s:
                    keyeventdict['down'] = True
                    directionqueue.put('down')
                    player1.direction = 'down'
                    player1.moving = True
                elif event.key == K_a:
                    keyeventdict['left'] = True
                    directionqueue.put('left')
                    player1.direction = 'left'
                    player1.moving = True
                elif event.key == K_d:
                    keyeventdict['right'] = True
                    directionqueue.put('right')
                    player1.direction = 'right'
                    player1.moving = True
                elif event.key == K_SPACE:
                        keyeventdict['space'] = True
            elif event.type == KEYUP:
                if event.key == K_w:
                    keyeventdict['up'] = False
                elif event.key == K_s:
                    keyeventdict['down'] = False
                elif event.key == K_a:
                    keyeventdict['left'] = False
                elif event.key == K_d:
                    keyeventdict['right'] = False
                elif event.key == K_SPACE:
                    keyeventdict['space'] = False
                if event.key in [K_w, K_s, K_a, K_d] and player1.moving:
                    if not keyeventdict[player1.direction]:
                        while not directionqueue.empty():
                            player1.direction = directionqueue.get()
                            if keyeventdict[player1.direction]:
                                break
                        if directionqueue.empty() and not keyeventdict[player1.direction]:
                            player1.moving = False
        if keyeventdict['space']:
            attackobstacle(player1.location, player1.direction)
        playerlist.update(1, obstaclelist)

        for enemy in enemylist:
            if not enemy.attemptmove(1, obstaclelist):
                attackobstacle(enemy.location, enemy.direction)

        obstaclelist.update()

        blocklist.draw(screen)

        pygame.display.flip()

        # TODO: Handle collisions with other fighters to avoid two winners
        winner = pygame.sprite.spritecollide(goal, fighterlist, False, pygame.sprite.collide_circle)
        if winner:
            print "{0} has reached the chalice!".format(winner[0].name)
            print 'Game over!'
            break

            #sys.exit(0)

if __name__ == '__main__':
    main()