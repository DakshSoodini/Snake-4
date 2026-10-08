# Snake Bot

A rule-based bot that plays Snake on a 10×10 board. It started as a neural-network project. That failed, so I rebuilt it with simple search rules, and the rules worked far better.

A real game from the current bot, 160 moves in (`@` is the head, `o` the body, `*` the food):

```
+----------+
|          |
| ooo      |
| o o      |
| ooo     *|
|@ooo      |
| ooo      |
| o        |
| o        |
| oooooo   |
|          |
+----------+
Score: 20  Tick: 160
```

## How it works

On every move, `bot.py` looks at each safe direction (one that doesn't hit a wall or the snake's body) and scores it on three things:

- **Distance to food:** closer is better, so the snake heads greedily for the food.
- **Free space (flood fill):** counts how many squares the snake could still reach after the move, so it avoids walling itself into a pocket.
- **Can it reach its tail:** if a path to the tail still exists, the snake can always follow its tail to safety. This check has the largest weight.

`snake.py` is the game engine. It handles wall and self collisions, food spawning, and an optional terminal display.

## Run it

Needs Python 3 and nothing else.

```bash
python snake.py   # watch one game in the terminal
python bot.py     # play 200 games without display; prints the average and best score
```

## Results

Each game is capped at 1,000 moves.

| Version | Average score | Best score |
|---|---|---|
| First attempt (neural network) | n/a | 3 |
| Rules-based, as first uploaded | about 10–12 | 36–46 |
| Rules-based, current | about 31–36 | 68–75 |

The current numbers come from five runs of 200 games each. The jump between the last two rows came from fixing one typo: the bot treated "up" as the opposite of "right", so whenever it was moving right it never considered turning up.

The `images/` folder has screenshots of earlier runs:
- `images/lost-version-best-54.png` is an earlier version that reached 54. I lost that version.
- `images/uploaded-version-best-36.png` is the version I first uploaded.

## What I learned

- Neural networks aren't the answer to everything. The network needed far more data and training than this problem justified. A few clear rules beat it easily.
- Small bugs can hide big losses. A one-word typo cost the bot about two-thirds of its score, and the code still ran without any error.
