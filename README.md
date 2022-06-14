# Janggi Game

A simple implementation of Janggi, also known as Korean Chess.

## Description

This program provides functionality for running a game of Janggi. The rule
set is simplified, containing all rules necessary for a funcitonal game including
moving and capturing pieces, individual piece rules, checking and checkmating.
Specialized movement of certain pieces like chariots and cannons inside of the
palace are not implemented.

## Getting Started

### Dependencies

No dependencies.

### Installing

No extra steps needed to install.

### Executing program

The program is not in a runnable state if executed as is. To use this program,
lines must be added to represent the moves made by players. See tests.py for examples,
or add the following line of code at the bottom of the file:
```
g = JanggiGame()
```

Moves can be made by adding the following line of code:
```
g.make_move('a7', 'a6')
```
Where 'a7' and 'a6' represent the coordinates of the squares being moved from and
to, respectively.

The current state of the game can be checked after any given move by using any of
the following lines of code:
```
g.get_game_state()
g.print_board()
g.is_in_check(PLAYER)
```
The first will return the current game state, either UNFINISHED, RED_WON, or BLUE_WON,
depending on if the game is still going or if a player has won. The second will print
out the board in its current state to the console, giving a rudimentary representation
of the board, and the last will inform if the specified player's general is in check, with
arguments being 'red' or 'blue' for the two players.

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details