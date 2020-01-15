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