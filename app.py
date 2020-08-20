from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board

app = Flask(__name__)
ui = WebInterface()
game = Board()
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame', methods=["POST"])
def newgame():
    game.start()
    # This gets a string display of the board state, which we display # using jinja2 using magic
    ui.board = game.display()
    wname, bname = request.form['wname'], request.form['bname']
    if wname and bname:
        return redirect('/play')
    else:
        return redirect('/')

@app.route('/play', methods=['POST'])
def play():
    move = request.form['player_input']

    if move:
        success, response = game.prompt(move)
        if success:
            start, end = response
            game.update(start, end)
            game.next_turn()
            ui.inputlabel = f'{game.turn} player:'
            ui.board = game.display()
            ui.errmsg = None
        else:
            ui.errmsg = response
        return redirect('/play')
    else:
        return render_template('chess.html', ui=ui)

    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')