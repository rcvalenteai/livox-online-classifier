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