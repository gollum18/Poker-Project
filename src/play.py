from constants import Constants
from game import Game
from deuces import Card
import threading
import util

training = 10000;
rounds = 10;
chips = 10000;
big = 30;
little = 20;
alpha = 0.5;
gamma = 0.8;
agent = Constants.GENERAL;

game = Game(rounds, chips, big, little, alpha, gamma, agent, training); 

# Used to save the qtable before we exit
#import atexit
#atexit.register(game.cleanup);

while game.isTraining():
    while not game.isGameOver():
        game.playRound();
    game.reset();

game.reset();
while not game.isGameOver():
    game.playRound();
