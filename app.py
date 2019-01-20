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
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
    return render_template("game.html", game=session["board"], turn=session["turn"], turncount=turncount)

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
    print(turncount)
    print(session["turn"])
    return redirect(url_for("index", game=session["board"], turncount=turncount, turn=session["turn"]))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))
