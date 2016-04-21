from dataviva import db
from sqlalchemy import ForeignKey
​
​
class HelpSubjectQuestion(db.Model):
    __tablename__ = 'help_subject_question'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(400))
    answer = db.Column(db.String(400))
    subject_id = db.Column(db.Integer, ForeignKey('help_subject.id'))
​
    def __repr__(self):
        return '<SubjectQuestion %r>' % (self.description)
​
​
class HelpSubject(db.Model):
    __tablename__ = 'help_subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    questions = db.relationship("HelpSubjectQuestion", backref='help_subject_question')
​
    def __repr__(self):
        return '<Subject %r>' % (self.name)