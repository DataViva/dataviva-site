CREATE TABLE search_profile(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE search_question(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    description varchar (400) NULL,
    answer varchar (400) NULL,
    profile_id int UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (profile_id) REFERENCES search_profile(id)
);

CREATE TABLE search_selector(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE search_question_selector(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    question_id int UNSIGNED NOT NULL,
    selector_id int UNSIGNED NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (question_id) REFERENCES search_question(id),
    FOREIGN KEY (selector_id) REFERENCES search_selector(id)
);
