ALTER TABLE `dataviva`.`blog_post` 
CHANGE COLUMN `release_date` `publish_date` DATETIME NULL DEFAULT NULL AFTER `thumb`,
CHANGE COLUMN `postage_date` `last_modification` DATETIME NULL DEFAULT NULL ;

UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-04 16:14:08' WHERE `id`='4';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-05-31 15:11:28' WHERE `id`='6';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-04 16:15:21' WHERE `id`='7';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-04 16:17:39' WHERE `id`='8';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-05-31 15:35:02' WHERE `id`='9';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-05 13:43:46' WHERE `id`='20';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-05 13:44:30' WHERE `id`='30';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-05 19:46:57' WHERE `id`='31';
UPDATE `dataviva`.`blog_post` SET `publish_date`='2016-07-05 19:09:19' WHERE `id`='32';