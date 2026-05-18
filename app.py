
from flask import Flask, render_template, redirect, url_for
from src.game_logic import TicTacToeGame
from src.score_storage import load_score, save_score

app = Flask(__name__)

game = TicTacToeGame()
score = load_score()


@app.route('/')
def index():
    return render_template(
        'index.html',
        board=game.board,
        current_player=game.current_player,
        winner=game.check_winner(),
        draw=game.check_draw(),
        score=score
    )


@app.route('/play/<int:cell>')
def play(cell):

    game.play_move(cell)

    winner = game.check_winner()
    draw = game.check_draw()

    # Record result once when the game ends
    if (winner or draw) and not game.result_recorded:
        if winner == "X":
            score["X"] += 1
        elif winner == "O":
            score["O"] += 1
        elif draw:
            score["draws"] += 1

            save_score(score)
            game.result_recorded = True

    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    game.reset()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
