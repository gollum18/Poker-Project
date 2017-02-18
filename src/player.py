from Hand import Hand

def Player:
    def __init__(self, chips):
        self.hand = None;
        self.chips = chips;

    def __str__(self):
        return "Chips: {0}".format(self.chips);

    def decrementChips(self, amt):
        if (self.chips < amt):
            return;
        self.chips -= amt;

    def incrementChips(self, amt):
        self.chips += amt;

    def getChipCount(self):
        return self.chips;

    def getHand(self):
        return self.hand;

    def setHand(self, hand):
        self.hand = hand;
