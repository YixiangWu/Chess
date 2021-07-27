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
        """Draw title surface."""
        title_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT // 5 * 2))
        title_surface.fill((255, 220, 140))
        self.window.blit(title_surface, (0, 0))

    def draw_texture(self):
        """Draw texture."""
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
        """Draw text."""
        font = self.__dict__['font' + size]
        self.window.blit(font.render(text, True, (0, 0, 0)),
                         ((WINDOW_WIDTH - font.size(text)[0]) // 2,
                          WINDOW_HEIGHT // position))

    def draw_button(self, text, coordinates):
        """Draw button."""
        pygame.draw.rect(self.window, (130, 180, 255), (
            coordinates[0], coordinates[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        text_width, text_height = self.font40.size(text)
        self.window.blit(self.font40.render(text, True, (0, 0, 0)),
                         (coordinates[0] + (BUTTON_WIDTH - text_width) // 2,
                          coordinates[1] + (BUTTON_HEIGHT - text_height) // 2))

    @staticmethod
    def is_button_clicked(coordinates):
        """Check whether a button gets clicked."""
        return True if coordinates[0] <= pygame.mouse.get_pos()[0] < \
                       coordinates[0] + BUTTON_WIDTH and coordinates[1] < \
                       pygame.mouse.get_pos()[1] < \
                       coordinates[1] + BUTTON_HEIGHT else False

    def main_menu(self):
        """Customize a menu page for the main menu."""
        self.draw_texture()
        self.draw_text('108', 'CHESS', 4)
        # return button names and the corresponding actions
        return ('Start', 'Exit'), (('in_main_menu', False), ('ongoing', False))

    def result_page(self):
        """Customize a menu page for the result page."""
        result, cause = '', ''
        if Game.result[1]['checkmate']:
            result, cause = Game.result[0] + ' wins', 'by ' + 'checkmate'
        elif Game.result[1]['stalemate']:
            result, cause = 'draw', 'by ' + 'stalemate'
        self.draw_text('108', result.title(), 5)
        self.draw_text('40', cause.title(), 3)
        # return button names and the corresponding actions
        return ('New Game', 'Main Menu'), (None, ('in_main_menu', True))

    def menu_page(self, page_name):
        """Build menu pages."""
        self.window.fill((220, 220, 220))  # fills background color
        self.draw_title_surface()
        button_names, actions = getattr(Menu, page_name)(self)
        button_coordinates = (
            ((WINDOW_WIDTH - BUTTON_WIDTH) // 2, WINDOW_HEIGHT // 10 * 7),
            ((WINDOW_WIDTH - BUTTON_WIDTH) // 2, WINDOW_HEIGHT // 10 * 8))
        for index, button_coordinate in enumerate(button_coordinates):
            self.draw_button(button_names[index], button_coordinate)
        while True:
            self.clock.tick(FPS)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ongoing = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for index, action in enumerate(actions):
                        # check which button is clicked and take the
                        # corresponding action to it
                        if self.is_button_clicked(button_coordinates[index]):
                            if action:
                                self.__dict__[action[0]] = action[1]
                            return

    def menu(self):
        """Meld menu pages with the chess game."""
        while self.ongoing:
            if self.in_main_menu:
                self.menu_page('main_menu')
            else:
                self.ongoing = Game().play()
                if not self.ongoing:
                    return
                self.menu_page('result_page')


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('chess')
    Menu()
