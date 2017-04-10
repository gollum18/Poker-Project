class Constants:
    # Represents stages
    FLOP = "FLOP";
    TURN = "TURN";
    RIVER = "RIVER";
    EVAL = "EVAL";
    TERMINAL = "TERMINAL STATE";

    # Represents players and eval status
    PLAYER = "PLAYER";
    BOT = "BOT";
    SPLIT = "SPLIT";

    # Represents Actions
    ALLIN = "ALLIN";
    CALL = "CALL";
    FOLD = "FOLD";
    RAISE = "RAISE";

    # Represents Betting Types
    SMALL = "SMALL";
    MEDIUM = "MEDIUM";
    LARGE = "LARGE";

    # Represents values specific for determining the bet amount
    LOUP = .06;
    LOIN = .7;
    MELO = .1;
    MEUP = .2;
    MEIN = .6;
    HIPOINT = .3;
    HIABOVE = .95;
    LOWESTRANK = 7462;
    FILENAME = "qtable.txt"

    # Constants needed by the bot
    WEIGHTS = ["HRANK", "MYAGGRO", "OPPAGGRO", "CPRATIO"];
    DEFAULT = 1.0;
    MIN_BET = 5;
