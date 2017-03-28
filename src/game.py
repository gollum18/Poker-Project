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
        self.moveLock = threading.Lock();
        self.dealer = choice([Constants.PLAYER, Constants.BOT]);

    '''
    Determines the winner at the end of a round.
    Will automatically deal out the pot.
    '''
    def _evaluate(self, pot):
        pstr = self.eval.evaluate(self.player.getCards(), self.table.getCards());
        bstr = self.eval.evaluate(self.bot.getCards(), self.table.getCards());
        if pstr > bstr:
            self.player.addChips(pot);
        elif pstr < bstr:
            self.bot.addChips(pot);
        else:
            self.player.addChips(pot/2);
            self.bot.addChips(pot/2);

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
        self.table.addToAnte(self.little);
        self.table.addToPot(self.little+self.big);
        # Sub the blinds off
        self.player.subChips(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.subChips(self.big if self.dealer == Constants.BOT else self.little);
        # Stores the current player to go
        turn = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER;
        # Store the current stage of the game
        stage = Constants.FLOP;
        # Stores the previous move

        while stage != Constants.EVAL and stage != Constants.FOLD and stage != Constants.ALLIN:
            # Deal out the cards
            if stage == Constants.FLOP:
                for i in range(0, 5):
                    if i < 3:
                        self.table.addCard(self.table.draw());
                    elif 3 <= i < 5:
                        if self.dealer == Constants.PLAYER:
                            self.bot.addCard(self.table.draw());
                            self.player.addCard(self.table.draw());
                        else:
                            self.player.addCard(self.table.draw());
                            self.bot.addCard(self.table.draw());
            elif stage == Constants.TURN or Constants.RIVER:
                self.table.addCard(self.table.draw());

            Card.print_pretty_cards(self.table.getCards());
            
            # Loop through the player moves
            for i in range(0, 2):
                if turn == Constants.PLAYER:
                    move = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), move);
                elif turn == Constants.BOT:
                    move = self.bot.getMove();

                # Deal with the most recent move
                # If the move is allin or a fold, deal with it outside, they are special conditions
                # Modifying data below, acquire lock and release when done
                self.moveLock.acquire();
                if move == Constants.ALLIN:
                    stage = move;
                    break;
                elif move == Constants.FOLD:
                    stage = move;
                    break;
                # Otherwise, deal with the move here
                elif move == Constants.CALL:
                    if turn == self.Constants.PLAYER:
                        self.player.subChips(self.table.getAnte()):
                    elif turn == self.Constants.BOT:
                        self.bot.subChips(self.table.getAnte());
                    self.table.addToPot(self.table.getAnte());
                    self.table.addToAnte(self.table.getAnte());
                elif move == Constants.RAISE:
                    raiseAmt = 0
                    if turn == Constants.PLAYER:
                        raiseAmt = self.player.getRaise();
                        self.player.subChips(self.table.getAnte() + raiseAmt);
                    elif turn == Constants.BOT:
                        raiseAmt = self.bot.getRaise();
                        self.bot.subChips(self.table.getAnte() + raiseAmt);
                    self.table.addToPot(self.table.getAnte() + raiseAmt);
                    self.table.addToAnte(raiseAmt);
                # Release the movelock
                self.moveLock.release();
                
                # Switch turns    
                turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT;

            # Increment the stage
            if stage == Constants.FLOP:
                stage = Constants.TURN;
            elif stage == Constants.TURN:
                stage = Constants.RIVER;
            elif stage == Constants.RIVER:
                stage = Constants.EVAL;

        # Check for all paths
        if stage == Constants.EVAL:
            self._evaluate(self.table.getPot());
        elif stage == Constants.FOLD:
            print Constants.FOLD;
        elif stage == Constants.ALLIN:
            print Constants.ALLIN;

        self.dealer = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER;
        self.player.empty();
        self.bot.empty();
        self.table.reset();
        
