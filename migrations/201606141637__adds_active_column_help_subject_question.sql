ALTER TABLE help_subject_question ADD active tinyint(1) AFTER subject_id;

SET SQL_SAFE_UPDATES = 0;

UPDATE help_subject_question 
SET active = 1;

SET SQL_SAFE_UPDATES = 1;