from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.api.attrs.models import Bra, Course_sc, School

class Sc(db.Model, AutoSerialize):
    __abstract__ = True

    year = db.Column(db.Integer(4), primary_key=True)
    age = db.Column(db.Float())
    classes = db.Column(db.Integer(11))
    enrolled = db.Column(db.Integer(11))
    enrolled_growth = db.Column(db.Float())
    enrolled_growth_5 = db.Column(db.Float())

class Yb_sc(Sc):
    __tablename__ = 'sc_yb'

    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    num_schools = db.Column(db.Integer(11))

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yb {0}.{1}>'.format(self.year, self.bra_id)

class Ys(Sc):

    __tablename__ = 'sc_ys'

    school_id = db.Column(db.String(8), db.ForeignKey(School.id), primary_key=True)

    def __repr__(self):
        return '<Ys %d.%s>' % (self.year, self.school_id)

class Ybs(Sc):

    __tablename__ = 'sc_ybs'

    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    school_id = db.Column(db.String(8), db.ForeignKey(School.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybs %d.%s.%s>' % (self.year, self.bra_id, self.school_id)

class Ybc_sc(Sc):
    __tablename__ = 'sc_ybc'

    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    course_sc_id = db.Column(db.String(5), db.ForeignKey(Course_sc.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    course_sc_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybc %d.%s.%s>' % (self.year, self.bra_id, self.course_sc_id)

class Yc_sc(Sc):
    __tablename__ = 'sc_yc'

    course_sc_id = db.Column(db.String(5), db.ForeignKey(Course_sc.id), primary_key=True)

    course_sc_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybc %d.%s>' % (self.year, self.course_sc_id)

class Ysc(Sc):

    __tablename__ = 'sc_ysc'

    school_id = db.Column(db.String(8), db.ForeignKey(School.id), primary_key=True)
    course_sc_id = db.Column(db.String(5), db.ForeignKey(Course_sc.id), primary_key=True)

    course_sc_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ysc %d.%s>' % (self.year, self.school_id)

class Ybsc(Sc):

    __tablename__ = 'sc_ybsc'

    bra_id = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    school_id = db.Column(db.String(8), db.ForeignKey(School.id), primary_key=True)
    course_sc_id = db.Column(db.String(5), db.ForeignKey(Course_sc.id), primary_key=True)

    course_sc_id_len = db.Column(db.Integer(1))
    bra_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybsc %d.%s.%s.%s>' % (self.year, self.bra_id, self.school_id, self.course_sc_id)
