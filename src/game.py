from deuces import *
from random import choice

'''
Defines a poker game.
A poker game has rounds, a player, a bot, the table, and the hand evaluator.
'''
class Game:
    '''
    Create a poker game.
    Takes a number of rounds and an amount of starting chips.
    '''
    def __init__(self, rounds, chips):
        # Constants, do not change
        self.PLAYER = -1;
        self.BOT = 1;
        self.SPLIT = 0;
        # Variables
        self.rounds = rounds;
        self.player = Player(chips);
        self.bot = Bot(chips);
        self.table = Table();
        self.eval = Evaluator();
        self.dealer = choice(self.PLAYER, self.BOT);

    '''
    Determines the winner at the end of a round.
    Returns 0 if there was a split, -1 if the player won, or 1 if the bot won.
    '''
    def _evaluate(self):
        pstr = self.eval.evaluate(self.table.getCards() + self.player.getCards());
        bstr = self.eval.evaluate(self.table.getCards() + self.bot.getCards());
        if pstr > bstr:
            return self.PLAYER;
        elif pstr < bstr:
            return self.BOT;
        else:
            return self.SPLIT;

    def _executeMove(self, move, player):

    '''
    Determines whether the game is over.
    A game is over if there are no more rounds, or a player is out of chips at the end
    of a round.
    '''
    def isGameOver(self):
        if self.rounds == 0:
            return True;
        elif self.player.getChips() == 0:
            return True;
        elif self.bot.getChips() == 0:
            return True;
        return False;

    '''
    Plays a round.
    '''
    def playRound(self):
        # Deal out the cards to the players, DEALER always has the advantage in Poker
        for i in range(0, 2):
            if self.dealer == self.PLAYER:
                self.bot + self.table.draw();
                self.player + self.table.draw();
            else:
                self.player + self.table.draw();
                self.bot + self.table.draw();

        # Deal out the flop
        for i in range (0, 3):
            self.table + self.table.draw();

        # Holds the last move
        move = "";

        # TODO: Core Game Logic Goes Here

        # End of round, decrement round count
        self.rounds -= 1;

        # Reset the table, swap dealers, and empty the hands
        self.dealer = (self.PLAYER if self.dealer == self.BOT else self.PLAYER);
        self.table.reset();
        self.player.empty();
        self.bot.empty();
