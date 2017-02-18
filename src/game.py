from random import random
from Deck import Deck
from Player import Player

class Stage:
    FLOP = "Flop";
    TURN = "Turn";
    RIVER = "River";
    EVALUATE = "Evaluate"

class Game:
    def __init__(self, big, little, initChips);
        # Create the player, bot, and deck
        self.player = Player();
        self.bot = Bot();
        self.deck = Deck();
        # Save the big and little blinds
        self.big = big;
        self.little = little;

    '''
    Determines whether the game is over.
    Returns:
        True if the game is over, and sets the winner.
        False if the game is still on.
    '''
    def isGameOver(self):
        if self.player.getChipCount() == 0:
            self.winner = 1;
            return True;
        elif self.bot.getChipCount() == 0:
            self.winner = 0;
            return True;
        return False;

    '''
    Gets the winner of the game.
    Returns:
        None if there is no winner yet.
        0 if the human player has won.
        1 if the bot has won.
    '''
    def getGameWinner(self):
        return self.winner;

    '''
    Evaluates the hands at the end of a round.
    '''
    def evaluateRound(self):
        TODO: Implement hand evaluations
        return None;

    '''
    Plays another round of texas hold-em.
    '''
    def playRound(self):
        # Rebuild and shuffle the deck
        self.deck.rebuild();
        self.deck.shuffle();

        # Pick a dealer and setup the turn
        dealer = int(random());
        turn = 0;

        # Pull out the big and little blinds
        if dealer == 0:
            self.player.decrementChips(little);
            self.bot.decrementChips(big);
            turn = 1;
        else:
            self.player.decrementChips(big);
            self.bot.decrementChips(little);
            turn = 0;
        self.pot = self.big + self.little;

        # Setup the round
        active = 2;
        stage = Stage.FLOP;

        while (active == 2 || stage != Stage.EVALUATE):
            if stage == Stage.FLOP:
                stage = Stage.TURN;
            elif stage == Stage.TURN:
                stage = Stage.RIVER;
            elif stage == Stage.RIVER;
                stage = Stage.EVALUATE;
