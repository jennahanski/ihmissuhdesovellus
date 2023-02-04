import secrets
import os
from db import db
from flask import request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return True

def logout():
    del session["user_id"]
    del session["user_name"]

def user_id():
    return session.get("user_id", 0)

def get_user_id(username):
    sql = "SELECT U.id FROM users U WHERE U.username=:username"
    return db.session.execute(sql, {"username":username}).fetchone()[0]

def username():
    return session.get("user_name", "")

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)