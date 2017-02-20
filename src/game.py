from Player import Player
from Bot import Bot
from Deck import Deck
from Console import Console
from Enums import *

class Game:
    def __init__(self, big, little, startingChips):
        # Set the fields
        self.big = big;
        self.little = little;
        self.winner = None;
        self.dealer = 1;

        # Create the game objects
        self.players = (Player(startingChips), Bot(startingChips));
        self.deck = Deck();

    def isGameOver(self):
        if self.players[0].getChips() == 0:
            self.winner = 0;
            return True;
        elif self.players[1].getChips() == 0:
            self.winner = 1;
            return True;
        return False;

    def getWinner(self):
        return self.winner;

    def restartGame(self, big, little, startingChips):
        self.big = big;
        self.little = little;
        self.startingChips = startingChips;
        self.winner = None;
        for player in self.players:
            self.player.subChips(self.player.getChips());
            self.player.addChips();
            self.player.emptyHand();

    def evalHand(self, cards):
        # Check for all the possible hand ranks and return
        #   appropriate value
        return 0;

    def resolveSplit(self, rank, phand, bhand):
        # Resolve the split based on rank
        return 0;
        
    def startGame(self):
        # Holds cards on the table
        table = set();
        # Holds the pot for the round
        pot = 0;
        # Holds the current bid
        bid = 0;

        # Shuffle the deck
        self.deck.shuffle();
        
        while not self.isGameOver():
            # Add blinds to the pot
            pot += self.big;
            pot += self.little;
            if dealer == 0:
                self.player.subChips(self.big);
                self.bot.subChips(self.little);
            else:
                self.player.subChips(self.little);
                self.bot.subChips(self.big);
            
            # Deal out the cards to the players
            for i in range (0, len(self.players)):
                if self.dealer == 0:
                    self.players[1].addCard(self.deck.draw());
                    self.players[0].addCard(self.deck.draw());
                else:
                    self.players[0].addCard(self.deck.draw());
                    self.players[1].addCard(self.deck.draw());

            # Loop through all poker stages
            for stage in PokerStages.stages:
                # Add cards to the table
                for i in range (i, stage):
                    table.add(self.deck.draw());

                # Print out the table and players cards
                Console.write("Table Cards: {0}".format(table));
                Console.write("Your Cards: {0}".format(self.player.getHand()););

                # Get the actions from the players
                if dealer == 0:
                    # Get bot action
                    # Get player action
                else:
                    # Get player action
                    # Get bot action
                
                
            # Evaluate the players hands
            playerrank = evalHand(set(self.player.getHand(), table));
            botrank = evalHand(set(self.bot.getHand(), table));

            # player has won
            if playerrank < botrank:
                self.player.addChips(self.pot):
            # Bot has won
            elif (botrank < playerrank):
                self.bot.addChips(self.pot);
            # Resolve the split
            else:
                resolveSplit();

            # Reset the deck
            self.deck.rebuild();
            self.deck.shuffle();

            # Empty the table
            table.clear();

            # Empty the players hands
            for i in range (0, 2):
                self.players[i].emptyHand();

            # Swap dealers
            if self.dealer == 0:
                self.dealer = 1;
            else:
                self.dealer = 0;

            # Reset the pot
            pot = 0;