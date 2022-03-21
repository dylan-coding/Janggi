# Author: Dylan Smith
# Description: A simple implementation of the board game Janggi, using PyGame

import copy
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
    """Creates a Janggi piece that defines the piece's team, type,
    and piece-specific rules."""
    
    def __init__(self, team, type, image):
        """
        Initializes the parameters for the Janggi playing piece.
        :param team: String, the team's name.
        :param type: String, the Piece's identifying name.
        :param image: String, the Piece's identifying symbol.
        """
        self._team = team
        self._type = type
        self._image = image
        self._moves = []
        self._blocked = None
        self._palace_only = False
        if type == 'general':
            # Set valid moves for general pieces
            self._palace_only = True
            self._moves = [[0, 0], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1],
                           [-1, -1], [0, 1], [0, -1]]
        elif type == 'guard':
            # Set valid moves for guard pieces
            self._palace_only = True
            self._moves = [[0, 0], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1],
                           [-1, -1], [0, 1], [0, -1]]
        elif type == 'chariot':
            # Set valid moves for chariot pieces
            self._moves = []
            for num in range(-8, 8):
                self._moves.append([0, num])
            for num in range(-9, 9):
                self._moves.append([num, 0])
        elif type == 'elephant':
            # Set valid moves and blockable squares for horse pieces
            self._moves = [[2, 3], [2, -3], [-2, 3], [-2, -3], [3, 2], [3, -2],
                           [-3, 2], [-3, -2], [0, 0]]
            self._blocked = {0: [[0, 1], [1, 2]],
                             1: [[0, -1], [1, -2]],
                             2: [[0, 1], [-1, 2]],
                             3: [[0, -1], [-1, -2]],
                             4: [[1, 0], [2, 1]],
                             5: [[1, 0], [2, -1]],
                             6: [[-1, 0], [-2, 1]],
                             7: [[-1, 0], [-2, -1]],
                             8: []}
        elif type == 'horse':
            # Set valid moves and blockable squares for horse pieces
            self._moves = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1],
                           [-2, 1], [-2, -1], [0, 0]]
            self._blocked = {0: [[0, 1]],
                             1: [[0, -1]],
                             2: [[0, 1]],
                             3: [[0, -1]],
                             4: [[1, 0]],
                             5: [[1, 0]],
                             6: [[-1, 0]],
                             7: [[-1, 0]],
                             8: []}
        elif type == 'cannon':
            # Set valid moves for cannon pieces
            self._moves = []
            for num in range(-8, -2):
                self._moves.append([0, num])
            for num in range(2, 8):
                self._moves.append([0, num])
            for num in range(-9, 2):
                self._moves.append([num, 0])
            for num in range(2, 9):
                self._moves.append([num, 0])
        elif type == 'soldier':
            # Set valid moves for soldier pieces
            if self._team == 'red':
                self._moves = [[0, 0], [1, 0], [0, -1], [0, 1]]
            else:
                self._moves = [[0, 0], [-1, 0], [0, -1], [0, 1]]
    
    def get_team(self):
        """Returns the piece's team."""
        return self._team
    
    def get_type(self):
        """Returns the piece's type."""
        return self._type
    
    def get_image(self):
        """Returns the image/token of the piece."""
        return self._image
    
    def get_moves(self):
        """Returns the set of valid moves for the piece."""
        return self._moves
    
    def get_blocked(self, move):
        """
        Returns the list of squares that, if occupied, prevents the unit
        from moving.
        :param move: Move being attempted by Horse or Elephant.
        :return: None if Piece can't be blocked, Array otherwise.
        """
        if self._blocked is None:
            return False
        key = 0
        for index in self.get_moves():
            if move == index:
                blocked_moves = self._blocked[key]
                return blocked_moves
            key += 1
    
    def get_palace_only(self):
        """Returns if the piece can only be in the palace."""
        return self._palace_only


