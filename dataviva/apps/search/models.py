from dataviva import db
from flask import g
from sqlalchemy import ForeignKey
from dataviva.utils.title_case import title_case


search_question_selector = db.Table(
    'search_question_selector',
    db.Column('question_id', db.Integer, ForeignKey('search_question.id')),
    db.Column('selector_id', db.Integer, ForeignKey('search_selector.id'))
)


class SearchQuestion(db.Model):
    __tablename__ = 'search_question'
    id = db.Column(db.Integer, primary_key=True)
    description_pt = db.Column(db.String(400))
    description_en = db.Column(db.String(400))
    answer = db.Column(db.String(400))
    selectors = db.relationship("SearchSelector", secondary=search_question_selector, backref="selector")
    profile_id = db.Column(db.Integer, ForeignKey('search_profile.id'))

    def description(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "description_" + lang))

    def __repr__(self):
        return '<SearchQuestion %r>' % (self.description)


class SearchProfile(db.Model):
    __tablename__ = 'search_profile'
    id = db.Column(db.Integer, primary_key=True)
    name_pt = db.Column(db.String(50))
    name_en = db.Column(db.String(50))
    questions = db.relationship("SearchQuestion", backref='search_question')

    def name(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "name_" + lang))

    def __repr__(self):
        return '<SearchProfile %r>' % (self.name)


class SearchSelector(db.Model):
    __tablename__ = 'search_selector'
    id = db.Column(db.Integer, primary_key=True)
    name_pt = db.Column(db.String(50))
    name_en = db.Column(db.String(50))

    def name(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "name_" + lang))

    def __repr__(self):
        return '<SearchSelector %r>' % (self.name)
