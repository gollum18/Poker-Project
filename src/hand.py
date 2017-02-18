class Hand:
    def __init__(self, left, right):
        self.left = left;
        self.right = right;

    def __str__(self):
        return "Left: {0}, Right{1}".format(str(self.left), str(self.right));

    def getLeftCard(self):
        return self.left;

    def getRightCard(self):
        return self.right;
