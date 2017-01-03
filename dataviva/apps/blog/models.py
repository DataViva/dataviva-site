from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.ext.declarative import declarative_base 
from dataviva import db
import flask_whooshalchemy


association_table = db.Table('blog_post_subject',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('blog_subject.id'))
)

class Post(db.Model):
    __tablename__ = 'blog_post'
    __searchable__ = ['title', 'author', 'main_subject', 'text_call']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    author = db.Column(db.String(100))
    text_call = db.Column(db.String(500))
    text_content = db.Column(db.Text(4194304))
    thumb = db.Column(db.Text(4194304))
    thumb_src = db.Column(db.String(400))
    publish_date = db.Column(db.DateTime)
    last_modification = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    show_home = db.Column(db.Boolean)
    language = db.Column(db.String(2))
    main_subject = db.Column(db.String(50))

    subjects = db.relationship(
        "Subject",
        secondary=association_table,
        backref=db.backref('posts', lazy='dynamic'))

    def date_str(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Post %r>' % (self.title)

    def add_subjects(self, subjects_input, language):
        for subject_input in subjects_input:
            subject = Subject.query.filter_by(
                name=subject_input, language=language).first()
            if not subject:
                self.subjects.append(Subject(subject_input, language))
            else:
                self.subjects.append(subject)
            if subject_input == subjects_input[0]:
                self.main_subject = subject_input


class Subject(db.Model):
    __tablename__ = 'blog_subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    language = db.Column(db.String(2))

    def __init__(self, name=None, language=None):
        self.name = name
        self.language = language

    def __repr__(self):
        return '<PostSubject %r (%r)>' % (self.name, self.language)
