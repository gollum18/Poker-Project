from deuces import *
from player import Player
from bot import Bot
from table import Table
from random import choice
from random import randint
from constants import Constants
from math import floor
import util

class Game:
    def __init__(self, rounds, chips, big, little, alpha, gamma, agent):
        self.rounds = rounds
        self.roundsSoFar = 0;
        self.chips = chips;
        self.player = Player(chips)
        self.bot = Bot(chips, alpha, gamma, agent)
        self.big = big
        self.little = little
        self.minBet = int(.25 * little);
        self.table = Table();
        self.eval = Evaluator();
        self.dealer = choice([Constants.PLAYER, Constants.BOT]);

    def evaluate(self):
        pot = self.table.getPot()
        board = self.table.getCards()
        pstr = self.eval.evaluate(self.player.getCards(), board)
        bstr = self.eval.evaluate(self.bot.getCards(), board)
        # Print showdown
        print("")
        print("==========================================")
        print("==========================================")
        print("                 SHOWDOWN")
        print("==========================================")
        print("==========================================")
        print("Cards on the board:")
        util.printCards(self.table.getCards())
        print("You have these cards:")
        util.printCards(self.player.getCards())
        print("The bot had these cards:")
        util.printCards(self.bot.getCards())

        print("The player had: {0}.".format(self.eval.class_to_string(self.eval.get_rank_class(pstr))))
        print("The bot had had: {0}.".format(self.eval.class_to_string(self.eval.get_rank_class(bstr))))
        # Deal out the chips appropriately
        # I know this seems weird but hands in deuces are ranked starting at
        # 1 with 1 being the best hand.
        if pstr < bstr:
            self.player.addChips(pot)
            print("The {0} has won!!".format(Constants.PLAYER))
            return Constants.PLAYER
        elif pstr > bstr:
            self.bot.addChips(pot)
            print("The {0} has won!!".format(Constants.BOT))
            return Constants.BOT
        else:
            self.player.addChips(int(floor(pot/2)))
            self.bot.addChips(int(floor(pot/2)))
            return "TIE"

    def getReward(self, state, action, nextState, winner):
        if winner == Constants.PLAYER:
            return -nextState[2]
        elif winner == Constants.BOT:
            return nextState[2]
        else:
            if action == Constants.CALL:
                return 0
            elif action == Constants.FOLD:
                return -nextState[2]
            else:
                percentiles = util.winningPercentage(self.eval,self.player.getCards(),nextState[1],nextState[0]) 
                if action == Constants.ALLIN:
                    return nextState[2]*(percentiles[Constants.BOT]-percentiles[Constants.PLAYER])
                else:
                    return -state[3]+(nextState[2]*percentile[Constants.BOT])
    '''
    Determines whether the game is over.
    A game is over if there are no more rounds, or a player is out of chips at the end
    of a round.
    '''
    def isGameOver(self):
        if self.roundsSoFar >= self.rounds:
            self.printResults();
            return True;
        elif self.player.getChips() == 0:
            self.printResults();
            return True;
        elif self.bot.getChips() == 0:
            self.printResults();
            return True;
        return False;

    '''
    Automatically called by play.py to write the q-table out to file.
    @Deprecated
    '''
    def cleanup(self):
        self.bot.write();

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
        print("")
        print("===================================");
        print(" After {0} rounds the results are".format(self.roundsSoFar));
        print("===================================");
        print(" The player had ${0} chips".format(pchips));
        print(" The bot had ${0} chips".format(bchips));
        print(" The Winner is: {0}".format(winner));
        print("===================================");

    def playRound(self):
        # setup for the round
        self.table.addToPot(self.little+self.big);
        self.player.subChips(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.subChips(self.big if self.dealer == Constants.BOT else self.little);
        self.player.addToChipsIn(self.big if self.dealer == Constants.PLAYER else self.little);
        self.bot.addToChipsIn(self.big if self.dealer == Constants.BOT else self.little);

        turn = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER
        stage = Constants.FLOP
        move = None
        state = None
        successor = None
        cumReward = 0;

        print("");
        print("==========================================");
        print("==========================================");
        print("            BEGINNING ROUND #{0}".format(self.roundsSoFar+1));
        print("             YOUR CHIPS: ${0}".format(self.player.getChips()));
        print("           OPPONENT CHIPS: ${0}".format(self.bot.getChips()));
        print("==========================================");
        print("==========================================");

        while (
            stage != Constants.EVAL
            and stage != Constants.FOLD
            and stage != Constants.ALLIN
            and stage != Constants.NOCHIPSLEFT
            ):
            # Deal out all the cards
            if stage == Constants.FLOP:
                for i in range (0, 5):
                    if i < 3:
                        # Deal out the cards for the flop 
                        self.table.addCard(self.table.draw())
                    else:
                        # Deal out the cards to the players based on dealer
                        if self.dealer == Constants.PLAYER:
                            self.bot.addCard(self.table.draw());
                            self.player.addCard(self.table.draw());
                        else:
                            self.player.addCard(self.table.draw());
                            self.bot.addCard(self.table.draw());
            # Otherwise, deal out the cards to the table
            elif stage == Constants.TURN or stage == Constants.RIVER:
                self.table.addCard(self.table.draw());

            if self.player.getChips() == 0:
                stage == Constants.ALLIN
                break;
            elif self.bot.getChips() == 0:
                stage == Constants.ALLIN
                break;

            # Get the players moves and react to them
            for i in range (0, 2):
                # Get the players move
                if turn == Constants.PLAYER:
                    move = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), move)
                    self.player.setPreviousMove(move)
                else:
                    state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), move)
                    move = self.bot.getMove(state);
                    self.bot.setPreviousMove(move)
                print("The {0}s' move was {1}.".format(turn, move))

                if move == Constants.ALLIN:
                    stage = Constants.ALLIN
                    break;
                elif move == Constants.FOLD:
                    stage = Constants.FOLD
                    break;
                elif move == Constants.RAISE:
                    if turn == Constants.PLAYER:
                        self.table.setAnte(self.player.getBet(self.little))
                        self.player.addToChipsIn(self.table.getAnte())
                        self.player.subChips(self.table.getAnte())
                        self.player.setAggression(self.table.getAnte(), self.little)
                        self.table.addToPot(self.table.getAnte())
                        state = (self.table.getCards(),self.bot.getCards(),self.table.getPot(),self.table.getAnte(),self.bot.getAggression(),move,self.dealer,self.bot.getChipsIn())
                        response = self.bot.getMove(state)
                        # was the bots response a call?
                        if response == Constants.CALL:
                            print("The BOT chose to CALL your RAISE.")
                            self.bot.setAggression(self.bot.getCall(self.table.getAnte()),self.table.getAnte())
                            self.bot.addToChipsIn(self.bot.getCall(self.table.getAnte()))
                            self.table.addToPot(self.bot.getCall(self.table.getAnte()))
                            self.bot.subChips(self.bot.getCall(self.table.getAnte()))
                            self.table.setAnte(0)
                            move = None
                        # was the bots response a fold?
                        else:
                            print("The BOT chose to FOLD on your RAISE.")
                            self.bot.setAggression(0, self.table.getAnte())
                            stage = Constants.FOLD
                            turn = Constants.BOT
                            break
                    elif turn == Constants.BOT:
                        self.table.setAnte(self.bot.getBet(self.little, self.bot.getBetType(self.bot.getCards(), self.table.getCards())))
                        self.bot.addToChipsIn(self.table.getAnte())
                        self.bot.subChips(self.table.getAnte())
                        self.bot.setAggression(self.table.getAnte(), self.little)
                        self.table.addToPot(self.table.getAnte())
                        response = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), Constants.RAISE)
                        if response == Constants.CALL:
                            print("The PLAYER chose to CALL the BOT's RAISE.")
                            self.player.setAggression(self.player.getCall(self.table.getAnte()),self.table.getAnte())
                            self.player.addToChipsIn(self.player.getCall(self.table.getAnte()));
                            self.table.addToPot(self.player.getCall(self.table.getAnte()))
                            self.player.subChips(self.player.getCall(self.table.getAnte()))
                            self.table.setAnte(0)
                            move = None;
                        else:
                            print("The PLAYER chose to FOLD on the BOT's RAISE.")
                            self.player.setAggression(0, self.table.getAnte())
                            stage = Constants.FOLD
                            turn = Constants.PLAYER
                            break
                    if self.player.getChips() == 0 or self.bot.getChips() == 0:
                        stage = Constants.NOCHIPSLEFT
                        break;
                # End of turn, swap turns
                turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT
            if stage == Constants.FLOP:
                stage = Constants.TURN
            elif stage == Constants.TURN:
                stage = Constants.RIVER
            elif stage == Constants.RIVER:
                stage = Constants.EVAL

        # This stage is reached when a call occurs where a player is left with no chips
        #   treat like and allin
        if stage == Constants.NOCHIPSLEFT:
            for i in range(5-len(self.table.getCards())):
                self.table.addCard(self.table.draw())
            winner = self.evaluate();
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), self.bot.getPreviousMove())
            reward = self.getReward(state, self.bot.getPreviousMove(), successor, winner)
            cumReward = cumReward + reward
            if self.bot.getAgent() == Constants.GENERAL:
                self.bot.update(state, self.bot.getPreviousMove(), successor, reward)
            else:
                self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, reward)
            
        elif stage == Constants.ALLIN:
            #print "A player went all in... The turn is now {0}".format(turn)
            
            response = None;

            if self.player.getChips != 0 and self.bot.getChips() != 0:
                # Take out all the chips
                if turn == Constants.PLAYER:
                    self.table.setAnte(self.player.getChips())
                    self.table.addToPot(self.table.getAnte())
                    self.player.addToChipsIn(self.table.getAnte())
                    self.player.setAggression(self.table.getAnte(), self.little)
                    self.player.subChips(self.table.getAnte())
                    state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), Constants.ALLIN, self.dealer, self.bot.getChipsIn())
                    response = self.bot.getMove(state)
                    if response == Constants.CALL:
                        print("The BOT chose to CALL your ALLIN.")
                        self.bot.setAggression(self.bot.getCall(self.table.getAnte), self.little)
                        self.bot.addToChipsIn(self.bot.getCall(self.table.getAnte()))
                        self.table.addToPot(self.bot.getCall(self.table.getAnte()))
                        self.bot.subChips(self.bot.getCall(self.table.getAnte()))
                        self.table.setAnte(0)
                    else:
                        print("The BOT chose to FOLD on your ALLIN.")
                        winner = Constants.PLAYER
                        self.player.addChips(self.table.getPot())
                else:
                    self.table.setAnte(self.bot.getChips())
                    self.table.addToPot(self.table.getAnte())
                    self.bot.addToChipsIn(self.table.getAnte())
                    self.bot.setAggression(self.table.getAnte(), self.little)
                    self.bot.subChips(self.table.getAnte())
                    response = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), Constants.ALLIN)
                    if response == Constants.CALL:
                        print("The PLAYER chose to CALL the BOTs' ALLIN.")
                        self.player.setAggression(self.player.getCall(self.table.getAnte), self.little)
                        self.player.addToChipsIn(self.player.getCall(self.table.getAnte()))
                        self.table.addToPot(self.player.getCall(self.table.getAnte()))
                        self.player.subChips(self.player.getCall(self.table.getAnte()))
                        self.table.setAnte(0)
                    else:
                        print("The PLAYER chose to FOLD on the BOTs' ALLIN.")
                        winner = Constants.BOT
                        self.bot.addChips(self.table.getPot())
                        successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), self.bot.getPreviousMove())
                        reward = self.getReward(state, self.bot.getPreviousMove(), successor, winner)
                        cumReward = cumReward + reward
                        if self.bot.getAgent() == Constants.GENERAL:
                            self.bot.update(state, self.bot.getPreviousMove(), successor, reward)
                        else:
                            self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, reward)
                            
            if response == Constants.CALL:
                # Deal out the remaining cards
                for i in range(5-len(self.table.getCards())):
                    self.table.addCard(self.table.draw())
                # Evaluate
                winner = self.evaluate();
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), self.bot.getPreviousMove())
                reward = self.getReward(state, self.bot.getPreviousMove(), successor, winner)
                cumReward = cumReward + reward
                if self.bot.getAgent() == Constants.GENERAL:
                    self.bot.update(state, self.bot.getPreviousMove(), successor, reward)
                else:
                    self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, reward)
                
        elif stage == Constants.FOLD:
            if turn == Constants.PLAYER:
                self.bot.addChips(self.table.getPot())
            elif turn == Constants.BOT:
                self.player.addChips(self.table.getPot())
        elif stage == Constants.EVAL:
            winner = self.evaluate();
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(), self.bot.getAggression(), None)
            reward = self.getReward(state, self.bot.getPreviousMove(), successor, winner)
            cumReward += reward
            if self.bot.getAgent() == Constants.GENERAL:
                self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
            else:
                self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, reward)

        self.roundsSoFar = self.roundsSoFar + 1;
        self.player.empty();
        self.bot.empty();
        self.table.reset();
        self.dealer = Constants.BOT if self.dealer == Constants.PLAYER else Constants.PLAYER
