ALTER TABLE help_subject_question ADD active tinyint(1) AFTER subject_id;

UPDATE help_subject_question 
SET active = 1;
