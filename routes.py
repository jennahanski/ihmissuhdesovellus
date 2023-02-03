from app import app
from db import db
from flask import render_template, redirect, request
import users
import games

@app.route("/")
def index():
    return render_template("index.html", games=games.get_all_games()) 

@app.route("/user/<username>")
def userpage(username):
    user_id = users.user_id()
    my_reviews = games.get_my_reviews(user_id)

    return render_template("userpage.html", name=username, reviews=my_reviews, id=user_id)

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]

    return render_template("result.html", results=games.search_game(query))

@app.route("/game/<int:game_id>", methods=["GET", "POST"])
def show_game(game_id):
    user_id = users.user_id()
    favorite = games.is_favorite(user_id, game_id)

    if request.method == "GET":
        info = games.get_game_info(game_id)
        reviews = games.get_reviews(game_id)
        check = games.check_for_review(user_id, game_id)
        if check:
            message = "Edit your review"
        else:
            message = "Add a review"

        return render_template("game.html", id=game_id, name=info[0], creator=info[1], year=info[2], reviews=reviews, message=message, favorite=favorite)
    
    if request.method == "POST":
        users.check_csrf()
        if request.form["fav"]:
            favorite= request.form["fav"]
            games.add_to_favorites(game_id, user_id, favorite)
            return redirect("/game/"+str(game_id))
        else:
            status = request.form["list"]
            if status == "0":
                games.add_to_list(game_id, user_id, status, 0, "")

            return render_template("addtolist.html", id=game_id, status=status)

@app.route("/review", methods=["POST"])
def review():
    users.check_csrf()

    game_id = request.form["game_id"]
    grade = int(request.form["grade"])

    if grade < 1 or grade > 10:
        return render_template("error.html", message="The grade must be between 1 and 10")

    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Comment is too long")

    if len(comment) == 0:
        comment = "-"

    check = games.check_for_review(users.user_id(), game_id)
    if check:
        games.edit_review(check[0], comment, grade)
    else:
        games.add_review(game_id, users.user_id(), comment, grade)

    return redirect("/game/"+str(game_id))

@app.route("/add", methods=["GET", "POST"])
def add_game():
    if request.method == "GET":
        return render_template("add.html")
    
    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        year = request.form["year"]
        if len(name) < 1 or len(name) > 30:
            return render_template("error.html", message="Length of the name must be between 1 and 30 characters")
        
        if len(year) != 4:
            return render_template("error.html", message="Incorrect year")
        
        game_id = games.add_game(name, year, users.user_id())
        return redirect("/game/"+str(game_id))

@app.route("/game/<int:game_id>/addtolist/<int:status>", methods=["POST"])
def add_to_list(game_id, status):
    user_id = users.user_id()
    users.check_csrf()
    playtime = int(request.form["playtime"])
    platform = request.form["platform"]

    games.add_to_list(game_id, user_id, status, playtime, platform)
    return redirect("/game/"+str(game_id))

@app.route("/remove", methods=["GET", "POST"])
def remove_review():
    if request.method == "GET":
        my_reviews = games.get_my_reviews(users.user_id())
        return render_template("remove.html", content=my_reviews)

    if request.method == "POST":
        users.check_csrf()
        if "review" in request.form:
            choices = request.form.getlist["review"]
            for review in choices:
                games.remove_review(review, users.user_id())

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 2 or len(username) > 20:
            return render_template("error.html", message="Username must be between 2 and 20 characters")
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="The passwords don't match")
        if password1 == "":
            return render_template("error.html", message="Password can't be empty")
    
    if not users.register(username, password1):
        return render_template("error.html", message="Registration failed")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if not users.login(username, password):
        return render_template("error.html", message="Incorrect username or password")
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")