CREATE TABLE news_publication(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    subject varchar (100) NULL,
    text_call varchar (500) NULL,
    text_content longtext NULL,
    image longtext NULL,
    thumb longtext NULL,
    postage_date datetime NULL,
    release_date datetime NULL,
    PRIMARY KEY (id)
);

CREATE TABLE news_author(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    publication_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (publication_id) REFERENCES news_publication(id)
);