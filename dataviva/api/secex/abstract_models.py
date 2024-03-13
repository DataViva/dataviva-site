from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.api.attrs.models import Wld, Hs, Bra
from sqlalchemy.ext.declarative import declared_attr

class BaseSecex(db.Model, AutoSerialize):
    __abstract__ = True
    year = db.Column(db.Integer(), primary_key=True)
    month = db.Column(db.Integer(), primary_key=True)

    import_val = db.Column(db.Numeric(16,2))
    export_val = db.Column(db.Numeric(16,2))

    import_kg = db.Column(db.Integer())
    export_kg = db.Column(db.Integer())

    import_val_growth = db.Column(db.Float())
    import_val_growth_5 = db.Column(db.Float())
    export_val_growth = db.Column(db.Float())
    export_val_growth_5 = db.Column(db.Float())

class BraDiversity(object):
    bra_diversity = db.Column(db.Integer())
    bra_diversity_eff = db.Column(db.Float())

class WldDistance(object):
    distance_wld = db.Column(db.Float())
    opp_gain_wld = db.Column(db.Float())

class WldDiversity(object):
    wld_diversity = db.Column(db.Integer())
    wld_diversity_eff = db.Column(db.Float())

class HsDiversity(object):
    hs_diversity = db.Column(db.Integer())
    hs_diversity_eff = db.Column(db.Float())

class HsId(object):
    hs_id_len = db.Column(db.Integer())

    @declared_attr
    def hs_id(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs.id), primary_key=True)

class WldId(object):
    wld_id_len = db.Column(db.Integer())

    @declared_attr
    def wld_id(cls):
        return db.Column(db.String(5),db.ForeignKey(Wld.id), primary_key=True)

class BraId(object):
    bra_id_len = db.Column(db.Integer())

    @declared_attr
    def bra_id(cls):
        return db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)

class Distance(object):
    distance = db.Column(db.Float())
    distance_wld = db.Column(db.Float())

class OppGain(object):
    opp_gain = db.Column(db.Float())
    opp_gain_wld = db.Column(db.Float())

class Rca(object):
    rca = db.Column(db.Float())

class Rca_wld(object):
    rca_wld = db.Column(db.Float())

class Eci(object):
    eci = db.Column(db.Float())

class Rcd(object):
    rcd = db.Column(db.Float())
