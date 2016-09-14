CREATE TABLE `news_publication_subject` (
  `publication_id` int(10) unsigned NOT NULL,
  `subject_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`publication_id`,`subject_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `news_publication_subject_ibfk_1` FOREIGN KEY (`publication_id`) REFERENCES `news_publication` (`id`),
  CONSTRAINT `news_publication_subject_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `news_subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT news_publication_subject (publication_id, subject_id)
SELECT id, subject_id FROM news_publication;

ALTER TABLE news_publication
DROP FOREIGN KEY news_publication_ibfk_1;
 
ALTER TABLE news_publication
DROP subject_id;

ALTER TABLE news_subject
CHANGE COLUMN name name_pt VARCHAR(50) NULL DEFAULT NULL,
ADD COLUMN name_en VARCHAR(50) NULL DEFAULT NULL;

UPDATE news_subject SET name_en='' WHERE name_en IS NULL;
