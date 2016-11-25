ALTER TABLE `dataviva`.`blog_post` 
ADD COLUMN `thumb_src` VARCHAR(400) NULL DEFAULT NULL AFTER `main_subject`;

ALTER TABLE `dataviva`.`news_publication` 
ADD COLUMN `thumb_src` VARCHAR(400) NULL DEFAULT NULL AFTER `main_subject`;
