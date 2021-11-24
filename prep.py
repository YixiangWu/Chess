from collections import deque
from os import chdir, path
import pygame


class Setup:
    """The class of chess game essentials."""

    def __init__(self):
        self.board = [
            'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR',
            # 00,   01,   02,   03,   04,   05,   06,   07
            # a8,   b8,   c8,   d8,   e8,   f8,   g8,   h8
            'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP',
            # 08,   09,   10,   11,   12,   13,   14,   15
            # a7,   b7,   c7,   d7,   e7,   f7,   g7,   h7
            '00', '00', '00', '00', '00', '00', '00', '00',
            # 16,   17,   18,   19,   20,   21,   22,   23
            # a6,   b6,   c6,   d6,   e6,   f6,   g6,   h6
            '00', '00', '00', '00', '00', '00', '00', '00',
            # 24,   25,   26,   27,   28,   29,   30,   31
            # a5,   b5,   c5,   d5,   e5,   f5,   g5,   h5
            '00', '00', '00', '00', '00', '00', '00', '00',
            # 32,   33,   34,   35,   36,   37,   38,   39
            # a4,   b4,   c4,   d4,   e4,   f4,   g4,   h4
            '00', '00', '00', '00', '00', '00', '00', '00',
            # 40,   41,   42,   43,   44,   45,   46,   47
            # a3,   b3,   c3,   d3,   e3,   f3,   g3,   h3
            'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP',
            # 48,   49,   50,   51,   52,   53,   54,   55
            # a2,   b2,   c2,   d2,   e2,   f2,   g2,   h2
            'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'
            # 56,   57,   58,   59,   60,   61,   62,   63
            # a1,   b1,   c1,   d1,   e1,   f1,   g1,   h1
        ]
        self.piece_coordinate = {
            'wP': [48, 49, 50, 51, 52, 53, 54, 55], 'wR': [56, 63],
            'wN': [57, 62], 'wB': [58, 61], 'wQ': [59], 'wK': [60],
            'bP': [8, 9, 10, 11, 12, 13, 14, 15], 'bR': [0, 7],
            'bN': [1, 6], 'bB': [2, 5], 'bQ': [3], 'bK': [4]
        }  # better way to locate pieces rather than looping through the board
        self.piece_type = {
            'pawn': ['wP', 'bP'], 'rook': ['wR', 'bR'], 'knight': ['wN', 'bN'],
            'bishop': ['wB', 'bB'], 'queen': ['wQ', 'bQ'], 'king': ['wK', 'bK']
        }
        self.turn = 'w'  # 'w' -> white, 'b' -> black
        self.en_passant = None
        self.castle_flags = {'w': {'short': True, 'long': True},
                             'b': {'short': True, 'long': True}}

    @staticmethod
    def _help_generate_legal_squares(board, start, potential_squares):
        """Take potential squares and return legal squares correspondingly."""
        squares = []
        if board[start][1] == 'R' or board[start][1] == 'B' or \
                board[start][1] == 'Q':
            for square in potential_squares:
                if board[square] != '00':
                    if board[start][0] != board[square][0]:
                        squares.append(square)
                    break
                squares.append(square)
        elif board[start][1] == 'N' or board[start][1] == 'K':
            for square in potential_squares:
                if 0 <= square <= 63:
                    if board[square] == '00' or \
                            board[start][0] != board[square][0]:
                        squares.append(square)
        return squares

    def pawn(self, board, start):
        """Generate pawn's legal squares."""
        squares = []
        direction = -1 if board[start][0] == 'w' else 1  # pawn-push direction
        if board[start + 8 * direction] == '00':
            squares.append(start + 8 * direction)
            if start // 8 == 3.5 + 2.5 * -direction and \
                    board[start + 16 * direction] == '00':
                # pawns can move forward two squares on their first move
                squares.append(start + 16 * direction)

        # pawn captures diagonally
        if start % 8 != 0 and board[start - 1 + 8 * direction] != '00' and \
                board[start - 1 + 8 * direction][0] != board[start][0]:
            squares.append(start - 1 + 8 * direction)
        if start % 8 != 7 and board[start + 1 + 8 * direction] != '00' and \
                board[start + 1 + 8 * direction][0] != board[start][0]:
            squares.append(start + 1 + 8 * direction)

        # en passant
        if (start - 1 == self.en_passant or start + 1 == self.en_passant) and \
                (start != 32 or self.en_passant != 31) and \
                (start != 31 or self.en_passant != 32):
            squares.append(self.en_passant + 8 * direction)
        return squares

    def rook(self, board, start):
        """Generate rook's legal squares."""
        squares = []
        potential_squares_list = [
            range(start - 8, start % 8 - 8, -8),  # going upwards
            range(start + 8, start % 8 + 63, 8),  # going downwards
            range(start - 1, start - start % 8 - 1, -1),  # going to the left
            range(start + 1, start - start % 8 + 8)  # going to the right
        ]
        for potential_squares in potential_squares_list:
            squares.extend(self._help_generate_legal_squares(
                board, start, potential_squares))
        return squares

    def knight(self, board, start):
        """Generate knight's legal squares."""
        squares = []
        potential_squares_dict = {
            '6': [start - 15, start + 17],
            '5': [start - 6, start + 10],
            '2': [start - 10, start + 6],
            '1': [start - 17, start + 15]
        }
        for file, potential_squares in potential_squares_dict.items():
            if int(file) == 6 or int(file) == 5:
                # ensure knights not moving out of the right edge
                if start % 8 > int(file):
                    continue
            if int(file) == 2 or int(file) == 1:
                # ensure knights not moving out of the left edge
                if start % 8 < int(file):
                    continue
            squares.extend(self._help_generate_legal_squares(
                board, start, potential_squares))
        return squares

    def bishop(self, board, start):
        """Generate bishop's legal squares."""
        squares = []
        min_distances = {  # minimum distance to the board edge
            '-7': min(start // 8 + 1, 8 - start % 8),  # upper right
            '-9': min(start // 8 + 1, start % 8 + 1),  # upper left
            '7': min(8 - start // 8, start % 8 + 1),  # lower left
            '9': min(8 - start // 8, 8 - start % 8)  # lower right
        }
        for increment, min_distance in min_distances.items():
            squares.extend(self._help_generate_legal_squares(
                board, start,
                range(start + int(increment),
                      start + int(increment) * min_distance,
                      int(increment))))
        return squares

    def queen(self, board, start):
        """Generate queen's legal squares."""
        return self.rook(board, start) + self.bishop(board, start)

    def _brave_king(self, board, start):
        """Generate all king's squares without examining dangers."""
        squares = []
        potential_squares_dict = {
            '-1': [start - 8, start + 8],
            # '-1' indicates no invalid file required for these two squares
            '0': [start - 9, start - 1, start + 7],
            '7': [start - 7, start + 1, start + 9]
        }
        for invalid_file, potential_squares in potential_squares_dict.items():
            if start % 8 != int(invalid_file):
                squares.extend(self._help_generate_legal_squares(
                    board, start, potential_squares))
        return squares

    def is_attacked(self, board, color, verifying_square=None):
        """Determine whether a square gets attacked."""
        if verifying_square is None:  # the default verifying piece is the king
            verifying_square = self.piece_coordinate[color + 'K'][0]

        temp_board = board[:]

        # verify vertically and horizontally
        temp_board[verifying_square] = color + 'R'
        for square in self.rook(temp_board, verifying_square):
            if board[square][1] == 'R' or board[square][1] == 'Q':
                return True

        # verify diagonally
        temp_board[verifying_square] = color + 'B'
        for square in self.bishop(temp_board, verifying_square):
            if board[square][1] == 'B' or board[square][1] == 'Q':
                return True
            if square // 8 == verifying_square // 8 + 1 and \
                    board[square] == 'wP':
                return True
            if square // 8 == verifying_square // 8 - 1 and \
                    board[square] == 'bP':
                return True

        # verify knights moves
        temp_board[verifying_square] = color + 'N'
        for square in self.knight(temp_board, verifying_square):
            if board[square][1] == 'N':
                return True

        # verify king moves
        temp_board[verifying_square] = color + 'K'
        for square in self._brave_king(temp_board, verifying_square):
            if board[square][1] == 'K':
                return True

    def castle(self, board, start):
        """Generate king's legal squares for castling."""
        squares = []
        if not self.is_attacked(board, board[start][0], start):
            if self.castle_flags[self.turn]['long']:  # long castle
                for square in range(start - 3, start):
                    if board[square] != '00':
                        # squares between king and rook involved are unoccupied
                        break
                    elif self.is_attacked(board, board[start][0], square) and \
                            square != start - 3:
                        # king cannot cross over nor end on squares
                        # that are attacked by an enemy piece
                        break
                    if square == start - 1:
                        squares.append(start - 2)
            if self.castle_flags[self.turn]['short']:  # short castle
                for square in range(start + 1, start + 3):
                    if board[square] != '00' or \
                            self.is_attacked(board, board[start][0], square):
                        break
                    if square == start + 2:
                        squares.append(start + 2)
        return squares

    def king(self, board, start):
        """Generate king's legal squares."""
        squares = self.castle(board, start)
        for square in self._brave_king(board, start):
            if not self.is_attacked(board, board[start][0], square):
                squares.append(square)
        return squares

    def legal(self, start):
        """Return legal squares for the specific piece."""
        squares, taking_en_passant = [], None
        for piece, symbols in self.piece_type.items():
            if self.board[start] in symbols:
                squares = getattr(Setup, piece)(self, self.board, start)

        # check whether an en passant move surrenders the king
        if self.en_passant and self.board[start][1] == 'P':
            taking_en_passant = self.en_passant - 8 if \
                self.board[start][0] == 'w' else self.en_passant + 8
            if taking_en_passant in squares and self.board[start][1] == 'P':
                temp_board = self.board[:]
                temp_board[start], temp_board[self.en_passant] = '00', '00'
                if self.is_attacked(temp_board, self.turn):
                    squares.remove(taking_en_passant)

        # check whether a chess move escapes checks by capturing or blocking
        # the dangerous source, also ensure pieces pinned to their king move
        # without surrendering the king
        fake_legal_squares, temp_board = squares[:], self.board[:]
        if self.board[start][1] != 'K':
            temp_board[start] = '00'
        if self.is_attacked(temp_board, self.turn):
            for square in fake_legal_squares:
                if square == taking_en_passant and square in squares:
                    # allow pawns to capture the dangerous source with en
                    # passant to escape checks
                    continue
                temp_board = self.board[:]
                temp_board[start], temp_board[square] = '00', self.board[start]
                verifying_square = None if \
                    self.board[start][1] != 'K' else square
                if self.is_attacked(temp_board, self.turn, verifying_square):
                    squares.remove(square)
        return squares


class Log:
    """The class for game logs."""

    def __init__(self):
        self.game_log = deque([])
        self.temp_log = deque([])
        self.san = []  # standard algebraic notation

    @staticmethod
    def _algebraic_square_notation(square):
        """Convert numeric square notation to algebraic square notation."""
        return chr(97 + square % 8) + str(8 - (square // 8))

    def track_the_game(self, board, start, target, identical_piece):
        """Keep track of the chess game."""
        move = board[start] + str(start).zfill(2) + str(target).zfill(2)
        # <piece symbol><start square><target square>
        move += 'x' + board[target] if board[target] != '00' else ''
        # notation examples: wP5236, wK6062, wN4528xbP, bP5462=bQ, wP1506xbN=wR
        # NOTE: pawn promotion log is added in the Game class
        if board[start][1] == 'P' and start % 8 != target % 8 and \
                board[target] == '00':  # if taking en passant
            move += 'EbP' if board[start][0] == 'w' else 'EwP'
            # en passant notation example: wP2819EbP
        self.game_log.append(move)

        # generate standard algebraic notation
        if board[start][1] == 'K' and target - start == 2:
            self.san.append('O-O')  # short castle
        elif board[start][1] == 'K' and start - target == 2:
            self.san.append('O-O-O')  # long castle
        else:
            san = board[start][1] if board[start][1] != 'P' else ''

            # it is necessary to disambiguate the move when two or more
            # identical pieces can move to the same target square
            identical_piece.remove(start)
            if len(identical_piece) >= 1:
                file, rank = [], []
                for square in identical_piece:
                    file.append(square % 8)
                    rank.append(square // 8)
                if start % 8 in file and start // 8 in rank:  # if there are
                    # two or more than two other identical pieces and
                    # board[start] conflicts with them in both rank and
                    # file, disambiguate the move with both rank and file
                    san += self._algebraic_square_notation(start)
                elif start % 8 in file:
                    # disambiguate the move with rank if on the same file
                    san += self._algebraic_square_notation(start)[1]
                else:  # otherwise, disambiguate the move with file
                    san += self._algebraic_square_notation(start)[0]

            elif board[start][1] == 'P' and start % 8 != target % 8:
                # specify a pawn's file whenever it captures a piece
                san += self._algebraic_square_notation(start)[0]
            # check if the move captures an enemy
            if board[target] != '00' or \
                    board[start][1] == 'P' and start % 8 != target % 8:
                # since target square of an en passant move is '00', it needs
                # to be specified in the if statement
                san += 'x'
            san += self._algebraic_square_notation(target)
            self.san.append(san)

    @staticmethod
    def _help_update_position(rewind_dict, piece, square, operation):
        """Help manage different operations that update a position."""
        getattr(rewind_dict['piece_coordinate'][piece], operation)(square)
        rewind_dict['board'][square] = '00' if operation == 'remove' else piece

    def update_position(self, rewind_dict, flag):
        """Update turn, board, and piece coordinates of a position."""
        move, operations = '', ['append', 'remove']
        if flag == 'last':  # to look for the last position
            move = self.game_log.pop()
            self.temp_log.appendleft(move)
            rewind_dict['turn'] = move[0]
        elif flag == 'next':  # to look for the next position
            move = self.temp_log.popleft()
            self.game_log.append(move)
            rewind_dict['turn'] = 'b' if move[0] == 'w' else 'w'
            operations = operations[::-1]  # reverse the operations list
        # move[:2] -> piece symbol, move[2:4] -> start, move[4:6] -> target
        self._help_update_position(
            rewind_dict, move[:2],
            int(move[2:4]), operations[0])
        if move[-3] == '=':  # if pawn gets promoted
            # move[-2:] -> piece symbol that the pawn promoted to
            self._help_update_position(
                rewind_dict, move[-2:],
                int(move[4:6]), operations[1])
            if move[-6] == 'x':  # if enemy piece got captured while promoting
                # move[-5:-3] -> piece symbol that gets captured
                getattr(rewind_dict['piece_coordinate'][move[-5:-3]],
                        operations[0])(int(move[4:6]))
                if flag == 'last':
                    rewind_dict['board'][int(move[4:6])] = move[-5:-3]
        else:
            self._help_update_position(
                rewind_dict, move[:2],
                int(move[4:6]), operations[1])
            if move[-3] == 'x':  # if enemy piece got captured
                # move[-2:] -> piece symbol that gets captured
                getattr(rewind_dict['piece_coordinate'][move[-2:]],
                        operations[0])(int(move[4:6]))
                if flag == 'last':
                    rewind_dict['board'][int(move[4:6])] = move[-2:]
            elif move[-3] == 'E':  # if en passant
                # move[-2:] -> the pawn that gets captured by en passant
                if move[-2] == 'b':  # if a black pawn got captured
                    self._help_update_position(
                        rewind_dict, move[-2:],
                        int(move[4:6]) + 8, operations[0])
                else:  # if a white pawn got captured
                    self._help_update_position(
                        rewind_dict, move[-2:],
                        int(move[4:6]) - 8, operations[0])
            elif move[1] == 'K' and int(move[4:6]) - int(move[2:4]) == 2:
                # update rook position if short castle
                self._help_update_position(
                    rewind_dict, move[0] + 'R',
                    int(move[2:4]) + 3, operations[0])
                self._help_update_position(
                    rewind_dict, move[0] + 'R',
                    int(move[2:4]) + 1, operations[1])
            elif move[1] == 'K' and int(move[2:4]) - int(move[4:6]) == 2:
                # update rook position if long castle
                self._help_update_position(
                    rewind_dict, move[0] + 'R',
                    int(move[2:4]) - 4, operations[0])
                self._help_update_position(
                    rewind_dict, move[0] + 'R',
                    int(move[2:4]) - 1, operations[1])
        return rewind_dict['turn']


def prep():
    """This function prepares the game execution."""
    # set cwd to the main.py file's directory
    chdir(path.dirname(path.realpath(__file__)))

    # initialize pygame
    pygame.init()
    pygame.display.set_caption('chess')
