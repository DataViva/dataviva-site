CREATE TABLE scholar_article(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    theme varchar (250) NULL,
    abstract varchar (250) NULL,
    file_path varchar (255) NULL,
    postage_date datetime NULL,
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
CREATE TABLE scholar_key_word(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE scholar_article_key_word(
    article_id int UNSIGNED NOT NULL,
    key_word_id int UNSIGNED NOT NULL,
    FOREIGN KEY (article_id) REFERENCES scholar_article(id),
    FOREIGN KEY (key_word_id) REFERENCES scholar_key_word(id)
);


​