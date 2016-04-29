from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.api.attrs.models import Bra, Course_hedu, University

class Hedu(db.Model, AutoSerialize):
    __abstract__ = True
    enrolled = db.Column(db.Integer(11))
    graduates = db.Column(db.Integer(11))
    entrants = db.Column(db.Integer(11))
    # students = db.Column(db.Integer(11))
    morning = db.Column(db.Integer(11))
    afternoon = db.Column(db.Integer(11))
    night = db.Column(db.Integer(11))
    full_time = db.Column(db.Integer(11))
    age = db.Column(db.Float())

    graduates_growth = db.Column(db.Float())
    enrolled_growth = db.Column(db.Float())

class Yc_hedu(Hedu):
    __tablename__ = 'hedu_yc'
    year = db.Column(db.Integer(4), primary_key=True)
    course_hedu_id = db.Column(db.String(6), db.ForeignKey(Course_hedu.id), primary_key=True)

    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybc {}.{}.{}>'.format(self.year, self.bra_id, self.course_hedu_id)

class Ybc_hedu(Hedu):
    __tablename__ = 'hedu_ybc'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    course_hedu_id = db.Column(db.String(6), db.ForeignKey(Course_hedu.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybc {}.{}.{}>'.format(self.year, self.bra_id, self.course_hedu_id)

class Ybuc(Hedu):
    __tablename__ = 'hedu_ybuc'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    course_hedu_id = db.Column(db.String(6), db.ForeignKey(Course_hedu.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybuc {}.{}.{}.{}>'.format(self.year, self.bra_id, self.university_id, self.course_hedu_id)

class Yb_hedu(Hedu):

    __tablename__ = 'hedu_yb'

    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    num_universities = db.Column(db.Integer(11))

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yb {}.{}>'.format(self.year, self.bra_id)

class Ybu(Hedu):

    __tablename__ = 'hedu_ybu'

    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybu {}.{}.{}>'.format(self.year, self.bra_id, self.university_id)

class Yu(Hedu):

    __tablename__ = 'hedu_yu'

    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)

    def __repr__(self):
        return '<Yu {}.{}>'.format(self.year, self.university_id)

class Yuc(Hedu):

    __tablename__ = 'hedu_yuc'

    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(5), db.ForeignKey(University.id), primary_key=True)
    course_hedu_id = db.Column(db.Integer(6), db.ForeignKey(Course_hedu.id), primary_key=True)

    course_hedu_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yuc {}.{}.{}>'.format(self.year, self.university_id, self.course_hedu_id)
