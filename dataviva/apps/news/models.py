from dataviva import db
from sqlalchemy import ForeignKey


class Publication(db.Model):
    __tablename__ = 'news_publication'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    author = db.Column(db.String(100))
    text_call = db.Column(db.String(500))
    text_content = db.Column(db.Text(4194304))
    thumb = db.Column(db.Text(4194304))
    last_modification = db.Column(db.DateTime)
    publish_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    show_home = db.Column(db.Boolean)
    subject = db.relationship('PublicationSubject', backref='news_publication', lazy='eager')

    def subject_str(self):
        return self.subject[0].name

    def date(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Publication %r>' % (self.title)


class PublicationSubject(db.Model):
    __tablename__ = 'news_author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    publication_id = db.Column(db.Integer, ForeignKey('news_publication.id'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<PublicationSubject %r>' % (self.name)
