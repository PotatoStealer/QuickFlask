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

@app.route('/play', methods=['GET'])
def play():
    # Just re-route everything to here. Any moves, either invalid or # valid should just be re-routed here, so that the board state can be rendered, and we can display error messages from `ui.errmsg` without doing other weird hacks. 
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    move = request.args.get('player_input')

    if move:
        s, r = game.prompt(move)
        if s:
            start, end = r
            game.update(start, end)
            game.next_turn()
            ui.inputlabel = f'{game.turn} player:'
            ui.board = game.display()
            ui.errmsg = None
        else:
            ui.errmsg = r
        return redirect('/play')
    else:
        return render_template('chess.html', ui=ui)

    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')