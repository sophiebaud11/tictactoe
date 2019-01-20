from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_FIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

turncount = 0

@app.route("/")
def index():
    global turncount
    turncount = 0
    print(turncount)
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
    return render_template("game.html", game=session["board"], turn=session["turn"], turncount=turncount)

@app.route("/check")
def check(game, turn):
    print("check city")
    print(game)
    for i in range(3):
        if (game[i][0] == game[i][1]) and (game[i][1] == game[i][2]) and game[i][1]:
            print(game[i][0])
            print(game[i][1])
            print(game[i][2])
            print("row")
            return True
        elif (game[0][i] == game[1][i]) and (game[1][i] == game[2][i]) and game[2][i]:
            print(game[0][i])
            print(game[1][i])
            print(game[2][i])
            print("column")
            return True
    if game[0][0] == game[1][1] and game[1][1] == game[2][2] and game[2][2]:
        print("diagonal1")
        return True
    elif game[2][0] == game[1][1] and game[1][1] == game[0][2] and game[0][2]:
        print("diagonal2")
        return True
    return False


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    global turncount
    turncount += 1
    if turncount % 2 == 0:
        session["turn"] = "X"
        session["board"][row][col] = "O"
    else:
        session["turn"] = "O"
        session["board"][row][col] = "X"
    print(session["board"])
    if check(session["board"], session["turn"]) == True:
        if session["turn"] == "O":
            winner = "X"
        else:
            winner = "O"
        return render_template("game.html", game=session["board"], turn=session["turn"], turncount=turncount, winner = winner)
    return redirect(url_for("index", game=session["board"], turncount=turncount, turn=session["turn"]))

@app.route("/minimax")
def minimax(game,turn):
    return value

@app.route("/reset")
def reset():
    session.clear()
    global turncount
    turncount = 0
    return redirect(url_for("index", turncount=turncount))
