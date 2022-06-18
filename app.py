import copy
from constants import UP, DOWN, LEFT, RIGHT, RUNNING, LOST, WON, QUIT

class App:
    def __init__(self, board, ui):
        self.board = board
        self.ui = ui
        self.state = RUNNING

    def run(self):
        premove_board = copy.deepcopy(self.board)
        self.ui.display_board(self.board)
        while self.state == RUNNING:
            if premove_board != self.board:
                self.board.spawn_random_block()
                self.ui.display_board(self.board)

            premove_board = copy.deepcopy(self.board)
            inp = self.ui.get_input(('q', 'w', 'a', 's', 'd'))
            self._handle_input(inp)
            self._update_state()

        if self.state == WON:
            self.ui.display_board(self.board)
            print('YOU WIN :)')

        if self.state == LOST:
            self.ui.display_board(self.board)
            print('YOU LOSE :(')
            
    def _handle_input(self, inp):
        if inp == 'q':
            self.state = QUIT
        elif inp == 'w':
            self.board.move(UP)
        elif inp == 'a':
            self.board.move(LEFT)
        elif inp == 's':
            self.board.move(DOWN)
        elif inp == 'd':
            self.board.move(RIGHT)
    
    def _update_state(self):
        are_zeros = False
        for row in self.board:
            for col in row:
                if col == 2048:
                    self.state = WON
                    return
                if not are_zeros and col == 0:
                    are_zeros = True
                    break
        
        if not are_zeros:
            for i in range(self.board.rows):
                for j in range(self.board.cols):
                    if not self.board.is_stuck(i, j):
                        return
            self.state = LOST
    