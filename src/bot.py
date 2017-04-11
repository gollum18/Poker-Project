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
    def __init__(self, chips, alpha, gamma):
        Player.__init__(self, chips);
        self.gamma = gamma;
        self.alpha = alpha;
        # Read in the table if it exists, otherwise create a new one
        if os.path.exists(Constants.FILENAME):
            self.values = util.readTable();
        else:
            self.values = defaultdict(float);
        self.eval = Evaluator();

    def writeTable(self):
        util.writeTable(self.values);

    def disableTraining(self):
        self.gamma = 1.0;
        self.alpha = 0.0

    def computeValueFromQValues(self, state):
        actions = self.getLegalActions(state);
        if not actions:
            return 0.0;
        maxValue = -float("inf");
        for action in actions:
            maxValue = max(maxValue, self.getQValue(util.getKey(state[0]+state[1]), action));
        return maxValue;

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

    def getQValue(self, state, action):
        if (state, action) not in self.values:
            return 0.0;
        return self.values[(state, action)];

    def getMove(self, state):
        return self.computeActionFromQValues(state);

    def getValue(self, state):
        return self.computeValueFromQValues(state);
    
    def update(self, state, action, successor, reward):
        state = util.getKey(state[0]+state[1]);
        sample = reward + self.gamma*self.getValue(successor);
        self.values[(state, action)] = ((1-self.alpha)*self.getQValue(state, action))+(self.alpha*sample);

    def getLegalActions(self, state):
        if state[5] == Constants.TERMINAL:
            return None;
        if state[5] == Constants.ALLIN:
            return [Constants.CALL, Constants.FOLD];
        return [Constants.CALL, Constants.ALLIN, Constants.FOLD, Constants.RAISE];
