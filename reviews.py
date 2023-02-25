from db import db

def get_reviews(game_id):
    sql = "SELECT U.username, R.comment, R.grade, R.id, R.user_id FROM reviews R, users U WHERE R.user_id=U.id AND R.game_id=:game_id AND R.visible=1 ORDER BY U.username"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def get_average(game_id):
    
    sql = "SELECT ROUND((SUM(R.grade)::float/COUNT(R.grade))::numeric, 2) FROM reviews R WHERE R.game_id=:game_id AND R.visible=1"
    return db.session.execute(sql, {"game_id":game_id}).fetchone()[0]

def get_best_games():
    sql = "SELECT DISTINCT G.id, G.name, (SELECT ROUND((SUM(A.grade)::float/COUNT(A.grade))::numeric, 2) FROM reviews A WHERE A.game_id=G.id AND A.visible=1) as avg \
        FROM reviews R, games G WHERE R.game_id=G.id AND G.visible=True ORDER BY avg DESC LIMIT 10"
    return db.session.execute(sql).fetchall()

def get_my_reviews(user_id):
    sql = "SELECT R.id, R.comment, R.grade, G.name, R.game_id FROM reviews R, games G WHERE R.user_id=:user_id AND R.game_id=G.id AND R.visible=1 AND G.visible=True ORDER BY R.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_new_reviews():
    sql = "SELECT U.username, G.name, R.grade, G.id, \
        (SELECT CASE WHEN LENGTH(comment)>25 THEN LEFT(comment, 25) || '...' ELSE comment END FROM reviews WHERE id=R.id) FROM users U, reviews R, games G WHERE R.game_id=G.id AND R.user_id=U.id ORDER BY R.id DESC LIMIT 5"
    return db.session.execute(sql).fetchall()

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