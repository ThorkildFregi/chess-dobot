# chess-dobot-api

The API to interact with Dobot Magician that play chess on a board using Stockfish
(To use it, it's highly recommended to use Chess Dobot app, repo :)

## Installation

You will need stockfish (the version is not important).

Then, clone the repo :

````git clone https://github.com/ThorkildFregi/mbot-V1-rescue-line/blob/main/README.md?plain=1 ```

Create a python environment.

Install the requirements :

```pip install -r requirements.txt```

And you are ready to interact with it !
(It is a local API be sure to be on the same network to use)

## Playing

### [/](/chess_dobot/main.py#L78-80)

The home link (yes there is a threat, ignore it).

----------------

### [/resetallcodes](/chess_dobot/main.py#L82-86)

Erase all the codes in the list.

----------------

### [/start?code=****&skilllevel=**](/chess_dobot/main.py#L88-108)

Start a new game with you're code and add it in the list. Moreover, you need to set the level of stockfish on a scale of 1 to 20 (don't be too confident if you want to win). Return stockfish parameters.

----------------

### [/join?code=****](/chess_dobot/main.py#L110-118)

Get then fen of the party on going, if you have the right code. Return the fen.

----------------

### [/makeamove?fen=*********************&move=****](/chess_dobot/main.py#L120-156)

Make the robot make the move. Need the fen now in the party and the move of the player in long algebraic notation. Return the move of the bot.

----------------