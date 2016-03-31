CREATE TABLE news_publication(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    subject varchar (100) NULL,
    text_call varchar (500) NULL,
    text_content longtext NULL,
    thumb longtext NULL,
    publish_date datetime NULL,
    last_modification datetime NULL,
    active TINYINT(1) NULL,
    show_home TINYINT(1) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE news_author(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    publication_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (publication_id) REFERENCES news_publication(id)
);
