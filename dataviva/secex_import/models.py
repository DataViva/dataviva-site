from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from sqlalchemy.ext.declarative import declared_attr
from dataviva.attrs.models import Hs, Bra, Wld

##
## FOR TEMP BACKWARDS COMPATABILITY ONLY
class BaseSecex(object):
    year = db.Column(db.Integer(4), primary_key=True)
    val_usd_growth = db.Column(db.Float())
    val_usd_growth_5 = db.Column(db.Float())


class BaseYw(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())
    hs_diversity = db.Column(db.Integer(11))
    hs_diversity_eff = db.Column(db.Float())

    wld_id_len = db.Column(db.Integer(1))

    @declared_attr
    def wld_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)

    def __repr__(self):
        return '<%s %d.%s>' % (self.__name__, self.year, self.wld_id)

class BaseYp(BaseSecex):    
    val_usd = db.Column(db.Numeric(16,2))
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())
    wld_diversity = db.Column(db.Integer(11))
    wld_diversity_eff = db.Column(db.Float())

    hs_id_len = db.Column(db.Integer(1))

    @declared_attr
    def hs_id(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    def __repr__(self):
        return '<%s %d.%s>' % (self.__name__, self.year, self.hs_id)


class BaseYb(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))
    hs_diversity = db.Column(db.Integer(11))
    hs_diversity_eff = db.Column(db.Float())
    wld_diversity = db.Column(db.Integer(11))
    wld_diversity_eff = db.Column(db.Float())

    bra_id_len = db.Column(db.Integer(1))

    @declared_attr
    def bra_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)

    def __repr__(self):
        return '<%s_secex %d.%s>' % (self.__name__, self.year, self.bra_id)


############################################################
# ----------------------------------------------------------
# 3 variable abstract tables
# 
############################################################

class BaseYpw(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))

    hs_id_len = db.Column(db.Integer(1))
    wld_id_len = db.Column(db.Integer(1))

    @declared_attr
    def hs_id(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    @declared_attr
    def wld_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)

    def __repr__(self):
        return '<Ypw %d.%s.%s>' % (self.year, self.hs_id, self.wld_id)


class BaseYbp(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))

    hs_id_len = db.Column(db.Integer(1))
    bra_id_len = db.Column(db.Integer(1))

    @declared_attr
    def bra_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)

    @declared_attr
    def hs_id(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    def __repr__(self):
        return '<Ybp %d.%s.%s>' % (self.year, self.bra_id, self.hs_id)

class BaseYbw(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))

    wld_id_len = db.Column(db.Integer(1))
    bra_id_len = db.Column(db.Integer(1))

    @declared_attr
    def bra_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)

    @declared_attr
    def wld_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    
    def __repr__(self):
        return '<Ybw Export %d.%s.%s>' % (self.year, self.bra_id, self.wld_id)

############################################################
# ----------------------------------------------------------
# 4 variable tables
# 
############################################################

class BaseYbpw(BaseSecex):    
    val_usd = db.Column(db.Numeric(16,2))

    wld_id_len = db.Column(db.Integer(1))
    bra_id_len = db.Column(db.Integer(1))
    hs_id_len = db.Column(db.Integer(1))
    
    @declared_attr
    def bra_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)

    @declared_attr
    def hs_id(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    @declared_attr
    def wld_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)

    def __repr__(self):
        return '<Ybpw %d.%s.%s.%s>' % (self.year, self.bra_id, self.hs_id, self.wld_id)

class Yb_import(db.Model, AutoSerialize, BaseYb):
    __tablename__ = 'secex_import_yb'

class Yw_import(db.Model, AutoSerialize, BaseYw):
    __tablename__ = 'secex_import_yw'

class Yp_import(db.Model, AutoSerialize, BaseYp):
    ___magic_reuse_previous_mapper__ = True
    __tablename__ = 'secex_import_yp'

class Ypw_import(db.Model, AutoSerialize, BaseYpw):
    __tablename__ = 'secex_import_ypw'

class Ybp_import(db.Model, AutoSerialize, BaseYbp):
    __tablename__ = 'secex_import_ybp'
    rcd = db.Column(db.Float())

class Ybw_import(db.Model, AutoSerialize, BaseYbw):
    __tablename__ = 'secex_import_ybw'

class Ybpw_import(db.Model, AutoSerialize, BaseYbpw):
    __tablename__ = 'secex_import_ybpw'
