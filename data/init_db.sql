-----------------------------------------------------
-- Information code
-----------------------------------------------------
DROP TABLE IF EXISTS simulation_code CASCADE;
CREATE TABLE simulation_code (
    id_code    SERIAL PRIMARY KEY,
    cle_HMAC    VARCHAR,
    lt_package    ARRAY,
    empreinte    INTEGER
);