class JanggiGame:
    """
    Represents the board game Janggi.
    """
    
    # To Do:
    # add check implementation
    # add additional rules for special movement in palace?
    
    def __init__(self):
        """
        Initializes the parameters for a game of Janggi, including:
            Playing board and palace
            Initial turn and game state
            Playing pieces
        """
        self._board = [[None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None]]
        self._palace = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3],
                        [2, 4], [2, 5], [7, 3], [7, 4], [7, 5], [8, 3], [8, 4],
                        [8, 5], [9, 3], [9, 4], [9, 5]]
        self._game_state = "UNFINISHED"
        self._current_turn = "blue"
        self._red_in_check = False
        self._blue_in_check = False
        self._red_general_square = [1, 4]
        self._blue_general_square = [8, 4]
        # Set pieces on board
        self._board[1][4] = Piece('red', 'general', 'G')
        self._board[0][0] = Piece('red', 'chariot', 'C')
        self._board[0][8] = Piece('red', 'chariot', 'C')
        self._board[0][1] = Piece('red', 'elephant', 'E')
        self._board[0][6] = Piece('red', 'elephant', 'E')
        self._board[0][2] = Piece('red', 'horse', 'H')
        self._board[0][7] = Piece('red', 'horse', 'H')
        self._board[0][3] = Piece('red', 'guard', 'U')
        self._board[0][5] = Piece('red', 'guard', 'U')
        self._board[2][1] = Piece('red', 'cannon', 'N')
        self._board[2][7] = Piece('red', 'cannon', 'N')
        self._board[3][0] = Piece('red', 'soldier', 'S')
        self._board[3][2] = Piece('red', 'soldier', 'S')
        self._board[3][4] = Piece('red', 'soldier', 'S')
        self._board[3][6] = Piece('red', 'soldier', 'S')
        self._board[3][8] = Piece('red', 'soldier', 'S')
        self._board[8][4] = Piece('blue', 'general', 'g')
        self._board[9][1] = Piece('blue', 'elephant', 'e')
        self._board[9][6] = Piece('blue', 'elephant', 'e')
        self._board[9][2] = Piece('blue', 'horse', 'h')
        self._board[9][7] = Piece('blue', 'horse', 'h')
        self._board[9][0] = Piece('blue', 'chariot', 'c')
        self._board[9][8] = Piece('blue', 'chariot', 'c')
        self._board[9][3] = Piece('blue', 'guard', 'u')
        self._board[9][5] = Piece('blue', 'guard', 'u')
        self._board[7][1] = Piece('blue', 'cannon', 'n')
        self._board[7][7] = Piece('blue', 'cannon', 'n')
        self._board[6][0] = Piece('blue', 'soldier', 's')
        self._board[6][2] = Piece('blue', 'soldier', 's')
        self._board[6][4] = Piece('blue', 'soldier', 's')
        self._board[6][6] = Piece('blue', 'soldier', 's')
        self._board[6][8] = Piece('blue', 'soldier', 's')
    
    def set_red_in_check(self, flag):
        """When invoked, changes the red_in_check flag to its opposite."""
        self._red_in_check = flag
    
    def set_blue_in_check(self, flag):
        """When invoked, changes the blue_in_check flag to its opposite."""
        self._blue_in_check = flag
    
    def get_general_square(self, team):
        """Gets the square that a specific general is at is at."""
        if team == "red":
            return self._red_general_square
        else:
            return self._blue_general_square
    
    def set_general_square(self, team, square):
        """Sets and tracks the square the generals are at."""
        if team == "red":
            self._red_general_square = square
        else:
            self._blue_general_square = square
    
    def convert_algebraic_notation(self, notation):
        """
        Takes the algebraic notation used to specify squares for make_move()
        and other functions and splits it into separate alpha-numeric values
        for accessing dictionary key-values and list indices.
        :param notation: A string in algebraic notation consisting of one
        letter from a-h and one number from 1-10.
        :return: Array.
        """
        cipher = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
            'i': 8, '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
            '8': 7, '9': 8, '0': 9
        }
        coordinates = []
        for char in notation:
            coordinates.append(cipher[char])
        if len(coordinates) == 3:
            coordinates.remove(coordinates[1])
        # Reverses dimensions to [y, x] format, due to how board is stored.
        coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
        return coordinates
    
    def get_board(self):
        """Returns the current state of the board."""
        return self._board
    
    def set_board(self, piece, square):
        """Sets or moves a specific piece to the designated square."""
        self._board[square[0]][square[1]] = piece
    
    def get_current_turn(self):
        """Returns the team of the current turn."""
        return self._current_turn
    
    def set_current_turn(self, team):
        """Changes the current turn to the specified team."""
        self._current_turn = team
    
    def get_palace(self):
        """Returns the squares designated as the palace."""
        return self._palace
    
    def print_board(self):
        """Prints the board to the console in human-readable text."""
        count = 1
        for row in self.get_board():
            for col in row:
                if col is None:
                    print('.', end=' ', flush=True)
                else:
                    print(col.get_image(), end=' ', flush=True)
                count += 1
                if count == 10:
                    print('\n')
                    count = 1
    
    def get_game_state(self):
        """Returns the current game state: UNFINISHED, RED_WON, or BLUE_WON."""
        return self._game_state
    
    def set_game_state(self, state):
        """Updates the current game state to RED_WON or BLUE_WON, indicating
        the game is finished."""
        self._game_state = state
    
    def is_in_check(self, player):
        """Returns if the specified player's general is in check."""
        if player == "red":
            return self._red_in_check
        else:
            return self._blue_in_check
    
    def get_piece(self, square):
        """ Gets a piece at a current square in [y, x] notation, returns None
        if no piece exists at that square."""
        board = self.get_board()
        piece = board[square[0]][square[1]]
        return piece
    
    def check_valid_turn(self, moving_piece):
        """Checks that the game is not finished, and that the correct player
        is attempting to move."""
        if self.get_game_state() != "UNFINISHED" or moving_piece is None:
            return False
        elif self.get_current_turn() != moving_piece.get_team():
            return False
        return True
    
    def check_valid_move(self, moving_piece, start, end):
        """
        Checks if the selected piece can move from current square to
        selected square. If a rule is broken in the designated move, returns
        False.
        :param moving_piece: The Piece to be moved.
        :param start: The square being moved from.
        :param end: The square being moved to.
        :return: Bool.
        """
        difference = [end[0] - start[0], end[1] - start[1]]
        captured_piece = self.get_piece(end)
        blocked = moving_piece.get_blocked(difference)
        if difference not in moving_piece.get_moves():
            return False
        if moving_piece.get_palace_only() and end not in self.get_palace():
            return False
        if blocked:
            if not self.check_blocked(blocked, start):
                return False
        if captured_piece is not None:
            if captured_piece.get_team() == moving_piece.get_team() and \
                    difference != [0, 0]:
                return False
        return True
    
    def check_blocked(self, blocked, start):
        """
        Checks if the Piece can be blocked.
        :param blocked: The Piece's list of blocking squares.
        :param start: The Piece's start square.
        :return: Bool.
        """
        for move in blocked:
            square = [start[0] + move[0], start[1] + move[1]]
            if self.get_piece(square) is not None:
                return False
        return True
    
    def make_move(self, start, end):
        """
        Takes algebraic notation for a start and end square and checks if
        the move is valid, performing it if it is. Reasons for a move to be
        invalid include the wrong player attempting to move, a piece moving
        to a square it cannot move to, or a piece being blocked by another
        piece.
        :param start: The square being moved from.
        :param end: The square being moved to.
        :return: Bool.
        """
        if self.get_game_state() != 'UNFINISHED':
            return False
        if isinstance(start, str):
            start = self.convert_algebraic_notation(start)
        moving_piece = self.get_piece(start)
        if moving_piece is None:
            return False
        player = moving_piece.get_team()
        captured = None
        if isinstance(end, str):
            end = self.convert_algebraic_notation(end)
        piece_type = moving_piece.get_type()
        if not self.check_valid_turn(moving_piece) or not \
                self.check_valid_move(moving_piece, start, end):
            return False
        if piece_type == 'cannon' and not self.move_cannon(start, end):
            return False
        if piece_type == 'chariot' and not self.move_chariot(start, end):
            return False
        if start != end:
            captured = self.get_piece(end)
            self.set_board(moving_piece, end)
            self.set_board(None, start)
            if piece_type == 'general':
                self.set_general_square(self.get_current_turn(), end)
        check = self.test_checks()
        if check == 'invalid':  # Move was invalid, reset board
            self.set_board(moving_piece, start)
            self.set_board(captured, end)
            if piece_type == 'general':
                self.set_general_square(self.get_current_turn(), start)
            return False
        elif check == 'red checks':  # Red has placed Blue in check
            self.set_blue_in_check(True)
            self.set_red_in_check(False)
        elif check == 'blue checks':  # Blue has placed Red in check
            self.set_red_in_check(True)
            self.set_blue_in_check(False)
        else:  # No check has been made
            self.set_blue_in_check(False)
            self.set_red_in_check(False)
        self.set_current_turn('red' if player == 'blue' else 'blue')
        if self.get_current_turn() == 'red' and self.is_in_check('red'):
            self.checkmate_checker('red')
        elif self.get_current_turn() == 'blue' and self.is_in_check('blue'):
            self.checkmate_checker('blue')
        return True
    
    def test_checks(self):
        """
        Checks the state of the board after a move was made to see if one
        player has placed the other in check, or if a move would result in
        the player's own general being placed in check.
        :return: check: Possible values are 'blue_checks', 'red_checks',
        False, and 'invalid'.
        """
        red_gen = self.get_general_square('red')
        blue_gen = self.get_general_square('blue')
        turn = self.get_current_turn()
        check = False
        row_count = 0
        for row in self.get_board():
            col_count = 0
            for col in row:
                if col is not None:
                    piece_team = col.get_team()
                    start = [row_count, col_count]
                    if turn == 'red':
                        if piece_team == 'red':
                            if self.test_move(start, blue_gen) is True:
                                check = 'red checks'  # Red checks Blue
                                return check
                        else:
                            if self.test_move(start, red_gen) is True:
                                check = 'invalid'  # Red made illegal move
                                return check
                    else:
                        if piece_team == 'blue':
                            if self.test_move(start, red_gen) is True:
                                check = 'blue checks'  # Blue checks Red
                                return check
                        else:
                            if self.test_move(start, blue_gen) is True:
                                check = 'invalid'  # Blue made illegal move
                                return check
                col_count += 1
            row_count += 1
        if not self.is_in_check(turn) and check is not False:
            check = 'invalid'
        return check
    
    def test_move(self, start, end):
        """
        Tests a move for a piece to see if it would be valid.
        :param start: Square to be moved from.
        :param end: Square to be moved to.
        :return: Bool.
        """
        moving_piece = self.get_piece(start)
        if not self.check_valid_move(moving_piece, start, end):
            return False
        if moving_piece.get_type() == 'cannon' and \
                not self.move_cannon(start, end):
            return False
        if moving_piece.get_type() == 'chariot' and \
                not self.move_chariot(start, end):
            return False
        return True
    
    def move_chariot(self, start, end):
        """
        Checks if a chariot is blocked by another piece.
        :param start: The square being moved from.
        :param end: The square being moved to.
        :return: Bool.
        """
        if start[0] == end[0]:
            arr = [start[1], end[1]]
            arr.sort()
            for i in range(arr[0] + 1, arr[1] - 1):
                if self.get_piece([start[0], i]) is not None:
                    return False
        else:
            arr = [start[0], end[0]]
            arr.sort()
            for i in range(arr[0] + 1, arr[1] - 1):
                if self.get_piece([i, start[1]]) is not None:
                    return False
        return True
    
    def move_cannon(self, start, end):
        """
        Checks if the move is valid for a cannon, checking that it jumps
        over exactly one other unit that is not another cannon and is not
        attempting to capture a cannon.
        :param start: Square to be moved from.
        :param end: Square to be moved to.
        :return: Bool.
        """
        if start[0] != end[0] and start[1] != end[1]:
            return False
        if start == end:
            return True
        if self.get_piece(end) is not None:
            if self.get_piece(end).get_type() == 'cannon':
                return False
        if start[0] == end[0]:
            return self.move_cannon_horizon(start, end)
        else:
            return self.move_cannon_vert(start, end)
    
    def move_cannon_horizon(self, start, end):
        """
        Counts the number of pieces between a cannon and it's
        destination for horizontal movement, returning True if the move is
        legal.
        :param start: Square to be moved from.
        :param end: Square to be moved to.
        :return: Bool.
        """
        count = 0
        arr = [start[1], end[1]]
        arr.sort()
        for i in range(arr[0] + 1, arr[1]):
            if self.get_piece([start[0], i]) is not None:
                if self.get_piece([start[0], i]).get_type() == 'cannon':
                    return False
                count += 1
        return True if count == 1 else False
    
    def move_cannon_vert(self, start, end):
        """
        Counts the number of pieces between a cannon and it's
        destination for vertical movement, returning True if the move is
        legal.
        :param start: Square to be moved from.
        :param end: Square to be moved to.
        :return: Bool.
        """
        count = 0
        arr = [start[0], end[0]]
        arr.sort()
        for i in range(arr[0] + 1, arr[1]):
            if self.get_piece([i, start[1]]) is not None:
                if self.get_piece([i, start[1]]).get_type() == 'cannon':
                    return False
                count += 1
        return True if count == 1 else False
    
    def checkmate_checker(self, team):
        row_count = 0
        for row in self.get_board():
            col_count = 0
            for col in row:
                if col is not None:
                    piece_team = col.get_team()
                    if piece_team == team:
                        start = [row_count, col_count]
                        moves = col.get_moves()
                        for move in moves:
                            end = [0, 0]
                            end[0] = move[0] + start[0]
                            end[1] = move[1] + start[1]
                            if (0 <= end[0] < 10) and (0 <= end[1] < 9):
                                pass
                                """result = self.make_move(start, end, True)
                                if result is False:
                                    return result"""
                col_count += 1
            row_count += 1
                            
        if team == 'red':
            # self.set_game_state('BLUE WON')
            pass
        else:
            # self.set_game_state('RED WON')
            pass


