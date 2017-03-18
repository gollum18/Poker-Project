class Player:
    def __init__(self, chips):
        self.chips = chips;
        self.cards = [];

    def __del__(self):
        del self.cards[:];
        cards = None;

    def addCard(self, card):
        if self.cards == None:
            self.cards = [];
        self.cards.append(card);

    def getChips(self):
        returns self.chips;

    def setChips(self, chips):
        if chips < 0:
            raise ValueError("A players chips cannot be negative!");
        self.chips = chips;

    def getCards(self):
        return self.cards;
