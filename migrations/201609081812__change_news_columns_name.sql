ALTER TABLE `dataviva`.`news_publication` 
CHANGE COLUMN `title` `title_pt` VARCHAR(400) NULL DEFAULT NULL ,
CHANGE COLUMN `text_call` `text_call_pt` VARCHAR(500) NULL DEFAULT NULL ,
CHANGE COLUMN `text_content` `text_content_pt` LONGTEXT NULL DEFAULT NULL ;