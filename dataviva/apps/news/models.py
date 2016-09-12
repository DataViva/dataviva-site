from sqlalchemy import ForeignKey, Table, Column
from dataviva import db


association_table = db.Table('news_publication_subject',
    db.Column('publication_id', db.Integer, db.ForeignKey('news_publication.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('news_subject.id'))
)

class Publication(db.Model):
    # TODO - Alter publication.thumb column to db.Column(db.String(400))
    __tablename__ = 'news_publication'
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
        "PublicationSubject",
        secondary=association_table,
        backref=db.backref('publications', lazy='dynamic'))

    def date(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Publication %r>' % (self.title)


class PublicationSubject(db.Model):
    __tablename__ = 'news_subject'
    id = db.Column(db.Integer, primary_key=True)
    name_pt = db.Column(db.String(50))
    name_en = db.Column(db.String(50))

    def __init__(self, name_pt=None, name_en=None):
        self.name_pt = name_pt
        self.name_en = name_en

    def __repr__(self):
        return '<PublicationSubject %r>' % (self.name_pt)
