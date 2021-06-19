import pygame
from prep import Prep


class Game(Prep):
    """This class runs the chess game."""

    def __init__(self):
        super().__init__()
        self.board = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR',
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
        #               56,   57,   58,   59,   60,   61,   62,   63
        #               a1,   b1,   c1,   d1,   e1,   f1,   g1,   h1

        self.turn = 'white'
        self.promote = None
        self.en_passant = None
        self.castle_flags = {'white': {'long': True, 'short': True},
                             'black': {'long': True, 'short': True}}
        self.game_state = {'white': {'checkmate': False, 'stalemate': False},
                           'black': {'checkmate': False, 'stalemate': False}}

        self.move = []
        self.highlights = []

        self.windowSize = (800, 800)
        self.squareSize = (self.windowSize[0] // 8, self.windowSize[1] // 8)
        self.window = pygame.display.set_mode(self.windowSize)
        self.images = self.load()

    def get_area(self, square):
        """This method returns the position and dimensions of a square."""
        return (self.squareSize[0] * (square % 8),
                self.squareSize[1] * (square // 8),
                self.squareSize[0], self.squareSize[1])

    def get_square(self):
        """This method turns the click position to a square location."""
        return (pygame.mouse.get_pos()[0] // self.squareSize[0] +
                pygame.mouse.get_pos()[1] // self.squareSize[1] * 8)

    def update_move(self, square):
        """This method updates chess moves."""
        self.move.clear() if square is None else self.move.append(square)

    def update_highlights(self, square):
        """This method updates right-click highlights."""
        if square is None:
            self.highlights.clear()
        elif square in self.highlights:
            self.highlights.remove(square)
        else:
            self.highlights.append(square)

    def update_en_passant(self, start, target):
        """This method helps update the chess board and game elements."""
        if self.en_passant:
            # capture the enemy pawn
            if self.board[start] == 'wP':
                if target + 8 == self.en_passant:
                    self.board[target + 8] = '00'
            elif self.board[start] == 'bP':
                if target - 8 == self.en_passant:
                    self.board[target - 8] = '00'

        # en passant capture must be made on the very next turn
        self.en_passant = None

        # check if a pawn moves forward two squares
        if self.board[start] == 'wP' and start - target == 16:
            self.en_passant = target
        elif self.board[start] == 'bP' and target - start == 16:
            self.en_passant = target

    def update_castle(self, start, target):
        """This method helps update the chess board and game elements."""
        if self.board[start] == 'wK' or self.board[start] == 'bK':
            rook = 'wR' if self.board[start] == 'wK' else 'bR'
            # reposition the rook after castling
            if target == start - 2:
                self.board[start - 4] = '00'
                self.board[start - 1] = rook
            elif target == start + 2:
                self.board[start + 3] = '00'
                self.board[start + 1] = rook

            # can't castle if the king has previously moved
            self.castle_flags[self.turn]['long'] = False
            self.castle_flags[self.turn]['short'] = False

        # check if the rook involved has moved or got captured
        if start == 0 or target == 0:
            self.castle_flags['black']['long'] = False
        if start == 7 or target == 7:
            self.castle_flags['black']['short'] = False
        if start == 56 or target == 56:
            self.castle_flags['white']['long'] = False
        if start == 63 or target == 63:
            self.castle_flags['white']['short'] = False

    def update_game(self, start, target, symbol=''):
        """This method updates the chess board and game elements."""
        if start != target:
            self.update_en_passant(start, target)
            self.update_castle(start, target)
            self.board[target] = self.board[start]
            self.board[start] = '00'
            self.turn = 'black' if self.turn == 'white' else 'white'
        if symbol:  # update pawn promotions
            self.board[target] = symbol
        for i in range(8):
            # check if one of the white pawns gets to eighth rank
            if self.board[i] == 'wP':
                self.promote = i
                break
            # check if one of the black pawns gets to first rank
            elif self.board[56 + i] == 'bP':
                self.promote = 56 + i
                break
            self.promote = None

    def update_game_state(self, castle, en_passant):
        """This method determines if the king gets checkmated or stalemated."""
        king = 'wK' if self.turn == 'white' else 'bK'
        square = self.coordinate(self.board, king).pop()
        if self.is_check(self.board, self.turn):
            if not self.king(self.board, square, castle) and \
                    not self.escape(self.board, self.turn, castle, en_passant):
                self.game_state[self.turn]['checkmate'] = True
        elif not self.all_legals(self.board, self.turn, castle, en_passant):
            self.game_state[self.turn]['stalemate'] = True

    def load(self):
        """This method loads piece images."""
        images = {}
        for color in self.pieceColor:
            for piece in self.pieceType:
                path = ('images/' + color + '_' + piece + '.png')
                # name example: white_rook.png
                piece = set(self.pieceType[piece]). \
                    intersection(self.pieceColor[color]).pop()
                img = pygame.image.load(path)
                images[piece] = pygame.transform.scale(img, self.squareSize)
        return images

    def draw_board(self):
        """This method draws the chess board and pieces."""
        colors = [(220, 230, 230), (120, 150, 170)]
        # light square RGB: 220, 230, 230; dark square RGB: 120, 150, 170
        for square in range(64):
            piece = self.board[square]
            if (square // 8) % 2 == 0:  # first squares on odd ranks are light
                color = colors[square % 2]
            else:  # first squares on even ranks are dark
                color = colors[(square + 1) % 2]
            pygame.draw.rect(self.window, color, self.get_area(square))
            if piece != '00':
                self.window.blit(self.images[piece], self.get_area(square))
        if self.promote:  # draw a window for pawn promotion prompt
            promote_window = pygame.Surface(
                (self.squareSize[0], self.windowSize[1] // 2))
            promote_window.fill((225, 225, 225))
            color = 'white' if self.board[self.promote] == 'wP' else 'black'
            square = self.promote if color == 'white' else self.promote - 24
            choices = self.pieceColor[color][1:5]  # promotion choices
            if color == 'white':
                choices = reversed(choices)
            self.window.blit(promote_window, self.get_area(square)[:2])
            for index, symbol in enumerate(choices):
                self.window.blit(self.images[symbol],
                                 self.get_area(square + 8 * index))

    def highlight(self, square, color):
        """This method highlights the specify square."""
        symbol = self.board[square]
        pygame.draw.rect(self.window, color, self.get_area(square))
        if symbol != '00':
            self.window.blit(self.images[symbol], self.get_area(square))

    def make_move(self):
        """This method makes chess moves."""
        square = self.get_square()
        castle, passant = self.castle_flags[self.turn], self.en_passant
        if not self.move:  # handles the start square of a chess move
            if self.board[square] in self.pieceColor[self.turn]:
                self.update_move(square)
                start = self.move[0]
                self.highlight(start, (200, 200, 255))
                for square in self.legal(self.board, start, castle, passant):
                    self.highlight(square, (100, 190, 150))
                return
        else:  # handles the target square of a chess move
            self.update_move(square)
            start, target = self.move
            if target in self.legal(self.board, start, castle, passant):
                self.update_game(start, target)
                self.update_game_state(castle, passant)
        self.draw_board()
        self.update_move(None)

    def pawn_promotion(self):
        """This method handles pawn promotions."""
        square, symbol = self.get_square(), ''
        if self.board[self.promote] == 'wP':  # handles white pawn promotions
            if square % 8 == self.promote and square // 8 <= 3:
                symbol = self.pieceColor['white'][4 - square // 8]
        else:  # handles black pawn promotions
            if square % 8 == self.promote - 56 and square // 8 >= 4:
                symbol = self.pieceColor['black'][square // 8 - 3]
        self.update_game(self.promote, self.promote, symbol)
        self.draw_board()

    def click(self, event):
        """This method handles mouse clicks."""
        if event.button == 1:  # left click
            self.update_highlights(None)
            self.make_move() if self.promote is None else self.pawn_promotion()
        elif event.button == 3:  # right click
            self.draw_board()
            self.update_highlights(self.get_square())
            for square in self.highlights:
                # highlight right clicks with RGB 255, 100, 130
                self.highlight(square, (255, 100, 130))

    def play(self):
        """This method takes user inputs, draws and updates the chess board."""
        self.draw_board()
        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('chess')
    Game().play()
