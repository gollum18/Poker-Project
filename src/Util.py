class Util:
    '''
    Stops execution of the program when called, runs when stuff is not implemented.
    '''
    def raiseNotDefined():
        fileName = inspect.stack()[1][1]
        line = inspect.stack()[1][2]
        method = inspect.stack()[1][3]

        print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
        sys.exit(1)

    '''
    Determines the rank of a hand.
    Parameters:
        hand:
            The hand to evaluate, includes the cards the player holds
            and the cards on the table.
    '''
    def rankHand(hand):
        raiseNotDefined();
