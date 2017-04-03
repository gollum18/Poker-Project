class Constants:
    # Represents stages
    FLOP = "FLOP";
    TURN = "TURN";
    RIVER = "RIVER";
    EVAL = "EVAL";

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
