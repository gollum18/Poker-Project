from Hand import Hand

class Action:
    FOLD = "Fold";
    CHECk = "Check";
    CALL = "Call";
    RAISE = "Raise";

'''
The generic player class. Humans players are this class, AI
players are the bot class, which are a subclass of this class.
'''
class Player:
    '''
    Create a plaer with the specified number of chips.
    '''
    def __init__(self, chips):
        self.hand = None;
        self.chips = chips;

    '''
    Return a string representation of this player.
    This method is called automatically when printing the player.
    '''
    def __str__(self):
        return "Chips: {0}".format(self.chips);

    '''
    Decerement the players chip count.
    '''
    def decrementChips(self, amt):
        if (self.chips < amt):
            self.chips = 0;
        self.chips -= amt;

    def incrementChips(self, amt):
        self.chips += amt;

    def getChipCount(self):
        return self.chips;

    def getHand(self):
        return self.hand;

    def setHand(self, hand):
        self.hand = hand;
