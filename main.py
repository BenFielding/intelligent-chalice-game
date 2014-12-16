#!/usr/bin/python

try:
    import pygame
    import sys
    from pygame.locals import *
    from Queue import Queue
    from Queue import PriorityQueue
    from block import Block
    from fighter import Fighter
    from enemy import Enemy
    from player import Player
    from obstacle import Obstacle
    from goal import Goal
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Node(object):

    def __init__(self, x, y):
        self.location = {'x': x, 'y': y}
        self.goal = False
        self.parent = None
        self.priority = 999999
        self.cost = 1

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

class Astar(object):

    def traverse(self, startnode, goal, nodelist, background):
        print 'called traverse'
        openlist = PriorityQueue()
        startnode.priority = 0
        startnode.cost = 0
        openlist.put(startnode)

        while not openlist.empty():
            current = openlist.get()
            # Test visualisations
            createvisualnode(current.location['x'], current.location['y'], background,
                             '/home/ben/Documents/uni_git/artificial_intelligence/sprites/yellow_fighter_up.png')
            if current.goal:
                print 'Found goal at {0} - exiting loop'.format(current.location)

                def reversepath(currentnode, startnode, goalnode):
                    if currentnode is startnode:
                        print 'Reached fighter'
                        createvisualnode(currentnode.location['x'], currentnode.location['y'], background,
                                         '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_up.png')
                    elif currentnode is goalnode:
                        createvisualnode(current.location['x'], current.location['y'], background,
                             '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice.png')
                        reversepath(currentnode.parent, startnode, goalnode)
                    else:
                        createvisualnode(currentnode.location['x'], currentnode.location['y'], background,
                                         '/home/ben/Documents/uni_git/artificial_intelligence/sprites/cyan_fighter_up.png')
                        reversepath(currentnode.parent, startnode, goalnode)

                reversepath(current, startnode, current)
                break

            for neighbour in self.getneighbours(current, nodelist):
                newcost = current.cost + neighbour.cost
                print 'cost: {0} neighbour cost: {1} newcost: {2}'.format(current.cost, neighbour.cost, newcost)
                if neighbour.parent is None or newcost < neighbour.cost:
                    print 'new path node chosen'
                    neighbour.cost = newcost
                    neighbour.priority = self.distancefromgoal(neighbour, goal) + newcost
                    print 'cost: {0} priority: {1}'.format(neighbour.cost, neighbour.priority)
                    openlist.put(neighbour)
                    neighbour.parent = current

    def distancefromgoal(self, node, goal):
        return abs(node.location['x'] - goal.location['x']) + abs(node.location['y'] - goal.location['y'])

    # Get neighbours from a node (add boundary checks here?)
    def getneighbours(self, node, nodelist):
        neighbours = []
        locations = [{'x': node.location['x'] + 1, 'y': node.location['y']},
                     {'x': node.location['x'], 'y': node.location['y'] + 1},
                     {'x': node.location['x'] - 1, 'y': node.location['y']},
                     {'x': node.location['x'], 'y': node.location['y'] - 1}]
        for location in locations:
            for node in nodelist:
                if node.location == location:
                    neighbours.append(node)
        return neighbours


def createfighter(name, imagelist, fightertype = Player):
    fighter = fightertype(name, imagelist)
    if pygame.sprite.spritecollide(fighter, blocklist, False, pygame.sprite.collide_circle):
        fighter.kill()
        fighter = createfighter(name, imagelist, fightertype)
    fighterlist.add(fighter)
    blocklist.add(fighter)
    return fighter

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


def creategoal():
    goalimagelist = {}
    goalimagelist['goal'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice.png'
    goal = Goal(goalimagelist)
    if not pygame.sprite.spritecollide(goal, blocklist, False, pygame.sprite.collide_circle):
        blocklist.add(goal)
    else:
        print 'Goal creation blocked!'
        goal.kill()
        goal = createenemy(goalimagelist)
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

# Test visualisations
def createvisualnode(x, y, background, imagefile):
    screen = pygame.display.get_surface()
    for visualnode in visualnodelist:
        screen.blit(background, visualnode.rect, visualnode.rect)
    visualimagelist = {}
    visualimagelist['image'] = imagefile
    visualnode = Block(visualimagelist)
    visualnode.rect = visualnode.rect.move(x*32, y*32)
    pygame.sprite.spritecollide(visualnode, visualnodelist, True, pygame.sprite.collide_circle)
    visualnodelist.add(visualnode)
    visualnodelist.draw(screen)
    pygame.display.flip()


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

    # Initialise goal
    goal = creategoal()

    # Initialise obstacles
    for i in range(0, 500):
        createobstacle()

    # Initialise players
    playerimagelist = {}
    playerimagelist['up'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_up.png'
    playerimagelist['down'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_down.png'
    playerimagelist['left'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_left.png'
    playerimagelist['right'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_right.png'
    player1 = createfighter('Player one', playerimagelist, Player)

    # Initialise enemies
    # TODO: Use OCEAN model for enemies
    enemyimagelist = {}
    enemyimagelist['up'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_up.png'
    enemyimagelist['down'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_down.png'
    enemyimagelist['left'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_left.png'
    enemyimagelist['right'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_right.png'
    enemyaggressive = createfighter('Aggressive enemy', enemyimagelist, Enemy)

    # Blit to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Initialise Astar
    nodelist = []
    for x in range(24):
        for y in range(24):
            node = Node(x, y)
            for obstacle in obstaclelist:
                if obstacle.location['x'] == x and obstacle.location['y'] == y:
                    if obstacle.strength == 'weak':
                        node.cost = 5
                    elif obstacle.strength == 'strong':
                        node.cost = 10
            if goal.location['x'] == x and goal.location['y'] == y:
                goalnode = node
                node.goal = True
            elif enemyaggressive.location['x'] == x and enemyaggressive.location['y'] == y:
                startnode = node
            nodelist.append(node)

    # Test visualisations
    global visualnodelist
    visualnodelist = pygame.sprite.Group()

    astar = Astar()
    astar.traverse(startnode, goalnode, nodelist, background)


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
                print player1.location
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