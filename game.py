from copy import deepcopy
import pygame
from prep import Log, prep, Setup


FPS = 30

# SIZE CONSTANTS
WINDOW_WIDTH = 800
SIDEBAR_WIDTH = WINDOW_WIDTH * 2 // 10
BOARD_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_WIDTH
SQUARE_WIDTH = BOARD_WIDTH // 8
SQUARE_HEIGHT = WINDOW_HEIGHT // 8
PIECE_SIZE = BOARD_WIDTH // 9
NOTATION_SIZE = BOARD_WIDTH // 50
SIDEBAR_LOG_LINE_SPACING = WINDOW_HEIGHT // 32

# COLOR TUPLES
BLACK = (0, 0, 0)
SIDEBAR_COLOR = (110, 95, 125)
BACKGROUND_COLOR = (215, 215, 215)
LIGHT_SQUARE = (220, 230, 230)
DARK_SQUARE = (120, 150, 170)
IN_CHECK_HIGHLIGHT = (255, 100, 130)
PIECE_SELECTED_HIGHLIGHT = (200, 200, 255)
LEGAL_SQUARE_HIGHLIGHT = (100, 190, 150)
RIGHT_CLICK_HIGHLIGHT = (220, 80, 20)


class Game(Setup, Log):
    """The class for chess games."""

    result = []

    def __init__(self):
        Setup.__init__(self)
        Log.__init__(self)
        self.move = []
        self.promote = None
        self.promotion_choices = []

        self.highlights = []
        self.rewind_dict = {}
        self.castle_flags_for_undoes = {'w': {}, 'b': {}}

        self.chess_font = pygame.font.Font('chess_font.ttf', PIECE_SIZE)
        self.notation_font = pygame.font.Font('chess_font.ttf', NOTATION_SIZE)
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
        if abs(start - target) == 16 and (self.board[start][1] == 'P'):
            self.en_passant = target

    def update_castle(self, start, target):
        """Update the castle status for the game."""
        if self.board[start][1] == 'K':
            if target == start + 2:  # if short castled
                # reposition the rook after castling
                self.piece_coordinate[self.turn + 'R'].remove(start + 3)
                self.piece_coordinate[self.turn + 'R'].append(start + 1)
                self.board[start + 3] = '00'
                self.board[start + 1] = self.turn + 'R'
            elif target == start - 2:  # if long castled
                # reposition the rook after castling
                self.piece_coordinate[self.turn + 'R'].remove(start - 4)
                self.piece_coordinate[self.turn + 'R'].append(start - 1)
                self.board[start - 4] = '00'
                self.board[start - 1] = self.turn + 'R'

            # save the current castle flags in case of undoing castling
            self.castle_flags_for_undoes[self.turn][str(len(
                self.game_log))] = deepcopy(self.castle_flags[self.turn])
            # can't castle if the king has previously moved
            self.castle_flags[self.turn]['short'] = False
            self.castle_flags[self.turn]['long'] = False

        # check if the rook involved has moved or got captured
        if start in {0, 7, 56, 63} or target in {0, 7, 56, 63}:
            # save the current castle flags in case of undoing castling
            self.castle_flags_for_undoes[self.turn][str(len(
                self.game_log))] = deepcopy(self.castle_flags[self.turn])
            if start == 0 or target == 0:
                self.castle_flags['b']['long'] = False
            if start == 7 or target == 7:
                self.castle_flags['b']['short'] = False
            if start == 56 or target == 56:
                self.castle_flags['w']['long'] = False
            if start == 63 or target == 63:
                self.castle_flags['w']['short'] = False

    def update_pawn_promotion(self, target, symbol=''):
        """Update the pawn promotion status for the game."""
        if symbol:  # update pawn promotions
            self.piece_coordinate[self.board[target]].remove(target)
            self.piece_coordinate[symbol].append(target)
            self.board[target] = symbol
            # update the promote information to the logs
            self.game_log[-1] += '=' + symbol
            self.san[-1] += '=' + symbol[1]
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

    def update_game_result(self):
        """Determine the result of chess games."""
        # check whether there are any legal moves
        verifying_squares = []
        for symbol in self.piece_coordinate:
            if symbol[0] == self.turn:
                verifying_squares.extend(self.piece_coordinate[symbol])
        for square in verifying_squares:
            if self.legal(square):
                break
        else:
            # determine whether the king gets checkmated or stalemated
            if self.is_attacked(self.board, self.turn):
                victor = 'black' if self.turn == 'w' else 'white'
                Game.result = [victor + ' wins', 'by checkmate']
                return
            else:
                Game.result = ['draw', 'by stalemate']
                return

        # check the possibility of checkmate
        if len(self.piece_coordinate['wB']) + \
                len(self.piece_coordinate['wN']) <= 1 and \
                len(self.piece_coordinate['bB']) + \
                len(self.piece_coordinate['bN']) <= 1:
            for symbol in self.piece_coordinate:
                if symbol[1] != 'B' and symbol[1] != 'N' and \
                        symbol[1] != 'K' and self.piece_coordinate[symbol]:
                    break
            else:
                Game.result = ['draw', 'insufficient material']
                return

        # check fifty-move rule and repetition
        move_count, repetition_count = 0, 0
        check_dict = {'turn': self.turn, 'board': self.board[:],
                      'piece_coordinate': deepcopy(self.piece_coordinate)}
        while True:
            if not self.game_log or self.game_log[-1][1] == 'P' or \
                    self.game_log[-1][-3] == 'x' or \
                    self.game_log[-1][-6] == 'x':
                self.game_log += self.temp_log
                self.temp_log.clear()
                break
            move_count += 1
            check_dict['turn'] = self.update_position(check_dict, 'last')
            if check_dict['piece_coordinate'] == self.piece_coordinate:
                repetition_count += 1
            if repetition_count == 2:
                Game.result = ['draw', 'repetition']
                return
            if move_count == 99:
                Game.result = ['draw', 'fifty-move rule']
                return

    def update_game(self, start, target, symbol=''):
        """Update the chess board and game elements."""
        identical_piece = []
        # look for pieces that share the same piece type with board[start]
        # and are also able to get to the target square
        for square in self.piece_coordinate[self.board[start]]:
            if target in self.legal(square):
                identical_piece.append(square)
        self.track_the_game(self.board, start, target, identical_piece)
        self.update_en_passant(start, target)
        if self.castle_flags[self.turn]['short'] or \
                self.castle_flags[self.turn]['long']:
            self.update_castle(start, target)
        # update the pieces coordinates set
        self.piece_coordinate[self.board[start]].remove(start)
        self.piece_coordinate[self.board[start]].append(target)
        if self.board[target] != '00':  # whether it's a capture
            self.piece_coordinate[self.board[target]].remove(target)
        # update chess board
        self.board[target] = self.board[start]
        self.board[start] = '00'
        # update the player turn
        self.turn = 'b' if self.turn == 'w' else 'w'
        self.update_pawn_promotion(target)
        self.update_game_result()

    def draw_piece(self, piece, square):
        """Draw chess piece on the specific square."""
        symbol = self.piece_symbol[piece]
        area = list(self.get_area(square))[:2]
        for area_index in range(2):  # center the piece symbol
            square_size = (SQUARE_WIDTH, SQUARE_HEIGHT)
            area[area_index] += (square_size[area_index] -
                                 self.chess_font.size(symbol)[area_index]) // 2
        self.window.blit(self.chess_font.render(symbol, True, BLACK), area)

    def draw_highlight(self, square, color, board=None):
        """Highlight the specific square."""
        board = board or self.board
        pygame.draw.rect(self.window, color, self.get_area(square))
        if board[square] != '00':
            self.draw_piece(board[square], square)

    def draw_board(self, turn=None, board=None, piece_coordinate=None):
        """Draw the chess board and pieces."""
        turn, board = turn or self.turn, board or self.board
        piece_coordinate = piece_coordinate or self.piece_coordinate
        colors = [LIGHT_SQUARE, DARK_SQUARE]
        for square in range(64):
            if (square // 8) % 2 == 0:  # first squares on odd ranks are light
                color = colors[square % 2]
            else:  # first squares on even ranks are dark
                color = colors[(square + 1) % 2]
            pygame.draw.rect(self.window, color, self.get_area(square))
        for symbol, squares in piece_coordinate.items():
            for square in squares:
                self.draw_piece(symbol, square)

        # highlight checks
        king_square = piece_coordinate[turn + 'K'][0]
        if self.is_attacked(board, turn, king_square):
            self.draw_highlight(king_square, IN_CHECK_HIGHLIGHT, board=board)

    def draw_promotion_prompt(self):
        """Draw a window for pawn promotion prompt."""
        if isinstance(self.promote, int):
            promote_window = pygame.Surface((SQUARE_WIDTH, WINDOW_HEIGHT // 2))
            promote_window.fill(BACKGROUND_COLOR)
            square = self.promote
            if self.board[self.promote] == 'wP':  # white pawn promotion prompt
                self.promotion_choices = ['wQ', 'wB', 'wN', 'wR']
            else:  # black pawn promotion prompt
                square -= 24
                self.promotion_choices = ['bR', 'bN', 'bB', 'bQ']
            self.window.blit(promote_window, self.get_area(square)[:2])
            for index, symbol in enumerate(self.promotion_choices):
                self.draw_piece(symbol, square + 8 * index)

    def draw_sidebar(self):
        """Draw a sidebar for logs in standard algebraic notations."""
        sidebar = pygame.Surface((SIDEBAR_WIDTH, WINDOW_HEIGHT))
        sidebar.fill(SIDEBAR_COLOR)
        self.window.blit(sidebar, (BOARD_WIDTH, 0))
        pygame.draw.line(self.window, BLACK, (BOARD_WIDTH, 0),
                         (BOARD_WIDTH, WINDOW_HEIGHT), (WINDOW_WIDTH // 250))

    def update_sidebar(self, move, san_length):
        """Update game logs for the sidebar accordingly."""
        move_count = (san_length + 1) // 2
        turn = 'w' if san_length % 2 == 1 else 'b'
        x_position = BOARD_WIDTH + SIDEBAR_WIDTH // 20 if \
            turn == 'w' else BOARD_WIDTH + SIDEBAR_WIDTH * 3 // 5
        y_position = (move_count % 30 if move_count % 30 != 0 or
                      move_count == 0 else 30) * SIDEBAR_LOG_LINE_SPACING

        # check if the sidebar is going out of space
        if san_length >= 61 and (san_length - 1) % 60 == 0:
            self.draw_sidebar()  # cover up old logs

        # neatly format the move log for the sidebar
        if move[0].isupper() and move[0] != 'O':  # if not a pawn move or
            # castling, display the piece notation in figurines for the sidebar
            for symbol in self.piece_symbol:
                if turn + move[0] == symbol:
                    move = self.piece_symbol[symbol] + move[1:]
        elif move[-2] == '=':  # if a pawn gets promoted, display the notation
            # of the piece it promoted to in figurines for the sidebar
            for symbol in self.piece_symbol:
                if turn + move[-1] == symbol:
                    move = move[:-1] + self.piece_symbol[symbol]

        # display a certain move on the sidebar
        display_object = str(move_count) + '. ' if turn == 'w' else ''
        self.window.blit(self.notation_font.render(
            display_object + move, True, BLACK), (x_position, y_position))

    def make_move(self):
        """Make chess move based on click inputs."""
        square = self.get_square()
        if not self.move:  # handles the start square of a chess move
            if self.board[square][0] == self.turn:
                self.move.append(square)
                self.draw_highlight(self.move[0], PIECE_SELECTED_HIGHLIGHT)
                for square in self.legal(self.move[0]):
                    self.draw_highlight(square, LEGAL_SQUARE_HIGHLIGHT)
                return
        else:  # handles the target square of a chess move
            self.move.append(square)
            if self.move[1] in self.legal(self.move[0]):
                self.update_game(self.move[0], self.move[1])
                self.update_sidebar(self.san[-1], len(self.san))
        self.draw_board()
        self.draw_promotion_prompt()
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
        self.update_pawn_promotion(self.promote, symbol)
        self.update_game_result()
        self.draw_board()
        self.update_sidebar(self.san[-1], len(self.san))

    def undo_move(self):
        """Undo chess move."""
        if not self.game_log or self.temp_log or self.promote:
            # if not self.game_log:
            # undoing move at the start position is inhibited
            # if self.temp_log:
            # undoing move while rewinding previous positions is inhibited
            # if self.promote:
            # undoing move while promoting is inhibited
            return
        if self.rewind_dict:
            self.rewind_dict.clear()
        self.turn = self.update_position(
            {'turn': self.turn, 'board': self.board,
             'piece_coordinate': self.piece_coordinate}, 'last')
        # check whether the undo move is en passant
        if self.temp_log[0][-3] == 'E':
            # reset the en passant flag after undoing an en passant move
            direction = 1 if self.turn == 'w' else -1
            self.en_passant = int(self.temp_log[0][4:6]) + 8 * direction
        # check whether the undo move is castling
        if str(move_count := len(self.game_log) + 1) in self. \
                castle_flags_for_undoes[self.turn]:
            # reset the corresponding castle flags
            self.castle_flags[self.turn] = deepcopy(
                self.castle_flags_for_undoes[self.turn].pop(str(move_count)))
        self.temp_log.clear()
        # cover up the undone move on the sidebar
        x_position = BOARD_WIDTH + SIDEBAR_WIDTH // 20 if \
            self.turn == 'w' else BOARD_WIDTH + SIDEBAR_WIDTH // 2
        y_position = (move_count % 30 if move_count % 30 != 0 or
                      move_count == 0 else 30) * SIDEBAR_LOG_LINE_SPACING
        cover_up = pygame.Surface((SIDEBAR_WIDTH, WINDOW_HEIGHT))
        cover_up.fill(SIDEBAR_COLOR)
        self.window.blit(cover_up, (x_position, y_position))
        self.san.pop()
        if len(self.san) % 60 == 0:  # if the sidebar is empty after covering
            # up and the current game logs are on the last sidebar page, draw
            # the least-thirty-move log
            for length, move in enumerate(self.san[-60:], len(self.san) - 59):
                self.update_sidebar(move, length)
        self.draw_board()

    def mouse_click(self, event):
        """Handle mouse clicks."""
        if pygame.mouse.get_pos()[0] >= BOARD_WIDTH:
            # return the function if the mouse click is out of the board
            return
        elif event.button == 1:  # left click
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
                self.draw_highlight(square, RIGHT_CLICK_HIGHLIGHT)

    def key_press(self, event):
        """Handle button presses."""
        if event.key == pygame.K_LEFT:  # left arrow key -> last position
            if not self.game_log:
                # looking for last position at the start position is inhibited
                return
            if not self.rewind_dict:
                # set to the current position
                self.rewind_dict['turn'] = self.turn
                self.rewind_dict['board'] = self.board[:]
                self.rewind_dict['piece_coordinate'] = \
                    deepcopy(self.piece_coordinate)
            self.rewind_dict['turn'] = self.\
                update_position(self.rewind_dict, 'last')
            self.draw_board(**self.rewind_dict)
        elif event.key == pygame.K_RIGHT:  # right arrow key -> next position
            if not self.temp_log or (self.promote and len(self.temp_log) == 1):
                # looking for next position at the latest position is inhibited
                # stop looking for next position before making promotion choice
                return
            self.rewind_dict['turn'] = self.\
                update_position(self.rewind_dict, 'next')
            self.draw_board(**self.rewind_dict)
        elif event.key == pygame.K_u:  # U key -> undo move
            self.undo_move()

    def play(self):
        """Take user inputs, draw and update the chess board."""
        Game.result = []
        self.draw_board()
        self.draw_sidebar()
        while True:
            self.clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # ongoing -> False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.rewind_dict:
                        self.mouse_click(event)
                    else:  # if the board just got rewound:
                        self.draw_board()
                        if self.promote:
                            self.draw_promotion_prompt()
                        # reset the rewind dictionary and game log
                        self.rewind_dict.clear()
                        self.game_log += self.temp_log
                        self.temp_log.clear()
                elif event.type == pygame.KEYDOWN:
                    self.key_press(event)
            if Game.result:
                return True  # ongoing -> True


if __name__ == '__main__':
    prep()
    Game().play()
