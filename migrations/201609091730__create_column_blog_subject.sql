ALTER TABLE `dataviva`.`blog_subject` 
ADD COLUMN `name_en` VARCHAR(50) NULL DEFAULT NULL AFTER `name_pt`;

UPDATE blog_subject SET name_en='' WHERE name_en IS NULL;