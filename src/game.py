from Player import Player
from Bot import Bot
from Deck import Deck
from Enums import *

class Game:
    def __init__(self, big, little, startingChips):
        # Set the fields
        self.big = big;
        self.little = little;
        self.winner = None;

        # Create the game objects
        self.players = (Player(startingChips), Bot(startingChips));
        self.deck = Deck();

    def isGameOver(self):
        if self.players[0].getChips() == 0:
            self.winner = "BOT";
            return True;
        elif self.players[1].getChips() == 0:
            self.winner = "PLAYER";
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
        
    def startGame(self):
        # Holds cards on the table
        table = set();

        # Shuffle the deck
        self.deck.shuffle();
        
        while not self.isGameOver():
            # Deal out the cards to the players
            for i in range (0, 2):
                self.players[0].addCard(self.deck.draw());
                self.players[1].addCard(self.deck.draw());

            # Loop through all poker stages
            for stage, count in PokerStages.stages:
                # Add cards to the table
                for i in range (i, count):
                    table.add(self.deck.draw());

                # Get the actions from the players
                
                
            # Evaluate the players hands

            # Adjust the chip counts for the players

            # Reset the deck
            self.deck.rebuild();
            self.deck.shuffle();

            # Empty the players hands
            for i in range (0, 2):
                self.players[i].emptyHand();
