import pygame
from prep import Prep


FPS = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SQUARE_WIDTH = WINDOW_WIDTH // 8
SQUARE_HEIGHT = WINDOW_HEIGHT // 8


class Game(Prep):
    """The class for chess games."""

    result = []

    def __init__(self):
        super().__init__()
        self.move = []
        self.highlights = []
        self.promote = None
        self.promotion_choices = []
        self.game_state = {'w': {'checkmate': False, 'stalemate': False},
                           'b': {'checkmate': False, 'stalemate': False}}

        self.chess_font = pygame.font.Font('chess_font.ttf', 86)
        self.piece_symbol = {'wP': '\u2659', 'wR': '\u2656', 'wN': '\u2658',
                             'wB': '\u2657', 'wQ': '\u2655', 'wK': '\u2654',
                             'bP': '\u265F', 'bR': '\u265C', 'bN': '\u265E',
                             'bB': '\u265D', 'bQ': '\u265B', 'bK': '\u265A'}

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    @staticmethod
    def get_area(square):
        """Return the coordinates and dimensions of a square."""
        return (SQUARE_WIDTH * (square % 8), SQUARE_HEIGHT * (square // 8),
                SQUARE_WIDTH, SQUARE_HEIGHT)

    @staticmethod
    def get_square():
        """Convert the click position to square coordinates."""
        return (pygame.mouse.get_pos()[0] // SQUARE_WIDTH +
                pygame.mouse.get_pos()[1] // SQUARE_HEIGHT * 8)

    def update_en_passant(self, start, target):
        """Update the en passant status for the game."""
        if self.en_passant:
            # capture the enemy pawn
            if self.board[start] == 'wP':
                if target + 8 == self.en_passant:
                    self.piece_coordinate['bP'].remove(target + 8)
                    self.board[target + 8] = '00'
            elif self.board[start] == 'bP':
                if target - 8 == self.en_passant:
                    self.piece_coordinate['wP'].remove(target - 8)
                    self.board[target - 8] = '00'

        # en passant capture must be made on the very next turn
        self.en_passant = None

        # check if a pawn moves forward two squares
        if abs(start - target) == 16 and \
                self.board[start] == 'wP' or self.board[start] == 'bP':
            self.en_passant = target

    def update_castle(self, start, target):
        """Update the castle status for the game."""
        if self.board[start][1] == 'K':
            # reposition the rook after castling
            if target == start - 2:
                self.piece_coordinate[self.turn + 'R'].remove(start - 4)
                self.piece_coordinate[self.turn + 'R'].add(start - 1)
                self.board[start - 4] = '00'
                self.board[start - 1] = self.turn + 'R'
            elif target == start + 2:
                self.piece_coordinate[self.turn + 'R'].remove(start + 3)
                self.piece_coordinate[self.turn + 'R'].add(start + 1)
                self.board[start + 3] = '00'
                self.board[start + 1] = self.turn + 'R'

            # can't castle if the king has previously moved
            self.castle_flags[self.turn]['long'] = False
            self.castle_flags[self.turn]['short'] = False

        # check if the rook involved has moved or got captured
        if start == 0 or target == 0:
            self.castle_flags['b']['long'] = False
        if start == 7 or target == 7:
            self.castle_flags['b']['short'] = False
        if start == 56 or target == 56:
            self.castle_flags['w']['long'] = False
        if start == 63 or target == 63:
            self.castle_flags['w']['short'] = False

    def update_pawn_promotion(self, target, symbol):
        """Update the pawn promotion status for the game."""
        if symbol:  # update pawn promotions
            self.piece_coordinate[self.board[target]].remove(target)
            self.piece_coordinate[symbol].add(target)
            self.board[target] = symbol
            self.promote = None
        for square in range(8):
            # check if one of the white pawns gets to eighth rank
            if self.board[square] == 'wP':
                self.promote = square
                break
            # check if one of the black pawns gets to first rank
            elif self.board[square + 56] == 'bP':
                self.promote = square + 56
                break

    def update_game_state(self):
        """Determine whether the king gets checkmated or stalemated."""
        symbol_index = 0 if self.turn == 'w' else 1
        # check whether there are any legal moves
        for symbols in self.piece_type.values():
            for square in self.piece_coordinate[symbols[symbol_index]]:
                if self.legal(square):
                    return
        if self.is_attacked(self.board, self.turn):
            self.game_state[self.turn]['checkmate'] = True
        else:
            self.game_state[self.turn]['stalemate'] = True

    def update_game(self, start, target, symbol=''):
        """Update the chess board and game elements."""
        if start != target:
            self.update_en_passant(start, target)
            self.update_castle(start, target)
            # update the pieces coordinates set
            self.piece_coordinate[self.board[start]].remove(start)
            self.piece_coordinate[self.board[start]].add(target)
            if self.board[target] != '00':  # whether it's a capture
                self.piece_coordinate[self.board[target]].remove(target)
            # update chess board
            self.board[target] = self.board[start]
            self.board[start] = '00'
            # update the player turn
            self.turn = 'b' if self.turn == 'w' else 'w'
        self.update_pawn_promotion(target, symbol)
        self.update_game_state()

    def draw_piece(self, piece, square):
        """Draw chess piece on the specific square."""
        symbol = self.piece_symbol[piece]
        area = list(self.get_area(square))[:2]
        for area_index in range(2):  # center the piece symbol
            square_size = (SQUARE_WIDTH, SQUARE_HEIGHT)
            area[area_index] += (square_size[area_index] -
                                 self.chess_font.size(symbol)[area_index]) // 2
        self.window.blit(self.chess_font.render(symbol, True, (0, 0, 0)), area)

    def draw_highlight(self, square, color):
        """Highlight the specific square."""
        pygame.draw.rect(self.window, color, self.get_area(square))
        if self.board[square] != '00':
            self.draw_piece(self.board[square], square)

    def draw_board(self):
        """Draw the chess board and pieces."""
        colors = [(220, 230, 230), (120, 150, 170)]
        # light square RGB: 220, 230, 230; dark square RGB: 120, 150, 170
        for square in range(64):
            if (square // 8) % 2 == 0:  # first squares on odd ranks are light
                color = colors[square % 2]
            else:  # first squares on even ranks are dark
                color = colors[(square + 1) % 2]
            pygame.draw.rect(self.window, color, self.get_area(square))
        for symbol, squares in self.piece_coordinate.items():
            for square in squares:
                self.draw_piece(symbol, square)

        # highlight checks
        king_square = next(iter(self.piece_coordinate[self.turn + 'K']))
        if self.is_attacked(self.board, self.turn, king_square):
            self.draw_highlight(king_square, (255, 100, 130))

        if self.promote:  # draw a window for pawn promotion prompt
            promote_window = pygame.Surface((SQUARE_WIDTH, WINDOW_HEIGHT // 2))
            promote_window.fill((225, 225, 225))
            square = self.promote
            if self.board[self.promote] == 'wP':  # white pawn promotion prompt
                self.promotion_choices = ['wQ', 'wB', 'wN', 'wR']
            else:  # black pawn promotion prompt
                square -= 24
                self.promotion_choices = ['bR', 'bN', 'bB', 'bQ']
            self.window.blit(promote_window, self.get_area(square)[:2])
            for index, symbol in enumerate(self.promotion_choices):
                self.draw_piece(symbol, square + 8 * index)

    def make_move(self):
        """Make chess move based on click inputs."""
        square = self.get_square()
        if not self.move:  # handles the start square of a chess move
            if self.board[square][0] == self.turn:
                self.move.append(square)
                self.draw_highlight(self.move[0], (200, 200, 255))
                for square in self.legal(self.move[0]):
                    self.draw_highlight(square, (100, 190, 150))
                return
        else:  # handles the target square of a chess move
            self.move.append(square)
            if self.move[1] in self.legal(self.move[0]):
                self.update_game(self.move[0], self.move[1])
        self.draw_board()
        self.move.clear()

    def pawn_promotion(self):
        """Handle pawn promotions."""
        square, symbol = self.get_square(), ''
        if self.board[self.promote] == 'wP':  # handles white pawn promotions
            if square % 8 == self.promote and square // 8 <= 3:
                symbol = self.promotion_choices[square // 8]
        else:  # handles black pawn promotions
            if square % 8 == self.promote - 56 and square // 8 >= 4:
                symbol = self.promotion_choices[square // 8 - 4]
        self.update_game(self.promote, self.promote, symbol)
        self.draw_board()

    def click(self, event):
        """Handle mouse clicks."""
        if event.button == 1:  # left click
            self.highlights.clear()
            self.draw_board()
            self.make_move() if self.promote is None else self.pawn_promotion()
        elif event.button == 3:  # right click
            self.draw_board()
            if self.get_square() not in self.highlights:
                self.highlights.append(self.get_square())
            else:
                self.highlights.remove(self.get_square())
            for square in self.highlights:
                self.draw_highlight(square, (220, 80, 20))

    def play(self):
        """Take user inputs, draw and update the chess board."""
        Game.result = []
        self.draw_board()
        while True:
            self.clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event)
            if self.game_state[self.turn]['checkmate'] or \
                    self.game_state[self.turn]['stalemate']:  # get results
                victor = 'black' if self.turn == 'w' else 'white'
                Game.result = [victor, self.game_state[self.turn]]
                return True


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('chess')
    Game().play()
