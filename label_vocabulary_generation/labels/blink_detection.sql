/*
Blink
Primary Key -> blink_id
 */
CREATE TABLE Blink
        (blink_id VARCHAR(32),
         group_id VARCHAR(32),
         label VARCHAR(2),
         Constraint p_key_blink Primary Key (blink_id));

/*
Phone
Primary Key -> blink_id
Foreign Key -> Blink.blink_id
 */
CREATE TABLE Phone
        (blink_id VARCHAR(32),
         lighting REAL,
         time TIMESTAMP,
         dev_orientation BOOLEAN,
         spacial_x REAL,
         spacial_y REAL,
         spacial_z REAL,
         face_x REAL,
         face_y REAL,
         face_z REAL,
         camera_res_x INTEGER,
         camera_res_y INTEGER,
         Constraint p_key_phone Primary Key (blink_id),
         Foreign Key (blink_id) References Blink(blink_id));

/*
Survey
Primary Key -> group_id
Foreign Key -> Blink.group_id
 */
CREATE TABLE Survey
        (group_id VARCHAR(32),
         face_lighting VARCHAR,
         environment VARCHAR,
         distance VARCHAR,
         accessories VARCHAR,
         Constraint p_key_survey Primary Key (group_id),
         Foreign Key (group_id) References Blink(group_id));