from constants import UP, DOWN, LEFT, RIGHT
import random

class Board(list):
    def __init__(self, rows, cols, board=None):
        self.rows = rows
        self.cols = cols
        if board:
            if len(board) != rows:
                raise ValueError(f'Board must have {rows} rows. Got: {len(board)}.')
            for i, row in enumerate(board):
                if len(row) != cols:
                    raise ValueError(f'All rows in board must be of length {cols}. Row {i} is of length {len(row)}.')
            list.__init__(self, board)
        else:
            self.create_empty_board()
            self.spawn_random_block()
            self.spawn_random_block()

    def create_empty_board(self):
        for i in range(self.rows):
            self.append([0 for i in range(self.cols)])

    def spawn_random_block(self):
        row = random.randint(0, self.rows-1)
        col = random.randint(0, self.cols-1)
        while self[row, col] != 0:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)
        num = 4 if random.random() >= 0.9 else 2
        self[row, col] = num

    def move(self, dir):
        self._compress(dir)
        self._merge(dir)
        self._compress(dir)
    
    def is_stuck(self, row_idx, col_idx):
        square_value = self[row_idx, col_idx]
        if row_idx > 0 and self[row_idx-1, col_idx] == square_value:
            return False
        if row_idx < self.rows-1 and self[row_idx+1, col_idx] == square_value:
            return False
        if col_idx > 0 and self[row_idx, col_idx-1] == square_value:
            return False
        if col_idx < self.cols-1 and self[row_idx, col_idx+1] == square_value:
            return False
        return True
        
    def _compress(self, dir):
        if dir == RIGHT or dir == LEFT:
            start = self.cols-1 if dir == RIGHT else 0
            end = -1 if dir == RIGHT else self.cols
            for row_idx in range(self.rows):
                zeros_idx = []
                i = start
                farthest = max if dir == RIGHT else min
                while i != end:
                    if self[row_idx, i] == 0:
                        zeros_idx.append(i)
                    elif zeros_idx:
                        farthest_zero = farthest(zeros_idx)
                        self[row_idx, farthest_zero] = self[row_idx, i]
                        self[row_idx, i] = 0
                        zeros_idx.remove(farthest_zero)
                        zeros_idx.append(i)
                    i -= dir[0]
        elif dir == UP or dir == DOWN:
            start = self.rows-1 if dir == DOWN else 0
            end = -1 if dir == DOWN else self.rows
            for col_idx in range(self.cols):
                zeros_idx = []
                i = start
                farthest = max if dir == DOWN else min
                while i != end:
                    if self[i, col_idx] == 0:
                        zeros_idx.append(i)
                    elif zeros_idx:
                        farthest_zero = farthest(zeros_idx)
                        self[farthest_zero, col_idx] = self[i, col_idx]
                        self[i, col_idx] = 0
                        zeros_idx.remove(farthest_zero)
                        zeros_idx.append(i)
                    i -= dir[1]
        else:
            raise ValueError(f'Invalid direction: {dir}') 


    def _merge(self, dir):
        if dir == RIGHT or dir == LEFT:
            start = self.rows-1 if dir == RIGHT else 0
            end = 0 if dir == RIGHT else self.rows-1
            for row_idx in range(self.rows):
                for i in range(start, end, -dir[0]):
                    if self[row_idx, i] == self[row_idx, i-dir[0]] != 0:
                        self[row_idx, i] *= 2
                        self[row_idx, i-dir[0]] = 0
        elif dir == UP or dir == DOWN:
            start = self.cols-1 if dir == DOWN else 0
            end = 0 if dir == DOWN else self.cols-1
            for col_idx in range(self.cols):
                for i in range(start, end, -dir[1]):
                    if self[i, col_idx] == self[i-dir[1], col_idx] != 0:
                        self[i, col_idx] *= 2
                        self[i-dir[1], col_idx] = 0
        else:
            raise ValueError(f'Invalid direction: {dir}')  

    def __getitem__(self, __i):
        row_idx, col_idx = __i
        if row_idx < 0 or row_idx >= self.rows or col_idx < 0 or col_idx >= self.cols:
            raise ValueError(f'Row index or column index out of bounds. Row index: {row_idx}, Column index: {col_idx}')
        return list.__getitem__(self, row_idx)[col_idx]
    
    def __setitem__(self, __i, __o):
        row_idx, col_idx = __i
        if row_idx < 0 or row_idx >= self.rows or col_idx < 0 or col_idx >= self.cols:
            raise ValueError(f'Row index or column index out of bounds. Row index: {row_idx}, Column index: {col_idx}')
        list.__getitem__(self, row_idx)[col_idx] = __o