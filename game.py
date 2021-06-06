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

    elements = {'turn': 'white', 'en_passant': 99,
                'castle': {'white': {'long': True, 'short': True},
                           'black': {'long': True, 'short': True}}}

    def __init__(self):
        super().__init__()
        self.windowSize = (800, 800)
        self.squareSize = (self.windowSize[0] // 8, self.windowSize[1] // 8)
        self.main()

    def get_area(self, square):
        """This method returns the position and dimensions of a square."""
        return (self.squareSize[0] * (square % 8),
                self.squareSize[1] * (square // 8),
                self.squareSize[0], self.squareSize[1])

    @classmethod
    def update_en_passant(cls, start, target):
        """This method helps update the chess board and game elements."""
        if cls.elements['en_passant'] != 99:
            # capture the enemy pawn
            if cls.board[start] == 'wP':
                if target + 8 == cls.elements['en_passant']:
                    cls.board[target + 8] = '00'
            elif cls.board[start] == 'bP':
                if target - 8 == cls.elements['en_passant']:
                    cls.board[target - 8] = '00'

        # en passant capture must be made on the very next turn
        cls.elements['en_passant'] = 99

        # check if a pawn moves forward two squares
        if cls.board[start] == 'wP' and start - target == 16:
            cls.elements['en_passant'] = target
        elif cls.board[start] == 'bP' and target - start == 16:
            cls.elements['en_passant'] = target

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
            cls.elements['castle'][cls.elements['turn']]['long'] = False
            cls.elements['castle'][cls.elements['turn']]['short'] = False

        # check if the rook involved has moved or got captured
        if start == 0 or target == 0:
            cls.elements['castle']['black']['long'] = False
        if start == 7 or target == 7:
            cls.elements['castle']['black']['short'] = False
        if start == 56 or target == 56:
            cls.elements['castle']['white']['long'] = False
        if start == 63 or target == 63:
            cls.elements['castle']['white']['short'] = False

    @classmethod
    def update(cls, start=64, target=64):
        """This method updates the chess board and game elements."""
        if start != target:
            cls.update_en_passant(start, target)
            cls.update_castle(start, target)
            cls.board[target] = cls.board[start]
            cls.board[start] = '00'
            if cls.elements['turn'] == 'white':
                cls.elements['turn'] = 'black'
            else:
                cls.elements['turn'] = 'white'
        return cls.board, cls.elements

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

    def draw(self, window, board, images):
        """This method draws the chess board and pieces."""
        colors = [(220, 230, 230), (120, 150, 170)]
        # light square RGB: 220, 230, 230; dark square RGB: 120, 150, 170
        for square in range(64):
            piece = board[square]
            if (square // 8) % 2 == 0:  # first squares on odd ranks are light
                color = colors[square % 2]
            else:  # first squares on even ranks are dark
                color = colors[(square + 1) % 2]
            pygame.draw.rect(window, color, self.get_area(square))
            if piece != '00':
                window.blit(images[piece], self.get_area(square))

    def highlight(self, window, board, images, square, castle, en_passant):
        """This method highlights the selected square and its legal squares."""
        pygame.draw.rect(window, (200, 200, 255), self.get_area(square))
        # highlight the selected square with RGB 200, 200, 255
        window.blit(images[board[square]], self.get_area(square))
        for square in self.legal(board, square, castle, en_passant):
            pygame.draw.rect(window, (255, 100, 130), self.get_area(square))
            # highlight legal squares with RGB 255, 100, 130
            if board[square] != '00':
                window.blit(images[board[square]], self.get_area(square))

    def click(self, window, board, images, squares, elements):
        """This method handles mouse clicks."""
        square = pygame.mouse.get_pos()[0] // self.squareSize[0] + \
            pygame.mouse.get_pos()[1] // self.squareSize[1] * 8
        castle = elements['castle'][elements['turn']]
        passant = elements['en_passant']
        squares.append(square)
        if len(squares) == 1:
            start = squares[0]
            if board[start] in self.pieceColor[elements['turn']]:
                self.highlight(window, board, images, start, castle, passant)
                return squares, elements
        else:
            start, target = squares
            if target in self.legal(board, start, castle, passant):
                board, elements = Game.update(start, target)
        self.draw(window, board, images)
        return [], elements

    def main(self):
        """This method takes user inputs, draws and updates the chess board."""
        pygame.init()
        pygame.display.set_caption('chess')
        window = pygame.display.set_mode(self.windowSize)
        board, elements = Game.update()
        images = self.load()
        squares = []
        self.draw(window, board, images)
        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    squares, elements = self.click(
                        window, board, images, squares, elements)


if __name__ == '__main__':
    Game()
