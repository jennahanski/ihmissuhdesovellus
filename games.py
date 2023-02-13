from db import db

def get_all_games():
    sql = "SELECT id, name FROM games ORDER BY name"
    return db.session.execute(sql).fetchall()

def search_game(query):
    sql = "SELECT id, name FROM games WHERE lower(name) LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def add_game(name, year, creator_id):
    sql = "INSERT INTO games (name, creator_id, year) VALUES (:name, :creator_id, :year) RETURNING id"
    result = db.session.execute(sql, {"name":name, "creator_id":creator_id, "year":year})
    game_id = result.fetchone()[0]
    db.session.commit()
    return game_id

def get_game_info(game_id):
    sql = "SELECT G.name, U.username, G.year FROM games G, users U WHERE G.id=:game_id AND G.creator_id=U.id"
    return db.session.execute(sql, {"game_id": game_id}).fetchone()

def add_to_list(game_id, user_id, status, playtime, platform):
    if check_for_list(user_id, game_id):
        sql = "UPDATE stats SET playtime=:playtime, platform=:platform, status=:status WHERE user_id=:user_id AND game_id=:game_id"
    else:
        sql = "INSERT INTO stats (user_id, game_id, status, playtime, platform, favorite) VALUES (:user_id, :game_id, :status, :playtime, :platform, 0)"

    db.session.execute(sql, {"user_id":user_id, "game_id":game_id, "status":status, "playtime":playtime, "platform":platform})
    db.session.commit()

def check_for_list(user_id, game_id):
    sql = "SELECT S.user_id FROM stats S WHERE S.user_id=:user_id AND S.game_id=:game_id"
    return db.session.execute(sql, {"user_id":user_id, "game_id":game_id}).fetchone()

def get_my_lists(user_id):
    sql = "SELECT S.game_id, G.name, S.status, S.playtime, S.platform, S.favorite FROM stats S, games G WHERE S.user_id=:user_id AND S.game_id=G.id ORDER BY S.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_playtime(user_id):
    sql = "SELECT SUM(S.playtime) FROM stats S WHERE S.user_id=:user_id"
    return db.session.execute(sql, {"user_id":user_id}).fetchone()

def add_to_favorites(game_id, user_id, favorite):
    sql = "UPDATE stats SET favorite=:favorite WHERE user_id=:user_id AND game_id=:game_id"
    db.session.execute(sql, {"favorite":favorite, "user_id":user_id, "game_id":game_id})
    db.session.commit()

def is_favorite(user_id, game_id):
    sql = "SELECT S.user_id FROM stats S WHERE S.favorite=1 AND S.user_id=:user_id AND S.game_id=:game_id"
    return db.session.execute(sql, {"user_id":user_id, "game_id":game_id}).fetchone()

def get_reviews(game_id):
    sql = "SELECT U.username, R.comment, R.grade FROM reviews R, users U WHERE R.user_id=U.id AND R.game_id=:game_id AND visible=1 ORDER BY U.username"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def get_average(game_id):
    try:
        sql = "SELECT SUM(R.grade)::float/COUNT(R.grade) FROM reviews R WHERE R.game_id=:game_id AND visible=1"
        return db.session.execute(sql, {"game_id":game_id}).fetchone()[0]
    except:
        return 0

def get_my_reviews(user_id):
    sql = "SELECT R.id, R.comment, R.grade, G.name, R.game_id FROM reviews R, games G WHERE R.user_id=:user_id AND R.game_id=G.id AND visible=1 ORDER BY R.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def check_for_review(user_id, game_id):
    sql = "SELECT R.id FROM reviews R, users U WHERE R.user_id=:user_id AND R.game_id=:game_id"
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

def check_tag(name, user_id, game_id):
    try:
        sql = "SELECT id FROM tags WHERE name=:name AND creator_id=:user_id AND game_id=:game_id"
        return db.session.execute(sql, {"name":name, "user_id":user_id, "game_id":game_id}).fetchone()
    except:
        return False

def get_my_tags(game_id, user_id):
    sql = "SELECT id, name, creator_id FROM tags WHERE game_id=:game_id AND creator_id=:user_id ORDER BY id"
    return db.session.execute(sql, {"game_id":game_id, "user_id":user_id}).fetchall()

def get_all_tags(game_id):
    sql = "SELECT T.name, COUNT(U.id) FROM tags T LEFT JOIN users U ON U.id=T.creator_id WHERE game_id=:game_id GROUP BY T.name"
    return db.session.execute(sql, {"game_id":game_id}).fetchall()

def add_tags(creator_id, game_id, name):
    sql = "INSERT INTO tags (creator_id, game_id, name) VALUES (:creator_id, :game_id, :name) RETURNING id"
    tag_id = db.session.execute(sql, {"creator_id":creator_id, "game_id":game_id, "name":name}).fetchone()
    db.session.commit()