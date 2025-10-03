# chess-dobot-api

The API to interact with Dobot Magician that play chess on a board using Stockfish
(To use it, it's highly recommended to use Chess Dobot app, repo :)

## Installation

You will need stockfish (the version is not important).

Then, clone the repo :

```git clone https://github.com/ThorkildFregi/mbot-V1-rescue-line/blob/main/README.md?plain=1```

Create a python environment.

Install the requirements :

```pip install -r requirements.txt```

And you are ready to interact with it !
(It is a local API be sure to be on the same network to use)

## Playing

### [/](/chess_dobot/main.py#L101-#L103)

The home link (yes there is a threat, ignore it).

----------------

### [/installation](/chess_dobot/main.py#L105-#L107)

The html page for the installation.

----------------

### [/resetparty](/chess_dobot/main.py#L109-#L120)

To reset all party on going.

----------------

### [/erasefromwaitingqueue?index=](/chess_dobot/main.py#L122-#L133)

Erase someone from waiting queue by index

----------------

### [/start?name=&code=&skilllevel=](/chess_dobot/main.py#L88-#L108)

Start a new game with you're code or add it in the waiting queue if a game is on going. Moreover, you need to set the level of stockfish on a scale of 1 to 20 (don't be too confident if you want to win). Return stockfish parameters. Bonus -> we take youre name for the waiting queue on the [/installation](#installation)

----------------

### [/join?code=](/chess_dobot/main.py#L110-#L118)

If you have the right code, return the fen of the party on going.

----------------

### [/makeamove?code=&fen=](/chess_dobot/main.py#L120-#L156)

Make the robot make the move. Need the fen now in the party and the code to identify. Return the move of the bot.

----------------