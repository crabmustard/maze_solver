from cell import Cell
import time
import random

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, 
                cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve(0,0)    
        
    def _create_cells(self):
        for x in range(self._num_cols):
            col_cells = []
            for y in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for x in range(self._num_cols):
            for y in range(self._num_rows):
                self._draw_cell(x, y)   

        
    def _draw_cell(self, x, y):
        if self._win is None:
            return
        x1 = self._x1 + (self._cell_size_x * x)
        y1 = self._y1 + (self._cell_size_y * y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[x][y].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.0001)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, x, y):
        self._cells[x][y].visited = True
        while True:
            tovisit = []

            if x > 0 and not self._cells[x-1][y].visited:
                tovisit.append((x-1, y))
            if x < self._num_cols - 1 and not self._cells[x+1][y].visited:
                tovisit.append((x+1, y))
            if y > 0 and not self._cells[x][y-1].visited:
                tovisit.append((x, y-1))
            if y < self._num_rows - 1 and not self._cells[x][y+1].visited:
                tovisit.append((x, y+1))
            
            if len(tovisit) == 0:
                self._draw_cell(x, y)
                print(f'{x}, {y}')
                return
            
            direction = random.randrange(len(tovisit))
            govisit = tovisit[direction]

            if govisit[0] == x - 1:
                self._cells[x][y].has_left_wall = False
                self._cells[x-1][y].has_right_wall = False
                print('left')
            if govisit[0] == x + 1:
                self._cells[x][y].has_right_wall = False
                self._cells[x+1][y].has_left_wall = False
                print('right')
            if govisit[1] == y - 1:
                self._cells[x][y].has_top_wall = False
                self._cells[x][y - 1].has_bottom_wall = False
                print('up')
            if govisit[1] == y + 1:
                self._cells[x][y].has_bottom_wall = False
                self._cells[x][y + 1].has_top_wall = False
                print('down')
            
            self._break_walls_r(govisit[0], govisit[1])

    def _reset_cells_visited(self):
        for c1 in self._cells:
            for cell in c1:
                cell.visited = False
        
    def solve(self, x, y):
        return self._solve_r(x, y)

    def _solve_r(self, x, y):
        self._animate()
        dingo = self._cells[x][y]
        dingo.visited = True
        if x == self._num_cols - 1 and y == self._num_rows - 1:
            return True
        takeout = []
        if not dingo.has_bottom_wall and y < self._num_rows - 1:
            if not self._cells[x][y+1].visited:
                takeout.append((x, y+1))
        if not dingo.has_top_wall and y > 0:
            if not self._cells[x][y-1].visited:
                takeout.append((x, y-1))
        if not dingo.has_left_wall and x > 0:
            if not self._cells[x-1][y].visited:
                takeout.append((x-1, y))
        if not dingo.has_right_wall and x < self._num_cols - 1:
            if not self._cells[x+1][y].visited:
                takeout.append((x+1, y))
        while takeout:
            m, n = takeout.pop()
            dingo.draw_move(self._cells[m][n])
            checker = self._solve_r(m, n)
            if checker == False:
                dingo.draw_move(self._cells[m][n], undo=True)
            else: return True


        return False
            

        

        
        











        #     if not dingo.has_right_wall and not self._cells[x+1][y].visited:
        #         dingo.draw_move(self._cells[x+1][y])
        #         if not self._solve_r(x+1, y):
        #             dingo.draw_move(self._cells[x+1][y], undo=True)
        #     if not dingo.has_bottom_wall and not self._cells[x][y+1].visited:
        #         dingo.draw_move(self._cells[x][y+1])
        #         if not self._solve_r(x, y+1):
        #             dingo.draw_move(self._cells[x][y+1], undo=True)
        #     if not dingo.has_top_wall and not self._cells[x][y-1].visited:
        #         dingo.draw_move(self._cells[x][y-1])
        #         if not self._solve_r(x, y-1):
        #             dingo.draw_move(self._cells[x][y-1], undo=True)
        #     if not dingo.has_left_wall and not self._cells[x-1][y].visited:
        #         dingo.draw_move(self._cells[x-1][y])
        #         if not self._solve_r(x-1, y):
        #             dingo.draw_move(self._cells[x-1][y], undo=True)
        # return False

        

        
        




