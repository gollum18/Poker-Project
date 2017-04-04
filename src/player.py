from deuces import Card
from constants import Constants

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
    Adds a card to the players hand
    '''
    def addCard(self, card):
        self.cards.append(card);

    '''
    Adds chips to the chips count.
    '''
    def addChips(self, chips):
        self.chips += chips;

    '''
    Subtracts chips from the chip count.
    '''
    def subChips(self, other):
        if type(other) is int:
            if self.chips - other < 0:
                self.chips = 0;
            else:
                self.chips -= other;

    '''
    Empties the players
    '''
    def empty(self):
        del self.cards[:];

    '''
    Get the players hand.
    '''
    def getCards(self):
        return self.cards;

    '''
    Get the players chips.
    '''
    def getChips(self):
        return self.chips;

    '''
    Get the players move from the command line.
    '''
    def getMove(self, cardsOnTable, pot, ante, prevMove):
        print("These Cards are on the Table:");
        Card.print_pretty_cards(cardsOnTable);
        print("Your Cards Are:");
        Card.print_pretty_cards(self.cards);
        print("You have ${0}, Pot is ${1}, Ante is ${2}.".format(self.chips, pot, ante));

        move = "";
        if prevMove == Constants.ALLIN:
            while move != "c" and move != "f":
                move = raw_input("Bot went all in!! Do you CALL [c], or FOLD [f]: ").lower();
        else:
            while move != "a" and move != "c" and move != "f" and move != "r":
                move = raw_input("Do you go ALL IN [a], CALL [c], FOLD [f], or RAISE [r]: ").lower();
        if move == "a":
            return Constants.ALLIN;
        elif move == "c":
            return Constants.CALL;
        elif move == "f":
            return Constants.FOLD;
        elif move == "r":
            return Constants.RAISE;

    def getBet(self):
        amt = -1;
        while amt < 0:
            try:
                amt = int(raw_input("Raise By: "));
            except ValueError:
                print("Must input a valid amount!");
        return amt;
