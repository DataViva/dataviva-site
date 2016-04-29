from dataviva import db
from flask.ext.babel import gettext
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.utils.exist_or_404 import exist_or_404
from dataviva.utils.num_format import num_format
from sqlalchemy import func, Float
from sqlalchemy.sql.expression import cast
from decimal import *

from flask import g
from dataviva.api.stats.util import parse_year
from dataviva.api.attrs.abstract_models import BasicAttr, ExpandedAttr


class Search(db.Model):
    __tablename__ = 'attrs_search'
    id = db.Column(db.String(9), primary_key=True)
    kind = db.Column(db.String(9), primary_key=True)

    weight = db.Column(db.Float())
    name_en =  db.Column(db.String(200))
    name_pt =  db.Column(db.String(200))
    color =  db.Column(db.String(7))

    def serialize(self, pt=False):
        return {
            "color": self.color,
            "content_type": self.kind,
            "id": self.id,
            "name" : self.name_en if not pt else self.name_pt
        }

    def __repr__(self):
        return "<SearchAttr {} {}>".format(self.id, self.kind)


class Cnae(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_cnae'
    id = db.Column(db.String(8), primary_key=True)

    yi = db.relationship("Yi", backref = 'cnae', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'cnae', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cnae', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cnae', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/cnae/cnae_%s.png" % (self.id[:1])

    def url(self):
        return "profiles/cnae/{}/".format(self.id)

    def __repr__(self):
        return '<Cnae %r>' % (self.name_en)


class Cbo(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_cbo'
    id = db.Column(db.String(6), primary_key=True)

    yo = db.relationship("Yo", backref = 'cbo', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'cbo', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cbo', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cbo', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/cbo/cbo_%s.png" % (self.id[:1])

    def url(self):
        return "profiles/cbo/{}/".format(self.id)

    def __repr__(self):
        return '<Cbo %r>' % (self.name_en)


class Hs(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_hs'
    id = db.Column(db.String(8), primary_key=True)

    ymp = db.relationship("Ymp", backref = 'hs', lazy = 'dynamic')
    ympw = db.relationship("Ympw", backref = 'hs', lazy = 'dynamic')
    ymbp = db.relationship("Ymbp", backref = 'hs', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'hs', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/hs/hs_%s.png" % (self.id[:2])

    def url(self):
        return "profiles/hs/{}/".format(self.id)

    def __repr__(self):
        return '<Hs %r>' % (self.name_en)


class Course_hedu(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_course_hedu'
    id = db.Column(db.String(8), primary_key=True)

    yc = db.relationship("Yc_hedu", backref = 'course_hedu', lazy = 'dynamic')
    yuc = db.relationship("Yuc", backref = 'course_hedu', lazy = 'dynamic')
    ybc = db.relationship("Ybc_hedu", backref = 'course_hedu', lazy = 'dynamic')
    ybuc = db.relationship("Ybuc", backref = 'course_hedu', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/course_hedu/course_hedu_%s.png" % (self.id[:2])

    def url(self):
        return "profiles/course_hedu/{}/".format(self.id)

    def __repr__(self):
        return '<Course_hedu %r>' % (self.name_en)


class Course_sc(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_course_sc'
    id = db.Column(db.String(8), primary_key=True)

    yc = db.relationship("Yc_sc", backref = 'course_sc', lazy = 'dynamic')
    ysc = db.relationship("Ysc", backref = 'course_sc', lazy = 'dynamic')
    ybc = db.relationship("Ybc_sc", backref = 'course_sc', lazy = 'dynamic')
    ybsc = db.relationship("Ybsc", backref = 'course_sc', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/course_sc/course_sc_%s.png" % (self.id[:2])

    def url(self):
        return "profiles/course_sc/{}/".format(self.id)

    def __repr__(self):
        return '<Course_sc %r>' % (self.name_en)


class School(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_school'
    id = db.Column(db.String(8), primary_key=True)
    is_vocational = db.Column(db.Integer(1))
    school_type_id = db.Column(db.String(1))
    school_type_en = db.Column(db.String(32))
    school_type_pt = db.Column(db.String(32))
    is_vocational = db.Column(db.Integer)

    ysc = db.relationship("Ysc", backref = 'school', lazy = 'dynamic')
    ybsc = db.relationship("Ybsc", backref = 'school', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/school/school_{}.png".format(self.school_type_id.lower())

    def url(self):
        return "profiles/school/{}/".format(self.id)

    def __repr__(self):
        return '<School %r>' % (self.name_en)


class University(db.Model, AutoSerialize, ExpandedAttr):

    __tablename__ = 'attrs_university'
    id = db.Column(db.String(8), primary_key=True)
    school_type_id = db.Column(db.String(1))
    school_type_en = db.Column(db.String(32))
    school_type_pt = db.Column(db.String(32))

    yu = db.relationship("Yu", backref = 'university', lazy = 'dynamic')
    yuc = db.relationship("Yuc", backref = 'university', lazy = 'dynamic')
    ybu = db.relationship("Ybu", backref = 'university', lazy = 'dynamic')
    ybuc = db.relationship("Ybuc", backref = 'university', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/university/university_{}.png".format(self.school_type_id.lower())

    def school_type(self):
        lang = getattr(g, "locale", "en")
        return getattr(self, "school_type_" + lang)

    def url(self):
        return "profiles/university/{}/".format(self.id)

    def __repr__(self):
        return '<University %r>' % (self.name_en)


############################################################
# ----------------------------------------------------------
# Geography
#
############################################################


class Wld(db.Model, AutoSerialize, BasicAttr):

    __tablename__ = 'attrs_wld'
    id = db.Column(db.String(5), primary_key=True)
    id_2char = db.Column(db.String(2))
    id_3char = db.Column(db.String(3))
    id_num = db.Column(db.Integer(11))
    id_mdic = db.Column(db.Integer(11))

    ymw = db.relationship("Ymw", backref = 'wld', lazy = 'dynamic')
    ympw = db.relationship("Ympw", backref = 'wld', lazy = 'dynamic')
    ymbw = db.relationship("Ymbw", backref = 'wld', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'wld', lazy = 'dynamic')

    def icon(self):
        if self.id == "all":
            return "/static/img/icons/wld/wld_sabra.png"
        else:
            return "/static/img/icons/wld/wld_%s.png" % (self.id)

    def url(self):
        if self.id == "sabra":
            return "/profiles/bra/all/"
        else:
            return "profiles/wld/{}/".format(self.id)

    def __repr__(self):
        return '<Wld %r>' % (self.id_3char)

bra_pr = db.Table('attrs_bra_pr',
    db.Column('bra_id', db.Integer, db.ForeignKey('attrs_bra.id')),
    db.Column('pr_id', db.Integer, db.ForeignKey('attrs_bra.id'))
)


class Bra(db.Model, AutoSerialize, BasicAttr):

    __tablename__ = 'attrs_bra'
    id = db.Column(db.String(10), primary_key=True)
    id_ibge = db.Column(db.Integer(7))
    abbreviation = db.Column(db.String(2))

    distance = 0

    # SECEX relations
    ymb = db.relationship("Ymb", backref = 'bra', lazy = 'dynamic')
    ymbp = db.relationship("Ymbp", backref = 'bra', lazy = 'dynamic')
    ymbw = db.relationship("Ymbw", backref = 'bra', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'bra', lazy = 'dynamic')

    # RAIS relations
    yb_rais = db.relationship("Yb_rais", backref = 'bra', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'bra', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'bra', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'bra', lazy = 'dynamic')

    # HEDU relations
    ybu = db.relationship("Ybu", backref = 'bra', lazy = 'dynamic')
    ybc = db.relationship("Ybc_hedu", backref = 'bra', lazy = 'dynamic')

    # SC relations
    ybc_sc = db.relationship("Ybc_sc", backref = 'bra', lazy = 'dynamic')

    # Neighbors
    neighbors = db.relationship('Distances', primaryjoin = "(Bra.id == Distances.bra_id_origin)", backref='bra_origin', lazy='dynamic')
    bb = db.relationship('Distances', primaryjoin = "(Bra.id == Distances.bra_id_dest)", backref='bra', lazy='dynamic')

    # Planning Regions
    pr = db.relationship('Bra',
        secondary = bra_pr,
        primaryjoin = (bra_pr.c.pr_id == id),
        secondaryjoin = (bra_pr.c.bra_id == id),
        backref = db.backref('bra', lazy = 'dynamic'),
        lazy = 'dynamic'
    )

    pr2 = db.relationship(
        'Bra',
        secondary = bra_pr,
        primaryjoin = (bra_pr.c.bra_id == id),
        secondaryjoin = (bra_pr.c.pr_id == id),
        backref = db.backref('bra2', lazy = 'dynamic'),
        lazy = 'dynamic'
    )

    def icon(self):
        if len(self.id) == 1:
            return None
        return "/static/img/icons/bra/bra_%s.png" % (self.id[:3])

    def get_neighbors(self, dist, remove_self=False):
        if dist == 0:
            return []
        q = self.neighbors.filter(Distances.distance <= dist).order_by(Distances.distance)
        if remove_self:
            q = q.filter(Distances.bra_id_dest != self.id) # filter out self
        return q.all()

    def url(self):
        return "/profiles/bra/{}/".format(self.id)

    def __repr__(self):
        return '<Bra %r>' % (self.name_en)

############################################################
# ----------------------------------------------------------
# Attr data
#
############################################################

class Distances(db.Model):

    __tablename__ = 'attrs_bb'
    bra_id_origin = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_dest = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    distance = db.Column(db.Float())

    def __repr__(self):
        return '<Bra_Dist %r-%r:%g>' % (self.bra_id_origin, self.bra_id_dest, self.distance)

    def serialize(self):
        return {
            "bra_id_origin": self.bra_id_origin,
            "bra_id_dest": self.bra_id_dest,
            "distance": self.distance
        }

class Yb(db.Model, AutoSerialize):

    __tablename__ = 'attrs_yb'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    population = db.Column(db.Integer)

    def __repr__(self):
        return '<Yb %r.%r>' % (self.year, self.bra_id)


class Stat(db.Model, AutoSerialize, BasicAttr):

    __tablename__ = 'attrs_stat'
    id = db.Column(db.String(20), primary_key=True)

    # name lookup relation
    bs = db.relationship("dataviva.api.attrs.models.Bs", backref = 'stat', lazy = 'dynamic')
    ybs = db.relationship("dataviva.api.attrs.models.Ybs", backref = 'stat', lazy = 'dynamic')


class Bs(db.Model, AutoSerialize):

    __tablename__ = 'attrs_bs'
    bra_id = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    stat_id = db.Column(db.String(20), db.ForeignKey(Stat.id), primary_key=True)
    stat_val = db.Column(db.String(40))

    def __repr__(self):
        return "<Bs {}.{}>".format(self.bra_id, self.stat_id)

class Ybs(db.Model, AutoSerialize):

    __tablename__ = 'attrs_ybs'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    stat_id = db.Column(db.String(20), db.ForeignKey(Stat.id), primary_key=True)
    stat_val = db.Column(db.Float)

    def __repr__(self):
        return "<Ybs {}.{}.{}>".format(self.year, self.bra_id, self.stat_id)

class Ybb(db.Model, AutoSerialize):

    __tablename__ = 'attrs_ybb'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_target = db.Column(db.String(10), db.ForeignKey(Bra.id), primary_key=True)
    prox_cnae = db.Column(db.Float)
    prox_cbo = db.Column(db.Float)
    prox_hs = db.Column(db.Float)
    prox_wld = db.Column(db.Float)

    def __repr__(self):
        return "<Ybb {}.{}.{}>".format(self.year, self.bra_id, self.bra_id_target)

class Ypp(db.Model, AutoSerialize):

    __tablename__ = 'attrs_ypp'
    year = db.Column(db.Integer(4), primary_key=True)
    hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    hs_id_target = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    prox_bra = db.Column(db.Float)

    def __repr__(self):
        return "<Ypp {}.{}.{}>".format(self.year, self.hs_id, self.hs_id_target)

class Yww(db.Model, AutoSerialize):

    __tablename__ = 'attrs_yww'
    year = db.Column(db.Integer(4), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    wld_id_target = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    prox_bra = db.Column(db.Float)

    def __repr__(self):
        return "<Yww {}.{}.{}>".format(self.year, self.wld_id, self.wld_id_target)

class Yii(db.Model, AutoSerialize):

    __tablename__ = 'attrs_yii'
    year = db.Column(db.Integer(4), primary_key=True)
    cnae_id = db.Column(db.String(8), db.ForeignKey(Cnae.id), primary_key=True)
    cnae_id_target = db.Column(db.String(8), db.ForeignKey(Cnae.id), primary_key=True)
    prox_bra = db.Column(db.Float)

    def __repr__(self):
        return "<Yii {}.{}.{}>".format(self.year, self.cnae_id, self.cnae_id_target)

class Yoo(db.Model, AutoSerialize):

    __tablename__ = 'attrs_yoo'
    year = db.Column(db.Integer(4), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    cbo_id_target = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    prox_bra = db.Column(db.Float)

    def __repr__(self):
        return "<Yoo {}.{}.{}>".format(self.year, self.cbo_id, self.cbo_id_target)

class Yuu(db.Model, AutoSerialize):

    __tablename__ = 'attrs_yuu'
    year = db.Column(db.Integer(4), primary_key=True)
    university_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    university_id_target = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    prox_course_hedu = db.Column(db.Float)

    def __repr__(self):
        return "<Yuu {}.{}.{}>".format(self.year, self.cbo_id, self.cbo_id_target)
