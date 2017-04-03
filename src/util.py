from random import random;

@staticmethod
def flipCoin(p):
    if p < random():
        return True;
    return False;

@staticmethod
def getAggression(raiseAmt, anteAmt):
    if anteAmt == 0:
        raise ValueError("ERROR: The ante amount must be greater than zero!");
    if raiseAmt < anteAmt:
        raise ValueError("ERROR: A player must raise at least the ante amount (a call)!");
    return float(raiseAmt/anteAmt);
