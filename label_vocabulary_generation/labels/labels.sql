/*
Images
Primary_Key -> image_id
 */
 CREATE TABLE Images
        (image_id VARCHAR(36),
         location VARCHAR(256),
         Constraint p_key_images Primary Key (image_id));

/*
Labels
Primary Key -> image_id, label
Foreign Key -> Images.image_id
 */
 CREATE TABLE Labels
        (image_id VARCHAR(36),
         label VARCHAR(32),
         confidence REAL,
         Constraint p_key_labels Primary Key (image_id, label),
         Foreign Key (image_id) References Images(image_id));

/*
         Foreign Key (image_id) References Images(image_id)
 */


/*
Tags
Primary Key -> image_id, tag
Foreign Key -> Images.image_id
 */
 CREATE TABLE Tags
        (image_id VARCHAR(36),
         tag VARCHAR(32),
         Constraint p_key_tags Primary Key (image_id, tag),
         Foreign Key (image_id) References Images(image_id));

/*
         Foreign Key (image_id) References Images(image_id)
 */

/*
Logs
Primary Key -> log_id
 */
 CREATE TABLE Logs
      (log_id VARCHAR(36),
       phrase VARCHAR(256),
       is_list BOOLEAN,
       question_phrase VARCHAR(256),
       list_phrase VARCHAR(256),
       timestamp DATETIME,
       Constraint p_key_logs Primary Key (log_id));

/*
Primary Key -> entity_id
Foreign Key -> Logs.log_id, Image.image_id
 */
 CREATE TABLE Entity
      (entity_id VARCHAR(36),
       log_id VARCHAR(36),
       image_id VARCHAR(36),
       entity VARCHAR(256),
       Constraint p_key_entity Primary Key (entity_id),
       Foreign Key(log_id) References Logs(log_id));


DROP TABLE Tags;
DROP TABLE Images;
DROP TABLE Labels;
DROP TABLE Entity;
DROP TABLE Logs;