try:
    import sys
    from fighter import Fighter
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Player(Fighter):
    """A Player character, inherits from Fighter
    Returns: A player object
    Functions: update, calcNewPos
    Attributes: """