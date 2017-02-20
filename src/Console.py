class Console:
    '''
    Writes to the command line using print.
    Parameters:
        msg:
            The message to write out.
    '''
    @staticmethod
    def write(self, msg):
        print str(msg);

    '''
    Read from the command line. Gets raw_input, needs converted before
    it can be used.
    '''
    @staticmethod
    def read(self):
        return raw_input();
