from game import Game
from deuces import Card
import util

game = Game(10, 1000, 30, 20, 50);

# Used to save the qtable before we exit
import atexit
atexit.register(game.cleanup);

# Train the agent
while game.isTraining():
    while not game.isGameOver():
        game.playRound();
    game.reset(10);
# Play against the agent
game.playRound();
