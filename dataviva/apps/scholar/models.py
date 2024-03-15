# -*- coding: utf-8 -*-
from dataviva import db
import datetime
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
    file_url = db.Column(db.String(400))
    theme = db.Column(db.String(250))
    postage_date = db.Column(db.DateTime)
    publication_date = db.Column(db.DateTime)
    approval_status = db.Column(db.Boolean)
    postage_img = db.Column(db.String())    
    authors = db.relationship('AuthorScholar',
                                backref='scholar_article',
                                lazy='joined',
                                cascade='all, delete-orphan')
    keywords = db.relationship('KeyWord',
                                secondary=article_keyword_table,
                                backref=db.backref('articles', lazy='dynamic'))

    def authors_str(self):
        author_names = [author.name for author in self.authors]
        return ', '.join(author_names)
    
    def keywords_str(self):
        keyword_names = [keyword.name for keyword in self.keywords]
        return ', '.join(keyword_names)

    def date_str(self, lang, dateType):
        if(dateType):
            monthsPt = [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]

            date = dateType.strftime("%B %d, %Y")       
            
            if(lang == 'en'):
                return dateType.strftime("%d of %B, %Y")
            else:
                dateObj = datetime.datetime.strptime(date, "%B %d, %Y")
                month = monthsPt[dateObj.month - 1] 
                return "{} de {}, {}".format(dateObj.day, month, dateObj.year)
        return None
            
    
    def __repr__(self):
        return '<Article %r>' % (self.title)


class AuthorScholar(db.Model):
    __tablename__ = 'scholar_author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    article_id = db.Column(db.Integer, ForeignKey('scholar_article.id'))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<AuthorScholar %r>' % (self.name)


class KeyWord(db.Model):
    __tablename__ = 'scholar_keyword'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Keyword %r>' % (self.name)
