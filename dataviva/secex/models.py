from dataviva import db
from dataviva.utils import AutoSerialize
from dataviva.attrs.models import Wld, Hs, Bra

############################################################
# ----------------------------------------------------------
# 2 variable tables
# 
############################################################

class Yw(db.Model, AutoSerialize):

    __tablename__ = 'secex_yw'
    year = db.Column(db.Integer(4), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    val_usd = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())
    eci = db.Column(db.Float())

    def __repr__(self):
        return '<Yw %d.%s>' % (self.year, self.wld_id)

class Yp(db.Model, AutoSerialize):

    __tablename__ = 'secex_yp'
    year = db.Column(db.Integer(4), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    val_usd = db.Column(db.Float())
    pci = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())

    def __repr__(self):
        return '<Yp %d.%s>' % (self.year, self.hs_id)

class Yb_secex(db.Model, AutoSerialize):

    __tablename__ = 'secex_yb'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    val_usd = db.Column(db.Float())
    eci = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())

    def __repr__(self):
        return '<Yb_secex %d.%s>' % (self.year, self.bra_id)

############################################################
# ----------------------------------------------------------
# 3 variable tables
# 
############################################################

class Ypw(db.Model, AutoSerialize):

    __tablename__ = 'secex_ypw'
    year = db.Column(db.Integer(4), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    val_usd = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())

    def __repr__(self):
        return '<Ypw %d.%s.%s>' % (self.year, self.hs_id, self.wld_id)

class Ybp(db.Model, AutoSerialize):

    __tablename__ = 'secex_ybp'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    val_usd = db.Column(db.Float())
    rca = db.Column(db.Float())
    rca_wld = db.Column(db.Float())
    distance = db.Column(db.Float())
    distance_wld = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    opp_gain_wld = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())

    def __repr__(self):
        return '<Ybp %d.%s.%s>' % (self.year, self.bra_id, self.hs_id)

class Ybw(db.Model, AutoSerialize):

    __tablename__ = 'secex_ybw'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    val_usd = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())

    def __repr__(self):
        return '<Ybw %d.%s.%s>' % (self.year, self.bra_id, self.wld_id)

############################################################
# ----------------------------------------------------------
# 4 variable tables
# 
############################################################

class Ybpw(db.Model, AutoSerialize):

    __tablename__ = 'secex_ybpw'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    val_usd = db.Column(db.Float())
    val_usd_growth_pct = db.Column(db.Float())
    val_usd_growth_pct_5 = db.Column(db.Float())
    val_usd_growth_val = db.Column(db.Float())
    val_usd_growth_val_5 = db.Column(db.Float())

    def __repr__(self):
        return '<Ybpw %d.%s.%s.%s>' % (self.year, self.bra_id, self.hs_id, self.wld_id)