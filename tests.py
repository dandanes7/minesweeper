import unittest2

from board import Board
from cell import Cell
from minesweeper import BoardState


class BoardTest(unittest2.TestCase):
    size = 5
    mines = 3

    def test_get_cell(self):
        dummy_board = Board(self.size, self.size, self.mines)
        initialCell = dummy_board.get_cell(1, 1)
        initialCell._place_mine()
        dummy_board.set_cell(1, 1, initialCell)
        newCell = dummy_board.get_cell(1, 1)
        self.assertTrue(newCell is not None)

    def test_board_is_set_up_correctly(self):
        dummy_board = Board(self.size, self.size, self.mines)
        mine_counter = 0
        row_counter = 0
        for row in dummy_board.board_matrix:
            row_counter += 1
            for i in range(self.size):
                cell = row[i]
                if cell.has_mine:
                    mine_counter += 1
        dummy_board.reveal_board()
        self.assertEquals(self.mines, mine_counter)
        self.assertEquals(self.size, row_counter)


class CellTest(unittest2.TestCase):
    def test_cell_marked(self):
        cell = Cell()
        cell.touch()
        cell.mark_as_safe()
        self.assertFalse(cell.marked)

    def test_cell_touched(self):
        cell = Cell()
        cell.mark_as_safe()
        cell.touch()
        self.assertFalse(cell.touched)

    def test_cell_mark_unmark(self):
        cell = Cell()
        cell.mark_as_safe()
        self.assertTrue(cell.marked)
        cell.unmark()
        self.assertFalse(cell.marked)

    def test_cell_touch(self):
        cell = Cell()
        cell.touch()
        self.assertTrue(cell.touched)


class BoardStateTest(unittest2.TestCase):
    size = 3
    mines = 1

    def test_board_status(self):
        board_state = BoardState(self.size, self.size, self.mines)
        board_state.check_won()
        self.assertEqual(BoardState.GAME_STATE_PLAYING, board_state.game_state)
        for row_no in range(self.size):
            row = board_state.board.board_matrix[row_no]
            for i in range(self.size):
                cell = row[i]
                if cell.has_mine:
                    board_state.mark_cell(row_no, i)
                else:
                    board_state.touch_cell(row_no, i)
        board_state.check_won()
        self.assertEqual(BoardState.GAME_STATE_WON, board_state.game_state)


if __name__ == '__main__':
    unittest2.main()
