from Enums import Suit
from Enums import Face

class Card:
    def __init__(self, suit, face):
        self.suit = suit;
        self.face = face;

    def getSuit(self):
        return self.suit;

    def getFace(self):
        return self.face;
