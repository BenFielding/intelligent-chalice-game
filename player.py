try:
    import sys
    from Queue import LifoQueue
    from fighter import Fighter
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Player(Fighter):
    """A Player character, inherits from Fighter
    Returns: A player object
    Functions: update, calcNewPos
    Attributes: """

    def __init__(self, name, imagelist, screenwidth, screenheight, *groups):
        super(Player, self).__init__(name, imagelist, screenwidth, screenheight, *groups)
        self.directionqueue = LifoQueue()
        self.directiondict = {'up': False, 'down': False, 'left': False, 'right': False}

    def handlekeyevent(self, keyevent):
        if keyevent['action'] == 'keydown':
            if keyevent['key'] in self.directiondict:
                self.directiondict[keyevent['key']] = True
                self.directionqueue.put(keyevent['key'])
                self.direction = keyevent['key']
                self.moving = True
            elif keyevent['key'] == 'space':
                self.attacking = True
        elif keyevent['action'] == 'keyup':
            if keyevent['key'] in self.directiondict:
                self.directiondict[keyevent['key']] = False
            elif keyevent['key'] == 'space':
                self.attacking = False
            if keyevent['key'] in self.directiondict and self.moving:
                if not self.directiondict[self.direction]:
                    while not self.directionqueue.empty():
                        self.direction = self.directionqueue.get()
                        if self.directiondict[self.direction]:
                            break
                    if self.directionqueue.empty():
                        self.moving = False
                        for direction, active in self.directiondict.iteritems():
                            if active:
                                self.direction = direction
                                self.moving = True