try:
    import sys
    import random
    import math
except ImportError, err:
    print "Couldn't load module:\n {}".format(err)
    sys.exit(2)


class Neuronlayer(object):

    def __init__(self, numbernodes, numberchildnodes, numberparentnodes, learningrate, momentumfactor):
        """
        Returns a new Neuronlayer object

        :param numbernodes: (int) Number of nodes in the layer
        :param numberchildnodes: (int) Number of nodes in the child layer
        :param numberparentnodes: (int) Number of nodes in the parent layer
        :param learningrate: (float) The learning rate
        :param momentumfactor: (float) The momentum factor
        :return: (Neuronlayer) Neuronlayer object
        """
        self.numbernodes = numbernodes
        self.numberchildnodes = numberchildnodes
        self.numberparentnodes = numberparentnodes

        self.parentlayer = None
        self.childlayer = None

        self.neuronvalues = [0 for i in range(numbernodes)]
        self.targetvalues = [0 for i in range(numbernodes)]
        self.errors = [0 for i in range(numbernodes)]

        self.weights = [[random.uniform(-1.0, 1.0) for i in range(numberchildnodes)] for j in range(numbernodes)]
        self.weightchanges = [[0 for i in range(numberchildnodes)] for j in range(numbernodes)]
        self.biasvalues = [-1 for i in range(numberchildnodes)]
        self.biasweights = [random.uniform(-1.0, 1.0) for i in range(numberchildnodes)]

        self.learningrate = float(learningrate)


        self.momentumfactor = momentumfactor

        for i in range(numbernodes):
            self.neuronvalues.append(0)
            self.targetvalues.append(0)
            self.errors.append(0)

    def initialise(self, parentlayer, childlayer):
        """
        Set parent and child layer attributes

        :param parentlayer: (Neuronlayer) Parent Neuronlayer object
        :param childlayer: (Neuronlayer) Child Neuronlayer object
        """
        self.parentlayer = parentlayer
        self.childlayer = childlayer

    def sigmoid(self, action):
        """
        Apply sigmoid function and return output

        :param action: (float) Input to function
        :return: (float) Result of function
        """
        return 1.0 / (1.0 + math.exp(-action))

    def calculateneuronvalues(self):
        """
        Calculate neuron values for this run (not input layer)
        """
        if self.parentlayer is not None:
            for j in range(self.numbernodes):
                action = 0
                for i in range(self.numberparentnodes):
                    action += self.parentlayer.neuronvalues[i] * self.parentlayer.weights[i][j]
                action += self.parentlayer.biasvalues[j] * self.parentlayer.biasweights[j]
                self.neuronvalues[j] = self.sigmoid(action)

    def calculateerrors(self):
        """
        Calculate errors for this run (not input layer)
        """
        # Output layer
        if self.childlayer is None:
            for i in range(self.numbernodes):
                self.errors[i] = (self.targetvalues[i] - self.neuronvalues[i]) * \
                                 self.neuronvalues[i] * (1.0 - self.neuronvalues[i])
        # Input layer
        elif self.parentlayer is None:
            for i in range(self.numbernodes):
                self.errors[i] = 0.0
        # Hidden layer
        else:
            for i in range(self.numbernodes):
                sum = 0
                for j in range(self.numberchildnodes):
                    sum += self.childlayer.errors[j] * self.weights[i][j]
                self.errors[i] = sum * self.neuronvalues[i] * (1.0 - self.neuronvalues[i])

    def adjustweights(self):
        """
        Adjust weights for this run (not output layer)
        """
        if self.childlayer is not None:
            for i in range(self.numbernodes):
                for j in range(self.numberchildnodes):
                    dw = self.learningrate * self.childlayer.errors[j] * self.neuronvalues[i]
                    self.weights[i][j] += dw + self.momentumfactor * self.weightchanges[i][j]
                    self.weightchanges[i][j] = dw
            for j in range(self.numberchildnodes):
                self.biasweights[j] += self.learningrate * self.childlayer.errors[j] * self.biasvalues[j]


