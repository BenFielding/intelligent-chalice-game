try:
    import pygame
    import sys
    import random
    from fighter import Fighter
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Enemy(Fighter):
    """An enemy character, inherits from Fighter
    Returns: An enemy object
    Functions: update
    Attributes: """

    def __init__(self, name, imagelist, colour, screenwidth, screenheight, *groups):
        super(Enemy, self).__init__(name, imagelist, colour, screenwidth, screenheight, *groups)
        self.path = None
        self.direction = None
        self.moving = True
        self.friendlist = []
        self.enemylist = []
        self.neuralnetwork = None
        self.personality = None
        self.target = None

    def update(self, magnitude, obstaclelist):
        """
        Pop direction off LIFO queue path and attempt movement in direction.
        Set attacking to True if movement fails

        :param magnitude: (int) Magnitude of movement
        :param obstaclelist: (pygame.sprite.Group()) List of obstacles which cannot be moved onto
        """
        self.direction = self.path.get()
        self.attacking = not super(Enemy, self).update(magnitude, obstaclelist)

    def calculatenewtarget(self, goallist):
        closestfriend = [99, None]
        for friend in self.friendlist:
            distancetofriend = self.normaliseddistancetotarget(friend)
            if distancetofriend < closestfriend[0]:
                closestfriend = [distancetofriend, friend]

        closestenemy = [99, None]
        for enemy in self.enemylist:
            distancetoenemy = self.normaliseddistancetotarget(enemy)
            if distancetoenemy < closestenemy[0]:
                closestenemy = [distancetoenemy, enemy]

        closestgoal = [99, None]
        for goal in goallist:
            distancetogoal = self.normaliseddistancetotarget(goal)
            if distancetogoal < closestgoal[0]:
                closestgoal = [distancetogoal, goal]

        outcome = self.neuralnetwork.recallnetwork([self.personality.aggressiveness,
                                                   self.personality.friendliness,
                                                   self.personality.ambitiousness,
                                                   closestenemy[0],
                                                   closestfriend[0],
                                                   closestgoal[0]])
        max = -1
        position = 0
        for count in range(len(outcome)):
            if outcome[count] > max:
                max = outcome[count]
                position = count

        if position == 0:
            self.target = closestenemy[1]
        elif position == 1:
            self.target = closestfriend[1]
        elif position == 2:
            self.target = closestgoal[1]
        else:
            self.target = None

    def normaliseddistancetotarget(self, target):
        """
        Return the normalised manhattan distance from the specified target
        Normalise method:
        (1/70 ~= 0.01429)

        :return: (float) Normalised (between 0 and 1) manhattan distance to target
        """

        return abs(self.location['x'] - target.location['x']) + abs(self.location['y'] - target.location['y']) * 0.01429