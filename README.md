# TicTacToe Engine (In progress)

A tic tac toe AI trained with reinforcement learning with +1 for win, -1 for loss, 0 for tie

Training for even 50,000 episodes results in an agent that garantees at least a draw

Re-traing takes less than 5 minutes 

The final weights are saved in the csv file

## Getting Started

Clone the entire project and run demo.py, the game currently runs in console only

When making moves position 1 is top left, position 2 is top middle, position 9 is bottom right etc



## Motivation

I wanted to create a "simple" AI without having to dive so deep into machine learning

TicTacToe seemed like an obvious choice as it has simple rules and small-ish sample space

Also has more traditional minimax strategy than I can compare to\

## More about this Q-Learning

Rewards:
1 for win
0 for tie
-1 for loss

The agent is trained against itself

At 0 episodes the moves are completely random so player X's win/loss is random

At 50,000 episode, when playing against itself, the AI will always tie as expected




