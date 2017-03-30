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

    def getRaise(self):
        #TODOL IMPLEMENT ME TO BE NON-TRIVIAL
        return .5*self.getChips();

    '''
    Gets the bots betting type.
    Determined via a percentile that is calculated by taking the modeled opponents aggression minus our
        aggression. If the result is negative, then we determine 0 and return a small bet.
    '''
    def getRaiseType(self, myAggro, oppAggro):
        # Check to see if the opponents aggresion outweighs our two factors, if so set out percentile to zero,
        #   otherwise just subtract it off.
        totalPercent = (myAggro - oppAggro if myAggro - oppAggro > 0 else 0);
        
        # Get the overall raise type, this is predetermined and non-adjustable by the AI
        # Return a small bet if we are not very confident.
        if totalPercent <= .33:
            return Constants.SMALL;
        
        # Return a medium bet if we are moderatly confident.
        elif totalPercent <= .66:
            return Constants.MEDIUM;

        # Return a large bet if we are highly confident.
        elif totalPercent <= 1:
            return Constants.LARGE;

        # Raise a value error if we have exceeded normal probabilistic bounds
        else:
            raise ValueError("Raise type percentage exceeded normal bounds! Must be between 0 <= x <= 1.");
