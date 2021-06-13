import pygame
from prep import Prep


class Game(Prep):
    """This class runs chess games with a graphical user interface."""

    board = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR',
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
    #          56,   57,   58,   59,   60,   61,   62,   63
    #          a1,   b1,   c1,   d1,   e1,   f1,   g1,   h1

    move = []
    highlights = []
    turn = 'white'
    promote = None
    en_passant = None
    castle_flags = {'white': {'long': True, 'short': True},
                    'black': {'long': True, 'short': True}}

    def __init__(self):
        super().__init__()
        self.windowSize = (800, 800)
        self.squareSize = (self.windowSize[0] // 8, self.windowSize[1] // 8)
        self.window = pygame.display.set_mode(self.windowSize)
        self.images = self.load()
        self.main()

    def get_area(self, square):
        """This method returns the position and dimensions of a square."""
        return (self.squareSize[0] * (square % 8),
                self.squareSize[1] * (square // 8),
                self.squareSize[0], self.squareSize[1])

    def get_square(self):
        """This method turns the click position to a square location."""
        return (pygame.mouse.get_pos()[0] // self.squareSize[0] +
                pygame.mouse.get_pos()[1] // self.squareSize[1] * 8)

    @classmethod
    def update_move(cls, square):
        """This method updates chess moves."""
        cls.move.clear() if square is None else cls.move.append(square)

    @classmethod
    def update_highlights(cls, square):
        """This method updates right-click highlights."""
        if square is None:
            cls.highlights.clear()
        elif square in cls.highlights:
            cls.highlights.remove(square)
        else:
            cls.highlights.append(square)

    @classmethod
    def update_en_passant(cls, start, target):
        """This method helps update the chess board and game elements."""
        if cls.en_passant:
            # capture the enemy pawn
            if cls.board[start] == 'wP':
                if target + 8 == cls.en_passant:
                    cls.board[target + 8] = '00'
            elif cls.board[start] == 'bP':
                if target - 8 == cls.en_passant:
                    cls.board[target - 8] = '00'

        # en passant capture must be made on the very next turn
        cls.en_passant = None

        # check if a pawn moves forward two squares
        if cls.board[start] == 'wP' and start - target == 16:
            cls.en_passant = target
        elif cls.board[start] == 'bP' and target - start == 16:
            cls.en_passant = target

    @classmethod
    def update_castle(cls, start, target):
        """This method helps update the chess board and game elements."""
        if cls.board[start] == 'wK' or cls.board[start] == 'bK':
            rook = 'wR' if cls.board[start] == 'wK' else 'bR'
            # reposition the rook after castling
            if target == start - 2:
                cls.board[start - 4] = '00'
                cls.board[start - 1] = rook
            elif target == start + 2:
                cls.board[start + 3] = '00'
                cls.board[start + 1] = rook

            # can't castle if the king has previously moved
            cls.castle_flags[cls.turn]['long'] = False
            cls.castle_flags[cls.turn]['short'] = False

        # check if the rook involved has moved or got captured
        if start == 0 or target == 0:
            cls.castle_flags['black']['long'] = False
        if start == 7 or target == 7:
            cls.castle_flags['black']['short'] = False
        if start == 56 or target == 56:
            cls.castle_flags['white']['long'] = False
        if start == 63 or target == 63:
            cls.castle_flags['white']['short'] = False

    @classmethod
    def update_game(cls, start, target, symbol=''):
        """This method updates the chess board and game elements."""
        if start != target:
            cls.update_en_passant(start, target)
            cls.update_castle(start, target)
            cls.board[target] = cls.board[start]
            cls.board[start] = '00'
            cls.turn = 'black' if cls.turn == 'white' else 'white'
        if symbol:  # update pawn promotions
            cls.board[target] = symbol
        for i in range(8):
            # check if one of the white pawns gets to eighth rank
            if cls.board[i] == 'wP':
                cls.promote = i
                break
            # check if one of the black pawns gets to first rank
            elif cls.board[56 + i] == 'bP':
                cls.promote = 56 + i
                break
            cls.promote = None

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

    def draw(self):
        """This method draws the chess board and pieces."""
        colors = [(220, 230, 230), (120, 150, 170)]
        # light square RGB: 220, 230, 230; dark square RGB: 120, 150, 170
        for square in range(64):
            piece = Game.board[square]
            if (square // 8) % 2 == 0:  # first squares on odd ranks are light
                color = colors[square % 2]
            else:  # first squares on even ranks are dark
                color = colors[(square + 1) % 2]
            pygame.draw.rect(self.window, color, self.get_area(square))
            if piece != '00':
                self.window.blit(self.images[piece], self.get_area(square))
        if Game.promote:  # draw a window for pawn promotion prompt
            promote_window = pygame.Surface(
                (self.squareSize[0], self.windowSize[1] // 2))
            promote_window.fill((225, 225, 225))
            color = 'white' if Game.board[Game.promote] == 'wP' else 'black'
            square = Game.promote if color == 'white' else Game.promote - 24
            choices = self.pieceColor[color][1:5]  # promotion choices
            if color == 'white':
                choices = reversed(choices)
            self.window.blit(promote_window, self.get_area(square)[:2])
            for index, symbol in enumerate(choices):
                self.window.blit(self.images[symbol],
                                 self.get_area(square + 8 * index))

    def highlight(self, square, color):
        """This method highlights the specify square."""
        symbol = Game.board[square]
        pygame.draw.rect(self.window, color, self.get_area(square))
        if symbol != '00':
            self.window.blit(self.images[symbol], self.get_area(square))

    def make_move(self):
        """This method makes chess moves."""
        square = self.get_square()
        castle, passant = Game.castle_flags[Game.turn], Game.en_passant
        if not Game.move:  # handles the start square of a chess move
            if Game.board[square] in self.pieceColor[Game.turn]:
                Game.update_move(square)
                start = Game.move[0]
                self.highlight(start, (200, 200, 255))
                for square in self.legal(Game.board, start, castle, passant):
                    self.highlight(square, (100, 190, 150))
                return
        else:  # handles the target square of a chess move
            Game.update_move(square)
            start, target = Game.move
            if target in self.legal(Game.board, start, castle, passant):
                Game.update_game(start, target)
        self.draw()
        Game.update_move(None)

    def pawn_promotion(self):
        """This method handles pawn promotions."""
        square, symbol = self.get_square(), ''
        if Game.board[Game.promote] == 'wP':  # handles white pawn promotions
            if square % 8 == Game.promote and square // 8 <= 3:
                symbol = self.pieceColor['white'][4 - square // 8]
        else:  # handles black pawn promotions
            if square % 8 == Game.promote - 56 and square // 8 >= 4:
                symbol = self.pieceColor['black'][square // 8 - 3]
        Game.update_game(Game.promote, Game.promote, symbol)
        self.draw()

    def click(self, event):
        """This method handles mouse clicks."""
        if event.button == 1:  # left click
            self.update_highlights(None)
            self.make_move() if Game.promote is None else self.pawn_promotion()
        elif event.button == 3:  # right click
            self.draw()
            self.update_highlights(self.get_square())
            for square in Game.highlights:
                # highlight right clicks with RGB 255, 100, 130
                self.highlight(square, (255, 100, 130))

    def main(self):
        """This method takes user inputs, draws and updates the chess board."""
        pygame.init()
        pygame.display.set_caption('chess')
        self.draw()
        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event)


if __name__ == '__main__':
    Game()
