from game import Game

game = Game(10, 1000, 30, 20);
while not game.isGameOver():
    game.playRound();
