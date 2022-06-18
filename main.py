from board import Board
from ui import Ui
from app import App

if __name__ == '__main__':
    board = Board(4, 4)
    ui = Ui()
    app = App(board, ui)
    app.run()
    