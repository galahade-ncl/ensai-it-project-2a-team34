-----------------------------------------------------
-- User table
-----------------------------------------------------
DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE user (
    id_user      SERIAL PRIMARY KEY,
    username     VARCHAR(30) UNIQUE,
    password     VARCHAR(256),
    email        VARCHAR(50),
    access_token VARCHAR(255)
);

-----------------------------------------------------
-- Project table
-----------------------------------------------------

DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE project (
    id_project      SERIAL PRIMARY KEY,
    name_project    VARCHAR,
    id_user         FOREIGN KEY,
    HMAC_key        BYTEA,
);

-----------------------------------------------------
-- File table
-----------------------------------------------------

DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE file (
    id_file         SERIAL PRIMARY KEY,
    name_file       VARCHAR,
    type_file       VARCHAR,
    project_file    FOREIGN KEY,
);

-----------------------------------------------------
-- Audit table
-----------------------------------------------------

DROP TABLE IF EXISTS user CASCADE;
CREATE TABLE audit (
    id_audit                                  SERIAL PRIMARY KEY,
    id_project                                FOREIGN KEY,
    date                                      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    max_vulnerability                         FLOAT,
    max_critical_vulnerability                FLOAT,
    complexity                                FLOAT,
    energy_comsumption                        FLOAT,
    carbon_emission_gco2e                     FLOAT,
    status_qualitygate                        VARCHAR
);