"""
if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
"""

g = JanggiGame()

print(g.make_move('c7', 'c6'))  # blue
print(g.make_move('c1', 'd3'))  # red
print(g.make_move('b10', 'd7'))  # blue
print(g.make_move('b3', 'e3'))  # red
print(g.make_move('c10', 'd8'))
print(g.make_move('h1', 'g3'))
print(g.make_move('e7', 'e6'))
print(g.make_move('e3', 'e6'))  # red cannon captures soldier -- check here
print('red False:', g.is_in_check('red'))
print(g.get_game_state())
print('blue False:', g.is_in_check('blue'))
print()

print(g.make_move('h8', 'c8'))  # blue moves -- check here
print(g.make_move('d3', 'e5'))  # red
print(g.make_move('c8', 'c4'))  # blue cannon captures red soldier -- check
# here
print('red False:', g.is_in_check('red'))
print(g.get_game_state())
print('blue False:', g.is_in_check('blue'))
print()

print(g.make_move('e5', 'c4'))  # red horse captures blue cannon
print(g.make_move('i10', 'i8'))  # blue chariot moves
print(g.make_move('g4', 'f4'))
print(g.make_move('i8', 'f8'))  # blue chariot moves sideway
print(g.make_move('g3', 'h5'))
print(g.make_move('h10', 'g8'))  # blue horse
print(g.make_move('e6', 'e3'))  # red CHECKS blue using a cannon -- special
# test for checks using a cannon -- check here
print('red False:', g.is_in_check('red'))
print(g.get_game_state())
print('blue True:', g.is_in_check('blue'))  # True
print()

