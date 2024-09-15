from tkinter import Tk, BOTH, Canvas
import time
from cell import Cell
import random
from enum import Enum
from constants import *

class Directions(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4



class Maze:
    def __init__(self, x1, y1, x2, y2, cell_size_x, cell_size_y, window=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__cells = None
        self.__window = window
        self.__canvas = None
        if seed is not None:
            self.__seed = random.seed(seed)
        else:
             self.__seed = seed

    def get_cells(self):
        return self.__cells

    def _create_cells(self):
        num_rows = int((self.__x2 - self.__x1) / self.__cell_size_x)
        num_cols = int((self.__y2 - self.__y1) / self.__cell_size_y)
        current_x = self.__x1
        current_y = self.__y1
        
        output = []

        for x in range(num_rows):
            column = []
            for y in range(num_cols):
                column.append(Cell(current_x, current_y, (current_x + self.__cell_size_x), (current_y + self.__cell_size_y)))
                current_y += self.__cell_size_y
            output.append(column)
            current_y = self.__y1
            current_x += self.__cell_size_x
        self.__cells = output

    def _draw_cells(self, canvas):
        self.__canvas = canvas
        for list in self.__cells:
            for cell in list:
                self._draw_cell(cell)
                
    def _draw_cell(self, cell):
        cell.draw(self.__canvas, "medium spring green")
        if self.__window is not None:
            self.__window.redraw()  
        time.sleep(SLEEP_TIME_MAZE_GEN)


    def _break_entrance_and_exit(self):
        entrance = self.__cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(entrance)
        exit = self.__cells[len(self.__cells) - 1][len(self.__cells[0])-1]
        exit.has_bottom_wall = False
        self._draw_cell(exit)

    def _break_walls_r(self, x, y):
        if self.__cells[x][y].get_visited() == False:
            #Set cell visited
            self.__cells[x][y].set_visited(True)

            cells_to_visit = []
            cell_above = None
            cell_left = None
            cell_below = None
            cell_right = None

            #Populate cells around current cell
            if y > 0 and self.__cells[x][y-1].get_visited() == False:
                cell_above = self.__cells[x][y-1]
                cells_to_visit.append((x, y-1))
            if x < len(self.__cells) - 1 and self.__cells[x+1][y].get_visited() == False:
                cell_right = self.__cells[x+1][y]
                cells_to_visit.append((x+1, y))
            if y < len(self.__cells[0]) - 1 and self.__cells[x][y+1].get_visited() == False:
                cell_below = self.__cells[x][y+1]
                cells_to_visit.append((x, y+1))
            if x > 0 and self.__cells[x-1][y].get_visited() == False:
                cell_left = self.__cells[x-1][y]
                cells_to_visit.append((x-1, y))

            #Pick random direction to move; Destroy wall between current cell and cells to be visitable from current location.
            find_direction = True
            while find_direction:
                if cell_above is None and cell_right is None and cell_below is None and cell_left is None:
                    find_direction = False
                direction = random.randrange(1,5)
                print(f"Trying to break in x: {x}, y: {y}, direction: {direction}, cell_above: {cell_above}, cell_below: {cell_below}, cell_right: {cell_right}, cell_left: {cell_left}")
                match(direction):
                    case 1:
                        if cell_above is not None:
                            self._set_cell_above(x, y)
                            find_direction = False
                    case 2:
                        if cell_right is not None:
                            self._set_cell_right(x, y)
                            find_direction = False
                    case 3:
                        if cell_below is not None:
                            self._set_cell_below(x, y)
                            find_direction = False
                    case 4:
                        if cell_left is not None:
                            self._set_cell_left(x, y)
                            find_direction = False

            #Recurrisvely visit neighboring cells
            for item in cells_to_visit:
                self._break_walls_r(item[0], item[1])
    
    def _set_cell_above(self, x, y):
        self.__cells[x][y].has_top_wall = False
        self.__cells[x][y-1].has_bottom_wall = False
    
    def _set_cell_right(self, x, y):
        self.__cells[x][y].has_right_wall = False
        self.__cells[x+1][y].has_left_wall = False
    
    def _set_cell_below(self, x, y):
        self.__cells[x][y].has_bottom_wall = False
        self.__cells[x][y+1].has_top_wall = False

    def _set_cell_left(self, x, y):
        self.__cells[x][y].has_left_wall = False
        self.__cells[x-1][y].has_right_wall = False

    def _reset_visited(self):
        for x in range(len(self.__cells)):
            for y in range(len(self.__cells[0])):
                self.__cells[x][y].set_visited(False)


    def _solve_r(self, x, y, direction):
        if x == len(self.__cells) - 1 and y == len(self.__cells[0]) - 1:
            return True
        
        #Make sure this cell hasn't been visited yet
        current_cell = self.__cells[x][y]
        if current_cell.get_visited() == False:
            print(f"Starting solve at cell {x}, {y}")   
            #Mark cell as having been visited
            self.__cells[x][y].set_visited(True)

            moving = True
            counter = 0
            
            while moving:
                print(f"In cell {x}, {y}, trying to move {direction} - West Value {Directions.WEST}")
                match(direction):
                    case Directions.NORTH.value:
                        if current_cell.has_top_wall == False and y > 0 and self.__cells[x][y-1].get_visited() == False:
                            current_cell.draw_move(self.__canvas, self.__cells[x][y-1])
                            self.__window.redraw()  
                            time.sleep(SLEEP_TIME)
                            direction = Directions.WEST.value
                            if self._solve_r(x, y-1, direction):
                                return True
                            else:
                                current_cell.draw_move(self.__canvas, self.__cells[x][y-1], True)
                                self.__window.redraw()  
                                time.sleep(SLEEP_TIME)
                                direction = Directions.EAST.value                                
                        else:
                            direction = Directions.EAST.value
                    case Directions.EAST.value:
                        if current_cell.has_right_wall == False and x < len(self.__cells) - 1 and self.__cells[x+1][y].get_visited() == False:
                            current_cell.draw_move(self.__canvas, self.__cells[x+1][y])
                            self.__window.redraw()  
                            time.sleep(SLEEP_TIME)
                            direction = Directions.NORTH.value
                            if self._solve_r(x+1, y, direction):
                                return True
                            else:
                                current_cell.draw_move(self.__canvas, self.__cells[x+1][y], True)
                                self.__window.redraw()  
                                time.sleep(SLEEP_TIME)
                                direction = Directions.SOUTH.value
                        else:
                            direction = Directions.SOUTH.value
                    case Directions.SOUTH.value:
                        if current_cell.has_bottom_wall == False and y < len(self.__cells[0]) - 1 and self.__cells[x][y+1].get_visited() == False:
                            current_cell.draw_move(self.__canvas, self.__cells[x][y+1])
                            self.__window.redraw()  
                            time.sleep(SLEEP_TIME)
                            direction = Directions.EAST.value
                            if self._solve_r(x, y+1, direction):
                                return True
                            else:
                                current_cell.draw_move(self.__canvas, self.__cells[x][y+1], True)
                                self.__window.redraw()  
                                time.sleep(SLEEP_TIME)
                                direction = Directions.WEST.value
                        else:
                            direction = Directions.WEST.value
                    case Directions.WEST.value:
                        if current_cell.has_left_wall == False and x > 0 and self.__cells[x-1][y].get_visited() == False:
                            current_cell.draw_move(self.__canvas, self.__cells[x-1][y])
                            self.__window.redraw()  
                            time.sleep(SLEEP_TIME)
                            direction = Directions.SOUTH.value
                            if self._solve_r(x-1, y, direction):
                                return True
                            else:
                                current_cell.draw_move(self.__canvas, self.__cells[x-1][y], True)
                                self.__window.redraw()  
                                time.sleep(SLEEP_TIME)
                                direction = Directions.NORTH.value
                        else:
                            direction = Directions.NORTH.value
                counter += 1
                if counter == 4:
                    return False


                
            