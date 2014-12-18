#!/usr/bin/python

try:
    import sys
    from game import Game
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

def main():

    numplayers = None
    numenemies = None
    print 'Welcome to the game'
    while numplayers not in [1, 2]:
        try:
            numplayers = int(raw_input('Please enter the number of players(1-2):'))
        except ValueError:
            print 'Invalid entry'
    print 'Player one will be blue'
    if numplayers == 2:
        'Player two will be red'
    #while numenemies not in range(0, 6):
    while numenemies not in range(0, 9999999):
        try:
            numenemies = int(raw_input('Please enter the number of enemies:'))
        except ValueError:
            print 'Invalid entry'
    print
    raw_input('Hit RETURN to start the game')

    playagain = True

    while playagain:
        print
        game = Game(numplayers, numenemies)
        winner, playagain = game.play()
        print '{0} won this round!'.format(winner)

if __name__ == '__main__':
    main()