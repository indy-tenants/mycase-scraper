CREATE TABLE IF NOT EXISTS `my_case_event` (
    `pk_event_id`       INTEGER UNIQUE NOT NULL PRIMARY KEY,
    `fk_case_id`        INTEGER NOT NULL,
    `event_type`        VARCHAR(255),
    `event_date`        DATE,
    `event_time`        TIME,
    `description`       VARCHAR(255),
    `judge`             VARCHAR(255),
    `case_event`        JSON,
    `hearing_event`     JSON,
    `disp_event`        JSON,
    `j_event`           JSON,
    `s_event`           JSON,
    `v_event`           JSON,
    `a_event`           JSON
);
