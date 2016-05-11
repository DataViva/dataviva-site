CREATE TABLE blog_subject(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE blog_post(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    author varchar (100) NULL,
    text_call varchar (500) NULL,
    text_content longtext NULL,
    thumb longtext NULL,
    postage_date datetime NULL,
    release_date datetime NULL,
    active TINYINT(1) NULL,
    subject_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (subject_id) REFERENCES blog_subject(id)
);
