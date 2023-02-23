from db import db

def get_all_games():
    sql = "SELECT id, name FROM games WHERE visible=True ORDER BY name"
    return db.session.execute(sql).fetchall()

def search_game(query):
    sql = "SELECT id, name FROM games WHERE visible=True AND lower(name) LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def add_game(name, year, creator_id):
    sql = "INSERT INTO games (name, creator_id, year) VALUES (:name, :creator_id, :year) RETURNING id"
    result = db.session.execute(sql, {"name":name, "creator_id":creator_id, "year":year})
    game_id = result.fetchone()[0]
    db.session.commit()
    return game_id

def edit_game(name, year, game_id):
    sql = "UPDATE games SET name=:name, year=:year WHERE id=:game_id"
    db.session.execute(sql, {"name":name, "year":year, "game_id":game_id})
    db.session.commit()

def delete_game(game_id):
    sql = "UPDATE games SET visible=False WHERE id=:game_id"
    db.session.execute(sql, {"game_id":game_id})
    db.session.commit()

def get_game_info(game_id):
    sql = "SELECT G.name, U.username, G.year FROM games G, users U WHERE G.id=:game_id AND G.creator_id=U.id"
    return db.session.execute(sql, {"game_id": game_id}).fetchone()