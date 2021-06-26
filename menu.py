import pygame
from game import Game


class Menu(Game):
    """This class builds a menu for the chess game."""

    def __init__(self):
        super().__init__()
        self.fontC32 = pygame.font.Font('resources/Chalkboard.ttc', 32)
        self.fontMF32 = pygame.font.Font('resources/MarkerFelt.ttc', 32)
        self.fontSP108 = pygame.font.Font('resources/SignPainter.ttc', 108)

        self.buttonWidth = self.windowSize[0] // 4
        self.buttonHeight = self.windowSize[1] // 16

        self.ongoing = True
        self.in_main_menu = True
        self.menu()

    def draw_title_surface(self):
        """This method draws a title surface."""
        title_surface = pygame.Surface(
            (self.windowSize[0], self.windowSize[1] // 5 * 2))
        title_surface.fill((255, 220, 140))
        self.window.blit(title_surface, (0, 0))

    def draw_text(self, font, text, position):
        """This method draws texts."""
        font = self.__dict__['font' + font]
        self.window.blit(font.render(text, True, (0, 0, 0)),
                         ((self.windowSize[0] - font.size(text)[0]) // 2,
                          self.windowSize[1] // position))

    def draw_button(self, text, coords):
        """This method draws a button."""
        pygame.draw.rect(self.window, (130, 180, 255), (
            coords[0], coords[1], self.buttonWidth, self.buttonHeight))
        text_width, text_height = self.fontMF32.size(text)
        self.window.blit(self.fontMF32.render(text, True, (0, 0, 0)),
                         (coords[0] + (self.buttonWidth - text_width) // 2,
                          coords[1] + (self.buttonHeight - text_height) // 2))

    def draw_two_buttons(self, upper_btn, lower_btn):
        """This method draws two buttons on the same page."""
        upper_btn_coords = ((self.windowSize[0] - self.buttonWidth) // 2,
                            self.windowSize[1] // 10 * 7)
        self.draw_button(upper_btn, upper_btn_coords)
        lower_btn_coords = ((self.windowSize[0] - self.buttonWidth) // 2,
                            self.windowSize[1] // 10 * 8)
        self.draw_button(lower_btn, lower_btn_coords)
        return [upper_btn_coords, lower_btn_coords]

    def is_button_clicked(self, coords):
        """This method check whether a button is clicked."""
        return True if coords[0] <= pygame.mouse.get_pos()[0] < \
                       coords[0] + self.buttonWidth and coords[1] < \
                       pygame.mouse.get_pos()[1] < \
                       coords[1] + self.buttonHeight else False

    @staticmethod
    def get_result():
        """This method gets game result from the Game class."""
        turn = 'black' if Game.result[0] == 'white' else 'white'
        for game_state in Game.result[1]:
            if Game.result[1][game_state]:
                result = ''
                if game_state == 'checkmate':
                    result = turn + ' wins'
                elif game_state == 'stalemate':
                    result = 'draw'
                return [result.title(), ('by ' + game_state).title()]

    def main_menu(self):
        """This method builds the main menu."""
        self.window.fill((220, 220, 220))  # fills background color
        self.draw_title_surface()
        self.draw_text('SP108', 'CHESS', 4)
        button_coords = self.draw_two_buttons('Start', 'Exit')
        while True:
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
        """This method builds the result page."""
        self.window.fill((220, 220, 220))  # fills background color
        self.draw_title_surface()
        self.draw_text('SP108', self.get_result()[0], 5)
        self.draw_text('C32', self.get_result()[1], 3)
        button_coords = self.draw_two_buttons('New Game', 'Main Menu')
        while True:
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
        """This method melds main menu and result page with the chess game."""
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
