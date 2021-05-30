class Prep:
    """This class prepares chess games."""

    def __init__(self):
        self.initialBoard = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR',
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
                             'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        #                      56,   57,   58,   59,   60,   61,   62,   63
        #                      a1,   b1,   c1,   d1,   e1,   f1,   g1,   h1
        self.pieceType = {'pawn': ['wP', 'bP'], 'rook': ['wR', 'bR'],
                          'knight': ['wN', 'bN'], 'bishop': ['wB', 'bB'],
                          'queen': ['wQ', 'bQ'], 'king': ['wK', 'bK']}
        self.pieceColor = {'white': ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK'],
                           'black': ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK']}

    def color(self, board, first, second):
        """This method compares color between two pieces."""
        if ((board[first] in self.pieceColor['white'] and
             board[second] in self.pieceColor['black']) or
            (board[first] in self.pieceColor['black'] and
             board[second] in self.pieceColor['white'])):
            return True

    @staticmethod
    def coordinate(board, piece):
        """This method returns the coordinates of specific piece(s)."""
        squares = []
        for square in range(64):
            if board[square] == piece:
                squares.append(square)
        return squares

    def pawn(self, board, start):
        """This method generates pawn's legal squares."""
        squares = []
        if board[start] in self.pieceColor['white']:
            if board[start - 8] == '00':
                squares.append(start - 8)
            if start % 8 != 0 and board[start - 9] in self.pieceColor['black']:
                squares.append(start - 9)
            if start % 8 != 7 and board[start - 7] in self.pieceColor['black']:
                squares.append(start - 7)
        else:
            if board[start + 8] == '00':
                squares.append(start + 8)
            if start % 8 != 0 and board[start + 7] in self.pieceColor['white']:
                squares.append(start + 7)
            if start % 8 != 7 and board[start + 9] in self.pieceColor['white']:
                squares.append(start + 9)
        return squares

    def rook(self, board, start):
        """This method generates rook's legal squares."""
        squares = []
        # Generates legal squares vertically.
        for i in range(1, start // 8 + 1):  # going upwards
            if board[start - 8 * i] != '00':
                if self.color(board, start, start - 8 * i):
                    squares.append(start - 8 * i)
                break
            squares.append(start - 8 * i)
        for i in range(1, 8 - start // 8):  # going downwards
            if board[start + 8 * i] != '00':
                if self.color(board, start, start + 8 * i):
                    squares.append(start + 8 * i)
                break
            squares.append(start + 8 * i)

        # Generates legal squares horizontally.
        for i in range(1, start % 8 + 1):  # going to the left
            if board[start - i] != '00':
                if self.color(board, start, start - i):
                    squares.append(start - i)
                break
            squares.append(start - i)
        for i in range(1, 8 - start % 8):  # going to the right
            if board[start + i] != '00':
                if self.color(board, start, start + i):
                    squares.append(start + i)
                break
            squares.append(start + i)
        return squares

    def knight(self, board, start):
        """This method generates knight's legal squares."""
        squares = []
        if start % 8 <= 6:
            for square in [start - 15, start + 17]:
                if 0 <= square <= 63 and \
                        (board[square] == '00' or
                         self.color(board, start, square)):
                    squares.append(square)
        if start % 8 <= 5:
            for square in [start - 6, start + 10]:
                if 0 <= square <= 63 and \
                        (board[square] == '00' or
                         self.color(board, start, square)):
                    squares.append(square)
        if start % 8 >= 2:
            for square in [start - 10, start + 6]:
                if 0 <= square <= 63 and \
                        (board[square] == '00' or
                         self.color(board, start, square)):
                    squares.append(square)
        if start % 8 >= 1:
            for square in [start - 17, start + 15]:
                if 0 <= square <= 63 and \
                        (board[square] == '00' or
                         self.color(board, start, square)):
                    squares.append(square)
        return squares

    def bishop(self, board, start):
        """This method generates bishop's legal squares."""
        squares = []
        # Generates legal squares for upper right.
        for i in range(1, min(start // 8 + 1, 8 - start % 8)):
            if board[start - 7 * i] != '00':
                if self.color(board, start, start - 7 * i):
                    squares.append(start - 7 * i)
                break
            squares.append(start - 7 * i)

        # Generate legal squares for upper left.
        for i in range(1, min(start // 8 + 1, start % 8 + 1)):
            if board[start - 9 * i] != '00':
                if self.color(board, start, start - 9 * i):
                    squares.append(start - 9 * i)
                break
            squares.append(start - 9 * i)

        # Generate legal squares for lower left.
        for i in range(1, min(8 - start // 8, start % 8 + 1)):
            if board[start + 7 * i] != '00':
                if self.color(board, start, start + 7 * i):
                    squares.append(start + 7 * i)
                break
            squares.append(start + 7 * i)

        # Generate legal squares for lower right.
        for i in range(1, min(8 - start // 8, 8 - start % 8)):
            if board[start + 9 * i] != '00':
                if self.color(board, start, start + 9 * i):
                    squares.append(start + 9 * i)
                break
            squares.append(start + 9 * i)
        return squares

    def queen(self, board, square):
        """This method generates queen's legal squares."""
        return self.rook(board, square) + self.bishop(board, square)

    def brave_king(self, board, start):
        """This method generates king's legal squares
        WITHOUT checking dangerous squares. """
        squares = []
        for square in [start - 8, start + 8]:
            if 0 <= square <= 63 and \
                    (board[square] == '00' or
                     self.color(board, start, square)):
                squares.append(square)
        if start % 8 != 0:
            for square in [start - 9, start - 1, start + 7]:
                if 0 <= square <= 63 and \
                        (board[square] == '00' or
                         self.color(board, start, square)):
                    squares.append(square)
        if start % 8 != 7:
            for square in [start - 7, start + 1, start + 9]:
                if 0 <= square <= 63 and \
                        (board[square] == '00' or
                         self.color(board, start, square)):
                    squares.append(square)
        return squares

    def danger(self, board, start):
        """This method generates dangerous squares for the king."""
        squares = []
        # Since moving a piece to a square occupied by a piece of the same
        # color is illegal, there are cases that the opponent's piece around
        # the king is guarded, but the square occupied by this piece is not
        # marked as a dangerous square. Turn every opponent's pieces around the
        # king into opposite-color pieces can resolve this problem.
        copy = board[:]
        for square in self.brave_king(board, start):
            if self.color(copy, start, square):
                copy[square] = 'bP' if copy[square] in \
                    self.pieceColor['white'] else 'wP'

        color = 'black' if board[start] in \
            self.pieceColor['white'] else 'white'
        for piece in self.pieceColor[color]:
            dangers = []
            if piece == 'wP':
                for square in self.coordinate(board, piece):
                    if start % 8 != 0:
                        dangers.append(square - 9)
                    if start % 8 != 7:
                        dangers.append(square - 7)
            elif piece == 'bP':
                for square in self.coordinate(board, piece):
                    if start % 8 != 0:
                        dangers.append(square + 7)
                    if start % 8 != 7:
                        dangers.append(square + 9)
            elif piece == 'wK' or piece == 'bK':
                for square in self.coordinate(board, piece):
                    dangers.extend(self.brave_king(board, square))
            else:
                for square in self.coordinate(board, piece):
                    for piece_type in self.pieceType:
                        if piece in self.pieceType[piece_type]:
                            piece = piece_type
                    dangers.extend(getattr(Prep, piece)(self, board, square))
            for square in dangers:  # prevent duplicates
                if square not in squares:
                    squares.append(square)
        return squares

    def king(self, board, start):
        """This method generates king's legal squares."""
        squares = []
        for square in self.brave_king(board, start):
            if square not in self.danger(board, start):
                squares.append(square)
        return squares

    def legal(self, board, start):
        """This method combines legal squares for the specify piece."""
        squares = []
        for piece in self.pieceType:
            if board[start] in self.pieceType[piece]:
                squares.extend(getattr(Prep, piece)(self, board, start))
        return squares
