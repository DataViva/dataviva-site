from dataviva import db
from sqlalchemy import ForeignKey

article_keyword_table = db.Table(
    'scholar_article_keyword',
    db.Column('article_id', db.Integer(), db.ForeignKey('scholar_article.id')),
    db.Column('keyword_id', db.Integer(), db.ForeignKey('scholar_keyword.id'))
)


class Article(db.Model):
    __tablename__ = 'scholar_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    abstract = db.Column(db.Text())
    theme = db.Column(db.String(250))
    file_path = db.Column(db.String(255))
    postage_date = db.Column(db.DateTime)
    authors = db.relationship('Author', backref='scholar_article', lazy='eager')
    keywords = db.relationship('KeyWord', secondary=article_keyword_table)

    def authors_str(self):
        author_names = [author.name for author in self.authors]
        return ', '.join(author_names)

    def keywords_str(self):
        keyword_names = [keyword.name for keyword in self.keywords]
        return ', '.join(keyword_names)

    def date_str(self):
        return self.postage_date.strftime('%d/%m/%Y')

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
    __tablename__ = 'scholar_keyword'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Keyword %r>' % (self.name)
