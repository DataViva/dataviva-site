from dataviva import db
from flask.ext.babel import gettext
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.utils.exist_or_404 import exist_or_404
from dataviva.utils.num_format import num_format
from sqlalchemy import func, Float
from sqlalchemy.sql.expression import cast
from decimal import *

from flask import g
from dataviva.stats.util import parse_year
from dataviva.attrs.abstract_models import BasicAttr, ExpandedAttr

''' A Mixin class for retrieving quick stats about a particular attribute'''
class Stats(object):

    def stats(self):
        from dataviva.attrs.models import Yb, Ybs
        from dataviva.rais.models import Ybi, Ybo, Yio, Yb_rais, Yi, Yo
        from dataviva.secex.models import Ymbp, Ymbw, Ympw, Ymb, Ymp, Ymw
        from dataviva.hedu.models import Yu, Yuc, Ybu, Yc_hedu
        from dataviva.sc.models import Ybc_sc, Yc_sc
        from dataviva import __year_range__

        stats = []
        attr_type = self.__class__.__name__.lower()
        if attr_type == "wld" and self.id == "all":
            attr_type = "bra"

        if attr_type == "bra" and self.id == "all":
            stats.append(self.get_val(Yb,"population",attr_type,"population"))
            stats.append(self.get_top_attr(Yi, "num_emp", attr_type, "cnae", "rais"))
            stats.append(self.get_top_attr(Yo, "num_emp", attr_type, "cbo", "rais"))
            stats.append(self.get_val(Yi, "wage", attr_type, "rais"))
            stats.append(self.get_top_attr(Ymp, "export_val", attr_type, "hs", "secex"))
            stats.append(self.get_top_attr(Ymw, "export_val", attr_type, "wld", "secex"))
            stats.append(self.get_val(Ymp, "export_val", attr_type, "secex"))
        elif attr_type == "bra":
            stats.append(self.get_val(Bs,"stat_val",attr_type,"stats",stat_id="demonym"))
            stats.append(self.get_val(Ybs,"stat_val",attr_type,"stats",stat_id="pop"))
            stats.append(self.get_val(Ybs,"stat_val",attr_type,"stats",stat_id="gini"))
            stats.append(self.get_val(Ybs,"stat_val",attr_type,"stats",stat_id="life_exp"))
            stats.append(self.get_val(Ybs,"stat_val",attr_type,"stats",stat_id="hdi"))
            stats.append(self.get_top_attr(Ybi,"num_emp",attr_type,"cnae","rais"))
            stats.append(self.get_top_attr(Ybo, "num_emp", attr_type, "cbo", "rais"))
            stats.append(self.get_val(Yb_rais, "wage", attr_type, "rais", name=gettext("Total Monthly Wage")))
            stats.append(self.get_top_attr(Ymbp, "export_val", attr_type, "hs", "secex"))
            stats.append(self.get_top_attr(Ymbw, "export_val", attr_type, "wld", "secex"))
            stats.append(self.get_val(Ymb, "export_val", attr_type, "secex", name=gettext("Total Exports")))
            stats.append(self.get_val(Ymb, "import_val", attr_type, "secex", name=gettext("Total Imports")))
            if len(self.id) == 9:
                stats.append(self.get_val(Bs,"stat_val",attr_type,"stats",stat_id="airport"))
                stats.append(self.get_val(Bs,"stat_val",attr_type,"stats",stat_id="airport_dist"))
                stats.append(self.get_val(Bs,"stat_val",attr_type,"stats",stat_id="seaport"))
                stats.append(self.get_val(Bs,"stat_val",attr_type,"stats",stat_id="seaport_dist"))
        elif attr_type == "cnae":
            dataset = "rais"
            five_years_ago = parse_year(__year_range__[dataset][-1]) - 5
            stats.append(self.get_top_attr(Ybi, "num_emp", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Yio, "num_emp", attr_type, "cbo", dataset))
            stats.append(self.get_val(Yi, "wage", attr_type, dataset, name=gettext("Total Monthly Wage")))
            stats.append(self.get_val(Yi, "wage_avg", attr_type, dataset, name=gettext("Average Monthly Wage")))
            stats.append(self.get_val(Yi, "wage_avg", attr_type, dataset, five_years_ago, name=gettext("Average Monthly Wage")))
        elif attr_type == "cbo":
            dataset = "rais"
            five_years_ago = parse_year(__year_range__[dataset][-1]) - 5
            stats.append(self.get_top_attr(Ybo, "num_emp", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Yio, "num_emp", attr_type, "cnae", dataset))
            stats.append(self.get_val(Yo, "wage", attr_type, dataset, name=gettext("Total Monthly Wage")))
            stats.append(self.get_val(Yo, "wage_avg", attr_type, dataset, name=gettext("Average Monthly Wage")))
            stats.append(self.get_val(Yo, "wage_avg", attr_type, dataset, five_years_ago, name=gettext("Average Monthly Wage")))
        elif attr_type == "hs":
            dataset = "secex"
            five_years_ago = parse_year(__year_range__[dataset][-1]) - 5
            stats.append(self.get_top_attr(Ymbp, "export_val", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Ympw, "export_val", attr_type, "wld", dataset))
            stats.append(self.get_val(Ymp, "export_val_growth", attr_type, dataset, name=gettext("Nominal Annual Growth Rate (1 year)")))
            stats.append(self.get_val(Ymp, "export_val_growth_5", attr_type, dataset, name=gettext("Nominal Annual Growth Rate (5 year)")))
            stats.append(self.get_val(Ymp, "export_val", attr_type, dataset, name=gettext("Total Exports")))
            stats.append(self.get_val(Ymp, "export_val", attr_type, dataset, five_years_ago, name=gettext("Total Exports")))
        elif attr_type == "wld":
            dataset = "secex"
            five_years_ago = parse_year(__year_range__[dataset][-1]) - 5
            stats.append(self.get_top_attr(Ymbw, "export_val", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Ympw, "export_val", attr_type, "hs", dataset))
            stats.append(self.get_val(Ymw, "export_val_growth", attr_type, dataset, name=gettext("Nominal Annual Growth Rate (1 year)")))
            stats.append(self.get_val(Ymw, "export_val_growth_5", attr_type, dataset, name=gettext("Nominal Annual Growth Rate (5 year)")))
            stats.append(self.get_val(Ymw, "eci", attr_type, dataset, name=gettext("Economic Complexity")))
            stats.append(self.get_val(Ymw, "export_val", attr_type, dataset, name=gettext("Total Exports")))
            stats.append(self.get_val(Ymw, "export_val", attr_type, dataset, five_years_ago, name=gettext("Total Exports")))
        elif attr_type == "university":
            dataset = "hedu"
            stats.append(self.get_top_attr(Yuc, "enrolled", attr_type, "course_hedu", "hedu"))
            stats.append(self.get_val(Yu, "enrolled", attr_type, dataset, name=gettext("Enrolled")))
            stats.append(self.get_val(Yu, "graduates", attr_type, dataset, name=gettext("Graduates")))
        elif attr_type == "course_hedu":
            dataset = "hedu"
            stats.append(self.get_top_attr(Yuc, "enrolled", attr_type, "university", "hedu"))
            stats.append(self.get_val(Yc_hedu, "enrolled", attr_type, dataset, name=gettext("Enrolled")))
            stats.append(self.get_val(Yc_hedu, "graduates", attr_type, dataset, name=gettext("Graduates")))
        elif attr_type == "course_sc":
            dataset = "sc"
            stats.append(self.get_top_attr(Ybc_sc, "enrolled", attr_type, "bra", "sc"))
            stats.append(self.get_val(Yc_sc, "enrolled", attr_type, dataset, name=gettext("Enrolled")))
            stats.append(self.get_val(Yc_sc, "age", attr_type, dataset, name=gettext("Average Age")))

        return stats

    ''' Given a "bra" string from URL, turn this into an array of Bra
        objects'''
    @staticmethod
    def parse_bras(bra_str):
        if ".show." in bra_str:
            # the '.show.' indicates that we are looking for a specific nesting
            bra_id, nesting = bra_str.split(".show.")
            # filter table by requested nesting level
            bras = Bra.query \
                    .filter(Bra.id.startswith(bra_id)) \
                    .filter(func.char_length(Attr.id) == nesting).all()
            bras = [b.serialize() for b in bras]
        elif "." in bra_str:
            # the '.' indicates we are looking for bras within a given distance
            bra_id, distance = bra_str.split(".")
            bras = exist_or_404(Bra, bra_id)
            neighbors = bras.get_neighbors(distance)
            bras = [g.bra.serialize() for g in neighbors]
        else:
            # we allow the user to specify bras separated by '+'
            bras = bra_str.split("+")
            # Make sure the bra_id requested actually exists in the DB
            bras = [exist_or_404(Bra, bra_id).serialize() for bra_id in bras]
        return bras

    def get_top_attr(self, tbl, val_var, attr_type, key, dataset):
        from dataviva import __year_range__
        latest_year = parse_year(__year_range__[dataset][-1].split("-")[0])
        name = gettext("Top")
        if key == "bra":
            name = gettext("Top Location")
            length = 9
        elif key == "hs":
            name = gettext("Top Product")
            length = 6
        elif key == "wld":
            name = gettext("Top Export Destination")
            length = 5
        elif key == "cnae":
            name = gettext("Top Industry")
            length = 6
        elif key == "cbo":
            name = gettext("Top Occupation")
            length = 4
        elif key == "course_hedu":
            name = gettext("Top Course")
            length = 6
        elif key == "university":
            name = gettext("Top University")
            length = 5

        if attr_type == "bra":
            agg = {'export_val':func.sum, 'eci':func.avg, 'eci_wld':func.avg, 'pci':func.avg,
                    'export_val_growth':func.avg, 'export_val_growth_5':func.avg,
                    'distance':func.avg, 'distance_wld':func.avg,
                    'opp_gain':func.avg, 'opp_gain_wld':func.avg,
                    'rca':func.avg, 'rca_wld':func.avg,
                    'wage':func.sum, 'num_emp':func.sum, 'num_est':func.sum,
                    'ici':func.avg, 'oci':func.avg,
                    'wage_growth_pct':func.avg, 'wage_growth_pct_5':func.avg,
                    'wage_growth_val':func.avg, 'wage_growth_val_5':func.avg,
                    'num_emp_growth_pct':func.avg, 'num_emp_pct_5':func.avg,
                    'num_emp_growth_val':func.avg, 'num_emp_growth_val_5':func.avg,
                    'distance':func.avg, 'importance':func.avg,
                    'opp_gain':func.avg, 'required':func.avg, 'rca':func.avg}

            if self.id == "all":
                top = tbl.query
            else:
                bras = self.parse_bras(self.id)

                # filter query
                if len(bras) > 1:
                    col_names = ["{0}_id".format(key)]
                    col_vals = [cast(agg[c](getattr(tbl, c)), Float) if c in agg else getattr(tbl, c) for c in col_names]
                    top = tbl.query.with_entities(*col_vals).filter(tbl.bra_id.in_([b["id"] for b in bras]))
                elif bras[0]["id"] != "all":
                    top = tbl.query.filter(tbl.bra_id == bras[0]["id"])
        else:
            top = tbl.query.filter(getattr(tbl, attr_type+"_id") == self.id)

        top = top.filter_by(year=latest_year) \
                    .filter(func.char_length(getattr(tbl, key+"_id")) == length) \
                    .group_by(getattr(tbl, key+"_id")) \
                    .order_by(func.sum(getattr(tbl, val_var)).desc())

        percent = 0
        if top.first() != None and getattr(top.first(),val_var) != None:
            if isinstance(top.first(),tuple):
                obj = globals()[key.capitalize()].query.get(top.first()[0])
                percent = None
            else:
                obj = getattr(top.first(),key)
                num = float(getattr(top.first(),val_var))
                den = 0
                for x in top.all():
                    value = getattr(x,val_var)
                    if value:
                        den += float(value)
                percent = (num/float(den))*100

            return {"name": name, 
                    "value": obj.name(), 
                    "percent": percent, 
                    "id": obj.id, 
                    "url": obj.url(),
                    "group": "{} {} ({})".format(latest_year, gettext("Stats"), dataset.split("_")[0].upper())}
        else:
            return {"name": name, 
                    "value": "-", 
                    "group": "{} {} ({})".format(latest_year, gettext("Stats"), dataset.split("_")[0].upper())}

    def get_val(self, tbl, val_var, attr_type, dataset, latest_year=None, stat_id=None, name=None):

        if latest_year == None:
            from dataviva import __year_range__
            latest_year = parse_year(__year_range__[dataset][-1].split("-")[0])

        if val_var == "wage_avg":
            calc_var = val_var
            val_var = "wage"
        else:
            calc_var = None

        if attr_type == "bra":
            agg = {'population':func.sum, 'export_val':func.sum, 'eci':func.avg, 'eci_wld':func.avg, 'pci':func.avg,
                    'export_val_growth_pct':func.avg, 'export_val_growth_pct_5':func.avg,
                    'export_val_growth_val':func.avg, 'export_val_growth_val_5':func.avg,
                    'distance':func.avg, 'distance_wld':func.avg,
                    'opp_gain':func.avg, 'opp_gain_wld':func.avg,
                    'rca':func.avg, 'rca_wld':func.avg,
                    'wage':func.sum, 'num_emp':func.sum, 'num_est':func.sum,
                    'ici':func.avg, 'oci':func.avg,
                    'wage_growth_pct':func.avg, 'wage_growth_pct_5':func.avg,
                    'wage_growth_val':func.avg, 'wage_growth_val_5':func.avg,
                    'num_emp_growth_pct':func.avg, 'num_emp_pct_5':func.avg,
                    'num_emp_growth_val':func.avg, 'num_emp_growth_val_5':func.avg,
                    'distance':func.avg, 'importance':func.avg,
                    'opp_gain':func.avg, 'required':func.avg, 'rca':func.avg}
            if self.id == "all":
                col_names = [val_var]
                col_vals = [cast(agg[c](getattr(tbl, c)), Float) if c in agg else getattr(tbl, c) for c in col_names]
                total = tbl.query.with_entities(*col_vals)
                if dataset == "rais":
                    total = total.filter(func.char_length(getattr(tbl,"cnae_id")) == 1)
                elif dataset == "secex":
                    total = total.filter(func.char_length(getattr(tbl,"hs_id")) == 2)
                elif dataset == "population":
                    total = total.filter(func.char_length(getattr(tbl,"bra_id")) == 2)
            else:
                bras = self.parse_bras(self.id)

                # filter query
                if len(bras) > 1:
                    col_names = [val_var]
                    col_vals = [cast(agg[c](getattr(tbl, c)), Float) if c in agg else getattr(tbl, c) for c in col_names]
                    total = tbl.query.with_entities(*col_vals).filter(tbl.bra_id.in_([b["id"] for b in bras]))
                elif bras[0]["id"] != "all":
                    total = tbl.query.filter(tbl.bra_id == bras[0]["id"])
            if stat_id:
                total = total.filter_by(stat_id=stat_id)
        else:
            total = tbl.query.filter(getattr(tbl, attr_type+"_id") == self.id)

        if "_y" in tbl.__tablename__:
            total = total.filter_by(year=latest_year)
        total = total.first()
        
        if total != None:
            if isinstance(total,tuple):
                val = total[0]
            else:
                val = getattr(total,val_var) or " - "

            if calc_var == "wage_avg":
                val = float(val)/getattr(total,"num_emp")
        else:
            val = 0
        
        val = num_format(val, key=val_var)
        # raise Exception(val)
        
        group = u"{} {} ({})".format(latest_year, gettext("Stats"), dataset.split("_")[0].upper())
        
        if val_var == "stat_val":
            group = ""
            if "_y" in tbl.__tablename__:
                name = u"{} ({})".format(total.stat.name(), latest_year)
            else:
                name = total.stat.name()
        elif not name:
            if calc_var:
                name = calc_var
            else:
                name = u"total_{0}".format(val_var)

        return {"name": name, "value": val, "group": group}

