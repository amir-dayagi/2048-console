class Ui:
    def display_board(self, board):
        print('', '-'*(board.cols*6+board.cols-1))
        for row in board:
            print('|      '*board.cols + '|')
            print('|', end='')
            for col in row:
                if col == 0:
                    print(' '*6, end='|')
                elif 0 < col < 10:
                    print(f'   {col}  ', end='|')
                elif 9 < col < 100:
                    print(f'  {col}  ', end='|')
                elif 99 < col < 1000:
                    print(f'  {col} ', end='|')
                else:
                    print(f' {col} ', end='|')
            print('\n'+'|      '*board.cols + '|')
            print('', '-'*(board.cols*6+board.cols-1))

    def get_input(self, legal_input):
        inp = input().lower()
        while inp not in legal_input:
            inp = input().lower()
        return inp