CREATE TABLE blog_post(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    subject varchar (100) NULL,
    text_content text NULL,
    image_path varchar (250) NULL,
    thumb_path varchar (250) NULL,
    postage_date datetime NULL,
    PRIMARY KEY (id)
);

CREATE TABLE blog_author(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    post_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (post_id) REFERENCES blog_post(id)
);