import json
import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Initialise game board and current player
board = [' '] * 9
current_player = 'X'

# Persistent score
SCORE_FILE = "score.json"
score = {"X": 0, "O": 0, "draws": 0}
result_recorded = False


def load_score():
    """Load score from score.json if it exists."""
    global score
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            score["X"] = int(data.get("X", 0))
            score["O"] = int(data.get("O", 0))
            score["draws"] = int(data.get("draws", 0))
        except (OSError, json.JSONDecodeError, ValueError):
            score = {"X": 0, "O": 0, "draws": 0}


def save_score():
    """Save score to score.json."""
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(score, f, indent=2)


# Load score once when app starts
load_score()


def check_winner():
    # Winning moves
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
        (0, 4, 8), (2, 4, 6)  # Diagonal
    ]
    for move in win_combinations:
        if board[move[0]] == board[move[1]] == board[move[2]] != ' ':
            return board[move[0]]
    return None


def check_draw():
    return ' ' not in board and check_winner() is None


@app.route('/')
def index():
    winner = check_winner()
    draw = check_draw()
    return render_template(
        'index.html',
        board=board,
        current_player=current_player,
        winner=winner,
        draw=draw,
        score=score
    )


@app.route('/play/<int:cell>')
def play(cell):
    global current_player, result_recorded

    # Optional: stop moves after game ends
    if check_winner() or check_draw():
        return redirect(url_for('index'))

    if board[cell] == ' ':
        board[cell] = current_player

        winner = check_winner()
        draw = check_draw()

        # Record result once when the game ends
        if (winner or draw) and not result_recorded:
            if winner == "X":
                score["X"] += 1
            elif winner == "O":
                score["O"] += 1
            elif draw:
                score["draws"] += 1

            save_score()
            result_recorded = True

        # Keep original turn switching behaviour
        if not winner and not draw:
            current_player = 'O' if current_player == 'X' else 'X'

    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    global board, current_player, result_recorded
    board = [' '] * 9
    current_player = 'X'
    result_recorded = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
