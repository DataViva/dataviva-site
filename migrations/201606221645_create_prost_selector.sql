create table blog_post_subject(
    post_id int UNSIGNED NOT NULL, 
    subject_id int UNSIGNED NOT NULL,
    CONSTRAINT pk_ps PRIMARY KEY(post_id, subject_id),
    FOREIGN KEY (post_id) REFERENCES blog_post(id),
    FOREIGN KEY (subject_id) REFERENCES blog_subject(id)
);

insert blog_post_subject (post_id, subject_id)
    select id, subject_id from blog_post;

ALTER TABLE blog_post
  DROP FOREIGN KEY blog_post_ibfk_1;
 