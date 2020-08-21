from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board, MoveHistory

app = Flask(__name__)
ui = WebInterface()
game = Board()
movehistory = MoveHistory(100)
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

@app.route('/play', methods=['POST', 'GET'])
def play():
    if request.method == "POST":
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
                if game.promotion(end) == True:
                    promotion = 1
                    col, row = end[0], end[1]
                    return redirect('/promote', coord = f'{col}{row}', promotion = 1)
            else:
                ui.errmsg = response
            return redirect('/play')
    else:
        return render_template('chess.html', ui=ui, game=game)

    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote', methods=['POST', 'GET'])
def promote():
    if request.method == "POST":
        confirm = request.form['promote_q']
        if confirm == "yes":
            piece = game.promotion()

app.run('0.0.0.0')

@app.route('/undo')
def undo():
    move = movehistory.pop()
    game.undo(move)
    game.next_turn()
    return redirect('/play')