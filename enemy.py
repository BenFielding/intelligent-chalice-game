import pygame
import sys
import random
import Queue
from fighter import Fighter


class Enemy(Fighter):
    """An enemy character, inherits from Fighter
    Returns: An enemy object
    Functions: update
    Attributes: """

    def __init__(self, name, imagelist, colour, screenwidth, screenheight, *groups):
        super(Enemy, self).__init__(name, imagelist, colour, screenwidth, screenheight, *groups)
        self.direction = None
        self.moving = True
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
        try:
            self.direction = self.path.get(False)
        except Queue.Empty:
            self.direction = None
        else:
            self.attacking = not super(Enemy, self).update(magnitude, obstaclelist)

    def calculatenewtarget(self, goallist):
        closestfriend = [99, 99, None]
        for friend in self.friendlist:
            distancetofriend = self.normaliseddistancetotarget(friend)
            if distancetofriend < closestfriend[0]:
                closestfriend = [distancetofriend, self.normalisedhp(friend.hp), friend]

        closestenemy = [99, 99, None]
        for enemy in self.enemylist:
            distancetoenemy = self.normaliseddistancetotarget(enemy)
            if distancetoenemy < closestenemy[0]:
                closestenemy = [distancetoenemy, self.normalisedhp(enemy.hp), enemy]

        closestgoal = [99, 99, None]
        for goal in goallist:
            distancetogoal = self.normaliseddistancetotarget(goal)
            if distancetogoal < closestgoal[0]:
                closestgoal = [distancetogoal, self.normalisedgoalworth(goal.worth), goal]

        outcome = self.neuralnetwork.recallnetwork([self.personality.aggressiveness,
                                                   self.personality.friendliness,
                                                   self.personality.ambitiousness,
                                                   self.hp,
                                                   closestenemy[0],
                                                   closestenemy[1],
                                                   closestfriend[0],
                                                   closestfriend[1],
                                                   closestgoal[0],
                                                   closestgoal[1]])
        max = -1
        position = 0
        for count in range(len(outcome)):
            if outcome[count] > max:
                max = outcome[count]
                position = count

        if position == 0:
            self.target = closestenemy[2]
        elif position == 1:
            self.target = closestfriend[2]
        elif position == 2:
            self.target = closestgoal[2]
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

    def normalisedhp(self, hp):
        """
        Return the normalised hitpoint value
        Normalise method:
        (1/15 ~= 0.06667)

        :return: (float) Normalised (between 0 and 1) hitpoint value
        """
        return hp * 0.06667

    def normalisedgoalworth(self, goalworth):
        """
        Return the normalised goal worth
        Normalise method:
        (1/32 ~= 0.03125)

        :return: (float) Normalised (between 0 and 1) goal worth
        """
        return goalworth * 0.03125
