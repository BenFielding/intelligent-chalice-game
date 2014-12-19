try:
    import sys
    from Queue import *
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)


class Node(object):

    def __init__(self, x, y):
        self.cost = 1
        self.direction = 'none'
        self.neighbours = []
        self.location = {'x': x, 'y': y}


class Astar(object):

    def __init__(self, gridwidth, gridheight):
        self.nodegraph = [[Node(x, y) for x in range(gridwidth)] for y in range(gridheight)]
        for x in range(len(self.nodegraph)):
            for y in range(len(self.nodegraph[x])):
                node = self.nodegraph[x][y]
                locations = {}
                if x < gridwidth - 1:
                    locations['right'] = {'x': x + 1, 'y': y}
                if x > 0:
                    locations['left'] = {'x': x - 1, 'y': y}
                if y < gridheight - 1:
                    locations['down'] = {'x': x, 'y': y + 1}
                if y > 0:
                    locations['up'] = {'x': x, 'y': y - 1}
                for direction, neighbourlocation in locations.iteritems():
                    if self.nodegraph[neighbourlocation['x']][neighbourlocation['y']]:
                        node.neighbours.append({'dir': direction,
                                                'node': self.nodegraph[neighbourlocation['x']][neighbourlocation['y']]})

    def traverse(self, startlocation, endlocation):
        """
        Return LIFO queue of individual directions to reach end location from start location

        :param startlocation: (dict) Dictionary of start location (keyed with 'x' and 'y')
        :param endlocation:  (dict) Dictionary of end location (keyed with 'x' and 'y')
        :return: (LifoQueue) LIFO queue of directions to reach end location from start location
        """
        openlist = PriorityQueue()
        chosenpath = LifoQueue()
        costsofar = {}
        parent = {}
        startnode = self.nodegraph[startlocation['x']][startlocation['y']]
        endnode = self.nodegraph[endlocation['x']][endlocation['y']]
        costsofar[startnode] = 0
        openlist.put((0, startnode))

        while not openlist.empty():
            current = openlist.get()[1]
            if current is endnode:

                def reversepath(current, startnode):
                    if current is startnode:
                        return
                    else:
                        chosenpath.put(current.direction)
                        reversepath(parent[current], startnode)

                reversepath(current, startnode)
                break
            for neighbour in current.neighbours:
                newcost = costsofar[current] + neighbour['node'].cost
                if neighbour['node'] not in parent or newcost < costsofar[neighbour['node']]:
                    costsofar[neighbour['node']] = newcost
                    priority = self.distancefromgoal(neighbour['node'], endnode) + newcost
                    neighbour['node'].direction = neighbour['dir']
                    parent[neighbour['node']] = current
                    openlist.put((priority, neighbour['node']))
        return chosenpath

    def distancefromgoal(self, node, goal):
        """
        Return the Manhattan distance between two nodes

        :param node: (Node) Start node
        :param goal: (Node) End node
        :return: (int) Manhattan distance between Start node and End node
        """
        return abs(node.location['x'] - goal.location['x']) + abs(node.location['y'] - goal.location['y'])