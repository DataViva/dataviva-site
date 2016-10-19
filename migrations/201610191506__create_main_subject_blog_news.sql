ALTER TABLE blog_post
ADD COLUMN `main_subject` VARCHAR(50) NULL AFTER `language`;

UPDATE blog_post AS p
join (SELECT post_id, name FROM blog_subject, blog_post_subject WHERE id=subject_id) AS a
ON p.id=a.post_id
SET p.main_subject=a.name
WHERE p.main_subject is null;

ALTER TABLE news_publication
ADD COLUMN `main_subject` VARCHAR(50) NULL AFTER `language`;

UPDATE news_publication AS p
join (SELECT publication_id, name from news_subject, news_publication_subject WHERE id=subject_id) AS a
ON p.id=a.publication_id
SET p.main_subject=a.name
WHERE p.main_subject is null;