print(g.make_move('e9', 'd9'))  # blue moves
print(g.make_move('c4', 'e5'))  # red
print(g.make_move('c6', 'd6'))
print(g.make_move('e5', 'c4'))
print(g.make_move('a7', 'a6'))  # blue
print(g.make_move('h3', 'h9'))  # red cannon moves to a position where it
# COULD Check but has not. -- check here
print(g.make_move('a10', 'a7'))
print(g.make_move('c4', 'd6'))  # red horse captures blue soldier
print(g.make_move('a6', 'b6'))
print(g.make_move('h5', 'g7'))
print(g.make_move('b8', 'b1'))  # blue cannon captures red elephant
print(g.make_move('a1', 'b1'))  # red chariot captures blue cannon
print(g.make_move('a7', 'a4'))
print(g.make_move('b1', 'c1'))
print(g.make_move('a4', 'a2'))  # blue CHECKS red using a chariot -- check here

print(g.make_move('e2', 'e1'))  # red general moves to avoid capture --
# check after this

print(g.make_move('i7', 'h7'))  # blue moves
print(g.make_move('c1', 'c9'))  # red chariot moves to the palace to
# CHECKMATE blue
print('red False:', g.is_in_check('red'))
print(g.get_game_state(), "should be RED_WON")
print('blue True:', g.is_in_check('blue'))  # True
