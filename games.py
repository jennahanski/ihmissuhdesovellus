from db import db

def get_all_games():
    sql = "SELECT id, name FROM games ORDER BY name"
    return db.session.execute(sql).fetchall()

def search_game(query):
    sql = "SELECT id, name FROM games WHERE lower(name) LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def add_game(name, creator_id):
    sql = "INSERT INTO games (name, creator_id) VALUES (:name, :creator_id) RETURNING id"
    result = db.session.execute(sql, {"name":name, "creator_id":creator_id})
    game_id = result.fetchone()[0]
    db.session.commit()
    return game_id

def get_game_info(game_id):
    sql = "SELECT G.name, U.username FROM games G, users U WHERE G.id=:game_id AND G.creator_id=U.id"
    return db.session.execute(sql, {"game_id": game_id}).fetchone()

def get_reviews(game_id):
    sql = "SELECT U.username, R.comment, R.grade FROM reviews R, users U WHERE R.user_id=U.id AND R.game_id=:game_id AND visible=1 ORDER BY R.id"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def get_my_reviews(user_id):
    sql = "SELECT R.id, R.comment, R.grade FROM reviews R WHERE R.user_id=:user_id AND visible=1 ORDER BY R.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def add_review(game_id, user_id, comment, grade):
    sql = "INSERT INTO reviews (user_id, game_id, comment, grade, visible) \
            VALUES (:user_id, :game_id, :comment, :grade, 1)"
    db.session.execute(sql, {"user_id":user_id, "game_id":game_id, "comment":comment, "grade":grade})
    db.session.commit()

def remove_review(r_id, user_id):
    sql = "UPDATE reviews SET visible=0 WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":r_id, "user_id":user_id})
    db.session.commit()
    