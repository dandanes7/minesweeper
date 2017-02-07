import random

from cell import Cell

MINE_FIELD = "X"
EMPTY_FIELD = "O"
DEFAULT_HEIGHT = 10
DEFAULT_WIDTH = 10


class Board():
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.mines = mines
        self.__set_up()
        self.__scatter_mines()
        self.__calculate_neighbour_values()

    def __set_up(self):
        self.board_matrix = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell())
            self.board_matrix.append(row)

    def __scatter_mines(self):
        mine_locations = set()
        while len(mine_locations) < self.mines:
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            mine_coordinates = (x, y)
            mine_locations.add(mine_coordinates)

        for coords in mine_locations:
            cell = self.get_cell(coords[0], coords[1])
            cell._place_mine()

    def __calculate_neighbour_values(self):
        for i in range(self.height):
            for j in range(self.width):
                main_cell = self.get_cell(i, j)
                if main_cell.has_mine:
                    # get the coordinates of all neighours
                    coordinates = set()
                    for x in (i - 1, i, i + 1):
                        for y in (j - 1, j, j + 1):
                            if not (x == i and y == j):
                                coordinates.add((x, y))
                    duplicateSet = coordinates.copy()
                    for item in duplicateSet:
                        if item[0] < 0 or item[1] < 0:
                            coordinates.remove(item)
                    for item in coordinates:
                        try:
                            neighbour = self.get_cell(item[0], item[1])
                            if not neighbour.has_mine:
                                neighbour.value += 1
                        except:
                            None

    def get_cell(self, x, y):
        row = self.board_matrix[x]
        return row[y]

    def set_cell(self, x, y, newCell):
        self.board_matrix[x - 1][y - 1] = newCell

    # Helper function, print board cell values & mines for debugging
    def reveal_board(self):
        for row in self.board_matrix:
            line = ""
            for cell in row:
                if (cell.has_mine):
                    line = line + MINE_FIELD + " "
                else:
                    line = line + str(cell.value) + " "
            print line
