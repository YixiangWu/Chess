class Prep:
    """This class prepares chess games."""

    def __init__(self):
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
    def coordinate(board, symbol):
        """This method returns the coordinates of specific piece(s)."""
        squares = []
        for square in range(64):
            if board[square] == symbol:
                squares.append(square)
        return squares

    def pawn(self, board, start, en_passant):
        """This method generates pawn's legal squares."""
        squares = []
        if board[start] in self.pieceColor['white']:
            if board[start - 8] == '00':
                squares.append(start - 8)
                if board[start - 16] == '00' and start // 8 == 6:
                    # pawns can move forward two squares on their first move.
                    squares.append(start - 16)
            if start % 8 != 0 and board[start - 9] in self.pieceColor['black']:
                squares.append(start - 9)
            if start % 8 != 7 and board[start - 7] in self.pieceColor['black']:
                squares.append(start - 7)
        else:
            if board[start + 8] == '00':
                squares.append(start + 8)
                if board[start + 16] == '00' and start // 8 == 1:
                    # pawns can move forward two squares on their first move.
                    squares.append(start + 16)
            if start % 8 != 0 and board[start + 7] in self.pieceColor['white']:
                squares.append(start + 7)
            if start % 8 != 7 and board[start + 9] in self.pieceColor['white']:
                squares.append(start + 9)
        if start - 1 == en_passant or start + 1 == en_passant:  # en passant
            if start // 8 == 3:
                squares.append(en_passant - 8)
            elif start // 8 == 4:
                squares.append(en_passant + 8)
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

    def queen(self, board, start):
        """This method generates queen's legal squares."""
        return self.rook(board, start) + self.bishop(board, start)

    @staticmethod
    def brave_king(start):
        """This method generates every king's squares."""
        squares = []
        for square in [start - 8, start + 8]:
            if 0 <= square <= 63:
                squares.append(square)
        if start % 8 != 0:
            for square in [start - 9, start - 1, start + 7]:
                if 0 <= square <= 63:
                    squares.append(square)
        if start % 8 != 7:
            for square in [start - 7, start + 1, start + 9]:
                if 0 <= square <= 63:
                    squares.append(square)
        return squares

    def dangerous_square(self, board, square):
        """This method helps generate dangerous squares for the king."""
        squares = []
        if board[square] == 'wP':
            if square % 8 != 0:
                squares.append(square - 9)
            if square % 8 != 7:
                squares.append(square - 7)
            return squares
        elif board[square] == 'bP':
            if square % 8 != 0:
                squares.append(square + 7)
            if square % 8 != 7:
                squares.append(square + 9)
            return squares
        elif board[square] == 'wK' or board[square] == 'bK':
            return self.brave_king(square)
        else:
            for piece in self.pieceType:
                if board[square] in self.pieceType[piece]:
                    return getattr(Prep, piece)(self, board, square)

    def danger(self, board, start, color=None):
        """This method generates dangerous squares for the king."""
        squares, temp, copy = [], {}, board[:]
        if color is None:
            color = 'black' if board[start] == 'wK' else 'white'
        # Since moving a piece to a square occupied by a piece of the same
        # color is illegal, there are cases that the opponent's piece around
        # the king is guarded, but the square occupied by this piece is not
        # marked as a dangerous square. Turn every opponent's pieces around the
        # king into opposite-color can resolve this problem.
        for square in self.brave_king(start):
            if self.color(copy, start, square):
                temp[square] = copy[square]
                copy[square] = 'bP' if color == 'white' else 'wP'
        copy[start] = '00'

        for symbol in self.pieceColor[color]:
            for square in self.coordinate(copy, symbol):
                for danger in self.dangerous_square(copy, square):
                    if danger not in squares:  # prevent duplicates
                        squares.append(danger)

        for square in temp:
            temp_copy = copy[:]
            temp_copy[square] = temp[square]
            for danger in self.dangerous_square(temp_copy, square):
                if danger not in squares:  # prevent duplicates
                    squares.append(danger)
        return squares

    def castle(self, board, start, condition):
        """This method generates king's legal squares for castling."""
        squares = []
        color = 'black' if board[start] == 'wK' else 'white'
        if start not in self.danger(board, start):
            if condition['long']:  # long castle
                for square in range(start - 3, start):
                    if board[square] != '00':
                        # squares between king and rook involved are unoccupied
                        break
                    elif square in self.danger(board, square, color):
                        # king cannot cross over nor end on squares
                        # that are attacked by an enemy piece
                        if square == start - 3:
                            continue
                        else:
                            break
                    if square == start - 1:
                        squares.append(start - 2)
            if condition['short']:  # short castle
                for square in range(start + 1, start + 3):
                    if board[square] != '00' or square in \
                            self.danger(board, square, color):
                        break
                    if square == start + 2:
                        squares.append(start + 2)
        return squares

    def king(self, board, start, condition):
        """This method generates king's legal squares."""
        squares = self.castle(board, start, condition)
        for square in self.brave_king(start):
            if board[square] == '00' or self.color(board, start, square):
                if square not in self.danger(board, start):
                    squares.append(square)
        return squares

    def legal(self, board, start, castle, en_passant):
        """This method combines legal squares for the specify piece."""
        for piece in self.pieceType:
            if board[start] in self.pieceType['pawn']:
                return self.pawn(board, start, en_passant)
            elif board[start] in self.pieceType['king']:
                return self.king(board, start, castle)
            elif board[start] in self.pieceType[piece]:
                return getattr(Prep, piece)(self, board, start)
