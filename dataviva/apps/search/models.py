from dataviva import db
from flask import g
from sqlalchemy import ForeignKey
from dataviva.utils.title_case import title_case


class SearchQuestionSelector(db.Model):
    __tablename__ = 'search_question_selector'
    question_id = db.Column(db.Integer, ForeignKey('search_question.id'), primary_key=True)
    selector_id = db.Column(db.Integer, ForeignKey('search_selector.id'), primary_key=True)
    order = db.Column(db.Integer)
    selector = db.relationship("SearchSelector")


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
    id = db.Column(db.Integer, primary_key=True)
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
    selectors = db.relationship("SearchQuestionSelector")
    profile_id = db.Column(db.Integer, ForeignKey('search_profile.id'))

    def selectors_str(self):
        selector_names = [selectors.selector_id for selectors in self.selectors]
        return ', '.join(selector_names)

    def description(self):
        lang = getattr(g, "locale", "en")
        return getattr(self, "description_" + lang)

    def selectors_sorted(self):
        selectors = self.selectors
        selectors_sorted = sorted(selectors, key=lambda selectors: selectors.order)
        return [x.selector_id for x in selectors_sorted]

    def __repr__(self):
        return '<SearchQuestion %r>' % (self.description())
