from flask import Flask
from flask import render_template, redirect, request
from chess import Board
from movehistory import MoveHistory
from webinterface import WebInterface

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
    ui.board = game.display()
    wname, bname = request.form['wname'], request.form['bname']
    if wname and bname:
        return redirect('/play')
    else:
        return redirect('/')

@app.route('/play', methods=['POST', 'GET'])
def play():
    if request.method == "POST":
        # Use this form to take in anything. It's great
        inp = request.form['player_input']
        if game.parseinput(inp) != True:
            ui.errmsg = game.parseinput(inp)
        else:
            start, end = inp.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            game.update(start, end)
            game.next_turn()
            movehistory.push((start, end))
            ui.inputlabel = f'{game.turn} player:'
            ui.board = game.display()
            ui.errmsg = None
            if game.pawnscanpromote():
                return redirect("/promote")
        return redirect('/play')    
    else:
        return render_template('chess.html', ui=ui, game=game)

    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote', methods=['POST', 'GET'])
def promote():
    inp = request.form.get('promote', None)
    if inp:
        game.promotepawns(PieceClass=inp)
        ui.board = game.display()
        game.next_turn()
        return redirect('/play')
    return render_template('promote.html', ui=ui, game=game)

@app.route('/undo', methods = ['POST','GET'])
def undo():    
    if movehistory.empty():
        ui.errmsg = "Move history is empty"
    else:
        start, end = movehistory.pop()
        game.move(end, start)
        game.next_turn()
        ui.board = game.display()
    return redirect('/play')

app.run('0.0.0.0')
