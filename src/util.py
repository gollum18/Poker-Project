from __future__ import division
from random import random;
from random import randint;
from constants import Constants
from deuces import Card
from collections import defaultdict

'''
Prints out cards to the terminal.
'''
def printCards(cards):
    outStr = "[ ";
    for i in range(0, len(cards)):
        outStr += "{0}".format(Card.int_to_str(cards[i]));
        if i != len(cards)-1:
            outStr += ", ";
    outStr += " ]";
    print outStr;

'''
Writes the q-learning dictionary to file, overwriting what was in there.
'''
def writeTable(qtable):
    outFile = open(Constants.FILENAME, 'w');
    for key, value in qtable.iteritems():
        outFile.write("{0} {1} {2}\n".format(key[0], key[1], value));
    outFile.close();

'''
Loads in the q-learning dictionary from file.
'''
def readTable():
    inFile = open(Constants.FILENAME, 'r');
    lines = [line.rstrip('\n') for line in inFile];
    inFile.close();
    qtable = defaultdict(float);
    for line in lines:
        split = line.split();
        qtable[(int(split[0]), split[1])] = float(split[2]);
    return qtable;

'''
Gets the winning percentages of each player.
Will return a dictionary that maps each player to their winning percentage: 0-1.
'''
def winningPercentage(evaluator, phand, ahand, cardsOnTable):
    percentile = defaultdict(float);
    # Determine the hand stength using deuces.
    # Subtract off 1 as highest rank in deuces is 1
    # This should effectively model raising in real life
    player = Constants.LOWESTRANK-(evaluator.evaluate(phand, cardsOnTable)-1);
    agent = Constants.LOWESTRANK-(evaluator.evaluate(ahand, cardsOnTable)-1);
    total = player+agent;
    percentile[Constants.PLAYER]=player/total;
    percentile[Constants.BOT]=agent/total;
    # Return it
    return percentile;

'''
Gets the hand strength of a single player.
Returns a float representing the hand strength of the player: 0-1.
'''
def strength(evaluator, hand, cardsOnTable):
    norm = Constants.LOWESTRANK-(evaluator.evaluate(hand, cardsOnTable)-1);
    norm = norm/Constants.LOWESTRANK;
    return norm;

'''
Gets the first half of the key for the q-learning dictionary.
Uniquely identifies a hand/community combination.
'''
def getKey(cards):
    return sum(cards);

'''
Determines the chipsIn ratio for us.
'''
def chipRatio(chipsIn, pot):
    return chipsIn/pot;

'''
Simulates noise in the environment. For our purposes, this will pair with the bots confidence
level to determine whether it takes safe or risky moves.
'''
def flipCoin(p):
    if p < random():
        return True;
    return False;

'''
Shuffles the deck.
Testing is required to ensure no bias is present.
'''
def shuffleDeck(deck):
    pos = 0;
    for i in range (len(deck)):
        pos = randint(i, len(deck)-1);
        temp = deck[pos];
        deck[pos] = deck[i];
        deck[i] = temp;
    return deck;

'''
Builds a deck that contains all of the cards that are not found in the provided card list.
'''
def buildDeck(cards):
    deck = list();
    for value in Card.STR_RANKS:
        for suit in 'shdc':
            if value+suit not in cards:
                deck.append(Card.new(value+suit));
    deck = shuffleDeck(deck);
    return deck;

'''
This algorithm is a modified version of the getBetAmt algorithm found in
'ALGORITHMS FOR EVOLVING NO-LIMIT TEXAS HOLD'EM POKER PLAYING AGENTS' by
Garret Nicolai and Robert Hilderman.
'''
def getBet(maxBet, minBet, betType):
    # Stores the final bet
    finalBet = 0;

    if maxBet < minBet:
        return maxBet;
    percentile = random();
    if betType == Constants.SMALL:
        if percentile < Constants.LOIN:
            percentile = random() * Constants.LOUP;
        else:
            percentile = Constants.LOUP + (randint(1, 6)/100.0);
    elif betType == Constants.MEDIUM:
        if percentile < Constants.MEIN:
            percentile = Constants.MELO + (randint(1, 10)/100.0);
        else:
            percentile = Constants.MEUP + (randint(1, 10)/100.0);
    elif betType == Constants.LARGE:
        if percentile < Constants.HIABOVE:
            percentile = Constants.HIPOINT + (randint(1, 30)/100.0);
        else:
            percentile = Constants.HIPOINT + (randint(30, 70)/100.0);

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
def getBetType(evaluator, hand, comm):
    # Get the normalized hand strength percentage
    norm = strength(evaluator, hand, comm);

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
