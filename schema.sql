CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    year INTEGER
);

CREATE TABLE stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games,
    status INTEGER,
    playtime INTEGER,
    platform TEXT,
    favorite INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games,
    comment TEXT,
    grade INTEGER,
    visible INTEGER
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games,
    name TEXT UNIQUE
);