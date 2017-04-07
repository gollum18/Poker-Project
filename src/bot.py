from player import Player
from constants import Constants
from deuces import Card
from deuces import Evaluator
from __future_ import division
from collections import default_dict
import random
import util

'''
Defines a bot.
A state is represented as: (community, move, dealer)
'''
class Bot(Player):
    
    '''
    Creates a bot by calling the parent constructor in the player class.
    '''
    def __init__(self, chips, discount, alpha):
        Player.__init__(self, chips);
        self.discount = discount;
        self.alpha = alpha;
        self.values = default_dict(float);
        self.eval = Evaluator();

    def disableTraining(self):
        self.discount = 1.0;
        self.alpha = 0.0

    def getSuccessorStates(self, state, action):

    def getReward(self, state, successor):

    def computeQValueFromQValues(self, state):
        actions = self.getLegalActions();
        if not actions:
            return 0.0;
        maxValue = -float("inf");
        for action in actions:
            maxValue = max(maxValue, self.getQValue(state, action));
        return maxValue;

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(state);
        if not actions:
            return None;
        possibleMoves = default_dict(float);
        for action in actions:
            possibleMoves[action] = self.getQValue(state, action);
        return max(possibleMoves, key=possibleMoves.get);

    def getQValue(self, state, action):
        if (state, action) not in self.values:
            return 0.0;
        return self.values[(, action)];

    def getPolicy(self, state):
        return self.ComputeActionFromQValues(state);

    def update(self, state, action, successor, reward):
        sample = reward + self.discount*self.getValue(successor);
        self.values[(state, action)] = ((1-self.alpha)*self.getQValue(state, action))+(self.alpha*sample);

    def getLegalActions(self, state):
        if state[1] == Constants.ALLIN:
            return [Constants.CALL, Constants.FOLD];
        return [Constants.CALL, Constants.ALLIN, Constants.FOLD, Constants.RAISE];

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

        finalBet = int(percentile * maxBet);
        if finalBet < minBet:
            finalBet = minBet;
        elif finalBet > maxBet:
            finalBet = maxBet;

        return finalBet;

    '''
    Gets the bots betting type.
    This algorithm is a modified version of the getBetAmt algorithm found in
    'ALGORITHMS FOR EVOLVING NO-LIMIT TEXAS HOLD'EM POKER PLAYING AGENTS' by
    Garret Nicolai and Robert Hilderman.
    '''
    def getBetType(self, state):
        # Get the normalized hand strength percentage
        norm = util.strength(self.eval, self.getCards(), state[0]);

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
