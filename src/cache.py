from deuces import Evaluator
from constants import Constants
from __future__ import division

import util

class Odds:
    CACHE_SIZE = 512;

    def __init__(self):
        self.pfOdds = dict();
        self.fOdds = dict();
        self.tOdds = dict();
        self.rOdds = dict();
        self.eval = Evaluator();

    def _getValue(self, cards):
        length = len(cards);
        if length == 2:
            if cards in self.pfOdds:
                return self.pfOdds[cards];
        elif length == 5:
            if cards in self.fOdds:
                return self.pfOdds[cards];
        elif length == 6:
            if cards in self.tOdds:
                return self.pfOdds[cards];
        elif length == 7:
            if cards in self.rOdds:
                return self.pfOdds[cards];
        return None;

    def getOdds(self, cards):
        value = self._getValue(cards);
        if value == None:
            return util.handStrength()/Constants.LOWESTRANK;
