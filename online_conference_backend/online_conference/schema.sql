DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    login_methods TEXT NOT NULL CHECK (login_method IN ('google', 'facebook', 'default'))
);