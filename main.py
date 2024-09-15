from graphics import Window
from line import Line
from cell import Cell
from maze import Maze
from constants import *


def main():
    win = Window(WINDOW_HEIGHT, WINDOW_WIDTH)

    maze = Maze(WINDOW_PADDING, WINDOW_PADDING, WINDOW_HEIGHT - WINDOW_PADDING, WINDOW_WIDTH - WINDOW_PADDING, CELL_SIZE, CELL_SIZE, win)
    maze._create_cells()
    win.draw_maze(maze)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    win.draw_maze(maze)
    maze._reset_visited()
    maze._solve_r(0, 0, 4)
    win.wait_for_close()


main()