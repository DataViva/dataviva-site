from dataviva import db
from sqlalchemy import ForeignKey

article_key_word_table = db.Table(
    'scholar_article_key_word',
    db.Column('article_id', db.Integer(), db.ForeignKey('scholar_article.id')),
    db.Column('key_word_id', db.Integer(), db.ForeignKey('scholar_key_word.id'))
)


class Article(db.Model):
    __tablename__ = 'scholar_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    abstract = db.Column(db.String(250))
    theme = db.Column(db.String(250))
    file_path = db.Column(db.String(255))
    postage_date = db.Column(db.DateTime)
    author = db.relationship('Author', backref='scholar_article', lazy='dynamic')
    key_words = db.relationship('KeyWord', secondary=article_key_word_table)

    def __repr__(self):
        return '<Article %r>' % (self.title)


class Author(db.Model):
    __tablename__ = 'scholar_author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    article_id = db.Column(db.Integer, ForeignKey('scholar_article.id'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % (self.name)


class KeyWord(db.Model):
    __tablename__ = 'scholar_key_word'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Key-Word %r>' % (self.name)
