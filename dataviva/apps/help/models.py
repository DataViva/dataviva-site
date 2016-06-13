from dataviva import db
from flask import g
from sqlalchemy import ForeignKey
from dataviva.utils.title_case import title_case


class HelpSubjectQuestion(db.Model):
    __tablename__ = 'help_subject_question'
    id = db.Column(db.Integer, primary_key=True)
    description_pt = db.Column(db.String(400))
    description_en = db.Column(db.String(400))
    answer_pt = db.Column(db.Text(4194304))
    answer_en = db.Column(db.Text(4194304))
    subject_id = db.Column(db.Integer, ForeignKey('help_subject.id'))
    subject = db.relationship('HelpSubject', backref='help_subject_question', lazy='eager')
    active = db.Column(db.Boolean)

    def description(self):
        lang = getattr(g, "locale", "en")
        return getattr(self, "description_" + lang)

    def answer(self):
        lang = getattr(g, "locale", "en")
        return getattr(self, "answer_" + lang)

    def __repr__(self):
        return '<SubjectQuestion %r>' % (self.description())


class HelpSubject(db.Model):
    __tablename__ = 'help_subject'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(50))
    name_pt = db.Column(db.String(50))

    def name(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "name_" + lang))

    def __repr__(self):
        return '<Subject %r>' % (self.name())
