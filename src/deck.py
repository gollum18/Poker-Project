from random import randrange
from Card import *

class Deck:
    def __init__(self):
        # Create the deck
        self.deck = list();
        self.drawn = list();
        for face in Face._facesList:
            for value in Value._valuesList:
                self.deck.append(Card(face, value));
        self.shuffle();

    def __str__(self):
        s = "{";
        for i in range(0, len(self.deck)):
            s += "{0}:{1}\r\n".format(self.deck[i].getFace(), self.deck[i].getValue());
        s += "}"
        return s;

    def shuffle(self):
        # Perform the fisher-yates shuffle on it
        l = len(self.deck);
        for i in range(0, l-1):
            j = randrange(i, l);
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i];

    def draw(self):
        draw = self.deck.pop();
        self.drawn.append(draw);
        return draw;

    def rebuild(self):
        # While the drawn pile still has cards in it
        while self.drawn:
            # Add them back to the deck
            self.deck.append(self.drawn.pop());
        # Shuffle the deck
        self.shuffle();
