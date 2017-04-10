from __future__ import division
from random import random;
from random import randint;
from constants import Constants
from deuces import Card
from collections import defaultdict

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
Determines the hand strength using the given evaluator, hand, and the cards
on the table. Will always be a decimal percentage from 0 to 1.
'''
def strength(evaluator, hand, cardsOnTable):
    # Determine the hand stength using deuces.
    # Subtract off 1 as highest rank in deuces is 1
    # This should effectively model raising in real life
    norm = evaluator.evaluate(hand, cardsOnTable)-1;
    # Flip it so we can normalize it
    norm = Constants.LOWESTRANK - norm;
    # Normalize the percentage
    norm = norm/Constants.LOWESTRANK;
    # Return it
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
