from random import random
from deck import Deck
from hand import Hand
from player import Player

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
    Returns:
        0 if there is a split.
        1 if the player won.
        2 if the bot won.
    '''
    def evaluateRound(self):
        winner = 0;
        
        TODO: Implement hand evaluations
        return winner;

    '''
    Deals out the cards for the stage.
    Parameters:
        table:
            The current state of the table.
        stage:
            The current stage of the current round.
        dealer:
            The dealer of the current round.
    '''
    def deal(self, table, stage, dealer):
        lim = 1;
        if stage == Stage.FLOP:
            cards = set();
            for i in range (0, 4):
                cards.add(self.deck.draw());
            if dealer == 0:
                self.player.setHand(cards[1], cards[3]);
                self.bot.setHand(cards[0], cards[2]);
            else:
                self.player.setHand(cards[0], cards[2]);
                self.bot.setHand(cards[1], cards[3]);
            cards = None;
            lim = 3;
        for i in range (0, lim):
            table.add(self.deck.draw());

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

        # Holds the cards on the table
        table = set();

        # Pull out the big and little blinds
        if dealer == 0:
            self.player.decrementChips(little);
            self.bot.decrementChips(big);
            turn = 1;
        else:
            self.player.decrementChips(big);
            self.bot.decrementChips(little);
            turn = 0;
        pot = self.big + self.little;

        # Setup the round
        active = {0, 1};
        stage = Stage.FLOP;

        # Run the round
        while (len(active) == 2 || stage != Stage.EVALUATE):
            # Deal out the cards for the stage
            deal(table, stage, dealer);

            # Get the player and bot actions

            # Advance the round
            if stage == Stage.FLOP:
                stage = Stage.TURN;
            elif stage == Stage.TURN:
                stage = Stage.RIVER;
            elif stage == Stage.RIVER;
                stage = Stage.EVALUATE;

        # Check end conditions
        if len(active) < 2:
            # Dole out the pot to the winner
            if active[0] == 0:
                self.player.incrementChips(pot);
            else:
                self.bot.incrementChips(pot);
        elif stage == Stage.EVALUATE:
            winner == evaluateRound();
            if winner == 0: # Split
                self.player.incrementChips(pot/2);
                self.bot.incrementChips(pot/2);
            elif winner == 1: # Player won
                self.player.incrementChips(pot);
            else: # Bot won
                self.bot.incrementChips(pot);
