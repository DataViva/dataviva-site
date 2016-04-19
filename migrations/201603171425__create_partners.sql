CREATE TABLE partner_call(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    link varchar(250) NULL,
    active int NULL,
    PRIMARY KEY (id)
);

CREATE TABLE calls(
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    title varchar (400) NULL,
    link varchar(250) NULL,
    active int NULL,
    PRIMARY KEY (id)
);