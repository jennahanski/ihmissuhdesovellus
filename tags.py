from db import db

def check_tag(name, user_id, game_id):
    try:
        sql = "SELECT id FROM tags WHERE name=:name AND creator_id=:user_id AND game_id=:game_id"
        return db.session.execute(sql, {"name":name, "user_id":user_id, "game_id":game_id}).fetchone()
    except:
        return False

def get_my_tags(game_id, user_id):
    sql = "SELECT id, name, creator_id FROM tags WHERE game_id=:game_id AND creator_id=:user_id ORDER BY id"
    return db.session.execute(sql, {"game_id":game_id, "user_id":user_id}).fetchall()

def get_games(tag):
    sql = "SELECT DISTINCT G.name FROM games G, tags T WHERE G.id=T.game_id AND T.name=:tag"
    return db.session.execute(sql, {"tag":tag}).fetchall()

def get_all_tags(game_id):
    sql = "SELECT T.name, COUNT(U.id) FROM tags T LEFT JOIN users U ON U.id=T.creator_id WHERE game_id=:game_id GROUP BY T.name"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def add_tags(creator_id, game_id, name):
    sql = "INSERT INTO tags (creator_id, game_id, name) VALUES (:creator_id, :game_id, :name) RETURNING id"
    tag_id = db.session.execute(sql, {"creator_id":creator_id, "game_id":game_id, "name":name}).fetchone()
    db.session.commit()