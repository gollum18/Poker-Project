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

    '''
    Adds to the current ante on the table.
    '''
    def addToAnte(self, amt):
        self.ante += amt;

    '''
    Adds to the current pot on the table.
    '''
    def addToPot(self, amt):
        self.pot += amt;

    '''
    Gets the current ante.
    '''
    def getAnte(self):
        return self.ante;

    '''
    Gets the current pot.
    '''
    def getPot(self):
        return self.pot;

    '''
    Gets the community cards on the table.
    '''
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
