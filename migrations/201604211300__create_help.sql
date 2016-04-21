CREATE TABLE help_subject(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar (50) NULL,
    PRIMARY KEY (id)
);
​
CREATE TABLE help_subject_question(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    description varchar (400) NULL,
    answer varchar (400) NULL,
    subject_id int UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (subject_id) REFERENCES help_subject(id)
);
