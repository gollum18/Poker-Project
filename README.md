# ai_poker_project
CSC 440 AI - Poker Playing Agent

A poker playing agent written in python.

Heads up no-limit texas hold-em. Two player only.

Requires Python 2.7.

You can get Python for your environment from python.org

Ships bundled with [deuces](https://github.com/worldveil/deuces).

This project is written in 100% pure python as is deuces. It may initially lag on startup in order to load in the qtable, but should run fine after that.

# INSTALLATION INSTRUCTIONS

In order to download and run this software please ensure that you first have an active internet connection. After this, follow these steps in order to setup for play.

1.) In a web browser of your choice navigate to https://github.com/gollum18/Poker-Project

2.) Once there, find the green button that says "clone or download" and click on it, a popup should come up below it.

3.) Inside this popup click on "Download Zip", the game should now download

4.) Once downloaded, open your downloads folder and extract the contents to a directory of your choosing, preferably without mixing them with other files.

5.) Finally, open a command prompt (if on windows) or a terminal (if on Linux) and navigate to the "src" folder

6.) Once there tpye this command without quotes...

"python play.py" (if on Windows)

"python2 play.py" (if on Debian/Arch based Linux systems)

# RULES

This poker game follows the standard rules of playing Texas Hold'Em.

Each round starts with the big and little blind being taken out from each player, these are added to the pot to give incentive for players not to immediately fold.

Next, play proceeds to the FLOP stage, where each player gets two cards and then three cards are dealt to the community.

Each player then has a chance to continue play by either going ALLIN, CALLING, FOLDING, or RAISING.

Going ALLIN or RAISING will require an immediate CALL or FOLD from the opposing player. Be warned, a CALL will require that the opposing player put in the amount of chips offered up by the opponent.

FOLDING will end the round and play will start with a new round.

A CALL serves as a pass, wherein the player offers up no chips and play proceeds to the next player.

Play proceeds in this fashion until either a player folds or goes ALLIN (with the opponent calling the ALLIN) OR play proceeds to the SHOWDOWN stage, where each players hand is evaluated and a winner is determined.

This continues until either player is out of chips, or 10 rounds have been played. 

# CONTROLS

Controls are simple, at each stage the player is prompted to enter a letter corresponding to an action in game. The list of available moves is dependent on whether or not the opponent went first in the round AND if they CALL OR went ALLIN.

If the opponent CALLED or went ALLIN, then the player is prompted to enter either a 'c' to CALL or 'f' to FOLD. This is a reactionary response and is required for play to continue. After this, the player may then take their normal turn.

With normal flow of the game, the player is prompted to enter either an 'a' to go ALLIN, a 'c' to CALL, a 'f' to FOLD, or a 'r' to RAISE. In the case of a raise, the player must then enter the amount of chips they wish to offer up. Note that the amount of chips you raise by must be an acceptable range, ie. greater than zero but not more than your total chip count.

# TROUBLESHOOTING

We have tried our best to make sure that both the poker client and agent are as bug free as possible. However if you find any issued either with the client or the agent OR you have any suggestions for improvement, please create an issue on the projects github page located at https://github.com/gollum18/Poker-Project

In addition, if you are on Windows and are receiving an error about python not being found when you try to launch the client, then you have to add python to your path.