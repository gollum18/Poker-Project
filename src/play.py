from game import Game

game = Game(10, 1000);
while not game.isGameOver():
    game.playRound();
