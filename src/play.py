from game import Game
from deuces import Card
import util

game = Game(10, 10000, 30, 20);

# Used to save the qtable before we exit
#import atexit
#atexit.register(game.cleanup);

while not game.isGameOver():
    game.playRound();
