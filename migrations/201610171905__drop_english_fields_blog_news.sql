ALTER TABLE blog_post
ADD COLUMN language VARCHAR(2) NULL DEFAULT 'pt';

ALTER TABLE news_publication
ADD COLUMN language VARCHAR(2) NULL DEFAULT 'pt';

ALTER TABLE `dataviva`.`news_publication` 
DROP COLUMN `dual_language`,
DROP COLUMN `text_content_en`,
DROP COLUMN `text_call_en`,
DROP COLUMN `title_en`,
CHANGE COLUMN `title_pt` `title` VARCHAR(400) NULL DEFAULT NULL ,
CHANGE COLUMN `text_call_pt` `text_call` VARCHAR(500) NULL DEFAULT NULL ,
CHANGE COLUMN `text_content_pt` `text_content` LONGTEXT NULL DEFAULT NULL ;

ALTER TABLE `dataviva`.`blog_post` 
DROP COLUMN `dual_language`,
DROP COLUMN `text_content_en`,
DROP COLUMN `text_call_en`,
DROP COLUMN `title_en`,
CHANGE COLUMN `title_pt` `title` VARCHAR(400) NULL DEFAULT NULL ,
CHANGE COLUMN `text_call_pt` `text_call` VARCHAR(500) NULL DEFAULT NULL ,
CHANGE COLUMN `text_content_pt` `text_content` LONGTEXT NULL DEFAULT NULL ;
