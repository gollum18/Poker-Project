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
def write(table, agent):
    outFile = None;
    if agent == Constants.GENERAL:
        outFile = open(Constants.QFILE, 'w');
    else:
        outFile = open(Constants.WFILE, 'w');
    for key, value in table.iteritems():
        if agent == Constants.GENERAL:
            outFile.write("{0} {1} {2}\n".format(key[0], key[1], value));
        else:
            outFile.write("{0} {1}\n".format(key, value));
    outFile.close();

'''
Loads in the q-learning dictionary from file.
'''
def read(agent):
    inFile = None;
    if agent == Constants.GENERAL:
        inFile = open(Constants.QFILE, 'r');
    else:
        inFile = open(Constants.WFILE, 'r');
    lines = [line.rstrip('\n') for line in inFile];
    inFile.close();
    table = defaultdict(float);
    for line in lines:
        split = line.split();
        if agent == Constants.GENERAL:
            table[int(split[0]), split[1]] = float(split[2]);
        else:
            table[split[0]] = float(split[1]);
    return table;

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
