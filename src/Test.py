from Deck import Deck

PL = 20;

# Test deck functions
deck = Deck();

deck.shuffle();

for i in range (0, len(deck.deck)):
    print "{0}".format(deck.draw());
