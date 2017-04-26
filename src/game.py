from deuces import *
from player import Player
from bot import Bot
from table import Table
from random import choice
from random import randint
from constants import Constants
from math import floor
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
    def __init__(self, rounds = 10, chips = 1000, big = 50, little = 25, alpha = 0.5, gamma = 0.8, agent = Constants.GENERAL):
        # Variables
        self.rounds = rounds;
        self.roundsSoFar = 0;
        self.chips = chips;
        self.player = Player(chips);
        self.bot = Bot(chips, alpha, gamma, agent);
        self.big = big;
        self.little = little;
        self.minBet = .25 * little;
        self.table = Table();
        self.eval = Evaluator();
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
        # Print showdown
        print("");
        print("==========================================");
        print("==========================================");
        print("                 SHOWDOWN");
        print("==========================================");
        print("==========================================");
        print("Cards on the board:");
        util.printCards(self.table.getCards());
        print("You have these cards:");
        util.printCards(self.player.getCards());
        print("THe bot had these cards:");
        util.printCards(self.bot.getCards());
        
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
            self.player.addChips(floor(pot/2));
            self.bot.addChips(floor(pot/2));
            return "TIE";

    '''
    Gets the reward for transitioning from one state to the next given a specific
    action.
    Rewards are as follows:
        A Fold returns -chipsIn
        A Call returns -ante
        A Raise or Allin returns pot*P(winning)
    '''
    def _getReward(self, state, action, nextState, winner):
        if winner == Constants.PLAYER:
            return -nextState[2];
        elif winner == Constants.BOT:
            return nextState[2];
        else:
            if action == Constants.CALL:
                return 0;
            elif action == Constants.FOLD:
                return -nextState[2];
            else:
                percentiles = util.winningPercentage(self.eval,self.player.getCards(),nextState[1],nextState[0]); 
                return nextState[2]*(percentiles[Constants.BOT]-percentiles[Constants.PLAYER]);

    def printResults(self):
        winner = None;
        pchips = self.player.getChips();
        bchips = self.bot.getChips();
        if pchips > bchips:
            winner = Constants.PLAYER
        elif pchips < bchips:
            winner = Constants.BOT
        elif pchips == bchips:
            winner = "SPLIT"
        print("===================================");
        print(" After {0} rounds the results are".format(self.roundsSoFar));
        print("===================================");
        print(" The player had ${0} chips".format(pchips));
        print(" Tha bot had ${0} chips".format(bchips));
        print(" The Winner is: {0}".format(winner));
        print("===================================");
            
    '''
    Determines whether the game is over.
    A game is over if there are no more rounds, or a player is out of chips at the end
    of a round.
    '''
    def isGameOver(self):
        if self.roundsSoFar >= self.rounds:
            printResults();
            return True;
        elif self.player.getChips() == 0:
            return True;
        elif self.bot.getChips() == 0:
            return True;
        return False;

    '''
    Automatically called by play.py to write the q-table out to file.
    @Deprecated
    '''
    def cleanup(self):
        self.bot.write();
    
    '''
    Plays a round.
    '''
    def playRound(self):
        self.table.addToPot(self.little+self.big);
        # Sub the blinds off
        self.player.subChips(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.subChips(self.big if self.dealer == Constants.BOT else self.little);
        self.player.addToChipsIn(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.addToChipsIn(self.big if self.dealer == Constants.BOT else self.little);
        # Stores the current player to go
        turn = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER;
        # Store the current stage of the game
        stage = Constants.FLOP;
        # Stores the previous move
        move = None;
        # Gets the winner
        winner = None;
        # Hold the successor state
        successor = None;
        # The last ante played
        lastAnte = 0;

        print("");
        print("==========================================");
        print("==========================================");
        print("            BEGINNING ROUND #{0}".format(self.roundsSoFar+1));
        print("             YOUR CHIPS: ${0}".format(self.player.getChips()));
        print("           OPPONENT CHIPS: ${0}".format(self.bot.getChips()));
        print("==========================================");
        print("==========================================");

        while stage != Constants.EVAL and stage != Constants.FOLD and stage != Constants.ALLIN:
            if self.player.getChips() == 0:
                turn = Constants.PLAYER;
                stage = Constants.ALLIN;
                lastAnte = self.table.getPot();
                break;
            elif self.bot.getChips() == 0:
                turn = Constants.BOT;
                stage = Constants.ALLIN;
                lastAnte = self.table.getPot();
                break;
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
               
            # Loop through the player moves
            for i in range(0, 2):
                state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), 0, self.bot.getAggression(), self.player.getPreviousMove(), self.dealer, self.bot.getChipsIn());
                
                if turn == Constants.PLAYER:
                    move = self.player.getMove(self.table.getCards(), self.table.getPot(), 0, self.bot.getPreviousMove());
                    self.player.setPreviousMove(move);
                else:
                    move = self.bot.getMove(state);
                    self.bot.setPreviousMove(move);
                print("The {0}s' move was {1}.".format(turn, self.player.getPreviousMove() if turn == Constants.PLAYER else self.bot.getPreviousMove()));

                # Deal with the most recent move
                if move == Constants.ALLIN:
                    stage = move;
                    break;
                elif move == Constants.FOLD:
                    stage = move;
                    break;
                
                if move == Constants.RAISE:
                    if turn == Constants.PLAYER:
                        amt = self.player.getBet(1);
                        ante = amt;
                        lastAnte = ante;
                        self.player.subChips(amt);
                        self.player.addToChipsIn(amt);
                        self.player.setAggression(amt, 1);
                        self.table.addToPot(amt);
                        response = self.bot.getMove(state);
                        if response == Constants.CALL:
                            self.bot.setPreviousMove(Constants.CALL);
                            self.bot.subChips(amt);
                            self.bot.addToChipsIn(amt);
                            self.bot.setAggression(amt, ante);
                            print("Adding to pot...");
                            self.table.addToPot(amt);
                        else:
                            turn = Constants.BOT;
                            stage == response;
                            break;
                    else:
                        amt = self.bot.getBet(1, self.bot.getBetType(self.bot.getCards(), self.table.getCards()));
                        ante = amt;
                        lastAnte = ante;
                        self.bot.subChips(amt);
                        self.bot.addToChipsIn(amt);
                        self.bot.setAggression(amt, 1);
                        self.table.addToPot(amt);
                        response = self.player.getMove(self.table.getCards(), self.table.getPot(), lastAnte, Constants.RAISE);
                        if response == Constants.CALL:
                            self.player.setPreviousMove(Constants.CALL);
                            self.player.subChips(amt);
                            self.player.addToChipsIn(amt);
                            self.player.setAggression(amt, ante);
                            print("Adding to pot...");
                            self.table.addToPot(amt);
                        else:
                            turn = Constants.PLAYER;
                            stage = response;
                            break;
                    successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), self.player.getPreviousMove(), self.dealer, self.bot.getChipsIn());
                    if self.player.getChips() == 0:
                        turn = Constants.PLAYER;
                        move = Constants.ALLIN;
                        break;
                    elif self.bot.getChips() == 0:
                        turn = Constants.BOT;
                        move = Constants.ALLIN;
                        break;

                # Call update in order to update the bots q-table
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), self.player.getPreviousMove(), self.dealer, self.bot.getChipsIn());
                if turn == Constants.BOT:
                    if self.bot.getAgent() == Constants.GENERAL:
                        self.bot.update(state, move, successor, self._getReward(state, move, successor, None));
                    else:
                        self.bot.updateApproximate(state, move, successor, self._getReward(state, move, successor, None));
                
                # Switch turns    
                turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT;

            self.player.setPreviousMove(None);
            self.bot.setPreviousMove(None);

            # Increment the stage
            if stage == Constants.FLOP:
                stage = Constants.TURN;
            elif stage == Constants.TURN:
                stage = Constants.RIVER;
            elif stage == Constants.RIVER:
                stage = Constants.EVAL;

        state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());

        # Check for all paths
        if stage == Constants.EVAL:
            print("The result was a {0} win!!!!".format(self._evaluate()));
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
        elif stage == Constants.FOLD:
            if turn == Constants.PLAYER:
                self.bot.addChips(self.table.getPot());
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
            else:
                self.player.addChips(self.table.getPot());
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
        # An all in is a bit more complex
        elif stage == Constants.ALLIN:
            # Take out the chips for the allin player
            if turn == Constants.PLAYER and self.player.getChips > 0:
                lastAnte = self.player.getChips();
                self.table.addToPot(self.player.getChips());
                self.player.addToChipsIn(self.player.getChips());
                self.player.setAggression(self.player.getChips(), 1);
                self.player.subChips(self.player.getChips());
            elif turn == Constants.BOT and self.bot.getChips() > 0:
                lastAnte = self.bot.getChips();
                self.table.addToPot(self.bot.getChips());
                self.bot.addToChipsIn(self.bot.getChips());
                self.bot.setAggression(self.bot.getChips(), 1);
                self.bot.subChips(self.bot.getChips());
            # Get the response from the opposing player
            turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT;
            if turn == Constants.PLAYER:
                move = self.player.getMove(self.table.getCards(), self.table.getPot(), lastAnte, move);
            else:
                move = self.bot.getMove((self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn()));
            # There was a call
            if move == Constants.CALL:
                # Take out the ante, or agents chips if taking ante would put the agent in the negative
                if turn == Constants.PLAYER:
                    self.table.addToPot(self.player.getChips() if self.player.getChips() - lastAnte < 0 else lastAnte);
                    self.player.addToChipsIn(self.player.getChips() if self.player.getChips() - lastAnte < 0 else lastAnte);
                    self.player.setAggression(lastAnte, 1);
                    self.player.subChips(self.player.getChips() if self.player.getChips() - lastAnte < 0 else lastAnte);
                else:
                    self.table.addToPot(self.bot.getChips() if self.bot.getChips() - lastAnte < 0 else lastAnte);
                    self.bot.addToChipsIn(self.bot.getChips() if self.bot.getChips() - lastAnte < 0 else lastAnte);
                    self.bot.setAggression(lastAnte, 1);
                    self.bot.subChips(self.bot.getChips() if self.bot.getChips() - lastAnte < 0 else lastAnte);
                # Deal out the remaining cards and evaluate
                for i in range(0, 5-len(self.table.getCards())):
                    self.table.addCard(self.table.draw());
                winner = self._evaluate();
                print("The result was a {0} win!!!!".format(winner));
            # There was a fold
            else:
                if turn == Constants.PLAYER:
                    self.bot.addChips(self.table.getPot());
                    winner = Constants.BOT;
                else:
                    self.player.addChips(self.table.getPot());
                    winner = Constants.PLAYER;

        if stage == Constants.EVAL or stage == Constants.ALLIN:
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn());
            if self.bot.getAgent() == Constants.GENERAL:
                self.bot.update(state, move, successor, self._getReward(state, self.bot.getPreviousMove(), (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn()), winner));
            else:
                self.bot.updateApproximate(state, move, successor, self._getReward(state, self.bot.getPreviousMove(), (self.table.getCards(), self.bot.getCards(), self.table.getPot(), lastAnte, self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn()), winner));

        # Swap turn for the next round
        turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT;
        # Resets for a new round
        self.dealer = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER;
        self.player.empty();
        self.bot.empty();
        self.table.reset();
        self.roundsSoFar += 1;
