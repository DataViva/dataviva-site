ALTER TABLE `dataviva`.`blog_post` 
CHANGE COLUMN `release_date` `publish_date` DATETIME NULL DEFAULT NULL AFTER `thumb`,
CHANGE COLUMN `postage_date` `last_modification` DATETIME NULL DEFAULT NULL ;

UPDATE `dataviva`.`blog_post` SET `publish_date`=`last_modification` WHERE `publish_date` IS NULL; 
