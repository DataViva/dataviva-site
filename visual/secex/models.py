from visual import db
from visual.utils import AutoSerialize
from visual.attrs.models import Wld, Hs, Bra

############################################################
# ----------------------------------------------------------
# 2 variable tables
# 
############################################################

class Yw(db.Model, AutoSerialize):

    __tablename__ = 'secex_yw'
    year = db.Column(db.Integer(4), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

    def __repr__(self):
        return '<Yw %d.%s>' % (self.year, self.wld_id)

class Yp(db.Model, AutoSerialize):

    __tablename__ = 'secex_yp'
    year = db.Column(db.Integer(4), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    complexity = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

    def __repr__(self):
        return '<Yp %d.%s>' % (self.year, self.hs_id)

class Yb_secex(db.Model, AutoSerialize):

    __tablename__ = 'secex_yb'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    complexity = db.Column(db.Float())
    complexity_wld = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

    def __repr__(self):
        return '<Yb_secex %d.%s>' % (self.year, self.bra_id)

class Bp(db.Model, AutoSerialize):

    __tablename__ = 'secex_bp'
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    mhat_rca = db.Column(db.Float())
    mhat_val_usd = db.Column(db.Float())

    def __repr__(self):
        return '<Bp %s.%s>' % (self.bra_id, self.hs_id)

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
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

    def __repr__(self):
        return '<Ypw %d.%s.%s>' % (self.year, self.hs_id, self.wld_id)

class Ybp(db.Model, AutoSerialize):

    __tablename__ = 'secex_ybp'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    hs_id = db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    rca = db.Column(db.Float())
    rca_wld = db.Column(db.Float())
    distance = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

    def __repr__(self):
        return '<Ybp %d.%s.%s>' % (self.year, self.bra_id, self.hs_id)

class Ybw(db.Model, AutoSerialize):

    __tablename__ = 'secex_ybw'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    wld_id = db.Column(db.String(5), db.ForeignKey(Wld.id), primary_key=True)
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

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
    val_qty = db.Column(db.Float())
    val_kg = db.Column(db.Float())
    val_usd = db.Column(db.Float())
    growth_pct = db.Column(db.Float())
    growth_pct_total = db.Column(db.Float())
    growth_val = db.Column(db.Float())
    growth_val_total = db.Column(db.Float())

    def __repr__(self):
        return '<Ybpw %d.%s.%s.%s>' % (self.year, self.bra_id, self.hs_id, self.wld_id)