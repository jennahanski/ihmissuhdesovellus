from db import db

def get_all_games():
    sql = "SELECT id, name FROM games WHERE visible=1 ORDER BY name"
    return db.session.execute(sql).fetchall()

def add_game(name, creator_id):
    sql = "INSERT INTO games (name, creator_id, visible) VALUES (:name, :creator_id, 1) RETURNING id"
    result = db.session.execute(sql, {"name":name, "creator_id":creator_id})
    game_id = result.fetchone()[0]
    db.session.commit()
    return game_id

def get_game_info(game_id):
    sql = "SELECT G.name, U.username FROM games G, users U WHERE G.id=:game_id AND G.creator_id=U.id"
    return db.session.execute(sql, {"game_id": game_id}).fetchone()

def get_reviews(game_id):
    sql = "SELECT U.username, R.comment, R.grade FROM reviews R, users U WHERE R.user_id=U.id AND R.game_id=:game_id ORDER BY R.id"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def add_review(game_id, user_id, comment, grade):
    sql = "INSERT INTO reviews (user_id, game_id, comment, grade) \
            VALUES (:user_id, :game_id, :comment, :grade)"
    db.session.execute(sql, {"user_id":user_id, "game_id":game_id, "comment":comment, "grade":grade})
    db.session.commit()
    