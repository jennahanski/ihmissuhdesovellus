from app import app
from flask import render_template, redirect, request
import users

@app.route("/")
def index():
    return render_template("index.html") 

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