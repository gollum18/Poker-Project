from constants import Constants
from game import Game
from deuces import Card
import util

training = 10000;
rounds = 10;
chips = 10000;
big = 30;
little = 20;
alpha = 0.5;
gamma = 0.8;
agent = Constants.GENERAL;

game = Game(rounds, chips, big, little, alpha, gamma, agent); 

# Used to save the qtable before we exit
#import atexit
#atexit.register(game.cleanup);

while not game.isGameOver():
    game.playRound();
