-----------------------------------------------------
-- Utilisateur
-----------------------------------------------------
DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE user (
    id_user    SERIAL PRIMARY KEY,
    username     VARCHAR(30) UNIQUE,
    password     VARCHAR(256),
    email        VARCHAR(50),
    access_token VARCHAR(255)
);

'''
    id_code    SERIAL PRIMARY KEY,
    cle_HMAC    VARCHAR,
    lt_package    ARRAY,
    empreinte    INTEGER
'''