try:
    import sys
    import random
except ImportError, error:
    print "Couldn't load module:\n {}".format(error)
    sys.exit(2)

class Fuzzylogic(object):

    def upslope(self, x, left, right):
        return (float(x) - left) / (right - left)

    def downslope(self, x, left, right):
        return (right - float(x)) / (right - left)

    def membershipdownslope(self, x, left, right):
        """
        Return membership to set with only a downslope

        :param x: (int) X value
        :param left: (int) Left x coordinate of slope
        :param right: (int) Right x coordinate of slope
        :return: (float) Membership to set
        """
        if x <= left:
            return 1
        elif x >= right:
            return 0 
        else:
            return self.downslope(x, left, right)

    def membershipboth(self, x, leftupslope, rightupslope, leftdownslope, rightdownslope):
        """
        Return membership to set with both upslope and downslope

        :param x: (int) X value
        :param leftupslope: (int) Left x coordinate of upslope
        :param rightupslope: (int) Right x coordinate of upslope
        :param leftdownslope: (int) Left x coordinate of downslope
        :param rightdownslope: (int) Right x coordinate of downslope
        :return: (float) Membership to set
        """
        if x <= leftupslope:
            return 0
        elif x >= rightdownslope:
            return 0
        elif leftupslope < x < rightupslope:
            return self.upslope(x, leftupslope, rightupslope)
        elif leftdownslope < x < rightdownslope:
            return self.downslope(x, leftdownslope, rightdownslope)
        else:
            return 1

    def membershipupslope(self, x, left, right):
        """
        Return membership to set with only an upslope

        :param x: (int) X value
        :param left: (int) Left x coordinate of slope
        :param right: (int) Right x coordinate of slope
        :return: (float) Membership to set
        """
        if x <= left:
            return 0
        elif x >= right:
            return 1
        else:
            return self.upslope(x, left, right)


