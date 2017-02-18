class Face:
    CLUBS = "CLUBS";
    DIAMONDS = "DIAMONDS";
    HEARTS = "HEARTS";
    SPADES = "SPADES";

    _facesList = [CLUBS, DIAMONDS,
                  HEARTS, SPADES];

class Value:
    ACE = "ACE";
    TWO = "TWO";
    THREE = "THREE";
    FOUR = "FOUR";
    FIVE = "FIVE";
    SIX = "SIX";
    SEVEN = "SEVEN";
    EIGHT = "EIGHT";
    NINE = "NINE";
    TEN = "TEN";
    JACK = "JACK";
    QUEEN = "QUEEN";
    KING = "KING";

    _valuesList = [ACE, TWO, THREE, FOUR,
                   FIVE, SIX, SEVEN, EIGHT,
                   NINE, TEN, JACK, QUEEN, KING];

class Card:
    def __init__(self, face, value):
        self.face = face;
        self.value = value;

    def __str__(self):
        return "{0}, {1}".format(self.value, self.face);

    def getFace(self):
        return self.face;

    def getValue(self):
        return self.value;
