import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        x1 = 10
        y1 = 40
        x2 = 110
        y2 = 240
        cell_width = 10
        cell_height = 40
        maze = Maze(x1, y1, x2, y2, cell_width, cell_height)
        maze._create_cells()
        cells = maze.get_cells()
        self.assertEqual(len(cells), (x2 - x1) / cell_width)
        self.assertEqual(len(cells[0]), (y2 - y1) / cell_height)

    def test_maze_has_entrance_and_exit(self):
        x1 = 10
        y1 = 40
        x2 = 110
        y2 = 240
        cell_width = 10
        cell_height = 40
        maze = Maze(x1, y1, x2, y2, cell_width, cell_height)
        maze._create_cells()
        maze._break_entrance_and_exit()
        cells = maze.get_cells()
        entrance = cells[0][0]
        exit = cells[len(cells)-1][len(cells[0])-1]
        self.assertEqual(entrance.has_top_wall, False)
        self.assertEqual(exit.has_bottom_wall, False)

    def test_maze_reset_visited(self):
        x1 = 10
        y1 = 40
        x2 = 110
        y2 = 240
        cell_width = 10
        cell_height = 40
        maze = Maze(x1, y1, x2, y2, cell_width, cell_height)
        maze._create_cells()
        maze._break_entrance_and_exit()
        maze._break_walls_r(0, 0)
        maze._reset_visited()
        for list in maze.get_cells():
            for item in list:
                self.assertEqual(item.get_visited(), False)

        

if __name__ == "__main__":
    unittest.main()