class Fuzzyocean(object):

    def __init__(self, o, c, e, a, n):

        self.fuzzylogic = Fuzzylogic()
        self.aggressiveness, self.friendliness, self.ambitiousness = self.assignpersonality(o, c, e, a, n)

    def centroid(self, membershiplow, lowvalues, membershipmid, midvalues, membershiphigh, highvalues):
        """
        Return centre of gravity of aggregated fuzzy set

        :param membershiplow: (float) Membership to 'low' set
        :param lowvalues:  (list) List of sample values in 'low' set
        :param membershipmid: (float) Membership to 'mid' set
        :param midvalues:  (list) List of sample values in 'mid' set
        :param membershiphigh: (float) Membership to 'high' set
        :param highvalues: (list) List of sample values in 'high' set
        :return: (float) Centre of gravity value for aggregated fuzzy set
        """
        try:
            return ((membershiplow * (sum(lowvalues))) +
                    (membershipmid * (sum(midvalues))) +
                    (membershiphigh * (sum(highvalues)))) / \
                   ((membershiplow * len(lowvalues)) +
                    (membershipmid * len(midvalues)) +
                    (membershiphigh * len(highvalues)))
        except ZeroDivisionError:
            return 0


    def clipcombineanddefuzzify(self, membershiplow, membershipmid, membershiphigh):
        """
        Return defuzzified result of clipping and combining sets based on membership

        :param membershiplow: (float) Membership in 'low' set
        :param membershipmid: (float) Membership in 'mid' set
        :param membershiphigh: (float) Membership in 'high' set
        :return: (float) Defuzzified result
        """
        low = {'left': 0, 'right': 0}
        mid = {'left': 0, 'right': 0}
        high = {'left': 0, 'right': 0}

        if membershiplow > 0:
            low['left'] = 10
            low['right'] = 20

        if membershipmid > 0:
            mid['left'] = 20
            mid['right'] = 80
            if membershipmid > membershiplow:
                low['right'] = mid['left']
            if membershipmid < membershiplow:
                mid['left'] = low['right']

        if membershiphigh > 0:
            high['left'] = 60
            high['right'] = 100
            if membershiphigh > membershipmid:
                mid['right'] = high['left']
            if membershiphigh < membershipmid:
                high['left'] = mid['right']

        lowvalues = []
        midvalues = []
        highvalues = []

        for i in range(low['left'], low['right'], 1):
            lowvalues.append(i)
        for i in range(mid['left'], mid['right'], 1):
            midvalues.append(i)
        for i in range(high['left'], high['right'], 1):
            highvalues.append(i)

        return self.centroid(membershiplow, lowvalues, membershipmid, midvalues, membershiphigh, highvalues) / 100.0

    def assignpersonality(self, o, c, e, a, n):
        """
        Return values for aggressiveness, friendliness and ambitiousness.
        Uses Mamdani method of fuzzy inference to:
        1. Fuzzify inputs
        2. Evaluate fuzzy inputs (using fuzzy AND/OR)
        3. Aggregate outputs (clip fuzzy sets and combine)
        4. Defuzzify aggregated output set using centroid technique

        :param o: Openness percentage
        :param c: Conscientiousness percentage
        :param e: Extraversion percentage
        :param a: Agreeableness percentage
        :param n: Neuroticism percentage
        :return: (int) Aggressiveness (0-1), (int) Friendliness (0-1), (int) Ambitiousness (0-1)
        """

        # Aggressive personality
        #    high  mid   low
        # O   -     ~     +
        # C   ~     ~     ~
        # E   ~     ~     ~
        # A   -     ~     +
        # N   +     ~     -

        membershiplow = min(self.membershipupper(o),
                            self.membershipupper(a),
                            self.membershiplower(n))

        membershiphigh = min(self.membershiplower(o),
                             self.membershiplower(a),
                             self.membershipupper(n))

        membershipmid = min(self.membershipnormal(o),
                            self.membershipnormal(c),
                            self.membershipnormal(e),
                            self.membershipnormal(a),
                            self.membershipnormal(n))

        aggressiveness = self.clipcombineanddefuzzify(membershiplow,
                                                      membershipmid,
                                                      membershiphigh)

        # Friendly personality
        #    high  mid   low
        # O   ~     ~     ~
        # C   ~     ~     ~
        # E   +     ~     -
        # A   +     ~     -
        # N   -     ~     +

        membershiplow = min(self.membershiplower(e),
                            self.membershiplower(a),
                            self.membershipupper(n))

        membershiphigh = min(self.membershipupper(e),
                             self.membershipupper(a),
                             self.membershiplower(n))

        friendliness = self.clipcombineanddefuzzify(membershiplow,
                                                    membershipmid,
                                                    membershiphigh)

        # Ambitious personality
        #    high  mid   low
        # O   ~     ~     ~
        # C   +     ~     -
        # E   -     ~     +
        # A   ~     ~     ~
        # N   -     ~     +

        membershiplow = min(self.membershiplower(c),
                            self.membershipupper(e),
                            self.membershipupper(n))

        membershiphigh = min(self.membershipupper(c),
                             self.membershiplower(e),
                             self.membershiplower(n))

        ambitiousness = self.clipcombineanddefuzzify(membershiplow,
                                                     membershipmid,
                                                     membershiphigh)

        return aggressiveness, friendliness, ambitiousness

    def membershiplower(self, value):
        """
        Return membership to lower set (slopes down from left to right)

        :param value: (int) X value
        :return: (float) Membership value
        """
        left = 25
        right = 100
        return self.fuzzylogic.membershipdownslope(value, left, right)


    def membershipnormal(self, value):
        """
        Return membership to normal set
        (slopes up from leftupslope to rightupslope and down from leftdownslope to rightdownslope)

        :param value: (int) X value
        :return: (float) Membership value
        """
        leftupslope = 0
        rightupslope = 25
        leftdownslope = 75
        rightdownslope = 100
        return self.fuzzylogic.membershipboth(value, leftupslope, leftdownslope, rightupslope, rightdownslope)

    def membershipupper(self, value):
        """
        Return membership to upper set (slopes up from left to right)

        :param value: (int) X value
        :return: (float) Membership value
        """
        left = 0
        right = 75
        return self.fuzzylogic.membershipupslope(value, left, right)

again = True
while again:
    o = random.randrange(101)
    c = random.randrange(101)
    e = random.randrange(101)
    a = random.randrange(101)
    n = random.randrange(101)

    print 'O: {0}'.format(o)
    print 'C: {0}'.format(c)
    print 'E: {0}'.format(e)
    print 'A: {0}'.format(a)
    print 'N: {0}'.format(n)

    personality = Fuzzyocean(o, c, e, a, n)

    print 'Aggressiveness: {0}'.format(personality.aggressiveness)
    print 'Friendliness: {0}'.format(personality.friendliness)
    print 'Ambitiousness: {0}'.format(personality.ambitiousness)

    if raw_input('Again?').lower == 'n':
        again = False





