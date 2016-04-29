CREATE TABLE scholar_article(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    theme varchar (250) NULL,
    abstract text NULL,
    postage_date datetime NULL,
    approval_status TINYINT(1) NULL,
    PRIMARY KEY (id)
);
​​
CREATE TABLE scholar_author(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    article_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (article_id) REFERENCES scholar_article(id)
);
​
CREATE TABLE scholar_keyword(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE scholar_article_keyword(
    article_id int UNSIGNED NOT NULL,
    keyword_id int UNSIGNED NOT NULL,
    FOREIGN KEY (article_id) REFERENCES scholar_article(id),
    FOREIGN KEY (keyword_id) REFERENCES scholar_keyword(id)
);


​