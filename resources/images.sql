/*
Images
Primary_Key -> image_id
 */
 CREATE TABLE Images
        (image_id VARCHAR(36),
         location VARCHAR(256),
         Constraint p_key_images Primary Key (image_id));