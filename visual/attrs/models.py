from visual import db
from visual.utils import AutoSerialize

from flask import g

class Isic(db.Model, AutoSerialize):

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
        return getattr(self,"name_"+g.locale)

    def __repr__(self):
        return '<Isic %r>' % (self.name_en)


class Cbo(db.Model, AutoSerialize):

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
        return getattr(self,"name_"+g.locale)

    def __repr__(self):
        return '<Cbo %r>' % (self.name_en)


class Hs(db.Model, AutoSerialize):

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
        return getattr(self,"name_"+g.locale)

    def __repr__(self):
        return '<Hs %r>' % (self.name_en)


############################################################
# ----------------------------------------------------------
# Geography
# 
############################################################ 


class Wld(db.Model, AutoSerialize):

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
        return getattr(self,"name_"+g.locale)
        
    def __repr__(self):
        return '<Wld %r>' % (self.id_3char)

class Bra(db.Model, AutoSerialize):

    __tablename__ = 'attrs_bra'
    __public__ = ('id', 'id_ibge', 'name_en', 'name_pt', 'color')
    id = db.Column(db.String(10), primary_key=True)
    id_ibge = db.Column(db.Integer(7))
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
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
    
    def name(self):
        return getattr(self,"name_"+g.locale)

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
