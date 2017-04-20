from __future__ import division
from player import Player
from constants import Constants
from deuces import Card
from deuces import Evaluator
from collections import defaultdict
from copy import deepcopy
import os.path
import random
import util

'''
Defines a bot.
A state is represented as:
    (community, hand, pot, ante, aggression, previousMove, dealer, chipsIn)
'''
class Bot(Player):
    
    '''
    Creates a bot by calling the parent constructor in the player class.
    '''
    def __init__(self, chips, alpha, gamma, agent):
        Player.__init__(self, chips);
        self.gamma = gamma;
        self.alpha = alpha;
        self.agent = agent;
        # Read in the table if it exists, otherwise create a new one
        if self.agent == Constants.APPROXIMATE:
            if os.path.exists(Constants.WFILE):
                self.weights = util.read(self.agent);
                self.values = defaultdict();
            else:
                self.weights = defaultdict(float);
                self.values = defaultdict();
        else:
            if os.path.exists(Constants.QFILE):
                self.values = util.read(self.agent);
            else:
                self.values = defaultdict(float);
        self.eval = Evaluator();

    def getAgent(self):
        return self.agent;

    '''
    Writes the q-table out to file.
    '''
    def write(self):
        util.write(self.values if self.agent == Constants.GENERAL else self.weights, self.agent);

    '''
    Computes the maximum q-value from a state.
    '''
    def computeValueFromQValues(self, state):
        actions = self.getLegalActions(state);
        if not actions:
            return 0.0;
        maxValue = -float("inf");
        for action in actions:
            maxValue = max(maxValue, self.getQValue(util.getKey(state[0]+state[1]), action));
        return maxValue;

    '''
    Computes the best action from a state.
    '''
    def computeActionFromQValues(self, state):
        # Get the legal actions
        actions = self.getLegalActions(state);
        if not actions:
            return None;
        # Get all possible moves from this state
        possibleMoves = defaultdict(float);
        for action in actions:
            possibleMoves[action] = self.getQValue(util.getKey(state[0]+state[1]), action);
        # Get the maximum value from the moves dictionary
        maxValue = possibleMoves[max(possibleMoves)];
        finalMoves = [];
        for move, value in possibleMoves.iteritems():
            if value == maxValue:
                finalMoves.append(move);
        # Arbitrarily pick a maximum move at random
        return random.choice(finalMoves);

    '''
    Gets the feature vector used in approximate q-learning.
    '''
    def getFeatures(self, state, action):
        features = defaultdict(float);

        # Get the chip ratio.
        features['C-RATIO'] = util.chipRatio(self.chipsIn, state[2]);
        # Get the agents hand strength.
        features['STRENGTH'] = util.strength(Evaluator(), self.getCards(), state[0]);
        # Get the agents aggression.
        features['AGGRESSION']= state[4];
        # Get the ratio representing the amount of chips the agent has in the pot
        features['A-RATIO'] = 0 if self.getChips() == 0 else state[3]/self.getChips();

        return features;

    '''
    Get the weight vector used in approximate q-learning.
    '''
    def getWeights(self):
        return self.weights;

    '''
    Runs approximate q-learning for a given state and action.
    '''
    def getQValueApproximate(self, state, action):
        q = 0;
        features = self.getFeatures(state, action);
        weights = self.getWeights();
        #print 'Features: ', features;
        #print 'Weights: ', weights;
        for feat in features:
            q += features[feat]*weights[feat];
        return q;

    '''
    Get the q-value from a given state and action.
    '''
    def getQValue(self, state, action):
        if (state, action) not in self.values:
            return 0.0;
        return self.values[(state, action)];

    '''
    Get the best move from a state.
    '''
    def getMove(self, state):
        self.previousMove = self.computeActionFromQValues(state);
        return self.previousMove;

    '''
    Get the best q-value from a state.
    '''
    def getValue(self, state):
        return self.computeValueFromQValues(state);

    '''
    Called by the environment in order to update the q-table, do not call this
    directly. This method is used with q-learning.
    '''
    def update(self, state, action, successor, reward):
        key = util.getKey(state[0]+state[1]);
        sample = reward + self.gamma*self.getValue(successor);
        self.values[(key, action)] = ((1-self.alpha)*self.getQValue(key, action))+(self.alpha*sample);

    '''
    Called by the environment in order to update the q-table, do not call this
    directly. This method is used with approximate q-learning.
    '''
    def updateApproximate(self, state, action, successor, reward):
        weights = self.getWeights();
        features = self.getFeatures(state, action);
        diff = reward+self.gamma*self.getValue(successor)-self.getQValueApproximate(state, action);
        for feat in features:
            weights[feat] += self.alpha*diff*features[feat];

    '''
    Gets the legal actions from a state.
    '''
    def getLegalActions(self, state):
        if state[5] == Constants.TERMINAL:
            return None;
        if state[5] == Constants.ALLIN:
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
    def getBetType(self, hand, comm):
        # Get the normalized hand strength percentage
        norm = util.strength(self.eval, hand, comm);

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
