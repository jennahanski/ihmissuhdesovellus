from db import db

def add_to_list(game_id, user_id, status, playtime, platform):
    if check_for_list(user_id, game_id):
        sql = "UPDATE stats SET playtime=:playtime, platform=:platform, status=:status WHERE user_id=:user_id AND game_id=:game_id"
    else:
        sql = "INSERT INTO stats (user_id, game_id, status, playtime, platform, favorite) VALUES (:user_id, :game_id, :status, :playtime, :platform, 0)"

    db.session.execute(sql, {"user_id":user_id, "game_id":game_id, "status":status, "playtime":playtime, "platform":platform})
    db.session.commit()

def check_for_list(user_id, game_id):
    try:
        sql = "SELECT user_id FROM stats S WHERE user_id=:user_id AND game_id=:game_id"
        return db.session.execute(sql, {"user_id":user_id, "game_id":game_id}).fetchone()[0]
    except:
        return False

def get_my_lists(user_id):
    sql = "SELECT S.game_id, G.name, S.status, S.playtime, S.platform, S.favorite FROM stats S, games G WHERE S.user_id=:user_id AND S.game_id=G.id AND G.visible=True ORDER BY S.id"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def get_playtime(user_id):
    sql = "SELECT SUM(S.playtime) FROM stats S, games G WHERE S.user_id=:user_id AND G.id=S.game_id AND G.visible=True"
    return db.session.execute(sql, {"user_id":user_id}).fetchone()

def add_to_favorites(game_id, user_id, favorite):
    if check_for_list(user_id, game_id):
        sql = "UPDATE stats SET favorite=:favorite WHERE user_id=:user_id AND game_id=:game_id"
    else:
        sql = "INSERT INTO stats (user_id, game_id, favorite) VALUES (:user_id, :game_id, :favorite)"
    db.session.execute(sql, {"favorite":favorite, "user_id":user_id, "game_id":game_id})
    db.session.commit()

def is_favorite(user_id, game_id):
    sql = "SELECT S.user_id FROM stats S WHERE S.favorite=1 AND S.user_id=:user_id AND S.game_id=:game_id"
    return db.session.execute(sql, {"user_id":user_id, "game_id":game_id}).fetchone()