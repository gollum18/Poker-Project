from card import Face
from card import Value

class Hand:
    # Holds card values, 0 is highest rank, 8 is lowest
    handValues = {
            STRAIGHT_FLUSH:0,
            FOUR:1,
            FULL_HOUSE:2,
            FLUSH:3,
            STRAIGHT:4,
            THREE:5,
            TWO:6,
            ONE:7,
            HIGH:8
            };

    '''
    Creates a hand.
    Parameters:
        left:
            The left card of the hand.
        right:
            The right hand of the card.
    '''
    def __init__(self, left, right):
        self.left = left;
        self.right = right;

    '''
    Returns the string representation of this hand.
    '''
    def __str__(self):
        return "Left: {0}, Right{1}".format(str(self.left), str(self.right));

    '''
    Determines the type of the hand.
    Parameters:
        table:
            The cards on the table.
    '''
    def rankHand(self, table):
        valueCount = {
                Value.ACE:0,
                Value.TWO:0,
                Value.THREE:0,
                Value.FOUR:0,
                Value.FIVE:0,
                Value.SIX:0,
                Value.SEVEN:0,
                Value.EIGHT:0,
                Value.NINE:0,
                Value.TEN:0,
                Value.JACK:0,
                Value.QUEEN:0,
                Value.KING:0
                }

        # Get the value counts
        valueCount[self.hand.left.getValue()] += 1;
        valueCount[self.hand.right.getValue()] += 1;

        faceCount = {
                Face.CLUBS:0,
                Face.DIAMONDS:0
                Face.HEARTS:0,
                Face.SPADES:0
                };

        # Get the face counts
        faceCount[self.hand.left.getFace()] += 1;
        faceCount[self.hand.right.getFace()] += 1;

        for i in range (0, len(table)):
            faceCount[table[i].getFace()] += 1;
            valuesCount[table[i].getValue] += 1;

        # Get the max face value
        face = max(faceCount, key=faceCount);

        # Store the hand value
        hValue = 0;

        # Check for a flush
        if face >= 5:
            # Check for a straight flush
            if
                hValue = hand.handValues[STRAIGHT_FLUSH];
            else:
                hValue = hand.handValues[FLUSH];
        # Check for four of a kind
        elif face >= 4:
            hValue = hand.handValues[FOUR];
        # Check for full house
        elif 2 in face.values() and 3 in face.values():
            hValue = hand.handValues[FULL_HOUSE];
        # Check for three of a kind
        elif:
            hValue = hand.handValues[THREE];
        # Check for two pair
        elif:
            hValue = hand.handValues[TWO];
        # Check for one pair
        elif:
            hValue = hand.handValues[ONE];
        # Check for high card
        else:
            hValue = hand.handValues[HIGH];
        # Check for rank in descending order

        return hValue;
