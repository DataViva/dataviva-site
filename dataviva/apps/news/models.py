from dataviva import db
from sqlalchemy import ForeignKey


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
    last_modification = db.Column(db.DateTime)
    publish_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    show_home = db.Column(db.Boolean)
    dual_language = db.Column(db.Boolean)
    subject_id = db.Column(db.Integer, ForeignKey('news_subject.id'))
    subject = db.relationship('PublicationSubject', backref='news_publication', lazy='eager')

    def date(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Publication %r>' % (self.title)


class PublicationSubject(db.Model):
    __tablename__ = 'news_subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<PublicationSubject %r>' % (self.name)
