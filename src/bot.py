from player import Player
from constants import Constants
from deuces import Card
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
        self.chipsIn = 0;
        self.aggression = 0.0;
        self.confidence = random.randint(-2, 2);

    def addToChipsIn(self, amt):
        if amt <= 0:
            return;
        self.chipsIn += amt;

    '''
    Overrides the parent method to empty the chips in on round reset.
    '''
    def empty(self):
        # Calls the parent method to clear the hand
        Player.empty(self);
        # In addition empty chips in for next round
        self.chipsIn = 0;

    '''
    Gets the bots move.
    The gamestate should contain just the following in this order:
        1.) The evaluator used by the client.
        2.) The cards on the board.
        3.) The current pot.
        4.) The players aggression level.
        5.) The previous move.
        6.) The opponents cards.
    '''
    def getMove(self, state):
        #TODO: IMPLEMENT ME TO BE NON-TRIVIAL
        # Maybe use feature based learning? I am actually leaning towards utilizing
        # outs alongside some kind of probabalistic model although this may prove too
        # difficult for the time remaining.
        maxValue = -float("inf");
        maxMove = None;
        for move in self.getLegalMoves(state):
            temp = self.monteCarlo(self.getNewState(state, move), Constants.PLAYER, 2);
            if temp > maxValue:
                maxValue = temp;
                maxMove = move;
        return move;

    def getNewState(self, state, move):
        # Have to copy everything inside the state as we do not want to change
        #   the original variables passed into the starting state
        return None;
    '''
    Performs monte carlo tree search to find the optimal solution.
    '''
    def monteCarlo(self, state, turn, depth):
        # Check for termination conditions
        # End of river
        if turn == Constants.PLAYER and state[4] == Constants.FOLD:
            return -self.chipsIn;
        elif turn == Constants.BOT and state[4] == Constants.FOLD:
            return state[2];

        if depth == 0:
            return util.handStrength(state[0], self.getHand(), state[1]) - util.handStrength(state[0], state[5], state[1]);
        
        if len(state[1]) == 5:
            # Then evaluate
            diff = util.handStrength(state[0], self.getHand(), state[1]) - util.handStrength(state[0], state[5], state[1]);
            if diff > 0:
                return state[2];
            elif diff < 0:
                return -state[2];
            else:
                return 0;

        p = 1.0/int(.33*len(state[1]));
        if turn == Constants.PLAYER:
            value = 0;
            for move in self.getLegalMoves(state):
                value += p * self.monteCarlo(self.getNewState(state, move), Constants.BOT, depth);
            return value;
        else:
            value = 0;
            for move in self.getLegalMoves(state):
                value += p * self.monteCarlo(self.getNewState(state, move), Constants.PLAYER, depth - 1);
            return value;

    def shift(self, won):
        if won:
            if self.confidence < 2:
                self.confidence += 1;
        else:
            if self.confidence > -2:
                self.confidence -= 1;

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
        norm = util.handStrength(state[1], self.getCards(), state[0]);

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
    Gets the bots legal moves based on the bots confidence level.
    '''
    def getLegalMoves(self, state):
        if state[4] == Constants.ALLIN:
            return [Constants.CALL, Constants.FOLD];
        else:
            return [Constants.CALL, Constants.RAISE, Constants.ALLIN, Constants.FOLD];
