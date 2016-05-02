CREATE TABLE search_profile(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name_pt varchar (50) NULL,
    name_en varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE search_question(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    description_pt varchar (400) NULL,
    description_en varchar (400) NULL,
    answer varchar (400) NULL,
    profile_id int UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (profile_id) REFERENCES search_profile(id)
);

CREATE TABLE search_selector(
    id varchar(50) NOT NULL,
    name_pt varchar (50) NULL,
    name_en varchar (50) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE search_question_selector(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    question_id int UNSIGNED NOT NULL,
    selector_id varchar(50) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (question_id) REFERENCES search_question(id),
    FOREIGN KEY (selector_id) REFERENCES search_selector(id)
);

INSERT INTO search_selector (id, name_pt, name_en) VALUES ('bra', 'Locations', 'Localidades');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('cbo', 'Occupations', 'Ocupações');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('cnae', 'Industries', 'Atividades Econômicas');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('hs', 'Products', 'Produtos');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('wld', 'Trade partners', 'Parceiro Comerciais');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('university', 'Universities', 'Universidades');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('course_hedu', 'Major', 'Ensino Superior');
INSERT INTO search_selector (id, name_pt, name_en) VALUES ('course_sc', 'Basic course', 'Curso Básico');
