from __future__ import division
from player import Player
from constants import Constants
from deuces import Card
from deuces import Evaluator
from collections import defaultdict
from copy import deepcopy
import random
import util

'''
Defines a bot.

'''
class Bot(Player):
    
    '''
    Creates a bot by calling the parent constructor in the player class.
    '''
    def __init__(self, chips, alpha, gamma):
        Player.__init__(self, chips);
        self.gamma = gamma;
        self.alpha = alpha;
        self.values = defaultdict(float);
        self.eval = Evaluator();

    def disableTraining(self):
        self.gamma = 1.0;
        self.alpha = 0.0

    def computeQValueFromQValues(self, state):
        actions = self.getLegalActions();
        if not actions:
            return 0.0;
        maxValue = -float("inf");
        for action in actions:
            maxValue = max(maxValue, self.getQValue(set(state[0], state[1]), action));
        return maxValue;

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(state);
        if not actions:
            return None;
        possibleMoves = defaultdict(float);
        for action in actions:
            possibleMoves[action] = self.getQValue(frozenset(state[0]+state[1]), action);
        return max(possibleMoves, key=possibleMoves.get);

    def getQValue(self, state, action):
        if (state, action) not in self.values:
            return 0.0;
        return self.values[(frozenset(state[0]+state[1]), action)];

    def getMove(self, state):
        return self.computeActionFromQValues(state);
    
    def update(self, state, action, successor, reward):
        state = frozenset(state(0)+state[1]);
        sample = reward + self.gamma*self.getValue(successor);
        self.values[(state, action)] = ((1-self.alpha)*self.getQValue(state, action))+(self.alpha*sample);

    def getLegalActions(self, state):
        if state[5] == Constants.TERMINAL:
            return None;
        if state[5] == Constants.ALLIN:
            return [Constants.CALL, Constants.FOLD];
        return [Constants.CALL, Constants.ALLIN, Constants.FOLD, Constants.RAISE];

## May or may not be needed, this is a way to generate successor states
##    '''
##    A state is represented as:
##        (community, hand, pot, ante, aggression, previousMove, dealer, chipsIn)
##    '''
##    def getSuccessorStates(self, state)
##        states = [];
##        for action in self.getLegalActions(state):
##            # Check who the dealer is
##            # If the dealer is the player, then the bot bets first
##            if state[6] == Constants.PLAYER:
##                if action == Constants.ALLIN:
##                    states.append(state[0], state[1], state[2]+self.getChips(), state[3]+self.getChips(), self.getChips()/state[3], Constants.ALLIN, state[6], self.getChipsIn()+self.getChips()); 
##                elif action == Constants.CALL:
##                    states.append(state[0], state[1], state[2]+state[3], state[3]*2, 1.0, Constants.CALL, state[6], state[3]+state[7]);
##                elif action == Constants.FOLD:
##                    states.append(state[0], state[1], state[2], state[3], state[4], Constants.TERMINAL, state[6], state[7]);
##                elif action == Constants.RAISE:
##                    amt = self.getBet(state[3], self.getBetType(state[1], state[0]));
##                    states.append(state[0], state[1], state[2]+amt, state[3]+amt, amt/state[3], Constants.RAISE, state[6], state[7]+amt);
##            # Otherwise the bot bets second in this round
##            else:
##                # Build a deck for each card
##                for card in util.buildDeck(state[0]+state[1]):
##                    # Copy everythong that needs copied
##                    comm = deepcopy(state[0]);
##                    comm.append(card);
##                    # Account for the appropriate action
##                    if action == Constants.ALLIN:
##                        states.append(comm, state[1], state[2]+self.getChips(), state[3]+self.getChips(), self.getChips()/state[3], Constants.ALLIN, state[6], self.getChipsIn()+self.getChips()); 
##                    elif action == Constants.CALL:
##                        states.append(comm, state[1], state[2]+state[3], state[3]*2, 1.0, Constants.CALL, state[6], state[3]+state[7]);
##                    elif action == Constants.FOLD:
##                        states.append(comm, state[1], state[2], state[3], state[4], Constants.TERMINAL, state[6], state[7]);
##                    elif actions == Constants.RAISE:
##                        amt = self.getBet(state[3], self.getBetType(state[1], comm));
##                        states.append(comm, state[1], state[2]+amt, state[3]+amt, amt/state[3], Constants.RAISE, state[6], state[7]+amt);
##        return states;
                
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
