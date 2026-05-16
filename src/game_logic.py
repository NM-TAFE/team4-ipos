class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.result_recorded = False

    def check_winner(self):
        # Winning combinations
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for a, b, c in win_combinations:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return None

    def check_draw(self):
        return ' ' not in self.board and self.check_winner() is None

    def play_move(self, cell):
        if self.board[cell] != ' ':
            return

        if self.check_winner() or self.check_draw():
            return

        self.board[cell] = self.current_player

        if not self.check_winner() and not self.check_draw():
            # Keep original turn switching behaviour
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.result_recorded = False
