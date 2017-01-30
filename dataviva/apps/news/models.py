from sqlalchemy import ForeignKey, Table, Column
from dataviva import db


association_table = db.Table('news_publication_subject',
    db.Column('publication_id', db.Integer, db.ForeignKey('news_publication.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('news_subject.id'))
)


class Publication(db.Model):
    # TODO - Alter publication.thumb column to db.Column(db.String(400))
    __tablename__ = 'news_publication'
    __searchable__ = ['title', 'author', 'main_subject', 'text_call']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    author = db.Column(db.String(100))
    text_call = db.Column(db.String(500))
    text_content = db.Column(db.Text(4194304))
    thumb = db.Column(db.Text(4194304))
    thumb_src = db.Column(db.String(400))
    publish_date = db.Column(db.DateTime)
    last_modification = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    show_home = db.Column(db.Boolean)
    language = db.Column(db.String(2))
    main_subject = db.Column(db.String(50))

    subjects = db.relationship(
        "PublicationSubject",
        secondary=association_table,
        backref=db.backref('publications', lazy='dynamic'))

    def date(self):
        return self.publish_date.strftime('%d/%m/%Y')

    def __repr__(self):
        return '<Publication %r>' % (self.title)

    def add_subjects(self, subjects_input, language):
        for subject_input in subjects_input:
            subject = PublicationSubject.query.filter_by(
                name=subject_input, language=language).first()
            if not subject:
                self.subjects.append(
                    PublicationSubject(subject_input, language))
            else:
                self.subjects.append(subject)
            if subject_input == subjects_input[0]:
                self.main_subject = subject_input


class PublicationSubject(db.Model):
    __tablename__ = 'news_subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    language = db.Column(db.String(2))

    def __init__(self, name=None, language=None):
        self.name = name
        self.language = language

    def __repr__(self):
        return '<PublicationSubject %r (%r)>' % (self.name, self.language)
