from board import Board


class BoardState:
    GAME_STATE_PLAYING = "PLAYING"
    GAME_STATE_WON = "WON"
    GAME_STATE_LOST = "LOST"

    def __init__(self, x, y, m):
        self.height = x
        self.width = y
        self.mines = m
        self.board = Board(x, y, m)
        self.has_mine = False
        self.touched_fields = 0
        self.marked_fields = 0
        self.total_fields = x * y
        self.game_state = self.GAME_STATE_PLAYING

    def touch_cell(self, x, y):
        cell = self.board.get_cell(x, y)
        self.has_mine = cell.touch()
        if (self.has_mine == True):
            self.game_state = self.GAME_STATE_LOST
        else:
            self.touched_fields += 1

    def mark_cell(self, x, y):
        cell = self.board.get_cell(x, y)
        if cell.marked:
            cell.unmark()
            self.marked_fields -= 1
        else:
            cell.mark_as_safe()
            self.marked_fields += 1

    def check_won(self):
        empty_cells_touched = 0
        for row in self.board.board_matrix:
            for cell in row:
                if not cell.has_mine and cell.touched:
                    empty_cells_touched += 1
        if empty_cells_touched == self.total_fields - self.mines:
            self.game_state = self.GAME_STATE_WON
