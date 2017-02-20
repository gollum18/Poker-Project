from random import randrange
from Enums import Suit
from Enums import Face
from Card import Card

class Deck:
    '''
    Creates an unshuffled deck.
    '''
    def __init__(self):
        self.deck = list();
        self.discard = list();

        for suit in Suit.suits:
            for face in  Face.faces:
                self.deck.append(Card(suit, face));

    '''
    Gets the top card from the deck.
    '''
    def draw(self):
        card = self.deck.pop();
        self.discard.append(card);
        return card;

    '''
    Adds all cards in discard back to the deck.
    '''
    def rebuild(self):
        while self.discard:
            self.deck.append(self.discard.pop());

    '''
    Shuffles the deck using Fisher-Yates.
    '''
    def shuffle(self):
        n = len(self.deck);
        for i in range (0, n-2):
            j = randrange(i, n);
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i];
