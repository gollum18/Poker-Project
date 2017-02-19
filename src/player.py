class Player:
    def __init__(self, chips):
        self.chips = chips;
        self.cards = set();

    def addToHand(self, card):
        self.cards.add(card);

    def emptyHand(self):
        self.cards.clear();

    def getHand(self):
        return (self.cards[0], self.cards[1]);

    def addChips(self, amt):
        self.chips += amt;

    def subChips(self, amt):
        if self.chips - amt < 0:
            self.chips == 0;
        else:
            self.chips -= amt;

    def getChips(self):
        return self.chips;
