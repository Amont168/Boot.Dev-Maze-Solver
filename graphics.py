from tkinter import Tk, BOTH, Canvas
#from point import Point
from line import Line
from cell import Cell
from maze import Maze


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="black", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

    def draw_cell(self, cell, color):
        cell.draw(self.__canvas, color)

    def draw_move(self, cell1, cell2):
        cell1.draw_move(self.__canvas, cell2)

    def draw_maze(self, maze):
        maze._draw_cells(self.__canvas)

