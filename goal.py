try:
    import sys
    import random
    from block import Block
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Goal(Block):
    """An obstacle, inherits from block
    Returns: An obstacle object
    Function:
    Attributes:"""

    def __init__(self, imagefile, screenwidth, screenheight, *groups):
        super(Goal, self).__init__(imagefile, screenwidth, screenheight, *groups)
        self.update()