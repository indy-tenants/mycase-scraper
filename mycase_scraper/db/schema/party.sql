CREATE TABLE IF NOT EXISTS `my_case_party` (
    `pk_case_party_id`      INTEGER UNIQUE NOT NULL PRIMARY KEY,
    `party_id`              INTEGER,
    `fk_case_id`            INTEGER NOT NULL,
    `base_connection_key`   VARCHAR(255),
    `name`                  VARCHAR(255),
    `extended_name`         VARCHAR(255),
    `dob`                   DATE,
    `address`               JSON,
    `removed_date`          DATE,
    `removed_reason`        VARCHAR(255),
    `attorney`              JSON
);
