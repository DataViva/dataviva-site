from dataviva import db
from sqlalchemy import ForeignKey


search_question_selector = db.Table(
    'search_question_selector',
    db.Column('question_id', db.Integer, ForeignKey('search_question.id')),
    db.Column('selector_id', db.Integer, ForeignKey('search_selector.id'))
)


class SearchQuestion(db.Model):
    __tablename__ = 'search_question'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(400))
    answer = db.Column(db.String(400))
    selectors = db.relationship("SearchSelector", secondary=search_question_selector, backref="selector")
    profile_id = db.Column(db.Integer, ForeignKey('search_profile.id'))

    def selectors_str(self):
        selector_names = [selector.name for selector in self.selectors]
        return ', '.join(selector_names)

    def __repr__(self):
        return '<SearchQuestion %r>' % (self.description)


class SearchProfile(db.Model):
    __tablename__ = 'search_profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    questions = db.relationship("SearchQuestion", backref='search_question')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<SearchProfile %r>' % (self.name)


class SearchSelector(db.Model):
    __tablename__ = 'search_selector'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<SearchSelector %r>' % (self.name)
