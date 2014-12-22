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
    from fuzzy import Fuzzyocean
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Game(object):

    def __init__(self, numplayers, numenemies, neuralnetwork, scorecard):
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
        # List of all active chalices
        self.chalicelist = pygame.sprite.Group()

        # Create astar instance
        self.astar = Astar(self.screen.get_width()/32, self.screen.get_height()/32)

        self.neuralnetwork = neuralnetwork

        # Initialise goals
        self.createchalices()
        # astar.nodegraph[self.goal.location['x']][self.goal.location['y']] = True

        # Initialise obstacles
        for i in range(0, 100):
            obstacle = self.createrandomobstacle()
            if obstacle.strength == 'strong':
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.strongmax
            else:
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.weakmax

        self.initialiseplayers(numplayers)
        self.initialiseenemies(numenemies)
        self.populaterelationships()

        # Initialise clock
        self.clock = pygame.time.Clock()

        self.scorecard = scorecard

    def populaterelationships(self):
        for enemy in self.enemylist:
            for enemycomparison in self.enemylist:
                if enemycomparison is not enemy and enemy.colour is enemycomparison.colour:
                    enemy.friendlist.add(enemycomparison)
                elif enemycomparison is not enemy:
                    enemy.enemylist.add(enemycomparison)
            for player in self.playerlist:
                enemy.enemylist.add(player)
        for player in self.playerlist:
            player.enemylist = self.enemylist
            for playercomparison in self.playerlist:
                if playercomparison is not player:
                    player.friendlist.add(playercomparison)

    def initialiseplayers(self, numplayers):
        imagedirectionlist = ['up', 'down', 'left', 'right']
        self.numplayers = numplayers
        playerimagelist = {}
        for direction in imagedirectionlist:
            playerimagelist[direction] = \
                '/home/ben/Documents/uni_git/artificial_intelligence/sprites/blue_fighter_{0}.png'.format(direction)
        self.player1 = self.createfighter('Player 1', playerimagelist, 'blue', Player)
        self.playerlist.add(self.player1)
        if self.numplayers == 2:
            for direction in imagedirectionlist:
                playerimagelist[direction] = \
                    '/home/ben/Documents/uni_git/artificial_intelligence/sprites/red_fighter_{0}.png'.format(direction)
            self.player2 = self.createfighter('Player 2', playerimagelist, 'red', Player)
            self.playerlist.add(self.player2)

    def initialiseenemies(self, numenemies):
        imagedirectionlist = ['up', 'down', 'left', 'right']
        if numenemies > 0:
            enemycolourlist = ['yellow', 'pink', 'cyan', 'green', 'orange']
            enemypersonalities = {'yellow': Fuzzyocean(random.randrange(101),
                                                       random.randrange(101),
                                                       random.randrange(101),
                                                       random.randrange(101),
                                                       random.randrange(101)),
                                  'pink': Fuzzyocean(random.randrange(101),
                                                     random.randrange(101),
                                                     random.randrange(101),
                                                     random.randrange(101),
                                                     random.randrange(101)),
                                  'cyan': Fuzzyocean(random.randrange(101),
                                                     random.randrange(101),
                                                     random.randrange(101),
                                                     random.randrange(101),
                                                     random.randrange(101)),
                                  'green': Fuzzyocean(random.randrange(101),
                                                      random.randrange(101),
                                                      random.randrange(101),
                                                      random.randrange(101),
                                                      random.randrange(101)),
                                  'orange': Fuzzyocean(random.randrange(101),
                                                       random.randrange(101),
                                                       random.randrange(101),
                                                       random.randrange(101),
                                                       random.randrange(101))}
            enemycolourcount = {'yellow': 0, 'pink': 0, 'cyan': 0, 'green': 0, 'orange': 0}
            for enemynumber in range(0, numenemies):
                enemyimagelist = {}
                colour = random.choice(enemycolourlist)
                enemycolourcount[colour] += 1
                for direction in imagedirectionlist:
                    enemyimagelist[direction] = \
                        '/home/ben/Documents/uni_git/artificial_intelligence/sprites/{0}_fighter_{1}.png' \
                        .format(colour, direction)
                enemy = self.createfighter('{0} enemy {1}'.format(colour, enemycolourcount[colour]),
                                           enemyimagelist, colour, Enemy)
                enemy.personality = enemypersonalities[colour]
                enemy.neuralnetwork = self.neuralnetwork
                self.enemylist.add(enemy)

    def createfighter(self, name, imagelist, colour, fightertype = Player):
        """
        Return a Fighter object

        :param name: (str) The name of the fighter
        :param imagelist: (dict) Dictionary of image locations (keyed by direction)
        :param fightertype: (class) Type of fighter
        :return: (Fighter) Fighter object
        """
        fighter = fightertype(name, imagelist, colour, self.screen.get_width(), self.screen.get_height())
        if pygame.sprite.spritecollide(fighter, self.blocklist, False, pygame.sprite.collide_circle):
            fighter.kill()
            fighter = self.createfighter(name, imagelist, colour, fightertype)
        self.fighterlist.add(fighter)
        self.fighterobstaclelist.add(fighter)
        self.blocklist.add(fighter)
        return fighter

    def createrandomobstacle(self):
        """
        Return a random child object of Obstacle object

        :return: (Crate or Rock) Crate or Rock (derived from Obstacle) object
        """
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

    def createchalices(self):
        """
        Create chalices and add to chalicelist

        """
        for i in range(1):
            chaliceimagelist = {}
            chaliceimagelist['image'] = \
                '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice_gold_gems.png'
            self.goal = self.creategoal(chaliceimagelist, 32, 'gold encrusted')
            self.chalicelist.add(self.goal)
            for i in range(2):
                chaliceimagelist['image'] = \
                    '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice_gold.png'
                self.chalicelist.add(self.creategoal(chaliceimagelist, 16, 'gold'))
                for i in range(2):
                    chaliceimagelist['image'] = \
                        '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice_silver_gems.png'
                    self.chalicelist.add(self.creategoal(chaliceimagelist, 8, 'silver encrusted'))
                    for i in range(2):
                        chaliceimagelist['image'] = \
                            '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice_silver.png'
                        self.chalicelist.add(self.creategoal(chaliceimagelist, 4, 'silver'))
                        for i in range(2):
                            chaliceimagelist['image'] = \
                                '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice_wood_gems.png'
                            self.chalicelist.add(self.creategoal(chaliceimagelist, 2, 'wood encrusted'))
                            for i in range(2):
                                chaliceimagelist['image'] = \
                                    '/home/ben/Documents/uni_git/artificial_intelligence/sprites/chalice_wood.png'
                                self.chalicelist.add(self.creategoal(chaliceimagelist, 1, 'wood'))

    def creategoal(self, goalimagelist, worth, name):
        goal = Goal(goalimagelist, worth, name, self.screen.get_width(), self.screen.get_height())
        if not pygame.sprite.spritecollide(goal, self.blocklist, False, pygame.sprite.collide_circle):
            self.blocklist.add(goal)
        else:
            goal.kill()
            goal = self.creategoal(goalimagelist, worth, name)
        return goal

    def attackorhealblock(self, originator, direction):
        """
        Attack or heal block in direction from originator (depending on if the block is an obstacle, enemy, or friend)

        :param originator: (pygame.sprite.Sprite) Sprite originator
        :param direction: (str) Direction of attack from originator
        """
        targetlocation = {'x': originator.location['x'], 'y': originator.location['y']}
        if direction == 'up':
            targetlocation['y'] = originator.location['y'] - 1
        elif direction == 'down':
            targetlocation['y'] = originator.location['y'] + 1
        elif direction == 'left':
            targetlocation['x'] = originator.location['x'] - 1
        elif direction == 'right':
            targetlocation['x'] = originator.location['x'] + 1
        else:
            targetlocation = None

        if targetlocation:
            foundblock = None
            for block in self.blocklist:
                if block.location == targetlocation:
                    foundblock = block

            if foundblock in self.obstaclelist:
                foundblock.hp -= 1
            elif foundblock in originator.enemylist:
                foundblock.attacked(1)
            elif foundblock in originator.friendlist:
                foundblock.healed(1)

            if foundblock and foundblock.hp <= 0:
                if foundblock in self.fighterlist:
                    print '{0} has been killed by {1}!'.format(foundblock.name, originator.name)
                foundblock.kill()
                self.astar.nodegraph[foundblock.location['x']][foundblock.location['y']].cost = 1
                if originator in self.enemylist:
                    originator.target = None


    def handlekeyevents(self):
        """
        Loop through event queue and interpret events based on rules

        :return: (str) Return 'quit', 'continue' or ''
        """
        player1keymapping = {K_w: 'up', K_s: 'down', K_a: 'left', K_d: 'right', K_SPACE: 'fire'}
        player2keymapping = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right', K_RCTRL: 'fire'}
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
        return ''

    def play(self):
        """
        Main game loop, returns the name of the winner and whether or not to play again

        :return: (str, bool) Name of winner, playagain
        """
        while True:

            # Set the fps to run at
            self.clock.tick(10)

            # Blit all blocks to the screen
            for block in self.blocklist:
                self.screen.blit(self.background, block.rect, block.rect)

            # handle all keyevents in the queue, returns false for QUIT
            if self.handlekeyevents() == 'quit':
                return 'no-one', False

            # Calculate new paths
            for enemy in self.enemylist:
                enemy.calculatenewtarget(self.chalicelist)
                if enemy.target:
                    enemy.path = self.astar.traverse(enemy.location, enemy.target.location)

            # Update all fighters
            for fighter in self.fighterlist:
                self.astar.nodegraph[fighter.location['x']][fighter.location['y']].cost = 1
                fighter.update(1, self.fighterobstaclelist)
                self.astar.nodegraph[fighter.location['x']][fighter.location['y']].cost = float('inf')

            # Check if fighters are attacking obstacles, attack if so
            for fighter in self.fighterlist:
                if fighter.attacking:
                    self.attackorhealblock(fighter, fighter.direction)

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

            # Check for fighter collision with the goal
            for fighter, chalicecollisionlist in pygame.sprite.groupcollide(self.fighterlist, self.chalicelist,
                                                        False, True, pygame.sprite.collide_circle).iteritems():
                for chalice in chalicecollisionlist:
                    fighter.points += chalice.worth
                if fighter.points >= 40:
                    font = pygame.font.SysFont("monospace", 32)
                    # Update scorecard
                    self.scorecard[fighter.name.partition(' ')[0]] += 1
                    # render text
                    self.screen.blit(self.background, (0, 0))
                    winnertext = font.render('{0} has won with {1} points!'.format(fighter.name, fighter.points), 1, (0, 204, 0))
                    scoreslist = []
                    for key, value in self.scorecard.iteritems():
                        if key == 'Player':
                            colours = (51, 51, 255)
                        else:
                            colours = (255, 52, 51)
                        scoreslist.append(font.render('{0} team has {1} points'.format(key, value), 1, colours))
                    playagaintext = font.render('Hit RETURN to play again or ESC to quit', 1, (0, 204, 0))
                    self.screen.blit(winnertext, (self.screen.get_width() / 8, self.screen.get_height() / 10))
                    count = 2
                    for item in scoreslist:
                        self.screen.blit(item, (self.screen.get_width() / 8, self.screen.get_height() / 10 * count))
                        count += 1
                    self.screen.blit(playagaintext, (self.screen.get_width() / 8,
                                                     (self.screen.get_height() / 10) * count))
                    pygame.display.flip()
                    while True:
                        playagain = self.handlekeyevents()
                        if playagain is 'quit':
                            return fighter.name, False
                        elif playagain is 'continue':
                            return fighter.name, True