CREATE TABLE IF NOT EXISTS `my_case_details` (
    `pk_case_id`            INTEGER UNIQUE NOT NULL PRIMARY KEY,
    `created_at`            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `uniform_case_number`   VARCHAR(20) NOT NULL,
    `file_date`             DATE,
    `case_status`           VARCHAR(255) NOT NULL,
    `case_status_date`      DATE NOT NULL,
    `style`                 VARCHAR(255),
    `is_active`             TINYINT(1) NOT NULL,
    `appear_by_date`        DATE,
    `cross_refs`            VARCHAR(255),
    `related_case`          JSON
);
