import sys
import random
from block import Block


class Goal(Block):
    """An obstacle, inherits from block
    Returns: An obstacle object
    Function:
    Attributes:"""

    def __init__(self, imagefile, worth, name, screenwidth, screenheight, *groups):
        super(Goal, self).__init__(imagefile, screenwidth, screenheight, *groups)
        self.worth = worth
        self.name = name
        self.update()