class Neuralnetwork(object):

    def __init__(self, numberinputs, numberhiddennodes, numberoutputs, learningrate, momentumfactor):
        """

        :param numberinputs: (int) Number of inputs to network
        :param numberhiddennodes: (int) Number of hidden nodes in network
        :param numberoutputs: (int) Number of outputs to network
        :param learningrate: (float) Learning rate of network
        :param momentumfactor: (float) Momentum factor of network
        :return: (Neuralnetwork) Neuralnetwork object
        """
        self.inputlayer = Neuronlayer(numberinputs, numberhiddennodes, 0, learningrate, momentumfactor)
        self.hiddenlayer = Neuronlayer(numberhiddennodes, numberoutputs, numberinputs, learningrate, momentumfactor)
        self.outputlayer = Neuronlayer(numberoutputs, 0, numberhiddennodes, learningrate, momentumfactor)

        self.inputlayer.initialise(None, self.hiddenlayer)
        self.hiddenlayer.initialise(self.inputlayer, self.outputlayer)
        self.outputlayer.initialise(self.hiddenlayer, None)


    def setinput(self, position, value):
        """
        Input value into the network

        :param position: (int) Position of the input value
        :param value: (float) Value to input
        """
        self.inputlayer.neuronvalues[position] = value

    def settarget(self, position, value):
        """
        Input target output value to the network

        :param position: (int) Position of the target output value
        :param value: (float) Value of target output
        """
        self.outputlayer.targetvalues[position] = value

    def feedforward(self):
        """
        Feed information through the neural network
        """
        self.inputlayer.calculateneuronvalues()
        self.hiddenlayer.calculateneuronvalues()
        self.outputlayer.calculateneuronvalues()

    def calculateerror(self):
        """
        Calculate the error of this run

        :return: (float) Error
        """
        error = float(0)

        for i in range(self.outputlayer.numbernodes):
            error += math.pow(self.outputlayer.neuronvalues[i] - self.outputlayer.targetvalues[i], 2)

        error /= self.outputlayer.numbernodes

        return error

    def backpropagate(self):
        """
        Backpropagate error through the neural network

        """
        self.outputlayer.calculateerrors()
        self.hiddenlayer.calculateerrors()

        self.hiddenlayer.adjustweights()
        self.inputlayer.adjustweights()

    def getoutput(self, position):
        """
        Return the output at specified position for this run

        :param position: (int) Position of output value to return
        :return:
        """
        return self.outputlayer.neuronvalues[position]


class Multilayerneuralnetwork(object):

    def __init__(self):

        # aggressiveness friendliness ambitiousness distance_to_enemy distance_to_friend distance_to_goal head_to_enemy head_to_friend head_to_goal
        self.trainingset = [[0.9, 0.1, 0.1, 0.67, 0.67, 0.67, 0.9, 0.1, 0.1],
                            [0.1, 0.9, 0.1, 0.67, 0.67, 0.67, 0.1, 0.9, 0.1],
                            [0.1, 0.1, 0.9, 0.67, 0.67, 0.67, 0.1, 0.1, 0.9],
                            [0.67, 0.67, 0.67, 0.9, 0.1, 0.1, 0.1, 0.1, 0.9],
                            [0.67, 0.67, 0.67, 0.1, 0.9, 0.1, 0.1, 0.1, 0.9],
                            [0.67, 0.67, 0.67, 0.1, 0.1, 0.9, 0.1, 0.9, 0.1]]

        self.testset = [[0.9, 0.1, 0.1, 0.67, 0.67, 0.67, 0.9, 0.1, 0.1],
                        [0.1, 0.9, 0.1, 0.67, 0.67, 0.67, 0.1, 0.9, 0.1],
                        [0.1, 0.1, 0.9, 0.67, 0.67, 0.67, 0.1, 0.1, 0.9],
                        [0.67, 0.67, 0.67, 0.9, 0.1, 0.1, 0.1, 0.1, 0.9],
                        [0.67, 0.67, 0.67, 0.1, 0.9, 0.1, 0.1, 0.1, 0.9],
                        [0.67, 0.67, 0.67, 0.1, 0.1, 0.9, 0.1, 0.9, 0.1]]

        self.numinputs = len(self.trainingset)
        self.numinputvalues = 6
        self.numoutputvalues = 3

        self.neuralnetwork = Neuralnetwork(7, 7, 3, 0.2, 0.9)
        self.trainnetwork()

    def trainnetwork(self):

        error = float(1)
        count = 0

        while error > 0.001 and count < 50000:
            error = 0
            count += 1
            lastinput = 0
            for i in range(self.numinputs):
                for j in range(self.numinputvalues):
                    self.neuralnetwork.setinput(j, self.trainingset[i][j])
                    lastinput = j

                for j in range(self.numoutputvalues):
                    self.neuralnetwork.settarget(j, self.trainingset[i][lastinput + 1])
                    lastinput += 1

                self.neuralnetwork.feedforward()

                error += self.neuralnetwork.calculateerror()

                self.neuralnetwork.backpropagate()

            error /= self.numinputs


    def testnetwork(self):

        for i in range(self.numinputs):
            print '{0}: '.format(i + 1),
            for j in range(self.numinputvalues + self.numoutputvalues):
                print '{0}; '.format(self.testset[i][j]),

            for j in range(self.numinputvalues):
                    self.neuralnetwork.setinput(j, self.testset[i][j])

            self.neuralnetwork.feedforward()

            max = -1000.0
            index = -1000
            for j in range(self.numoutputvalues):
                print self.neuralnetwork.getoutput(j),
                if max < self.neuralnetwork.getoutput(j):
                    max = self.neuralnetwork.getoutput(j)
                    index = j

            if index == 0:
                print ' head to enemy: {0}'.format(self.neuralnetwork.getoutput(index))
            elif index == 1:
                print ' head to friend: {0}'.format(self.neuralnetwork.getoutput(index))
            elif index == 2:
                print ' head to goal: {0}'.format(self.neuralnetwork.getoutput(index))

    def recallnetwork(self, data):

        for i in range(self.numinputvalues):
                self.neuralnetwork.setinput(i, data[i])

        self.neuralnetwork.feedforward()

        outputs = []
        for i in range(self.numoutputvalues):
            outputs.append(self.neuralnetwork.getoutput(i))
        return outputs

# nn = Multilayerneuralnetwork()
# nn.testnetwork()