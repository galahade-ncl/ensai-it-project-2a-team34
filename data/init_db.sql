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
    secretHMACkey   BYTEA,
    FOREIGN KEY (id_user)
    REFERENCES user_table(id_user)
);

-----------------------------------------------------
-- Audit table
-----------------------------------------------------

DROP TABLE IF EXISTS audit_table CASCADE;
CREATE TABLE audit_table (
    id_audit                SERIAL PRIMARY KEY,
    id_project              INT,
    date                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    complexity              FLOAT,
    energy_comsumption      FLOAT,
    carbon_emission_gco2e   FLOAT,
    type_qualitygate        VARCHAR,
    status_qualitygate      VARCHAR,
    certificate_pdf         BYTEA,
    certificate_signed      JSONB,
    certificate_id          TEXT UNIQUE,
    sbom_content            BYTEA,
    FOREIGN KEY (id_project) REFERENCES project_table(id_project)
);