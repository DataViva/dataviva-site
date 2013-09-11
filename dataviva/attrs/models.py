from dataviva import db, __latest_year__
from dataviva.utils import AutoSerialize, exist_or_404
from sqlalchemy import func, Float
from sqlalchemy.sql.expression import cast

from flask import g

''' A Mixin class for retrieving quick stats about a particular attribute'''
class Stats(object):
    
    def stats(self):
        from dataviva.rais.models import Ybi, Ybo, Yio, Yb_rais, Yi, Yo
        from dataviva.secex.models import Ybp, Ybw, Ypw, Yb_secex, Yp, Yw
        
        stats = []
        attr_type = self.__class__.__name__.lower()
        
        if attr_type == "bra":
            stats.append(self.get_top_attr(Ybi, "wage", attr_type, "isic", "rais"))
            stats.append(self.get_top_attr(Ybo, "wage", attr_type, "cbo", "rais"))
            stats.append(self.get_top_attr(Ybp, "val_usd", attr_type, "hs", "secex"))
            stats.append(self.get_top_attr(Ybw, "val_usd", attr_type, "wld", "secex"))
            stats.append({"name": "wage", "value": self.get_val(Yb_rais, "wage", attr_type, "rais")})
            stats.append({"name": "val_usd", "value": self.get_val(Yb_secex, "val_usd", attr_type, "secex")})
        elif attr_type == "isic":
            dataset = "rais"
            stats.append(self.get_top_attr(Ybi, "wage", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Yio, "wage", attr_type, "cbo", dataset))
            stats.append({"name": "wage", "value": self.get_val(Yi, "wage", attr_type, dataset)})
        elif attr_type == "cbo":
            dataset = "rais"
            stats.append(self.get_top_attr(Ybo, "wage", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Yio, "wage", attr_type, "isic", dataset))
            stats.append({"name": "wage", "value": self.get_val(Yo, "wage", attr_type, dataset)})
        elif attr_type == "hs":
            dataset = "secex"
            stats.append(self.get_top_attr(Ybp, "val_usd", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Ypw, "val_usd", attr_type, "wld", dataset))
            stats.append({"name": "val_usd", "value": self.get_val(Yp, "val_usd", attr_type, dataset)})
            stats.append({"name": "val_usd_growth_pct", "value": self.get_val(Yp, "val_usd_growth_pct", attr_type, dataset)})
            stats.append({"name": "val_usd_growth_pct_5", "value": self.get_val(Yp, "val_usd_growth_pct_5", attr_type, dataset)})
        elif attr_type == "wld":
            dataset = "secex"
            stats.append(self.get_top_attr(Ybw, "val_usd", attr_type, "bra", dataset))
            stats.append(self.get_top_attr(Ypw, "val_usd", attr_type, "hs", dataset))
            stats.append({"name": "val_usd", "value": self.get_val(Yw, "val_usd", attr_type, dataset)})
            stats.append({"name": "val_usd_growth_pct", "value": self.get_val(Yw, "val_usd_growth_pct", attr_type, dataset)})
            stats.append({"name": "val_usd_growth_pct_5", "value": self.get_val(Yw, "val_usd_growth_pct_5", attr_type, dataset)})
            stats.append({"name": "eci", "value": self.get_val(Yw, "eci", attr_type, dataset)})
            
        return stats
        
    ''' Given a "bra" string from URL, turn this into an array of Bra
        objects'''
    @staticmethod
    def parse_bras(bra_str):
        if "mgplr" in bra_str:
            planning_region = Bra.query.get(bra_str)
            bras = [b.serialize() for b in planning_region.pr.all()]
        elif ".show." in bra_str:
            # the '.show.' indicates that we are looking for a specific nesting
            bar_id, nesting = bra_str.split(".show.")
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
        latest_year = __latest_year__[dataset]
        if key == "bra":
            length = 8
        elif key == "isic" or key == "wld":
            length = 5
        elif key == "cbo":
            length = 4
        elif key == "hs":
            length = 6
            
        if attr_type == "bra":
            agg = {'val_usd':func.sum, 'eci':func.avg, 'eci_wld':func.avg, 'pci':func.avg,
                    'val_usd_growth_pct':func.avg, 'val_usd_growth_pct_5':func.avg, 
                    'val_usd_growth_val':func.avg, 'val_usd_growth_val_5':func.avg,
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
            
            bras = self.parse_bras(self.id)

            # filter query
            if len(bras) > 1:
                col_names = ["{0}_id".format(key)]
                col_vals = [cast(agg[c](getattr(tbl, c)), Float) if c in agg else getattr(tbl, c) for c in col_names]
                top = tbl.query.with_entities(*col_vals).filter(tbl.bra_id.in_([b["id"] for b in bras]))
            else:
                top = tbl.query.filter(tbl.bra_id == bras[0]["id"])
        else:
            top = tbl.query.filter(getattr(tbl, attr_type+"_id") == self.id)
            
        top = top.filter_by(year=latest_year) \
                    .filter(func.char_length(getattr(tbl, key+"_id")) == length) \
                    .group_by(getattr(tbl, key+"_id")) \
                    .order_by(func.sum(getattr(tbl, val_var)).desc()).first()

        if isinstance(top,tuple):
            obj = globals()[key.title()].query.get(top[0])
        else:
            obj = getattr(top, key)
        
        return {"name": "top_{0}".format(key), "value": obj.name(), "id": obj.id}

    def get_val(self, tbl, val_var, attr_type, dataset):
        latest_year = __latest_year__[dataset]
        
        if attr_type == "bra":
            agg = {'val_usd':func.sum, 'eci':func.avg, 'eci_wld':func.avg, 'pci':func.avg,
                    'val_usd_growth_pct':func.avg, 'val_usd_growth_pct_5':func.avg, 
                    'val_usd_growth_val':func.avg, 'val_usd_growth_val_5':func.avg,
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
            
            bras = self.parse_bras(self.id)
            
            # filter query
            if len(bras) > 1:
                col_names = [val_var]
                col_vals = [cast(agg[c](getattr(tbl, c)), Float) if c in agg else getattr(tbl, c) for c in col_names]
                total = tbl.query.with_entities(*col_vals).filter(tbl.bra_id.in_([b["id"] for b in bras]))
            else:
                total = tbl.query.filter(tbl.bra_id == bras[0]["id"])
        else:
            total = tbl.query.filter(getattr(tbl, attr_type+"_id") == self.id)
        
        total = total.filter_by(year=latest_year).first()
                 
        if isinstance(total,tuple):
            val = total[0]
        else:
            val = getattr(total,val_var)
                    
        return val

class Isic(db.Model, AutoSerialize, Stats):

    __tablename__ = 'attrs_isic'
    __public__ = ('id', 'name_en', 'name_pt', 'desc_en', 'desc_pt', 'keywords_en', 'keywords_pt', 'color')
    id = db.Column(db.String(5), primary_key=True)
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
    yi = db.relationship("Yi", backref = 'isic', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'isic', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'isic', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'isic', lazy = 'dynamic')
    
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/isic/isic_%s.png" % (self.id[:1])

    def __repr__(self):
        return '<Isic %r>' % (self.name_en)


class Cbo(db.Model, AutoSerialize, Stats):

    __tablename__ = 'attrs_cbo'
    __public__ = ('id', 'name_en', 'name_pt', 'desc_en', 'desc_pt', 'keywords_en', 'keywords_pt', 'color')
    id = db.Column(db.String(6), primary_key=True)
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
    yo = db.relationship("Yo", backref = 'cbo', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'cbo', lazy = 'dynamic')
    yio = db.relationship("Yio", backref = 'cbo', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'cbo', lazy = 'dynamic')
    
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/cbo/cbo_%s.png" % (self.id[:1])

    def __repr__(self):
        return '<Cbo %r>' % (self.name_en)


class Hs(db.Model, AutoSerialize, Stats):

    __tablename__ = 'attrs_hs'
    __public__ = ('id', 'name_en', 'name_pt', 'desc_en', 'desc_pt', 'keywords_en', 'keywords_pt', 'color')
    id = db.Column(db.String(8), primary_key=True)
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
    yp = db.relationship("Yp", backref = 'hs', lazy = 'dynamic')
    ypw = db.relationship("Ypw", backref = 'hs', lazy = 'dynamic')
    ybp = db.relationship("Ybp", backref = 'hs', lazy = 'dynamic')
    ybpw = db.relationship("Ybpw", backref = 'hs', lazy = 'dynamic')
    
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/hs/hs_%s.png" % (self.id[:2])

    def __repr__(self):
        return '<Hs %r>' % (self.name_en)


############################################################
# ----------------------------------------------------------
# Geography
# 
############################################################ 


class Wld(db.Model, AutoSerialize, Stats):

    __tablename__ = 'attrs_wld'
    __public__ = ('id', 'id_3char', 'name_en', 'name_pt', 'color')
    id = db.Column(db.String(5), primary_key=True)
    id_2char = db.Column(db.String(2))
    id_3char = db.Column(db.String(3))
    id_num = db.Column(db.Integer(5))
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    gender_pt = db.Column(db.SmallInteger)
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
    yw = db.relationship("Yw", backref = 'wld', lazy = 'dynamic')
    ypw = db.relationship("Ypw", backref = 'wld', lazy = 'dynamic')
    ybw = db.relationship("Ybw", backref = 'wld', lazy = 'dynamic')
    ybpw = db.relationship("Ybpw", backref = 'wld', lazy = 'dynamic')
    
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/wld/wld_%s.png" % (self.id)
        
    def __repr__(self):
        return '<Wld %r>' % (self.id_3char)

bra_pr = db.Table('attrs_bra_pr',
    db.Column('bra_id', db.Integer, db.ForeignKey('attrs_bra.id')),
    db.Column('pr_id', db.Integer, db.ForeignKey('attrs_bra.id'))
)

class Bra(db.Model, AutoSerialize, Stats):

    __tablename__ = 'attrs_bra'
    __public__ = ('id', 'id_ibge', 'name_en', 'name_pt', 'color', 'distance')
    id = db.Column(db.String(10), primary_key=True)
    id_ibge = db.Column(db.Integer(7))
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
    
    distance = 0
    
    # SECEX relations
    yb_secex = db.relationship("Yb_secex", backref = 'bra', lazy = 'dynamic')
    ybp = db.relationship("Ybp", backref = 'bra', lazy = 'dynamic')
    ybw = db.relationship("Ybw", backref = 'bra', lazy = 'dynamic')
    ybpw = db.relationship("Ybpw", backref = 'bra', lazy = 'dynamic')
    # RAIS relations
    yb_rais = db.relationship("Yb_rais", backref = 'bra', lazy = 'dynamic')
    ybi = db.relationship("Ybi", backref = 'bra', lazy = 'dynamic')
    ybo = db.relationship("Ybo", backref = 'bra', lazy = 'dynamic')
    ybio = db.relationship("Ybio", backref = 'bra', lazy = 'dynamic')
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
    
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/bra/bra_%s.png" % (self.id[:2])

    def get_neighbors(self, dist, remove_self=False):
        q = self.neighbors.filter(Distances.distance <= dist).order_by(Distances.distance)
        if remove_self:
            q = q.filter(Distances.bra_id_dest != self.id) # filter out self
        return q.all()

    def __repr__(self):
        return '<Bra %r>' % (self.name_en)

############################################################
# ----------------------------------------------------------
# Attr data
# 
############################################################

class Distances(db.Model):

    __tablename__ = 'attrs_bb'
    bra_id_origin = db.Column(db.String(10), db.ForeignKey('attrs_bra.id'), primary_key=True)
    bra_id_dest = db.Column(db.String(10), db.ForeignKey('attrs_bra.id'), primary_key=True)
    distance = db.Column(db.Float())

    def __repr__(self):
        return '<Bra_Dist %r-%r:%g>' % (self.bra_id_origin, self.bra_id_dest, self.distance)

    def serialize(self):
        return {
            "bra_id_origin": self.bra_id_origin,
            "bra_id_dest": self.bra_id_dest,
            "distance": self.distance
        }

class Yb(db.Model):

    __tablename__ = 'attrs_yb'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(10), db.ForeignKey('attrs_bra.id'), primary_key=True)
    population = db.Column(db.Integer)

    def __repr__(self):
        return '<Yb %r.%r>' % (self.year, self.bra_id)
