4Connect
========

Python framework and UI and AI of gravity-based Connect-Four style games.

Usage
========

To create a new game instance, construct a new Game object.

```
g = Game(7,6,4, players = [Human, DumbAI])
g.play()
```

The arguments are:

```
Game(columns, rows, win_length, (players), (pause))
```

columns: width of the board.
rows: height of the board  
win_length: amount of pieces needed in a row to win  
players (optional): a list of classes that denote the type of players.  
pause (optional): a boolean.  If True, the game will pause between turns.