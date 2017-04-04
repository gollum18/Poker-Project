from player import Player
from constants import Constants
import random
import util

'''
Defines a bot.
'''
class Bot(Player):
    
    '''
    Creates a bot by calling the parent constructor in the player class.
    '''
    def __init__(self, chips):
        Player.__init__(self, chips);
        # Stores the chips that the player currently has in the pot
        #   gets reset at the end of the round
        self.chipsIn = 0;
        # The predictor is used to model confidence in our AI
        self.predictor = 0;

    # Shifts the predictor up or down
    def shift(self, shift):
        if shift == Constants.SHIFT_LEFT:
            if self.predictor > Constants.LOWER_PREDICTOR:
                self.predictor -=1;
        elif shift == Constants.SHIFT_RIGHT:
            if self.predictor < Constants.UPPER_PREDICTOR:
                self.predictor += 1;

    '''
    Gets the bots move.
    '''
    def getMove(self, state, prevMove):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        # Maybe use feature based learning? I am actually leaning towards utilizing
        # outs alongside some kind of probabalistic model although this may prove too
        # difficult for the time remaining
        if prevMove == Constants.ALLIN:
            return random.choice([Constants.CALL, Constants.FOLD]);
        return random.choice([Constants.ALLIN, Constants.RAISE, Constants.CALL, Constants.FOLD]);

    '''
    This algorithm is a modified version of the getBetAmt algorithm found in
    'ALGORITHMS FOR EVOLVING NO-LIMIT TEXAS HOLD'EM POKER PLAYING AGENTS' by
    Garret Nicolai and Robert Hilderman.
    '''
    def getBet(self, minBet, betType):
        # The max a player can bet is their current amount of chips 
        maxBet = self.getChips();
        # Stores the final bet
        finalBet = 0;

        if maxBet < minBet:
            return maxBet;
        percentile = random.random();
        if betType == Constants.SMALL:
            if percentile < Constants.LOIN:
                percentile = random.random() * Constants.LOUP;
            else:
                percentile = Constants.LOUP + (random.randint(1, 6)/100.0);
        elif betType == Constants.MEDIUM:
            if percentile < Constants.MEIN:
                percentile = Constants.MELO + (random.randint(1, 10)/100.0);
            else:
                percentile = Constants.MEUP + (random.randint(1, 10)/100.0);
        elif betType == Constants.LARGE:
            if percentile < Constants.HIABOVE:
                percentile = Constants.HIPOINT + (random.randint(1, 30)/100.0);
            else:
                percentile = Constants.HIPOINT + (random.randint(30, 70)/100.0);

        finalBet = percentile * maxBet;
        if finalBet < minBet:
            finalBet = minBet;
        elif finalBet > maxBet:
            finalBet = maxBet;

        return int(finalBet);

    '''
    Gets the bots betting type.
    The state here should just consist of these items in this order:
        1.) The current cards on the board.
        2.) The evaluator used by the board.
    This algorithm is a modified version of the getBetAmt algorithm found in
    'ALGORITHMS FOR EVOLVING NO-LIMIT TEXAS HOLD'EM POKER PLAYING AGENTS' by
    Garret Nicolai and Robert Hilderman.
    '''
    def getBetType(self, state):
        # Determine the hand stength using deuces.
        # Subtract off 1 as highest rank in deuces is 1
        # This should effectively model raising in real life
        norm = state[1].evaluate(self.getCards(), state[0])-1;
        # Flip it so we can normalize it
        norm = Constants.LOWESTRANK - norm;
        # Normalize the percentage
        norm = float(norm/Constants.LOWESTRANK);

        # Get the overall raise type, this is predetermined and non-adjustable by the AI
        # Return a small bet if we are not very confident.
        if norm <= .33:
            return Constants.SMALL;
        
        # Return a medium bet if we are moderatly confident.
        elif norm <= .66:
            return Constants.MEDIUM;

        # Return a large bet if we are highly confident.
        elif norm <= 1:
            return Constants.LARGE;

        # Raise a value error if we have exceeded normal probabilistic bounds
        else:
            raise ValueError("Raise type percentage exceeded normal bounds! Must be between 0 <= x <= 1.");

    '''
    Resets certain round dependent features for the bot.
    '''
    def reset(self):
        self.chipsIn = 0;
