from app import app
from db import db
from flask import render_template, redirect, request
import users
import games

@app.route("/")
def index():
    return render_template("index.html", games=games.get_all_games()) 

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]

    return render_template("result.html", results=games.search_game(query))

@app.route("/game/<int:game_id>")
def show_game(game_id):
    info = games.get_game_info(game_id)

    reviews = games.get_reviews(game_id)

    return render_template("game.html", id=game_id, name=info[0], creator=info[1], reviews=reviews)

@app.route("/review", methods=["POST"])
def review():
    users.check_csrf()

    game_id = request.form["game_id"]
    grade = int(request.form["grade"])
    if grade < 1 or grade > 10:
        return render_template("error.html", message="Arvosanan tulee olla välillä 1-10")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Lyhennä kommenttia")

    if len(comment) == 0:
        comment = "-"
    
    games.add_review(game_id, users.user_id(), comment, grade)

    return redirect("/game/"+str(game_id))

@app.route("/add", methods=["GET", "POST"])
def add_game():
    if request.method == "GET":
        return render_template("add.html")
    
    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Nimen tulee olla 1-20 merkkiä pitkä.")
        
        game_id = games.add_game(name, users.user_id())
        return redirect("/game/"+str(game_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 2 or len(username) > 20:
            return render_template("error.html", message="Tunnuksen on oltava 2-20 merkkiä pitkä.")
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää.")
        if password1 == "":
            return render_template("error.html", message="Salasana ei voi olla tyhjä.")
    
    if not users.register(username, password1):
        return render_template("error.html", message="Rekisteröinti epäonnistui.")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if not users.login(username, password):
        return render_template("error.html", message="Antamasi tunnus tai salasana on virheellinen")
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")