from deuces import *
from player import Player
from bot import Bot
from table import Table
from random import choice
from constants import Constants
import threading
import util

'''
Defines a poker game.
A poker game has rounds, a player, a bot, the table, and the hand evaluator.
'''
class Game:
    '''
    Create a poker game.
    Takes a number of rounds and an amount of starting chips.
    '''
    def __init__(self, rounds = 10, chips = 1000, big = 50, little = 25, alpha = 0.5, gamma = 0.8):
        # Variables
        self.rounds = rounds;
        self.player = Player(chips);
        self.bot = Bot(chips, alpha, gamma);
        self.big = big;
        self.little = little;
        self.minBet = .25 * little;
        self.table = Table();
        self.eval = Evaluator();
        self.moveLock = threading.Lock();
        self.dealer = choice([Constants.PLAYER, Constants.BOT]);

    '''
    Determines the winner at the end of a round. Will automatically deal out the pot.
    This is a private to be called by this class only (hence the _), do not call it.
    '''
    def _evaluate(self):
        # Get the pot and cards on the board
        pot = self.table.getPot();
        board = self.table.getCards();
        # Get the strengths of both players hands
        pstr = self.eval.evaluate(self.player.getCards(), board);
        bstr = self.eval.evaluate(self.bot.getCards(), board);
        # Print the strength of the hands
        print("The player with the lower hand strength wins.");
        print("The players had the following hand strengths:");
        print("Player strength: {0}".format(pstr));
        print("Bot stength: {0}".format(bstr));
        # Print the players ranks
        print("The player had the following hand: {0}.".format(self.eval.class_to_string(self.eval.get_rank_class(pstr))));
        print("The bot had the following hand: {0}".format(self.eval.class_to_string(self.eval.get_rank_class(bstr))));
        # Deal out the chips appropriately
        # I know this seems weird but hands in deuces are ranked starting at
        # 1 with 1 being the best hand.
        if pstr < bstr:
            self.player.addChips(pot);
            return Constants.PLAYER;
        elif pstr > bstr:
            self.bot.addChips(pot);
            return Constants.BOT;
        else:
            self.player.addChips(pot/2);
            self.bot.addChips(pot/2);
            return "TIE";

    '''
    Gets the reward for transitioning from one state to the next given a specific
    action.
    Rewards are as follows:
        A Fold returns -chipsIn
        A Call returns -ante
        A Raise or Allin returns pot*P(winning)-chipsIn
    '''
    def _getReward(self, state, action, nextState):
        if action == Constants.RAISE or action == Constants.ALLIN:
            return nextState[2]*util.strength(self.eval,nextState[1],nextState[0])-nextState[7];
        elif action == Constants.CALL:
            return -nextState[3];
        return -nextState[7];

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

    def cleanup(self):
        self.bot.writeTable();
    
    '''
    Plays a round.
    '''
    def playRound(self):
        self.table.addToAnte(self.little);
        self.table.addToPot(self.little+self.big);
        # Sub the blinds off
        self.player.subChips(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.subChips(self.big if self.dealer == Constants.BOT else self.little);
        self.bot.addToChipsIn(self.big if self.dealer == Constants.BOT else self.little);
        # Stores the current player to go
        turn = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER;
        # Store the current stage of the game
        stage = Constants.FLOP;
        # Stores the previous move
        move = None;
        # Gets the winner
        winner = None;

        print("==========================================");
        print("==========================================");
        print("            BEGINNING ROUND #{0}".format(11-self.rounds));
        print("             YOUR CHIPS: ${0}".format(self.player.getChips()));
        print("           OPPONENT CHIPS: ${0}".format(self.bot.getChips()));
        print("==========================================");
        print("==========================================");

        while stage != Constants.EVAL and stage != Constants.FOLD and stage != Constants.ALLIN:
            # Deal out the cards
            if stage == Constants.FLOP:
                for i in range(0, 5):
                    # Deal out the cards to the table
                    if i < 3:
                        self.table.addCard(self.table.draw());
                    # Deal out the cards to the players
                    else:
                        if self.dealer == Constants.PLAYER:
                            self.bot.addCard(self.table.draw());
                            self.player.addCard(self.table.draw());
                        else:
                            self.player.addCard(self.table.draw());
                            self.bot.addCard(self.table.draw());
            elif stage == Constants.TURN or stage == Constants.RIVER:
                self.table.addCard(self.table.draw());

            state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
            
            # Loop through the player moves
            for i in range(0, 2):
                if turn == Constants.PLAYER:
                    move = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), move);
                else:
                    move = self.bot.getMove(state);
                print("The {0}s' move was {1}.".format(turn, move));

                # Deal with the most recent move
                # If the move is allin or a fold, deal with it outside, they are special conditions
                if move != Constants.ALLIN and move != Constants.FOLD:
                    # We will be modifying data, need to lock here
                    self.moveLock.acquire();
                else:
                    if move == Constants.ALLIN:
                        stage = move;
                        break;
                    elif move == Constants.FOLD:
                        stage = move;
                        break;

                ante = self.table.getAnte();
                
                # Otherwise, deal with the move here
                if move == Constants.CALL:
                    if turn == Constants.PLAYER:
                        self.player.subChips(ante);
                        self.player.setAggression(ante, ante);
                    else:
                        self.bot.subChips(ante);
                        self.bot.setAggression(ante, ante);
                    self.table.addToPot(ante);
                elif move == Constants.RAISE:
                    raiseAmt = 0;
                    if turn == Constants.PLAYER:
                        raiseAmt = self.player.getBet();
                        self.player.subChips(ante + raiseAmt);
                        self.player.setAggression(raiseAmt, ante);
                    else:
                        raiseAmt = self.bot.getBet(self.minBet, self.bot.getBetType(self.bot.getCards(), self.table.getCards()));
                        self.bot.addToChipsIn(ante + raiseAmt);
                        self.bot.subChips(ante + raiseAmt);
                        self.bot.setAggression(raiseAmt, ante);
                    self.table.addToPot(ante + raiseAmt);
                    self.table.addToAnte(raiseAmt);
                # Release the movelock
                self.moveLock.release();

                # Call update in order to update the bots q-table
                if turn == Constants.BOT:
                    successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
                    self.bot.update(state, move, successor, self._getReward(state, move, successor));
                
                # Switch turns    
                turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT;

            # Increment the stage
            if stage == Constants.FLOP:
                stage = Constants.TURN;
            elif stage == Constants.TURN:
                stage = Constants.RIVER;
            elif stage == Constants.RIVER:
                stage = Constants.EVAL;

        state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());

        # Check for all paths
        if stage == Constants.EVAL:
            print("The result was a {0} win!!!!".format(self._evaluate()));
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
            self.bot.update(state, move, successor, self._getReward(state, move, successor));
        elif stage == Constants.FOLD:
            if turn == Constants.PLAYER:
                self.bot.addChips(self.table.getPot());
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
                self.bot.update(state, move, successor, self._getReward(state, move, successor));
            else:
                self.player.addChips(self.table.getPot());
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
                self.bot.update(state, move, successor, self._getReward(state, move, successor));
        # An all in is a bit more complex
        elif stage == Constants.ALLIN:
            # Take out the chips for the allin player
            if turn == Constants.PLAYER:
                self.table.addToPot(self.player.getChips());
                self.table.addToAnte(self.player.getChips());
                self.player.subChips(self.player.getChips());
                self.player.setAggression(self.player.getChips(), self.table.getAnte());
            else:
                self.table.addToPot(self.bot.getChips());
                self.table.addToAnte(self.bot.getChips());
                self.bot.addToChipsIn(self.bot.getChips());
                self.bot.subChips(self.bot.getChips());
                self.bot.setAggression(self.player.getChips(), self.table.getAnte());
            # Get the response from the opposing player
            turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT;
            if turn == Constants.PLAYER:
                move = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), move);
            else:
                move = self.bot.getMove((self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn()));
            # There was a call
            if move == Constants.CALL:
                # Take out the ante, or agents chips if taking ante would put the agent in the negative
                if turn == Constants.PLAYER:
                    self.table.addToPot(self.player.getChips());
                    self.player.addToChipsIn(self.table.getAnte());
                    self.player.setAggression(self.table.getAnte(), self.table.getAnte());
                    self.player.subChips(self.table.getAnte());
                else:
                    self.table.addToPot(self.bot.getChips());
                    self.bot.addToChipsIn(self.table.getAnte());
                    self.bot.setAggression(self.table.getAnte(), self.table.getAnte());
                    self.bot.subChips(self.table.getAnte());
                # Deal out the remaining cards and evaluate
                for i in range(0, 5-len(self.table.getCards())):
                    self.table.addCard(self.table.draw());
                print("The result was a {0} win!!!!".format(self._evaluate()));
            # There was a fold
            else:
                if turn == Constants.PLAYER:
                    self.bot.addChips(self.table.getPot());
                else:
                    self.player.addChips(self.table.getPot());

            if turn == Constants.BOT:
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
                self.bot.update(state, move, successor, self._getReward(state, move, successor));

        self.dealer = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER;
        self.player.empty();
        self.bot.empty();
        self.table.reset();
        self.rounds -=1;
        
