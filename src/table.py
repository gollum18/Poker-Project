from deuces import Deck

'''
Defines a poker table.
A poker table stores the deck, and the cards on the board.
'''
class Table:
    '''
    Creates a poker table containing the deck, and a means to store the cards.
    '''
    def __init__(self):
        self.deck = Deck();
        self.cards = [];

    '''
    Adds a card to the cards on the table.
    '''
    def add(self, card):
        self.cards.append(other);

    def getCards(self):
        return self.cards;

    '''
    Draws from the deck.
    '''
    def draw(self):
        return self.deck.draw();

    '''
    Resets the table.
    '''
    def reset(self):
        self.deck.shuffle();
        del self.cards[:];
