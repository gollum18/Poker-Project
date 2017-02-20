from Enums import Suit
from Enums import Face

class Card:
    def __init__(self, suit, face):
        self.suit = suit;
        self.face = face;

    def __str__(self):
        return "{0}:{1}".format(self.suit, self.face);

    def getSuit(self):
        return self.suit;

    def getFace(self):
        return self.face;
