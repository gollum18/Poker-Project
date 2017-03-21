from player import Player
from constants import Constants

'''
Defines a bot.
'''
class Bot(Player):
    '''
    Creates a bot by calling the parent constructor in the player class.
    '''
    def __init__(self, chips):
        Player.__init__(self, chips);

    '''
    Gets the bots move.
    '''
    def getMove(self):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        return Constants.FOLD;

    '''
    Gets the bots raise.
    '''
    def getRaise(self):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        return 0;
