ALTER TABLE news_subject
ADD COLUMN language VARCHAR(2) NULL DEFAULT 'pt';

INSERT INTO news_subject
(name_pt, language)
(SELECT name_en, 'en' FROM news_subject WHERE name_en != '');

ALTER TABLE news_subject
DROP COLUMN name_en,
CHANGE COLUMN name_pt name VARCHAR(50) NULL DEFAULT NULL;
