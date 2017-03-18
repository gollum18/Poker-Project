def Table:
    '''
    Create a poker table. A poker table contains the cards on the table,
    the pot, and the ante.
    '''
    def __init__(self):
        self.cards = [];
        self.pot = 0;
        self.ante = 0;

    def __del__(self):
        del self.cards[:];
        self.cards = None;

    def addCard(self, card):
        if self.cards == None:
            self.cards = [];
        self.cards.append(card);

    def getCards(self):
        return self.cards;

    def getPot(self):
        return self.pot;

    def getAnte(self):
        return self.ante;

    def increment(self, amt):
        self.pot += (ante + amt);
        self.ante += amt;
