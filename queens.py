from random import choice, randint, seed
from time import time
from typing import List, Tuple

import pygame

from game import BOARD_WIDTH, WINDOW_HEIGHT, \
    DARK_SQUARE, FPS, Game, LIGHT_SQUARE


class EightQueens(Game):
    """The class for the eight queens puzzle."""

    def __init__(self):
        super().__init__()
        self.window = pygame.display.set_mode((BOARD_WIDTH, WINDOW_HEIGHT))
        self.position = -1
        self.color = '00'
        self.count = -1

    def eight_queens(
        self,
        column: int = 0,
        board: List[Tuple[int, int, int]] = None
    ):
        """
        Generate eight queens on the chessboard so that there is no such case
        where two queens threaten each other.

        @param column: the current working column
        @param board[column](row, (row + column), (row - column))
        """
        board = board or list()

        for row in range(8):
            for queen in board:
                if row == queen[0] or row + column == queen[1] or \
                        row - column == queen[2]:
                    # row check: row == queen[0]
                    # left diagonal check: row + column == queen[1]
                    # right diagonal check: row - column == queen[2]
                    break
            else:  # if valid choice:
                board.append((row, row + column, row - column))
                if column != 7:  # if more decision to make:
                    self.eight_queens(column + 1, board)
                else:  # reach the leaf -> means candidate solution
                    self.count += 1

                if self.count == self.position:
                    # generate the solution
                    chessboard = []
                    for queen in board:
                        chessboard.extend(
                            ['00', '00', '00', '00', '00', '00', '00', '00'])
                        chessboard[queen[0] - 8] = self.color

                    # draw the solution on the chessboard
                    for square, piece in enumerate(chessboard):
                        if piece != '00':
                            self.draw_piece(piece, square)
                    return
                board.pop()  # undo choice

    def draw_empty_board(self):
        """Draw an empty chessboard for the puzzle."""
        colors = [LIGHT_SQUARE, DARK_SQUARE]
        for square in range(64):
            color = colors[square % 2] if \
                (square // 8) % 2 == 0 else colors[(square + 1) % 2]
            pygame.draw.rect(self.window, color, self.get_area(square))

    def play(self):
        """New play method for the eight queens puzzle."""
        self.draw_empty_board()
        while True:
            self.clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.draw_empty_board()  # draw a new empty chessboard

                        # generate a new random eight-queens position
                        seed(time())
                        self.position = randint(1, 92)
                        self.color = choice(['wQ', 'bQ'])
                        self.count = 0
                        self.eight_queens()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('eight queens')
    EightQueens().play()
