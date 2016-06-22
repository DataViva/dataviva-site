create table blog_post_subject(
    id_post int not null,
    id_subject int not null
);

insert blog_post_subject (id_post, id_subject)
    select id, subject_id from blog_post;
