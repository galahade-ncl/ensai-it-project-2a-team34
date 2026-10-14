-----------------------------------------------------
-- User table
-----------------------------------------------------
DROP TABLE IF EXISTS user_table CASCADE;
CREATE TABLE user_table (
    id_user      SERIAL PRIMARY KEY,
    username     VARCHAR(30) UNIQUE,
    password     VARCHAR(256),
    email        VARCHAR(50),
    access_token VARCHAR(255)
);

-----------------------------------------------------
-- Project table
-----------------------------------------------------

DROP TABLE IF EXISTS project_table CASCADE;
CREATE TABLE project_table (
    id_project      SERIAL PRIMARY KEY,
    name_project    VARCHAR,
    id_user         INT,
    HMAC_key        BYTEA,
    FOREIGN KEY (id_user)
    REFERENCES user_table(id_user)
);

-----------------------------------------------------
-- File table
-----------------------------------------------------

DROP TABLE IF EXISTS file_table CASCADE;
CREATE TABLE file_table (
    id_file         SERIAL PRIMARY KEY,
    name_file       VARCHAR,
    date            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "path"          VARCHAR,
    type_file       VARCHAR,
    project_file    INT,
    FOREIGN KEY (project_file)
    REFERENCES project_table(id_project)
);

-----------------------------------------------------
-- Audit table
-----------------------------------------------------

DROP TABLE IF EXISTS audit_table CASCADE;
CREATE TABLE audit_table (
    id_audit                                  SERIAL PRIMARY KEY,
    id_project                                INT,
    date                                      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_vulnerability                       FLOAT,
    total_critical_vulnerability              FLOAT,
    complexity                                FLOAT,
    energy_comsumption                        FLOAT,
    carbon_emission_gco2e                     FLOAT,
    status_qualitygate                        VARCHAR,
    FOREIGN KEY (id_project)
    REFERENCES project_table(id_project)
);