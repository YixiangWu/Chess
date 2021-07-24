import pygame
from game import Game, WINDOW_WIDTH, WINDOW_HEIGHT, FPS


BUTTON_WIDTH = WINDOW_WIDTH // 4
BUTTON_HEIGHT = WINDOW_HEIGHT // 16


class Menu(Game):
    """The class for the game menu."""

    def __init__(self):
        super().__init__()
        self.font40 = pygame.font.Font(None, 40)
        self.font108 = pygame.font.Font(None, 108)

        self.ongoing = True
        self.in_main_menu = True
        self.menu()

    def draw_title_surface(self):
        """Draw a title surface."""
        title_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT // 5 * 2))
        title_surface.fill((255, 220, 140))
        self.window.blit(title_surface, (0, 0))

    def draw_texture(self):
        """Draw textures."""
        for ratio in range(1, 4):
            interval, color = 13, (0, 130, 130)
            pos_x = WINDOW_WIDTH * ratio // interval
            pos_y = WINDOW_HEIGHT * ratio // interval
            pygame.draw.line(self.window, color, (0, pos_y), (pos_x, 0), 3)
            pygame.draw.line(
                self.window, color,
                (WINDOW_WIDTH, WINDOW_HEIGHT - pos_y),
                (WINDOW_WIDTH - pos_x, WINDOW_HEIGHT), 3)

    def draw_text(self, size, text, position):
        """Draw texts."""
        font = self.__dict__['font' + size]
        self.window.blit(font.render(text, True, (0, 0, 0)),
                         ((WINDOW_WIDTH - font.size(text)[0]) // 2,
                          WINDOW_HEIGHT // position))

    def draw_button(self, text, coords):
        """Draw a button."""
        pygame.draw.rect(self.window, (130, 180, 255), (
            coords[0], coords[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        text_width, text_height = self.font40.size(text)
        self.window.blit(self.font40.render(text, True, (0, 0, 0)),
                         (coords[0] + (BUTTON_WIDTH - text_width) // 2,
                          coords[1] + (BUTTON_HEIGHT - text_height) // 2))

    def draw_two_buttons(self, upper_button, lower_button):
        """Draw two buttons on the same page and return their coordinates."""
        upper_button_coords = ((WINDOW_WIDTH - BUTTON_WIDTH) // 2,
                               WINDOW_HEIGHT // 10 * 7)
        self.draw_button(upper_button, upper_button_coords)
        lower_button_coords = ((WINDOW_WIDTH - BUTTON_WIDTH) // 2,
                               WINDOW_HEIGHT // 10 * 8)
        self.draw_button(lower_button, lower_button_coords)
        return [upper_button_coords, lower_button_coords]

    @staticmethod
    def is_button_clicked(coords):
        """Check whether a button gets clicked."""
        return True if coords[0] <= pygame.mouse.get_pos()[0] < \
                       coords[0] + BUTTON_WIDTH and coords[1] < \
                       pygame.mouse.get_pos()[1] < \
                       coords[1] + BUTTON_HEIGHT else False

    @staticmethod
    def get_result():
        """Get game result from the Game class."""
        if Game.result[1]['checkmate']:
            return [(Game.result[0] + ' wins').title(),
                    ('by ' + 'checkmate').title()]
        elif Game.result[1]['stalemate']:
            return ['Draw', ('by ' + 'stalemate').title()]

    def main_menu(self):
        """Build the main menu."""
        self.window.fill((220, 220, 220))  # fills background color
        self.draw_title_surface()
        self.draw_texture()
        self.draw_text('108', 'CHESS', 4)
        button_coords = self.draw_two_buttons('Start', 'Exit')
        while True:
            self.clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ongoing = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check whether the Start button is clicked
                    if self.is_button_clicked(button_coords[0]):
                        self.in_main_menu = False
                        return
                    # check whether the Exit button is clicked
                    elif self.is_button_clicked(button_coords[1]):
                        self.ongoing = False
                        return

    def result_page(self):
        """Build the result page."""
        self.window.fill((220, 220, 220))  # fills background color
        self.draw_title_surface()
        self.draw_text('108', self.get_result()[0], 5)
        self.draw_text('40', self.get_result()[1], 3)
        button_coords = self.draw_two_buttons('New Game', 'Main Menu')
        while True:
            self.clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ongoing = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check whether the New Game button is clicked
                    if self.is_button_clicked(button_coords[0]):
                        return
                    # check whether the Main Menu button is clicked
                    elif self.is_button_clicked(button_coords[1]):
                        self.in_main_menu = True
                        return

    def menu(self):
        """Meld main menu and result page with the chess game."""
        while self.ongoing:
            if self.in_main_menu:
                self.main_menu()
            else:
                self.ongoing = Game().play()
                if not self.ongoing:
                    return
                self.result_page()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('chess')
    Menu()
