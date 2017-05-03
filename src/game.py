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
        self.roundsSoFar = 0
        self.chips = chips
        self.player = Player(chips)
        self.bot = Bot(chips, alpha, gamma, agent)
        self.big = big
        self.little = little
        self.minBet = int(.25 * little)
        self.table = Table()
        self.eval = Evaluator()
        self.dealer = choice([Constants.PLAYER, Constants.BOT])

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
        print("The bot had: {0}.".format(self.eval.class_to_string(self.eval.get_rank_class(bstr))))
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
        elif pstr == bstr:
            print("The players have split the pot!!")
            self.player.addChips(int(floor(pot/2)))
            self.bot.addChips(int(floor(pot/2)))
            return Constants.SPLIT
        else:
            return None

    '''
    Gets the reward for transitioning from one state to another using a given action.
    '''
    def getReward(self, state, action, nextState):
        p = util.winningPercentage(self.eval, self.player.getCards(), self.bot.getCards(), state[0])
        botDiff = p[Constants.BOT] - p[Constants.PLAYER]
        if sum(state[0]) != sum(nextState[0]):
            np = util.winningPercentage(self.eval, self.player.getCards(), self.bot.getCards(), nextState[0])
            botDiff = (np[Constants.BOT] - np[Constants.PLAYER]) - botDiff
        if nextState[4] == state[4]:
            aggDiff = 1
        else:
            aggDiff = nextState[4] - state[4]
        reward = 0

        # Check for a winner
        if nextState[8] == Constants.PLAYER:
            reward = -nextState[7]*p[Constants.BOT]
        elif nextState[8] == Constants.BOT:
            reward = nextState[7]*p[Constants.BOT]
        else:
            if action == Constants.ALLIN:
                reward = (nextState[7]*botDiff)/aggDiff
            elif action == Constants.CALL:
                reward = 1*botDiff
            elif action == Constants.FOLD:
                reward = -nextState[7]
            elif action == Constants.RAISE:
                reward = nextState[7]*botDiff
        return reward

    '''
    Determines whether the game is over.
    A game is over if there are no more rounds, or a player is out of chips at the end
    of a round.
    '''
    def isGameOver(self):
        if self.roundsSoFar >= self.rounds:
            self.printResults()
            return True
        elif self.player.getChips() == 0:
            self.printResults()
            return True
        elif self.bot.getChips() == 0:
            self.printResults()
            return True
        return False

    '''
    Automatically called by play.py to write the q-table out to file.
    @Deprecated
    '''
    def cleanup(self):
        self.bot.write()

    def printResults(self):
        winner = None
        pchips = self.player.getChips()
        bchips = self.bot.getChips()
        if pchips > bchips:
            winner = Constants.PLAYER
        elif pchips < bchips:
            winner = Constants.BOT
        elif pchips == bchips:
            winner = "SPLIT"
        print("")
        print("===================================")
        print(" After {0} rounds the results are".format(self.roundsSoFar))
        print("===================================")
        print(" The player had ${0} chips".format(pchips))
        print(" The bot had ${0} chips".format(bchips))
        print(" The Winner is: {0}".format(winner))
        print("===================================")

    def playRound(self):
        # Take out the blinds
        if self.dealer == Constants.PLAYER:
            # Check if the player has enough for the big blind
            if self.player.getChips() < self.big:
                self.table.addToPot(self.player.getChips())
                self.player.subChips(self.player.getChips())
            else:
                self.table.addToPot(self.big)
                self.player.subChips(self.big)
            # Check if the bot has enough for the little blind
            if self.bot.getChips() < self.little:
                self.table.addToPot(self.bot.getChips())
                self.bot.subChips(self.bot.getChips())
            else:
                self.table.addToPot(self.little)
                self.bot.subChips(self.little)
        else:
            # Check if the bit has enough for the big blind
            if self.bot.getChips() < self.big:
                self.table.addToPot(self.bot.getChips())
                self.bot.subChips(self.bot.getChips())
            else:
                self.table.addToPot(self.big)
                self.bot.subChips(self.big)
            # Check if the player has enough for the little blind
            if self.player.getChips() < self.little:
                self.table.addToPot(self.player.getChips())
                self.player.subChips(self.player.getChips())
            else:
                self.table.addToPot(self.little)
                self.player.subChips(self.little)

        turn = Constants.PLAYER if self.dealer == Constants.BOT else Constants.PLAYER
        stage = Constants.FLOP
        move = None
        state = None
        cumReward = 0

        if self.player.getChips() == 0 or self.bot.getChips() == 0:
            stage = Constants.NOCHIPSLEFT
        
        print("")
        print("==========================================")
        print("==========================================")
        print("            BEGINNING ROUND #{0}".format(self.roundsSoFar+1))
        print("             YOUR CHIPS: ${0}".format(self.player.getChips()))
        print("           OPPONENT CHIPS: ${0}".format(self.bot.getChips()))
        print("==========================================")
        print("==========================================")

        while (
            stage != Constants.EVAL
            and stage != Constants.FOLD
            and stage != Constants.ALLIN
            and stage != Constants.NOCHIPSLEFT):
            # Deal out all the cards
            if stage == Constants.FLOP:
                for i in range (0, 5):
                    if i < 3:
                        # Deal out the cards for the flop 
                        self.table.addCard(self.table.draw())
                    else:
                        # Deal out the cards to the players based on dealer
                        if self.dealer == Constants.PLAYER:
                            self.bot.addCard(self.table.draw())
                            self.player.addCard(self.table.draw())
                        else:
                            self.player.addCard(self.table.draw())
                            self.bot.addCard(self.table.draw())
            # Otherwise, deal out the cards to the table
            elif stage == Constants.TURN or stage == Constants.RIVER:
                self.table.addCard(self.table.draw())

            # Get the players moves and react to them
            for i in range (0, 2):
                # Get the players move
                if turn == Constants.PLAYER:
                    move = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), move)
                    self.player.setPreviousMove(move)
                else:
                    state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                             self.bot.getAggression(), None, self.dealer, self.bot.getChipsIn(), None)
                    move = self.bot.getMove(state)
                    self.bot.setPreviousMove(move)
                print("The {0}s' move was {1}.".format(turn, move))

                if move == Constants.ALLIN:
                    stage = Constants.ALLIN
                    break
                elif move == Constants.FOLD:
                    stage = Constants.FOLD
                    break
                elif turn == Constants.BOT and move == Constants.CALL:
                    successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                 self.bot.getAggression(), self.bot.getPreviousMove(), self.dealer, self.bot.getChipsIn(), None)
                    reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                    cumReward = cumReward + reward
                    if self.bot.getAgent() == Constants.GENERAL:
                        self.bot.update(state, self.bot.getPreviousMove(), successor, reward)
                    else:
                        self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, reward)
                elif move == Constants.RAISE:
                    if turn == Constants.PLAYER:
                        self.table.setAnte(self.player.getBet(self.little))
                        self.player.addToChipsIn(self.table.getAnte())
                        self.player.subChips(self.table.getAnte())
                        self.player.setAggression(self.table.getAnte(), self.little)
                        self.table.addToPot(self.table.getAnte())
                        state = (self.table.getCards(),self.bot.getCards(),self.table.getPot(),self.table.getAnte(),
                                 self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn(), None)
                        response = self.bot.getMove(state)
                        self.bot.setPreviousMove(response)
                        # was the bots response a call?
                        if response == Constants.CALL:
                            print("The BOT chose to CALL your RAISE.")
                            self.bot.setAggression(self.bot.getCall(self.table.getAnte()),self.table.getAnte())
                            self.bot.addToChipsIn(self.bot.getCall(self.table.getAnte()))
                            self.table.addToPot(self.bot.getCall(self.table.getAnte()))
                            self.bot.subChips(self.bot.getCall(self.table.getAnte()))
                            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                         self.bot.getAggression(), self.bot.getPreviousMove(), self.dealer, self.bot.getChipsIn(), None)
                            reward = self.getReward(state, response, successor)
                            cumReward = cumReward + reward
                            self.table.setAnte(0)
                            move = None
                        # was the bots response a fold?
                        else:
                            print("The BOT chose to FOLD on your RAISE.")
                            self.bot.setAggression(0, self.table.getAnte())
                            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                         self.bot.getAggression(), self.bot.getPreviousMove(), self.dealer, self.bot.getChipsIn(), Constants.PLAYER)
                            reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                            cumReward = cumReward + reward
                            if self.bot.getAgent() == Constants.GENERAL:
                                self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
                            else:
                                self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)
                            stage = Constants.FOLD
                            turn = Constants.BOT
                            break
                    elif turn == Constants.BOT:
                        self.table.setAnte(self.bot.getBet(self.little, self.bot.getBetType(self.bot.getCards(), self.table.getCards())))
                        self.bot.addToChipsIn(self.table.getAnte())
                        self.bot.subChips(self.table.getAnte())
                        self.bot.setAggression(self.table.getAnte(), self.little)
                        self.table.addToPot(self.table.getAnte())
                        state = (self.table.getCards(),self.bot.getCards(),self.table.getPot(),self.table.getAnte(),
                                 self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn(), None)
                        response = self.player.getMove(self.table.getCards(), self.table.getPot(), self.table.getAnte(), Constants.RAISE)
                        if response == Constants.CALL:
                            print("The PLAYER chose to CALL the BOT's RAISE.")
                            self.player.setAggression(self.player.getCall(self.table.getAnte()),self.table.getAnte())
                            self.player.addToChipsIn(self.player.getCall(self.table.getAnte()))
                            self.table.addToPot(self.player.getCall(self.table.getAnte()))
                            self.player.subChips(self.player.getCall(self.table.getAnte()))
                            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                         self.bot.getAggression(), response, self.dealer, self.bot.getChipsIn(), None)
                            reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                            cumReward = cumReward + reward
                            self.table.setAnte(0)
                            move = None
                        else:
                            print("The PLAYER chose to FOLD on the BOT's RAISE.")
                            self.player.setAggression(0, self.table.getAnte())
                            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                         self.bot.getAggression(), response, self.dealer, self.bot.getChipsIn(), Constants.BOT)
                            reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                            cumReward = cumReward + reward
                            if self.bot.getAgent() == Constants.GENERAL:
                                self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
                            else:
                                self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)
                            stage = Constants.FOLD
                            turn = Constants.PLAYER
                            break
                    if self.player.getChips() == 0 or self.bot.getChips() == 0:
                        stage = Constants.NOCHIPSLEFT
                        break
                # End of turn, swap turns
                turn = Constants.PLAYER if turn == Constants.BOT else Constants.BOT
            if stage == Constants.FLOP:
                stage = Constants.TURN
            elif stage == Constants.TURN:
                stage = Constants.RIVER
            elif stage == Constants.RIVER:
                stage = Constants.EVAL

        # Check if a player does not have cards, if so deal them out
        if len(self.player.getCards()) == 0:
            for i in range(0, 2):
                if self.dealer == Constants.BOT:
                    self.player.addCard(self.table.draw())
                    self.bot.addCard(self.table.draw())
                else:
                    self.bot.addCard(self.table.draw())
                    self.player.addCard(self.table.draw())

        # This stage is reached when a call occurs where a player is left with no chips
        #   treat like and allin
        if stage == Constants.NOCHIPSLEFT:
            state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                     self.bot.getAggression(), self.bot.getPreviousMove(), self.dealer, self.bot.getChipsIn())
            for i in range(5-len(self.table.getCards())):
                self.table.addCard(self.table.draw())
            winner = self.evaluate()
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                         self.bot.getAggression(), self.bot.getPreviousMove(), self.dealer, self.bot.getChipsIn(), winner)
            reward = self.getReward(state, self.bot.getPreviousMove(), successor)
            cumReward = cumReward + reward
            if self.bot.getAgent() == Constants.GENERAL:
                self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
            else:
                self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)
            
        elif stage == Constants.ALLIN:
            #print "A player went all in... The turn is now {0}".format(turn)
            
            response = None

            if self.player.getChips != 0 and self.bot.getChips() != 0:
                # Take out all the chips
                if turn == Constants.PLAYER:
                    self.table.setAnte(self.player.getChips())
                    self.table.addToPot(self.table.getAnte())
                    self.player.addToChipsIn(self.table.getAnte())
                    self.player.setAggression(self.table.getAnte(), self.little)
                    self.player.subChips(self.table.getAnte())
                    state = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                             self.bot.getAggression(), self.bot.getPreviousMove(), self.dealer, self.bot.getChipsIn(), None)
                    response = self.bot.getMove(state)
                    self.bot.setPreviousMove(response)
                    if response == Constants.CALL:
                        print("The BOT chose to CALL your ALLIN.")
                        self.bot.setAggression(self.bot.getCall(self.table.getAnte), self.little)
                        self.bot.addToChipsIn(self.bot.getCall(self.table.getAnte()))
                        self.table.addToPot(self.bot.getCall(self.table.getAnte()))
                        self.bot.subChips(self.bot.getCall(self.table.getAnte()))
                        self.table.setAnte(0)
                    else:
                        print("The BOT chose to FOLD on your ALLIN.")
                        self.bot.setAggression(0, self.table.getAnte())
                        successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                     self.bot.getAggression(), response, self.dealer, self.bot.getChipsIn(), Constants.PLAYER)
                        reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                        cumReward = cumReward + reward
                        if self.bot.getAgent() == Constants.GENERAL:
                            self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
                        else:
                            self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)
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
                        self.player.setAggression(0, self.table.getAnte())
                        successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                                     self.bot.getAggression(), response, self.dealer, self.bot.getChipsIn(), Constants.BOT)
                        reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                        cumReward = cumReward + reward
                        if self.bot.getAgent() == Constants.GENERAL:
                            self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
                        else:
                            self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)
                        self.bot.addChips(self.table.getPot())
                            
            if response == Constants.CALL:
                # Deal out the remaining cards
                for i in range(5-len(self.table.getCards())):
                    self.table.addCard(self.table.draw())
                # Evaluate
                winner = self.evaluate()
                successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                             self.bot.getAggression(), response, self.dealer, self.bot.getChipsIn(), winner)
                reward = self.getReward(state, self.bot.getPreviousMove(), successor)
                cumReward = cumReward + reward
                if self.bot.getAgent() == Constants.GENERAL:
                    self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
                else:
                    self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)
                
        elif stage == Constants.FOLD:
            if turn == Constants.PLAYER:
                self.bot.addChips(self.table.getPot())
            elif turn == Constants.BOT:
                self.player.addChips(self.table.getPot())
                
        elif stage == Constants.EVAL:
            winner = self.evaluate()
            successor = (self.table.getCards(), self.bot.getCards(), self.table.getPot(), self.table.getAnte(),
                         self.bot.getAggression(), move, self.dealer, self.bot.getChipsIn(), winner)
            reward = self.getReward(state, self.bot.getPreviousMove(), successor)
            cumReward = cumReward + reward
            if self.bot.getAgent() == Constants.GENERAL:
                self.bot.update(state, self.bot.getPreviousMove(), successor, cumReward)
            else:
                self.bot.updateApproximate(state, self.bot.getPreviousMove(), successor, cumReward)

        self.roundsSoFar = self.roundsSoFar + 1
        self.player.empty()
        self.bot.empty()
        self.table.reset()
        self.dealer = Constants.BOT if self.dealer == Constants.PLAYER else Constants.PLAYER
