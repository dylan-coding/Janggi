# Author: Dylan Smith
# Description: A simple implementation of the board game Janggi, using PyGame

import pygame
from pygame.locals import *

# Commented out code is for pyGame implementation
"""
class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size,
                                                     pygame.HWSURFACE |
                                                     pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
"""

class Piece:
    """Creates a Janggi piece that defines the piece's team and type."""

    def __init__(self, team, type, image):
        """Initializes the parameters for the Janggi playing piece."""
        self._team = team
        self._type = type
        self._image = image

    def get_team(self):
        return self._team

    def get_type(self):
        return self._type

    def get_image(self):
        return self._image


class JanggiGame:
    """Represents the board game Janggi."""

    def __init__(self):
        """Initializes the parameters for a game of Janggi, including:
            playing board and palace
            initial turn and game state
            playing pieces"""
        self._board = [['C', 'E', 'H', 'U', '.', 'U', 'E', 'H', 'C'],
                       ['.', '.', '.', '.', 'G', '.', '.', '.', '.'],
                       ['.', 'N', '.', '.', '.', '.', '.', 'N', '.'],
                       ['S', '.', 'S', '.', 'S', '.', 'S', '.', 'S'],
                       ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['s', '.', 's', '.', 's', '.', 's', '.', 's'],
                       ['.', 'n', '.', '.', '.', '.', '.', 'n', '.'],
                       ['.', '.', '.', '.', 'g', '.', '.', '.', '.'],
                       ['c', 'e', 'h', 'u', '.', 'u', 'e', 'h', 'c']]
        self._palace = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3],
                        [2, 4], [2, 5], [7, 3], [7, 4], [7, 5], [8, 3], [8, 4],
                        [8, 5], [9, 3], [9, 4], [9, 5]]
        self._game_state = "UNFINISHED"
        self._current_turn = "blue"
        self._red_in_check = False
        self._blue_in_check = False
        # Change implementation to self._board[x][y] = Piece(...)???
        self._red_general = Piece('red', 'general', 'G')
        self._red_elephant = Piece('red', 'elephant', 'E')
        self._red_horse = Piece('red', 'horse', 'H')
        self._red_chariot = Piece('red', 'chariot', 'C')
        self._red_guard = Piece('red', 'guard', 'U')
        self._red_cannon = Piece('red', 'cannon', 'N')
        self._red_soldier = Piece('red', 'soldier', 'S')
        self._blue_general = Piece('blue', 'general', 'g')
        self._blue_elephant = Piece('blue', 'elephant', 'e')
        self._blue_horse = Piece('blue', 'horse', 'h')
        self._blue_chariot = Piece('blue', 'chariot', 'c')
        self._blue_guard = Piece('blue', 'guard', 'u')
        self._blue_cannon = Piece('blue', 'cannon', 'n')
        self._blue_soldier = Piece('blue', 'soldier', 's')

    def convert_algebraic_notation(self, notation):
        """Takes the algebraic notation used to specify squares for make_move()
        and other functions and splits it into separate alpha-numeric values
        for accessing dictionary key-values and list indices."""
        cipher = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
            'i': 8, '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
            '8': 7, '9': 8, '0': 9
        }
        coordinates = []
        for char in notation:
            coordinates.append(cipher[char])
        # if len(coordinates) == 3:
            # coordinates.remove(coordinates[1])
        # Reverses dimensions to [y, x] format, due to how board is stored.
        temp = coordinates[0]
        coordinates[0] = coordinates[1]
        coordinates[1] = temp
        return coordinates

    def get_board(self):
        return self._board

    def get_current_turn(self):
        return self._current_turn

    def get_palace(self):
        return self._palace

    def print_board(self):
        for row in self.get_board():
            print(' '.join(row))

    def get_game_state(self):
        return self._game_state

    def is_in_check(self, player):
        if player == "red":
            self._red_in_check
        else:
            self._blue_in_check

    def make_move(self, start, end):
        """UNFINISHED IMPLEMENTATION"""
        if self.get_game_state() != "UNFINISHED":
            return False
        start = self.convert_algebraic_notation(start)
        end = self.convert_algebraic_notation(end)
        difference = [end[0] - start[0], end[1] - start[1]]



"""
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
"""