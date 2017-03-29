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
    Calculates a percentile used to determine the bet type. We factor in the AIs' aggression along with
        the its normalization percentage. We subtract off the opponents aggression to account for it.
        Finally, we normalize by two as the best we can get is a 2.0 if the AIs' aggression is 1, the
        normalization percentage is 1 and the opponents aggresion is 0.
    Ultimately these values should all be weighted as well considering we want the AI to learn instead of
        us telling it what to do.
    Will raise a value error if the calculated percentile exceeds normal probabilistic bounds.
    '''
    def getRaiseType(self, myAggro, oppAggro, normPercentage):
        # Normalize the factors to be at most 1, the weights that factor into each of the three components
        #   here can be adjusted by the AI as gameplay proceeds
        totalPercent = myAggro + normPercentage;
        
        # Check to see if the opponents aggresion outweighs our two factors, if so set out percentile to zero,
        #   otherwise just subtract it off.
        totalPercent = (totalPercent - oppAggro if totalPercent - oppAggro > 0 else 0);
        
        # Divide by two to normalize, if it is zero from the opponents aggression dominating the other factors, then
        #   the result will still just be zero.
        totalPercent /= 2.0;
        
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
