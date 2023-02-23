from db import db

def get_reviews(game_id):
    sql = "SELECT U.username, R.comment, R.grade, R.id, R.user_id FROM reviews R, users U WHERE R.user_id=U.id AND R.game_id=:game_id AND R.visible=1 ORDER BY U.username"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def get_average(game_id):
    try:
        sql = "SELECT SUM(R.grade)::float/COUNT(R.grade) FROM reviews R WHERE R.game_id=:game_id AND R.visible=1"
        return db.session.execute(sql, {"game_id":game_id}).fetchone()[0]
    except:
        return 0

def get_my_reviews(user_id):
    sql = "SELECT R.id, R.comment, R.grade, G.name, R.game_id FROM reviews R, games G WHERE R.user_id=:user_id AND R.game_id=G.id AND R.visible=1 AND G.visible=True ORDER BY R.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def check_for_review(user_id, game_id):
    sql = "SELECT R.id FROM reviews R, users U WHERE R.user_id=:user_id AND R.game_id=:game_id AND visible=1"
    return db.session.execute(sql, {"user_id":user_id, "game_id":game_id}).fetchone()

def add_review(game_id, user_id, comment, grade):
    sql = "INSERT INTO reviews (user_id, game_id, comment, grade, visible) \
            VALUES (:user_id, :game_id, :comment, :grade, 1)"
    db.session.execute(sql, {"user_id":user_id, "game_id":game_id, "comment":comment, "grade":grade})
    db.session.commit()

def edit_review(r_id, comment, grade):
    sql = "UPDATE reviews SET comment=:comment, grade=:grade WHERE id=:id AND visible=1"
    db.session.execute(sql, {"comment":comment, "grade":grade, "id":r_id})
    db.session.commit()

def remove_review(r_id, user_id):
    sql = "UPDATE reviews SET visible=0 WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":r_id, "user_id":user_id})
    db.session.commit()