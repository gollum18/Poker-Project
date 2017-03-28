class Constants:
    # Represents stages
    FLOP = "FLOP";
    TURN = "TURN";
    RIVER = "RIVER";
    EVAL = "EVAL";

    # Represents players and eval status
    PLAYER = -1;
    BOT = 1;
    SPLIT = 0;

    # Represents Actions
    ALLIN = "ALLIN";
    CALL = "CALL";
    FOLD = "FOLD";
    RAISE = "RAISE";

    # Represents Betting Types
    LOW = "LOW";
    MEDIUM = "MEDIUM";
    HIGH = "HIGH";

    # Represents Floating Points for Betting
    LOUPPER = 0.06;
    LOINSIDE = 0.7;
    MEDLOWER = 0.1;
    MEDUPPER = 0.2;
    MEDINSIDE = 0.6;
    MEDOUTLO = 0.1;
    MEDOUTHI = 0.3;
    HIPOINT = 0.3;
    HIABOVE = 0.95;
    HIBELOW = 0.05;
    HIALLIN = 0.1;
