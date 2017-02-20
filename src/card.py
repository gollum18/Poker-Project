from Enums import Suit
from Enums import Face

class Card:
    ranks = {"2":0, "3":1, "4":2, "5":3,
        "6":4, "7":5, "8":6, "9":7,
        "10":8, "J":9, "Q":10, "K":11, "A":12};
    
    def __init__(self, suit, face):
        self.suit = suit;
        self.face = face;

    def __str__(self):
        return "{0}:{1}".format(self.suit, self.face);

    def __eq__(self, other):
        if type(other) == Card:
            if self.suit == other.suit and self.face == other.face:
                return True;
        return False;

    def __hash__(self):
        return hash((self.suit, self.face));

    def __cmp__(self, other):
        if ranks[self.getFace()] > ranks[other.getFace()]:
            +1;
        elif ranks[self.getFace()] < ranks[other.getFace()]:
            -1;
        else:
            return 0;

    def getSuit(self):
        return self.suit;

    def getFace(self):
        return self.face;

    def getRank(self):
        return ranks[self.getFace()];
