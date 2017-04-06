from game import Game
from deuces import Card
import util

game = Game(10, 1000, 30, 20);
while not game.isGameOver():
    game.playRound();
