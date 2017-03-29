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
        self.pot = 0;
        self.ante = 0;

    '''
    Adds a card to the cards on the table.
    '''
    def addCard(self, card):
        self.cards.append(card);

    def addToAnte(self, amt):
        self.ante += amt;

    def addToPot(self, amt):
        self.pot += amt;

    def getAnte(self):
        return self.ante;

    def getPot(self):
        return self.pot;

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
        self.ante = 0;
        self.pot = 0;
