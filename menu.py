import pygame
from game import Game, FPS, WINDOW_WIDTH, \
    WINDOW_HEIGHT, BLACK, BACKGROUND_COLOR


TITLE_SURFACE_HEIGHT = WINDOW_HEIGHT // 5 * 2
BUTTON_WIDTH = WINDOW_WIDTH // 4
BUTTON_HEIGHT = WINDOW_HEIGHT // 16
LARGER_FONT_SIZE = WINDOW_HEIGHT // 8
SMALLER_FONT_SIZE = WINDOW_HEIGHT // 20
TITLE_SURFACE_COLOR = (255, 220, 140)
BUTTON_COLOR = (130, 180, 255)


class Menu(Game):
    """The class for the game menu."""

    def __init__(self):
        super().__init__()
        self.larger_font = pygame.font.Font(None, LARGER_FONT_SIZE)
        self.smaller_font = pygame.font.Font(None, SMALLER_FONT_SIZE)

        self.ongoing = True
        self.in_main_menu = True
        self.menu()

    def draw_title_surface(self):
        """Draw title surface."""
        title_surface = pygame.Surface((WINDOW_WIDTH, TITLE_SURFACE_HEIGHT))
        title_surface.fill(TITLE_SURFACE_COLOR)
        self.window.blit(title_surface, (0, 0))

    def draw_text(self, size, text, position):
        """Draw text."""
        font = self.__dict__[size + '_font']
        self.window.blit(font.render(text, True, BLACK),
                         ((WINDOW_WIDTH - font.size(text)[0]) // 2,
                          WINDOW_HEIGHT // position))

    def draw_button(self, text, coordinates):
        """Draw button."""
        pygame.draw.rect(self.window, BUTTON_COLOR, (
            coordinates[0], coordinates[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        text_width, text_height = self.smaller_font.size(text)
        self.window.blit(self.smaller_font.render(text, True, BLACK),
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
        self.draw_text('larger', 'CHESS', 4)
        # return button names and the corresponding actions
        return ('START', 'EXIT'), (('in_main_menu', False), ('ongoing', False))

    def result_page(self):
        """Customize a menu page for the result page."""
        self.draw_text('larger', Game.result[0].title(), 5)
        self.draw_text('smaller', Game.result[1].title(), 3)
        # return button names and the corresponding actions
        return ('New Game', 'Main Menu'), (None, ('in_main_menu', True))

    def menu_page(self, page_name):
        """Build menu pages."""
        self.window.fill(BACKGROUND_COLOR)  # fills background color
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
