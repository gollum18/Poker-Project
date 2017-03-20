from deuces import Deck

'''
Defines a poker table.
A poker table stores the deck, pot, ante, and the cards on the board.
'''
class Table:
    '''
    Creates a poker table containing the deck, pot, ante, and a means to store the
    cards.
    '''
    def __init__(self):
        self.deck = Deck();
        self.pot = 0;
        self.ante = 0;
        self.cards = [];

    '''
    Adds a card to the cards on the table or increments the pot and ante.
    '''
    def __add__(self, other):
        if type(other) is Card:
            self.cards.append(other);
        elif type(other) is int:
            if other > 0:
                self.pot += ante + other;
                self.ante += other;

    '''
    Returns the ante.
    '''
    def getAnte(self):
        return self.ante;

    def getCards(self):
        return self.cards;

    '''
    Returns the pot.
    '''
    def getPot(self):
        return self.pot;

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
        self.pot = 0;
        self.ante = 0;
        del self.cards[:];
