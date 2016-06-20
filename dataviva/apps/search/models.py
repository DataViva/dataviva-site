from dataviva import db
from flask import g
from sqlalchemy import ForeignKey
from dataviva.utils.title_case import title_case


class SearchProfile(db.Model):
    __tablename__ = 'search_profile'
    id = db.Column(db.String(50), primary_key=True)
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
    id = db.Column(db.String(50), primary_key=True)
    name_pt = db.Column(db.String(50))
    name_en = db.Column(db.String(50))

    def name(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "name_" + lang))

    def __repr__(self):
        return '<SearchSelector %r>' % (self.name)


class SearchQuestion(db.Model):
    __tablename__ = 'search_question'
    id = db.Column(db.Integer, primary_key=True)
    description_pt = db.Column(db.String(400))
    description_en = db.Column(db.String(400))
    answer = db.Column(db.String(400))
    profile_id = db.Column(db.String(50), ForeignKey('search_profile.id'))
    selectors = db.Column(db.String(400))

    def description(self):
        lang = getattr(g, "locale", "en")
        return getattr(self, "description_" + lang)

    def __repr__(self):
        return '<SearchQuestion %r>' % (self.description())
