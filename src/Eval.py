class Eval:
    @staticmethod
    def isFlush(cards):
        # Determine whether there is a flush
        suits = dict();
        for suit in Suit.suits:
            suits[suit] = 0;
        for card in cards:
            suits[card.getSuit()] += 1;
        if max(suits.values()) >= 5:
            return True;
        return False;

    @staticmethod
    def isStraight(cards):
        ranks = list[];
        for card in cards:
            ranks.append(card.getRank());
        # remove duplicate entries from the ranks list, and convert to sorted list
        ranks = sorted(list(set(ranks)));
        # Deal with an ace straight
        if 12 in ranks:
            if 11 in ranks and 10 in ranks and 9 in ranks and 8 in ranks:
                return True;
            elif 2 in ranks and 3 in ranks and 4 in ranks and 5 in ranks:
                return True;
        # Deal with the general case
        else:
            rank = ranks.pop();
            for i in ranks:
                if i != rank + 1:
                    return False;
                rank = i;
            return True;

    @staticmethod
    def isStraightFlush(cards):
        if isFlush(cards) and isStraight(cards):
            return True;
        return False;

    @staticmethod
    def isRoyalFlush(cards):
        isAce = False;
        for card in cards:
            if card.getRank() == 12:
                if isFlush(cards) and isStraight(cards):
                    return True;
        return False;

    @staticmethod
    def isFourKind(cards):
        # Determine whether it is a four of the kind
        faces = dict();
        for face in Face.faces:
            faces[face] = 0;
        for card in cards:
            faces[card.getFace()] += 1;
        if max(faces.values() >= 4):
            return True;
        return False;

    @staticmethod
    def isFullHouse(cards):
        faces = dict();
        for face in Face.faces:
            faces[face] = 0;
        for card in cards:
            faces[card.getFace()] += 1;
        if 2 is in faces.values() and 3 is in faces.values():
            return True;
        return False;

    @staticmethod
    def isThreeKind(cards):
        # Determine whether it is a four of the kind
        faces = dict();
        for face in Face.faces:
            faces[face] = 0;
        for card in cards:
            faces[card.getFace()] += 1;
        if max(faces.values() >= 3):
            return True;
        return False;

    @staticmethod
    def isTwoPair(cards):
        faces = dict();
        for face in Face.faces:
            faces[face] = 0;
        for card in cards:
            faces[card.getFace()] += 1;
        values = faces.values();
        if 2 is in values: # Check for the first pair
            values.remove(2): # Remove it
                if 2 is in values: # Check for a second pair
                    values.remove(2); # Remove it
                    return True;
        return False;

    @staticmethod
    def isPair(cards):
        faces = dict();
        for face in Face.faces:
            faces[face] = 0;
        for card in cards:
            faces[card.getFace()] += 1;
        if 2 is in faces.values():
            return True;
        return False;