class Cnae(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_cnae'
    id = db.Column(db.String(8), primary_key=True)

    yi = db.relationship("Yi", backref = 'cnae', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'cnae', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cnae', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cnae', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/cnae/cnae_%s.png" % (self.id[:1])

    def url(self):
        return "/profiles/cnae/{}/".format(self.id)

    def __repr__(self):
        return '<Cnae %r>' % (self.name_en)


class Cbo(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_cbo'
    id = db.Column(db.String(6), primary_key=True)

    yo = db.relationship("Yo", backref = 'cbo', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'cbo', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cbo', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cbo', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/cbo/cbo_%s.png" % (self.id[:1])

    def url(self):
        return "/profiles/cbo/{}/".format(self.id)

    def __repr__(self):
        return '<Cbo %r>' % (self.name_en)


class Hs(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_hs'
    id = db.Column(db.String(8), primary_key=True)

    ymp = db.relationship("Ymp", backref = 'hs', lazy = 'dynamic')
    ympw = db.relationship("Ympw", backref = 'hs', lazy = 'dynamic')
    ymbp = db.relationship("Ymbp", backref = 'hs', lazy = 'dynamic')
    ymbpw = db.relationship("Ymbpw", backref = 'hs', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/hs/hs_%s.png" % (self.id[:2])

    def url(self):
        return "/profiles/hs/{}/".format(self.id)

    def __repr__(self):
        return '<Hs %r>' % (self.name_en)


class Course_hedu(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_course_hedu'
    id = db.Column(db.String(8), primary_key=True)

    yc = db.relationship("Yc_hedu", backref = 'course_hedu', lazy = 'dynamic')
    yuc = db.relationship("Yuc", backref = 'course_hedu', lazy = 'dynamic')
    ybc = db.relationship("Ybc_hedu", backref = 'course_hedu', lazy = 'dynamic')
    ybuc = db.relationship("Ybuc", backref = 'course_hedu', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/course_hedu/course_hedu_%s.png" % (self.id[:2])

    def url(self):
        return "/profiles/course_hedu/{}/".format(self.id)

    def __repr__(self):
        return '<Course_hedu %r>' % (self.name_en)


class Course_sc(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_course_sc'
    id = db.Column(db.String(8), primary_key=True)

    yc = db.relationship("Yc_sc", backref = 'course_sc', lazy = 'dynamic')
    ysc = db.relationship("Ysc", backref = 'course_sc', lazy = 'dynamic')
    ybc = db.relationship("Ybc_sc", backref = 'course_sc', lazy = 'dynamic')
    ybsc = db.relationship("Ybsc", backref = 'course_sc', lazy = 'dynamic')

    def icon(self):
        return "/static/img/icons/course_sc/course_sc_%s.png" % (self.id[:2])

    def __repr__(self):
        return '<Course_sc %r>' % (self.name_en)

class School(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_school'
    id = db.Column(db.String(8), primary_key=True)
    is_vocational = db.Column(db.Integer(1))
    school_type_en = db.Column(db.String(32))
    school_type_pt = db.Column(db.String(32))

    def icon(self):
        return None

    def __repr__(self):
        return '<School %r>' % (self.name_en)


class University(db.Model, AutoSerialize, Stats, ExpandedAttr):

    __tablename__ = 'attrs_university'
    id = db.Column(db.String(8), primary_key=True)
    school_type_en = db.Column(db.String(32))
    school_type_pt = db.Column(db.String(32))

    yu = db.relationship("Yu", backref = 'university', lazy = 'dynamic')
    yuc = db.relationship("Yuc", backref = 'university', lazy = 'dynamic')
    ybu = db.relationship("Ybu", backref = 'university', lazy = 'dynamic')
    ybuc = db.relationship("Ybuc", backref = 'university', lazy = 'dynamic')

    def icon(self):
        return None

    def school_type(self):
        lang = getattr(g, "locale", "en")
        return getattr(self, "school_type_" + lang)

    def url(self):
        return "/profiles/university/{}/".format(self.id)

    def __repr__(self):
        return '<University %r>' % (self.name_en)


############################################################
# ----------------------------------------------------------
# Geography
#
############################################################


class Wld(db.Model, AutoSerialize, Stats, BasicAttr):

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
        return "/profiles/wld/{}/".format(self.id)

    def __repr__(self):
        return '<Wld %r>' % (self.id_3char)

bra_pr = db.Table('attrs_bra_pr',
    db.Column('bra_id', db.Integer, db.ForeignKey('attrs_bra.id')),
    db.Column('pr_id', db.Integer, db.ForeignKey('attrs_bra.id'))
)

class Bra(db.Model, AutoSerialize, Stats, BasicAttr):

    __tablename__ = 'attrs_bra'
    id = db.Column(db.String(10), primary_key=True)
    id_ibge = db.Column(db.Integer(7))

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
            lazy = 'dynamic')

    pr2 = db.relationship('Bra',
            secondary = bra_pr,
            primaryjoin = (bra_pr.c.bra_id == id),
            secondaryjoin = (bra_pr.c.pr_id == id),
            backref = db.backref('bra2', lazy = 'dynamic'),
            lazy = 'dynamic')

    def icon(self):
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
    bs = db.relationship("dataviva.attrs.models.Bs", backref = 'stat', lazy = 'dynamic')
    ybs = db.relationship("dataviva.attrs.models.Ybs", backref = 'stat', lazy = 'dynamic')

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
