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
        pot = self.big + self.little;
        self.player.sub(self.little if self.dealer == Constants.PLAYER else self.big);
        self.bot.sub(self.little if self.dealer == Constants.BOT else self.big);
        ante = self.little;
        for i in range(0, 2):
            if self.dealer == Constants.PLAYER:
                self.bot.add(self.table.draw());
                self.player.add(self.table.draw());
            else:
                self.player.add(self.table.draw());
                self.bot.add(self.table.draw());
        stage = None;
        move = None;
        prevMove = None;
        turn = (Constants.BOT if self.dealer == Constants.PLAYER else Constants.PLAYER);
        while stage != Constants.EVAL or stage != Constants.FOLD or stage Constants.ALLIN:
            if stage == Constants.FLOP:
                for i in range(0, 3):
                    self.table.add(self.table.draw());
            else:
                self.table.add(self.table.draw());
            # Get the players moves, respond to them
            for iterTurn in range(0, 2):
                prevMove = move;
                move = (self.player.getMove(self.table.getCards(), pot, ante, prevMove) if turn == Constants.PLAYER else self.bot.getMove());
                turn = (Constants.PLAYER if turn == Constants.BOT else Constants.PLAYER);
                # Check for alternative path 2
                if move == Constants.ALLIN:
                    stage = Constants.ALLIN;
                    break;
                # Check for alternative path 1
                elif move == Constants.FOLD:
                    stage = Constants.FOLD;
                    break;
                elif move == Constants.CALL:
                    pot += ante;
                    if turn == Constants.PLAYER:
                        self.bot.sub(ante);
                    else:
                        self.player.sub(ante);
                elif move == Constants.RAISE:
                    amt = 0;
                    if turn == Constants.PLAYER:
                        amt = self.bot.getRaise();
                        self.bot.sub(ante+amt);
                    else:
                        amt = self.bot.getRaise();
                        self.player.sub(ante+amt);
                    ante += amt;
                    pot += ante;
            # Advances to the next stage
            if stage == Constants.FLOP:
                stage = Constants.TURN;
            elif stage == Constants.TURN:
                stage = Constants.RIVER:
            elif stage == Constants.RIVER:
                stage = Constants.EVAL;
        # Check for eval conditions
        # Can either be EVAL, FOLD, or ALLIN
        # Each stage is handled differently
        # Normal path, reached through expected game play
        if stage == Constants.EVAL:
            winner = self._evaluate();
            if winner == Constants.SPLIT:
                self.player.add(pot/2);
                self.bot.add(pot/2);
            elif winner == Constants.PLAYER:
                self.player.add(pot);
            elif winner == Constants.BOT:
                self.bot.add(pot);
        # Alternative path 1, a player folded
        elif stage == Constants.FOLD:
            # Here the player currently selected by turn is the next player after the fold
            if turn == Constants.PLAYER:
                self.bot.add(pot);
            else:
                self.player.add(pot);
        # Alternative path 2, a player went all in
        elif stage == Constants.ALLIN:
            # Get the other players response, same situation as in fold
            response = None;
            if turn == Constants.PLAYER:
                # Add the bots chips to the pot, sub them out
                pot += self.bot.getChips();
                self.bot.sub(self.bot.getChips());
                # Get the Bots response
                response = self.bot.getMove();
            else:
                # Add the players chips to the pot, sub them out
                pot += self.player.getChips();
                self.player.sub(self.player.getChips());
                # Get the Players response
                response = self.player.getMove(self.table.getCards(), pot, ante, Constants.ALLIN);
            # Execute the response
            if response == Constants.FOLD:
                if turn == Constants.PLAYER:
                    self.player.add(pot);
                else:
                    self.bot.add(pot);
            elif response == Constants.CALL:
                if turn == Constants.PLAYER:
                    self.bot.sub(ante);
                else:
                    self.player.sub(ante);
                # Deal out the remaining cards
                for i in range(0, 5-len(self.table.getCards())):
                    self.table.add(self.table.draw());
                # Handle like the eval stage, will fix reuse later
                winner = self._evaluate();
                if winner == Constants.SPLIT:
                    self.player.add(pot/2);
                    self.bot.add(pot/2);
                elif winner == Constants.PLAYER:
                    self.player.add(pot);
                elif winner == Constants.BOT:
                    self.bot.add(pot);
        # Reset for the next round
        self.dealer = (Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER);
        self.player.empty();
        self.bot.empty();
        self.table.reset();
