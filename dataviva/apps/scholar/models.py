from dataviva import db
from sqlalchemy import ForeignKey


article_author_table = db.Table('article_author',
    db.Column('article_id', db.Integer(), db.ForeignKey('scholar_article.id')),
    db.Column('author_id', db.Integer(), db.ForeignKey('scholar_author.id'))
)

article_key_word_table = db.Table('article_key_word',
    db.Column('article_id', db.Integer(), db.ForeignKey('scholar_article.id')),
    db.Column('key_word_id', db.Integer(), db.ForeignKey('scholar_key_word.id'))
)


class Article(db.Model):
    __tablename__ = 'scholar_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    abstract = db.Column(db.String(250))
    file_path = db.Column(db.String(100))
    postage_date = db.Column(db.DateTime)
    theme = db.relationship('Theme', backref='scholar_article', lazy='dynamic')
    author = db.relationship('Author', secondary=article_author_table)
    key_word = db.relationship('KeyWord', secondary=article_key_word_table)

    def __init__(self, title=None, abstract=None, file_path=None, postage_date=None):
        self.title = title
        self.abstract = abstract
        self.file_path = file_path
        self.postage_date = postage_date

    def __repr__(self):
        return '<Title %r>' % (self.title)


class Theme(db.Model):
    __tablename__ = 'scholar_theme'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50))
    article_id = db.Column(db.Integer, ForeignKey('scholar_article.id'))

    def __init__(self, theme=None, article_id=None):
        self.theme = theme
        self.article_id = article_id

    def __repr__(self):
        return '<Theme %r>' % (self.theme)


class Author(db.Model):
    __tablename__ = 'scholar_author'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __init__(self, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<Author %r>' % (self.first_name)


class KeyWord(db.Model):
    __tablename__ = 'scholar_key_word'
    id = db.Column(db.Integer, primary_key=True)
    key_word = db.Column(db.String(50))

    def __init__(self, key_word=None):
        self.key_word = key_word

    def __repr__(self):
        return '<Key-Word %r>' % (self.key_word)
