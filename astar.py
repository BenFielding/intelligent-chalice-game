try:
    from Queue import *
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Node(object):

    def __init__(self, x, y):
        self.location = {'x': x, 'y': y}
        self.goal = False
        self.parent = None
        self.priority = 999999
        self.cost = 1
        self.costsofar = 0
        self.direction = 'none'

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

class Astar(object):

    def __init__(self, obstaclelist, startblock, endblock):
        self.nodelist = []
        for x in range(24):
            for y in range(24):
                node = Node(x, y)
                for obstacle in obstaclelist:
                    if obstacle.location['x'] == x and obstacle.location['y'] == y:
                        if obstacle.strength == 'weak':
                            node.cost = obstacle.weakmax
                        elif obstacle.strength == 'strong':
                            node.cost = obstacle.strongmax
                if endblock.location['x'] == x and endblock.location['y'] == y:
                    self.goalnode = endblock
                    node.goal = True
                elif startblock.location['x'] == x and startblock.location['y'] == y:
                    self.startnode = node
                self.nodelist.append(node)

    def traverse(self):
        openlist = PriorityQueue()
        chosenpath = LifoQueue()
        self.startnode.priority = 0
        self.startnode.cost = 0
        openlist.put(self.startnode)

        while not openlist.empty():
            current = openlist.get()
            if current.goal:

                def reversepath(current, startnode, goalnode):
                    if current is startnode:
                        return
                    else:
                        chosenpath.put(current.direction)
                        reversepath(current.parent, startnode, goalnode)

                reversepath(current, self.startnode, current)
                break
            for neighbour in self.getneighbours(current):
                newcost = current.costsofar + neighbour['node'].cost
                if neighbour['node'].parent is None or newcost < neighbour['node'].costsofar:
                    neighbour['node'].costsofar = newcost
                    neighbour['node'].priority = self.distancefromgoal(neighbour['node'], self.goalnode) + newcost
                    neighbour['node'].direction = neighbour['dir']
                    neighbour['node'].parent = current
                    openlist.put(neighbour['node'])
        return chosenpath

    def distancefromgoal(self, node, goal):
        return abs(node.location['x'] - goal.location['x']) + abs(node.location['y'] - goal.location['y'])

    # Get neighbours from a node (add boundary checks here?)
    def getneighbours(self, node):
        neighbours = []
        locations = {'right': {'x': node.location['x'] + 1, 'y': node.location['y']},
                     'down': {'x': node.location['x'], 'y': node.location['y'] + 1},
                     'left': {'x': node.location['x'] - 1, 'y': node.location['y']},
                     'up': {'x': node.location['x'], 'y': node.location['y'] - 1}}
        for direction, location in locations.iteritems():
            for node in self.nodelist:
                if node.location == location:
                    neighbours.append({'dir': direction, 'node': node})
        return neighbours