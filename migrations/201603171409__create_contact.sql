CREATE TABLE `contact_message` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `name` VARCHAR(100) NULL COMMENT '',
  `email` VARCHAR(100) NULL COMMENT '',
  `subject` VARCHAR(200) NULL COMMENT '',
  `message` TEXT NULL COMMENT '',
  `postage_date` DATETIME NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');