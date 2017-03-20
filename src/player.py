from deuces import Card

'''
Defines a player.
'''
class Player:
    '''
    Creates a player.
    A player takes in a number of starting chips and contains their chip count and cards.
    '''
    def __init__(self, chips):
        self.chips = chips;
        self.cards = [];

    '''
    Adds chips to the chips count or a card to the hand.
    '''
    def __add__(self, other):
        if type(other) is int:
            self.chips += other;
        elif type(other) is Card:
            self.cards.append(other);

    '''
    Subtracts chips from the chip count.
    '''
    def __sub__(self, other):
        if type(other) is int:
            if self.chips - other < 0:
                self.chips == 0;
            else:
                self.chips -= other;

    def empty(self):
        del self.cards[:];

    def getCards(self):
        return self.cards;

    def getChips(self):
        return self.chips;

    def getMove(self, cardsOnTable, pot, ante, prevMove):
        print("These Cards are on the Table:");
        Card.print_pretty_cards(cardsOnTable);
        print("Your Cards Are:");
        Card.print_pretty_cards(self.cards);
        print("Pot is {0}, Ante is {1}.".format(pot, ante));

        move = "";
        if prevMove = "a":
            while move != 'c' or 'f':
                move = raw_input("Bot went all in!! Do you CALL [c], or FOLD [f]: ").ower();
        else:
            while move != 'a' or move != "c" or move != "f" or move != "r":
                move = raw_input("ALL IN [a], CALL [c], FOLD [f], or RAISE [r]: ").lower();
        return move;

    def getRaise(self):
        amt = -1;
        while amt < 0:
            try:
                amt = int(raw_input("Raise By: "));
        return amt;
