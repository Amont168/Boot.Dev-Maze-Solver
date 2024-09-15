from tkinter import Tk, BOTH, Canvas


class Cell:
    def __init__(self, x1, y1, x2, y2):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__visited = False

    def draw(self, canvas, color):
        if canvas is not None:
            if self.has_left_wall:
                canvas.create_line(self.__x1, self.__y1, self.__x1, self.__y2, fill=color, width = 2)
            else:
                canvas.create_line(self.__x1, self.__y1, self.__x1, self.__y2, fill="black", width = 2)

            if self.has_top_wall:
                canvas.create_line(self.__x1, self.__y1, self.__x2, self.__y1, fill=color, width = 2)
            else:
                canvas.create_line(self.__x1, self.__y1, self.__x2, self.__y1, fill="black", width = 2)

            if self.has_right_wall:
                canvas.create_line(self.__x2, self.__y1, self.__x2, self.__y2, fill=color, width = 2)
            else:
                canvas.create_line(self.__x2, self.__y1, self.__x2, self.__y2, fill="black", width = 2)

            if self.has_bottom_wall:
                canvas.create_line(self.__x1, self.__y2, self.__x2, self.__y2, fill=color, width = 2)
            else:
                canvas.create_line(self.__x1, self.__y2, self.__x2, self.__y2, fill="black", width = 2)

    def draw_move(self, canvas, to_cell, undo=False):
        color = "red"
        if undo:
            color = "white"
        x1 = (self.__x1 + self.__x2) / 2
        y1 = (self.__y1 + self.__y2) / 2
        x2 = (to_cell.__x1 + to_cell.__x2) / 2
        y2 = (to_cell.__y1 + to_cell.__y2) / 2
        canvas.create_line(x1, y1, x2, y2, fill=color, width = 2)
    
    def get_visited(self):
        return self.__visited
    
    def set_visited(self, val):
        self.__visited = val