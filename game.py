try:
    import pygame
    import sys
    import random
    from itertools import cycle
    from pygame.locals import *
    from Queue import *
    from block import Block
    from fighter import Fighter
    from enemy import Enemy
    from player import Player
    from obstacle import *
    from goal import Goal
    from astar import *
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Game(object):

    def __init__(self, numplayers, numenemies):
        # Initialise screen
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 1024))
        pygame.display.set_caption('Artificial intelligence assignment')

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        # Initialise sprite groups
        # List of all active blocks
        self.blocklist = pygame.sprite.Group()

        # List of all active fighters
        self.fighterlist = pygame.sprite.Group()

        # List of all active players
        self.playerlist = pygame.sprite.Group()

        # List of all active enemies
        self.enemylist = pygame.sprite.Group()

        # List of all active obstacles
        self.obstaclelist = pygame.sprite.Group()

        # List of all active fighters and obstacles
        self.fighterobstaclelist = pygame.sprite.Group()

        self.astar = Astar(self.screen.get_width()/32, self.screen.get_height()/32)

        # Initialise goal
        self.goal = self.creategoal()
        # astar.nodegraph[self.goal.location['x']][self.goal.location['y']] = True

        # Initialise obstacles
        for i in range(0, 500):
            obstacle = self.createrandomobstacle()
            if obstacle.strength == 'strong':
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.strongmax
            else:
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.weakmax

        # Initialise fighters
        imagedirectionlist = ['up', 'down', 'left', 'right']

        # Initialise players
        self.numplayers = numplayers
        playerimagelist = {}
        for direction in imagedirectionlist:
            playerimagelist[direction] = \
                '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_{0}.png'.format(direction)
        self.player1 = self.createfighter('Player one', playerimagelist, Player)
        self.playerlist.add(self.player1)
        if self.numplayers == 2:
            for direction in imagedirectionlist:
                playerimagelist[direction] = \
                    '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_{0}.png'.format(direction)
            self.player2 = self.createfighter('Player two', playerimagelist, Player)
            self.playerlist.add(self.player2)

        # Initialise enemies
        # TODO: Use OCEAN model for enemies?
        if numenemies > 0:
            enemycolourlist = ['yellow', 'pink', 'cyan', 'green', 'orange']
            for enemynumber in range(0, numenemies):
                enemyimagelist = {}
                colour = random.choice(enemycolourlist)
                for direction in imagedirectionlist:
                    # enemyimagelist[direction] = \
                    #     '/home/ben/Documents/uni_git/artificial_intelligence/sprites/{0}_fighter_{1}.png' \
                    #     .format(enemycolourlist[enemynumber], direction)
                    enemyimagelist[direction] = \
                        '/home/ben/Documents/uni_git/artificial_intelligence/sprites/{0}_fighter_{1}.png' \
                        .format(colour, direction)
                #enemy = self.createfighter('{0} enemy'.format(enemycolourlist[enemynumber]), enemyimagelist, Enemy)
                enemy = self.createfighter('{0} enemy'.format(colour), enemyimagelist, Enemy)
                self.enemylist.add(enemy)

        # Initialise clock
        self.clock = pygame.time.Clock()

    def createfighter(self, name, imagelist, fightertype = Player):
        fighter = fightertype(name, imagelist, self.screen.get_width(), self.screen.get_height())
        if pygame.sprite.spritecollide(fighter, self.blocklist, False, pygame.sprite.collide_circle):
            fighter.kill()
            fighter = self.createfighter(name, imagelist, fightertype)
        self.fighterlist.add(fighter)
        self.fighterobstaclelist.add(fighter)
        self.blocklist.add(fighter)
        return fighter

    def createrandomobstacle(self):
        obstacleimagelistchoice = \
            {'crate': {'strong': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate_metal.png',
                       'weak': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/crate_wood.png'},
             'rock': {'strong': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/rock_strong.png',
                      'weak': '/home/ben/Documents/uni_git/artificial_intelligence/sprites/rock_weak.png'}}
        obstaclename, obstacletype = random.choice([['crate', Crate], ['rock', Rock]])
        obstacle = obstacletype(obstacleimagelistchoice[obstaclename], obstaclename, self.screen.get_width(), self.screen.get_height())
        if not pygame.sprite.spritecollide(obstacle, self.blocklist, False, pygame.sprite.collide_circle):
            self.obstaclelist.add(obstacle)
            self.fighterobstaclelist.add(obstacle)
            self.blocklist.add(obstacle)
        else:
            obstacle.kill()
            self.createrandomobstacle()
        return obstacle

    def creategoal(self):
        goalimagelist = {}
        goalimagelist['goal'] = '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice.png'
        goal = Goal(goalimagelist, self.screen.get_width(), self.screen.get_height())
        if not pygame.sprite.spritecollide(goal, self.blocklist, False, pygame.sprite.collide_circle):
            self.blocklist.add(goal)
        else:
            print 'Goal creation blocked!'
            goal.kill()
            goal = self.creategoal()
        return goal

    def attackobstacle(self, location, direction):
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
        for obstacle in self.obstaclelist:
            if obstacle.location == objlocation:
                foundobstacle = obstacle

        if foundobstacle:
            foundobstacle.hp -= 1
            if foundobstacle.hp <= 0:
                foundobstacle.kill()

    def handlekeyevents(self):
        player1keymapping = {K_w: 'up', K_s: 'down', K_a: 'left', K_d: 'right', K_SPACE: 'space'}
        player2keymapping = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right', K_RCTRL: 'space'}
        eventmapping = {KEYDOWN: 'keydown', KEYUP: 'keyup'}
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return 'quit'
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return 'continue'
            elif event.type in eventmapping:
                if event.key in player1keymapping:
                    self.player1.handlekeyevent({'key': player1keymapping[event.key],
                                                 'action': eventmapping[event.type]})
                if self.numplayers == 2 and event.key in player2keymapping:
                    self.player2.handlekeyevent({'key': player2keymapping[event.key],
                                                 'action': eventmapping[event.type]})

    def play(self):
        while True:

            # Set the fps to run at
            self.clock.tick(60)

            # Blit all blocks to the screen
            for block in self.blocklist:
                self.screen.blit(self.background, block.rect, block.rect)

            # handle all keyevents in the queue, returns false for QUIT
            if self.handlekeyevents() == 'quit':
                return 'no-one', False

            # # Calculate new paths
            for enemy in self.enemylist:
                enemy.path = self.astar.traverse(enemy.location, self.goal.location)

            # Update all fighters
            self.fighterlist.update(1, self.fighterobstaclelist)

            # Check if fighters are attacking obstacles, attack if so
            for fighter in self.fighterlist:
                if fighter.attacking:
                    self.attackobstacle(fighter.location, fighter.direction)

            # Update all obstacles
            # self.astar = self.obstaclelist.update(self.astar)
            for obstacle in self.obstaclelist:
                obstacle.update()
                if obstacle.strength == 'strong':
                    self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.strongmax
                else:
                    self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.weakmax

            # Draw all blocks
            self.blocklist.draw(self.screen)

            # Update the entire surface
            pygame.display.flip()

            # TODO: Handle collisions with other fighters to avoid two winners
            # Check for fighter collision with the goal
            winner = pygame.sprite.spritecollide(self.goal, self.fighterlist, False, pygame.sprite.collide_circle)
            if winner:
                font = pygame.font.SysFont("monospace", 32)
                # render text
                self.screen.blit(self.background, (0, 0))
                winnertext = font.render('{0} has reached the chalice!'.format(winner[0].name), 1, (0, 204, 0))
                playagaintext = font.render('hit RETURN to play again or ESC to quit', 1, (0, 204, 0))
                self.screen.blit(winnertext, (self.screen.get_width()/8, self.screen.get_height()/3))
                self.screen.blit(playagaintext, (self.screen.get_width()/8, (self.screen.get_height()/3)*2))
                pygame.display.flip()
                while True:
                    playagain = self.handlekeyevents()
                    if playagain is 'quit':
                        return winner[0].name, False
                    elif playagain is 'continue':
                        return winner[0].name, True