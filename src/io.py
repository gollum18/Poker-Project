from deuces import Card

def IO:
    '''
    The default input method.
    Gets player input from the console.
    Input can be in the form [a,c,f,r].
    '''
    @staticmethod
    def getMoveFromConsole(table, player, allin):
        print("Cards on the table: ");
        Card.print_pretty_cards(table.getCards());
        print("Cards in your hand: ");
        Card.print_pretty_cards();
        print("Current Pot: {0}".format());
        print("Current Ante: {0}".format());

        move = "";
        if allin:
            print("Opposing player went all in!!");
            while move != "c" and move != "f":
                move = raw_input("Do you call[c] or fold[f]: ").lower();
        else:
            while move != "a" and move != "c" and move != "f" and move != "r":
                move = raw_input("Do you go all in [a], call [c], fold[f], or raise[r]: ").lower();
        return move;
