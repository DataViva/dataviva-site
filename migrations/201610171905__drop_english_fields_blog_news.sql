ALTER TABLE blog_post
ADD COLUMN language VARCHAR(2) NULL DEFAULT 'pt';

ALTER TABLE news_publication
ADD COLUMN language VARCHAR(2) NULL DEFAULT 'pt';
