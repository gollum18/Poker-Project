from deuces import *
from player import Player
from bot import Bot
from table import Table
from random import choice
from constants import Constants

'''
Defines a poker game.
A poker game has rounds, a player, a bot, the table, and the hand evaluator.
'''
class Game:
    '''
    Create a poker game.
    Takes a number of rounds and an amount of starting chips.
    '''
    def __init__(self, rounds, chips, big, little):
        # Variables
        self.rounds = rounds;
        self.player = Player(chips);
        self.bot = Bot(chips);
        self.big = big;
        self.little = little;
        self.table = Table();
        self.eval = Evaluator();
        self.dealer = choice([Constants.PLAYER, Constants.BOT]);

    '''
    Determines the winner at the end of a round.
    Returns 0 if there was a split, -1 if the player won, or 1 if the bot won.
    '''
    def _evaluate(self):
        pstr = self.eval.evaluate(self.player.getCards(), self.table.getCards());
        bstr = self.eval.evaluate(self.bot.getCards(), self.table.getCards());
        if pstr > bstr:
            return Constants.PLAYER;
        elif pstr < bstr:
            return Constants.BOT;
        else:
            return Constants.SPLIT;

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
        # Setup the round
        pot = self.big + self.little;
        self.player.subChips(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.subChips(self.big if self.dealer == Constants.BOT else self.little);
        ante = self.little;

        # Deal out the cards
        for i in range(0, 2):
            if self.dealer == Constants.PLAYER:
                self.bot.addCard(self.table.draw());
                self.player.addCard(self.table.draw());
            else:
                self.player.addCard(self.table.draw());
                self.bot.addCard(self.table.draw());

        # TODO: Implement Logic Here
        stage = Constants.FLOP;
        turn = (Constants.BOT if self.dealer == Constants.PLAYER else Constants.PLAYER);
        move = None;
        while stage != Constants.EVAL and stage != Constants.ALLIN and stage != Constants.FOLD:
            if stage == Constants.FLOP:
                for i in range(0, 3):
                    self.table.addCard(self.table.draw());
            else:
                self.table.addCard(self.table.draw());
            # Get the players moves, based on dealer
            for i in range(0, 2):
                # Get the move
                if turn == Constants.PLAYER:
                    move = self.player.getMove(self.table.getCards(), pot, ante, move);
                else:
                    move = self.bot.getMove(move);
                # Check if it is a fold or allin
                if move == Constants.ALLIN:
                    stage = Constants.ALLIN;
                    break;
                elif move == Constants.FOLD:
                    stage = Constants.FOLD;
                    break;
                elif move == Constants.CALL:
                    pot += ante;
                    if turn == Constants.PLAYER:
                        self.player.subChips(ante);
                    else:
                        self.bot.subChips(ante);
                elif move == Constants.RAISE:
                    amt = 0;
                    if turn == Constants.PLAYER:
                        amt = self.player.getRaise();
                        self.player.subChips(ante+amt);
                    else:
                        amt = self.bot.getRaise();
                        self.bot.subChips(ante+amt);
                    ante += amt;
                    pot += ante;
                turn = (Constants.PLAYER if turn == Constants.BOT else Constants.BOT);
            # End of stage, advance
            if stage == Constants.ALLIN or stage == Constants.FOLD:
                break;
            elif stage == Constants.FLOP:
                stage = Constants.TURN;
            elif stage == Constants.TURN:
                stage = Constants.RIVER;
            elif stage == Constants.RIVER:
                stage = Constants.EVAL;

        # Check for the paths
        # The normal path
        if stage == Constants.EVAL:
            winner = self._evaluate();
            if winner == Constants.PLAYER:
                self.player.addChips(pot);
            elif winner == Constants.BOT:
                self.bot.addChips(pot);
            else:
                self.player.addChips(pot/2);
                self.bot.addChips(pot/2);
        # Alternative path 1
        elif stage == Constants.FOLD:
            if turn == Constants.PLAYER:
                self.bot.addChips(pot);
            else:
                self.player.addChips(pot);
        # Alternative path 2
        elif stage == Constants.ALLIN:
            if turn == Constants.PLAYER:
                if self.bot.getMove(move) == Constants.FOLD:
                    self.player.addChips(pot);
                else:
                    self.bot.subChips(ante);
                    pot += ante;
            else:
                if self.player.getMove(self.table.getCards(), pot, ante, Constants.ALLIN) == Constants.FOLD:
                    self.bot.addChips(pot);
                else:
                    self.player.subChips(ante);
                    pot += ante;
            winner = self._evaluate();
            if winner == Constants.PLAYER:
                self.player.addChips(pot);
            elif winner == Constants.BOT:
                self.bot.addChips(pot);
            else:
                self.player.addChips(pot/2);
                self.bot.addChips(pot/2);
        # Subtract off the round
        self.rounds -= 1;
        # Reset for next round
        self.dealer = (Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER);
        self.player.empty();
        self.bot.empty();
        self.table.reset();
