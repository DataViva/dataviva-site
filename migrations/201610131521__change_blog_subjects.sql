ALTER TABLE blog_subject
ADD COLUMN language VARCHAR(2) NULL DEFAULT 'pt';

INSERT INTO blog_subject
(name_pt, language)
(SELECT name_en, 'en' FROM blog_subject WHERE name_en != '');

ALTER TABLE blog_subject
DROP COLUMN name_en,
CHANGE COLUMN name_pt name VARCHAR(50) NULL DEFAULT NULL;
