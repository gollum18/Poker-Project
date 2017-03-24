'''
Initially will start off empty. The cache will fill over time and
entries will be swapped in and out as needed.
'''
def Cache():
    TIMER = 5;
    ENTRIES = 256;
    FILENAME = 'hand_table.cache';
    ENDING = "\n";
    
    def __init__(self):
        self.cache = [];

    def __del__(self):
        if not self.file_handler.closed:
            self.file_handler.close();

    def deleteFromFile(self, hid):
        f = open(Cache.FILENAME, 'r+');
        lines = f.readlines();
        f.close();
        f = open(Cache.FILENAME, 'w');
        for line in lines:
            if line != hid+Cache.ENDING:
                f.write(line);
        f.close();
        
    def readFromFile(self, hid):
        f = open(Cache.FILENAME, 'r');
        lines = f.readlines();
        f.close();
        s = None;
        for line in lines:
            if hid in line:
                s = line;
                break;
        self.deleteFromFile(hid);
        return s;

    def writeToFile(self, hid):

    def read(self, hid):

    def write(self, hid):

def Entry(self):
    def __init__(self):
        self.hid = None;
        self.prob = 0;
        self.freq = 0;
        self.empty = False;
        self.ref = False;
        self.mod = False;

    def getHandID(self):
        return self.hid;

    def getFrequency(self):
        return self.freq;

    def getProbability(self):
        return self.prob;

    def isEmpty(self):
        return self.empty;

    def isModified(self):
        return self.mod;

    def isReferenced(self):
        return self.ref;
