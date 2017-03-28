from player import Player
from constants import Constants
import random

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
    def getMove(self, state):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        return random.choice([Constants.CALL, Constants.FOLD]);

    '''
    Gets the bots betting type.
    Total percent consists of our aggresiveness + opponents aggresiveness + normalize percentage.
        Should always be between 0 and 1;
    '''
    def getRaiseType(self, totalPercent):
        # Get the overall raise type
        rType = None;
        if totalPercent < .33:
            rType = Constants.LOW;
        elif totalPercent < .66:
            rType = Constants.MEDIUM;
        elif totalPercent < 1:
            rType = Constants.HIGH;
        return rType;
