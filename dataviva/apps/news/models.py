from dataviva import db
from sqlalchemy import ForeignKey


class Publication(db.Model):
    __tablename__ = 'news_publication'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    subject = db.Column(db.String(100))
    text_call = db.Column(db.String(500))
    text_content = db.Column(db.Text(4194304))
    thumb = db.Column(db.Text(4194304))
    last_modification = db.Column(db.DateTime)
    publish_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    show_home = db.Column(db.Boolean)
    authors = db.relationship('AuthorNews', backref='news_publication', lazy='eager')

    def authors_str(self):
        author_names = [author.name for author in self.authors]
        return ', '.join(author_names)

    def date(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Publication %r>' % (self.title)


class AuthorNews(db.Model):
    __tablename__ = 'news_author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    publication_id = db.Column(db.Integer, ForeignKey('news_publication.id'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<AuthorNews %r>' % (self.name)
