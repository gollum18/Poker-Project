from Player import Player

class Bot(player):
    def __str__(self):
        return "Bots Chips: {0}".format(self.chips);
    
    def determineAction(self):
        Util.raiseNotDefined();
