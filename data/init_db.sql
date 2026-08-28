-----------------------------------------------------
-- User table
-----------------------------------------------------
DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE user (
    id_user    SERIAL PRIMARY KEY,
    username     VARCHAR(30) UNIQUE,
    password     VARCHAR(256),
    email        VARCHAR(50),
    access_token VARCHAR(255)
);

-----------------------------------------------------
-- File table
-----------------------------------------------------

DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE file (
    id_file    SERIAL PRIMARY KEY,
    name_file  VARCHAR
    id_user    FOREIGN KEY,
    HMAC_key    BYTEA,
);