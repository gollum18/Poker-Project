from player import Player
from random import choice
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
    def getMove(self, prevMove):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        if prevMove == Constants.ALLIN:
            return choice([Constants.CALL, Constants.FOLD]);
        return choice([Constants.ALLIN, Constants.CALL, Constants.FOLD, Constants.RAISE]);

    '''
    Gets the bots raise.
    '''
    def getRaise(self):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        return int(.5*self.chips);
