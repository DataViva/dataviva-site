from dataviva import db
from sqlalchemy import ForeignKey


class HelpSubjectQuestion(db.Model):
    __tablename__ = 'help_subject_question'
    id = db.Column(db.Integer, primary_key=True)
    description_pt = db.Column(db.String(400))
    description_en = db.Column(db.String(400))
    answer_pt = db.Column(db.Text(4194304))
    answer_en = db.Column(db.Text(4194304))
    subject_id = db.Column(db.Integer, ForeignKey('help_subject.id'))

    def __repr__(self):
        return '<SubjectQuestion %r>' % (self.description)


class HelpSubject(db.Model):
    __tablename__ = 'help_subject'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(50))
    name_pt = db.Column(db.String(50))
    questions = db.relationship("HelpSubjectQuestion", backref='help_subject_question')

    def __repr__(self):
        return '<Subject %r>' % (self.name)
