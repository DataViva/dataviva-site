CREATE TABLE blog_post(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    text_desc varchar (500) NULL,
    image_path varchar (100) NULL,
    thumb_path varchar (100) NULL,
    postage_date datetime NULL,
    PRIMARY KEY (id)
);

CREATE TABLE blog_category(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    category varchar (50) NULL,
    post_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (post_id) REFERENCES blog_post(id)
);

CREATE TABLE blog_author(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    first_name varchar (50) NULL,
    last_name varchar (50) NULL,
    PRIMARY KEY (id)
);
​
CREATE TABLE blog_post_author(
    post_id int UNSIGNED NOT NULL,
    author_id int UNSIGNED NOT NULL,
    FOREIGN KEY (post_id) REFERENCES blog_post(id),
    FOREIGN KEY (author_id) REFERENCES blog_author(id)
);