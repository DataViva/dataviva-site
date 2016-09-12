from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.ext.declarative import declarative_base 
from dataviva import db


association_table = db.Table('blog_post_subject',
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('blog_subject.id'))
)

class Post(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title_pt = db.Column(db.String(400))
    title_en = db.Column(db.String(400))
    author = db.Column(db.String(100))
    text_call_pt = db.Column(db.String(500))
    text_call_en = db.Column(db.String(500))
    text_content_pt = db.Column(db.Text(4194304))
    text_content_en = db.Column(db.Text(4194304))
    thumb = db.Column(db.Text(4194304))
    publish_date = db.Column(db.DateTime)
    last_modification = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    show_home = db.Column(db.Boolean)
    dual_language = db.Column(db.Boolean)

    subjects = db.relationship(
        "Subject",
        secondary=association_table,
        backref=db.backref('posts', lazy='dynamic'))

    def date_str(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Post %r>' % (self.title)


class Subject(db.Model):
    __tablename__ = 'blog_subject'
    id = db.Column(db.Integer, primary_key=True)
    name_pt = db.Column(db.String(50))
    name_en = db.Column(db.String(50))

    def __repr__(self):
        return '<PostSubject %r>' % (self.name_pt)
