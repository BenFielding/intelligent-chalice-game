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

        # Assign neuralnetwork instance
        self.neuralnetwork = neuralnetwork

        # Initialise goals
        self.initialisechalices()
        numobstacles = 200
        self.initialiseobstacles(numobstacles)
        self.initialiseplayers(numplayers)
        self.initialiseenemies(numenemies)
        self.populaterelationships()

        self.clock = pygame.time.Clock()
        self.scorecard = scorecard

    def populaterelationships(self):
        """
        Populate each fighters friend/enemy (based on colours for autonomous agents) (players are on same team)
        """
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

    def initialiseobstacles(self, numobstacles):
        """
        Create and initialise obstacles (crates and rocks).

        :param numobstacles: (int) Number of obstacles to create
        """
        for i in range(0, numobstacles):
            obstacle = self.createrandomobstacle()
            if obstacle.strength == 'strong':
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.strongmax
            else:
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.weakmax


    def initialiseplayers(self, numplayers):
        """
        Create and initialise players (red and blue). Players are on the same team.
        Add to playerlist

        :param numplayers: (int) Number of players to create (1-2)
        """
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
        """
        Create and initialise randomly coloured enemies. (colours = teams)
        Add to enemylist.

        :param numenemies: (int) Number of enemies to create
        """
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
        Return a Fighter object (recursive until no longer blocked)

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
        Return a random child object of Obstacle object (recursive until no longer blocked)

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

    def initialisechalices(self):
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
        """
        Create a new goal object (recursive until no longer blocked)

        :param goalimagelist: (Dict) Dict of images to create the goal (should contain one, keyed on 'image'))
        :param worth: (int) Points value of the goal
        :param name: (string) Name of the goal
        :return: (Goal) Goal object
        """
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

    def gamewon(self, fighter):
        """
        End the game and display winning message/scoreboard.
        Handle whether or not to play again.

        :param fighter: (Fighter) Winning Fighter object
        :return: (str) Name of winner, (bool) Whether to play again
        """
        font = pygame.font.SysFont("monospace", 32)
        self.screen.blit(self.background, (0, 0))
        if fighter:
            # Update scorecard
            self.scorecard[fighter.name.partition(' ')[0]] += 1
            # render text
            winnertext = font.render('{0} has won with {1} points!'.format(fighter.name, fighter.points), 1, (0, 204, 0))
        else:
            winnertext = font.render('No-one has won this round!', 1, (0, 204, 0))
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
                return False
            elif playagain is 'continue':
                return True

    def calculatepaths(self):
        """
        Use neural network to calculate new target for each autonomous agent.
        Use Astar algorithm to generate best path to new target for each agent.
        """
        for enemy in self.enemylist:
            enemy.calculatenewtarget(self.chalicelist)
            if enemy.target:
                enemy.path = self.astar.traverse(enemy.location, enemy.target.location)

    def updatefighters(self):
        """
        Update location of each fighter based on direction.
        Update Astar nodegraph for new location.
        """
        for fighter in self.fighterlist:
            self.astar.nodegraph[fighter.location['x']][fighter.location['y']].cost = 1
            fighter.update(1, self.fighterobstaclelist)
            self.astar.nodegraph[fighter.location['x']][fighter.location['y']].cost = float('inf')

    def attacksandheals(self):
        """
        Check if fighter is flagged as attacking or healing and trigger action.
        """
        for fighter in self.fighterlist:
            if fighter.attacking:
                self.attackorhealblock(fighter, fighter.direction)

    def updateobstacles(self):
        """
        Update each obstacle, set image based on hp.
        Update Astar nodegraph with obstacles new cost (based on visuals)
        """
        for obstacle in self.obstaclelist:
            obstacle.update()
            if obstacle.strength == 'strong':
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.strongmax
            else:
                self.astar.nodegraph[obstacle.location['x']][obstacle.location['y']].cost = obstacle.weakmax

    def checkgameendstates(self):
        """
        check for any collisions between fighters and chalices.
        Update fighter points and trigger gamewon if necessary.

        :return: (bool) Whether a fighter has won (bool) Whether or not to play again
        """
        # Check if the number of fighters alive is < 2
        if len(self.fighterlist) == 1:
            return True, self.gamewon(self.fighterlist.sprites()[0])
        elif len(self.fighterlist) == 0:
            return True, self.gamewon(None)
        # Check if the number of chalices left is 0
        if len(self.chalicelist) == 0:
            points = -1
            winner = None
            for fighter in self.fighterlist:
                if fighter.points > points:
                    points = fighter.points
                    winner = fighter
            return True, self.gamewon(winner)
        # Check all fighter - chalice gollisions
        for fighter, chalicecollisionlist in pygame.sprite.groupcollide(self.fighterlist, self.chalicelist,
                                                                        False, True,
                                                                        pygame.sprite.collide_circle).iteritems():
                for chalice in chalicecollisionlist:
                    fighter.points += chalice.worth
                if fighter.points >= 30:
                    return True, self.gamewon(fighter)
        return False, None

    def blitallblocks(self):
        for block in self.blocklist:
            self.screen.blit(self.background, block.rect, block.rect)

    def play(self):
        """
        Main game loop, returns the name of the winner and whether or not to play again

        :return: (str) Name of winner, (bool) Whether to play again
        """
        while True:

            # Set the fps to run at
            self.clock.tick(10)

            # Blit all blocks to the screen
            self.blitallblocks()

            # handle all keyevents in the queue, returns false for QUIT
            if self.handlekeyevents() == 'quit':
                return False

            # Calculate new paths
            self.calculatepaths()

            # Update all fighters
            self.updatefighters()

            # Perform attacks and heals
            self.attacksandheals()

            # Update all obstacles
            self.updateobstacles()

            # Draw all blocks
            self.blocklist.draw(self.screen)

            # Update the entire surface
            pygame.display.flip()

            # Check for the end of a game
            winner, playagain = self.checkgameendstates()
            if winner:
                return playagain
