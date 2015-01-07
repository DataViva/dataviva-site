from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Wld, Hs, Bra
from sqlalchemy.ext.declarative import declared_attr

############################################################
# ----------------------------------------------------------
# 2 variable abstract tables
# 
############################################################

class BaseSecex(object):
    year = db.Column(db.Integer(4), primary_key=True)
    val_usd_growth = db.Column(db.Float())
    val_usd_growth_5 = db.Column(db.Float())


class BaseYw(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))
    eci = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())
    hs_diversity = db.Column(db.Integer(11))
    hs_diversity_eff = db.Column(db.Float())

    @declared_attr
    def wld_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)

    def __repr__(self):
        return '<%s %d.%s>' % (self.__name__, self.year, self.wld_id)

class BaseYp(BaseSecex):    
    val_usd = db.Column(db.Numeric(16,2))
    pci = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())
    wld_diversity = db.Column(db.Integer(11))
    wld_diversity_eff = db.Column(db.Float())
    rca_wld = db.Column(db.Float())

    @declared_attr
    def hs_id(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

    def __repr__(self):
        return '<%s %d.%s>' % (self.__name__, self.year, self.hs_id)


class BaseYb(BaseSecex):
    val_usd = db.Column(db.Numeric(16,2))
    eci = db.Column(db.Float())
    hs_diversity = db.Column(db.Integer(11))
    hs_diversity_eff = db.Column(db.Float())
    wld_diversity = db.Column(db.Integer(11))
    wld_diversity_eff = db.Column(db.Float())

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
    rca = db.Column(db.Float())
    rca_wld = db.Column(db.Float())
    distance = db.Column(db.Float())
    distance_wld = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    opp_gain_wld = db.Column(db.Float())

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

############################################################
# ----------------------------------------------------------
# Non-abstract Tables
# 
############################################################

class Yw(db.Model, AutoSerialize, BaseYw):
    __tablename__ = 'secex_export_yw'

class Yw_Imports(db.Model, AutoSerialize, BaseYw):
    __tablename__ = 'secex_import_yw'

class Yp(db.Model, AutoSerialize, BaseYp):
    __tablename__ = 'secex_export_yp'

class Yp_Imports(db.Model, AutoSerialize, BaseYp):
    __tablename__ = 'secex_import_yp'

class Yb_secex(db.Model, AutoSerialize, BaseYb):
    __tablename__ = 'secex_export_yb'

class Yb_secex_Imports(db.Model, AutoSerialize, BaseYb):
    __tablename__ = 'secex_import_yb'

class Ypw(db.Model, AutoSerialize, BaseYpw):
    __tablename__ = 'secex_export_ypw'

class Ypw_Imports(db.Model, AutoSerialize, BaseYpw):
    __tablename__ = 'secex_import_ypw'

class Ybp(db.Model, AutoSerialize, BaseYbp):
    __tablename__ = 'secex_export_ybp'

class Ybp_Imports(db.Model, AutoSerialize, BaseYbp):
    __tablename__ = 'secex_import_ybp'

class Ybw(db.Model, AutoSerialize, BaseYbw):
    __tablename__ = 'secex_export_ybw'

class Ybw_Imports(db.Model, AutoSerialize, BaseYbw):
    __tablename__ = 'secex_import_ybw'

class Ybpw(db.Model, AutoSerialize, BaseYbpw):
    __tablename__ = 'secex_export_ybpw'

class Ybpw_Imports(db.Model, AutoSerialize, BaseYbpw):
    __tablename__ = 'secex_import_ybpw'