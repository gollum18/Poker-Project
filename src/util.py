from random import random;
from random import randint;
from constants import Constants
from deuces import Card

'''
Determines the hand strength using the given evaluator, hand, and the cards
on the table. Will always be a decimal percentage from 0 to 1.
'''
def handStrength(evaluator, hand, cardsOnTable):
    # Determine the hand stength using deuces.
    # Subtract off 1 as highest rank in deuces is 1
    # This should effectively model raising in real life
    norm = evaluator.evaluate(hand, cardsOnTable)-1;
    # Flip it so we can normalize it
    norm = Constants.LOWESTRANK - norm;
    # Normalize the percentage
    norm = float(norm/Constants.LOWESTRANK);
    # Return it
    return norm;

'''
Determines the chipsIn ratio for us.
'''
def chipRatio(chipsIn, pot):
    return float(chipsIn/pot);

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
    return deck;

'''
Generates a random sampling of the search space monte-carlo style.
This deck is a randomly selected subset of the original deck
'''
def generateMonteCarloDeck(cards, amt):
    deck = buildDeck(cards);
    for i in range(amt):
        deck.pop(randint(0, len(deck)-1));
    return shuffleDeck(deck);
