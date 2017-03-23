import pygame
import pygame.draw
import pygame.event
import pygame.font
from pygame.locals import *

from boardstate import BoardState


class Game:
    DIFFICULTY_EASY = [5, 5, 5]
    DIFFICULTY_MEDIUM = [10, 10, 25]
    DIFFICULTY_HARD = [15, 15, 45]
    DIFFICULTY_DEFAULT = DIFFICULTY_MEDIUM

    BLACK = (38, 50, 56)
    WHITE = (245, 245, 245)
    RED = (255, 205, 210)
    BLUE_GRAY = (84, 110, 122)
    BURGUNDY = (106, 27, 154)
    GREEN = (46, 125, 50)
    ORANGE = (245, 124, 0)

    BACKGROUND_COLOR = BLUE_GRAY
    CLOSED_FIELD = BLACK
    OPEN_FIELD = WHITE
    OPEN_FIELD_WITH_VALUE = RED
    MINE_FIELD_BACKGROUND_COLOR = BURGUNDY

    FIELD_SIZE = 30
    GAP_SIZE = 4
    PANEL_HEIGHT = 45

    def __init__(self):
        self.fps_clock = pygame.time.Clock()
        self.display = pygame.display
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        self.difficulty = self.select_difficulty_menu()
        self.board_state = BoardState(self.difficulty[0], self.difficulty[1], self.difficulty[2])
        self.loop()

    def loop(self):
        board = self.board_state.board
        self.display = pygame.display.set_mode(
            (board.width * (self.FIELD_SIZE + self.GAP_SIZE) + self.GAP_SIZE,
             board.height * (self.FIELD_SIZE + self.GAP_SIZE) + self.GAP_SIZE + self.PANEL_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        while True:
            button = None
            mouse_clicked = False

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.exit_game()
                elif event.type == MOUSEBUTTONUP:
                    button = event.button
                    mouse_x, mouse_y = event.pos
                    mouse_clicked = True

            if mouse_clicked:
                x, y = self.get_selected_mine_field(mouse_x, mouse_y)
                if (x, y) != (None, None):
                    if button == 1:
                        self.board_state.touch_cell(y, x)
                    elif button == 3:
                        self.board_state.mark_cell(y, x)

            self.board_state.check_won()
            self.draw_board(board)

            if self.board_state.game_state == BoardState.GAME_STATE_WON:
                message = "You won!"
                self.add_message_on_lower_panel(message)
                pygame.display.update()
                pygame.time.wait(3000)
                self.__init__()

            elif self.board_state.game_state == BoardState.GAME_STATE_LOST:
                message = "You lost!"
                self.add_message_on_lower_panel(message)
                pygame.display.update()
                pygame.time.wait(3000)
                self.__init__()

            pygame.display.update()
            self.fps_clock.tick(50)

    def draw_board(self, board):
        self.display.fill(self.BACKGROUND_COLOR)
        for x in range(board.width):
            for y in range(board.height):
                cell = board.get_cell(x, y)
                self.draw_cell(cell, x, y)

    def draw_cell(self, cell, x, y):
        left, top = self.get_top_left_coordinates_of_cell(y, x)
        if cell.marked:
            pygame.draw.rect(self.display, self.GREEN, (left, top, self.FIELD_SIZE, self.FIELD_SIZE))
            text_surface_obj = self.font.render("#", True, self.BLACK)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (left + (self.FIELD_SIZE / 2), top + (self.FIELD_SIZE / 2))
            self.display.blit(text_surface_obj, text_rect_obj)
        elif not cell.touched:
            pygame.draw.rect(self.display, self.CLOSED_FIELD, (left, top, self.FIELD_SIZE, self.FIELD_SIZE))
        elif cell.has_mine:
            pygame.draw.rect(self.display, self.BURGUNDY, (left, top, self.FIELD_SIZE, self.FIELD_SIZE))
            pygame.draw.circle(self.display, self.BLACK,
                               (int(left + (self.FIELD_SIZE / 2)), int(top + (self.FIELD_SIZE / 2))), 9, 0)
            pygame.draw.circle(self.display, self.WHITE,
                               (int(left + (self.FIELD_SIZE / 2)), int(top + (self.FIELD_SIZE / 2))), 3, 0)
        elif cell.touched:
            if cell.value == 0:
                pygame.draw.rect(self.display, self.OPEN_FIELD, (left, top, self.FIELD_SIZE, self.FIELD_SIZE))
            else:
                pygame.draw.rect(self.display, self.OPEN_FIELD_WITH_VALUE,
                                 (left, top, self.FIELD_SIZE, self.FIELD_SIZE))
                text_surface_obj = self.font.render(str(cell.value), True, self.BLACK)
                text_rect_obj = text_surface_obj.get_rect()
                text_rect_obj.center = (left + (self.FIELD_SIZE / 2), top + (self.FIELD_SIZE / 2))
                self.display.blit(text_surface_obj, text_rect_obj)

    def get_selected_mine_field(self, mouse_x, mouse_y):
        for x in range(self.board_state.width):
            for y in range(self.board_state.height):
                left, top = self.get_top_left_coordinates_of_cell(x, y)
                fieldRect = pygame.Rect(left, top, self.FIELD_SIZE, self.FIELD_SIZE)
                if fieldRect.collidepoint(mouse_x, mouse_y):
                    return x, y
        return None, None

    def get_top_left_coordinates_of_cell(self, x, y):
        left = self.GAP_SIZE + x * (self.FIELD_SIZE + self.GAP_SIZE)
        top = self.GAP_SIZE + (y * (self.FIELD_SIZE + self.GAP_SIZE))
        return left, top

    def select_difficulty_menu(self):
        self.display = pygame.display.set_mode((400, 50))
        self.display.fill(self.BACKGROUND_COLOR)
        self.display.blit(self.font.render("Press 'e' for easy, 'm' for medium and 'h' for hard", 1, self.ORANGE),
                          (15, 15))
        pygame.display.set_caption("Select difficulty")
        pygame.display.flip()
        pygame.display.update()
        while 1:
            inkey = self.get_key_or_quit_game()
            if inkey == K_e:
                return self.DIFFICULTY_EASY
            elif inkey == K_m:
                return self.DIFFICULTY_MEDIUM
            elif inkey == K_h:
                return self.DIFFICULTY_HARD
            else:
                return self.DIFFICULTY_MEDIUM

    def get_key_or_quit_game(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                self.exit_game()
            else:
                pass

    def add_message_on_lower_panel(self, message):
        text_surface_obj = self.font.render(message, True, self.ORANGE)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (self.board_state.width * len(message),
                                self.board_state.height * (self.FIELD_SIZE + self.GAP_SIZE) + self.GAP_SIZE * 4)
        self.display.blit(text_surface_obj, text_rect_obj)

    def exit_game(self):
        pygame.quit()
        quit()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    game = Game()
    game.loop()
