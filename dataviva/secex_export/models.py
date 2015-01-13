from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.secex.abstract_models import *


class Yb_secex(db.Model, AutoSerialize, BaseYb):
    __tablename__ = 'secex_export_yb'
    eci = db.Column(db.Float())


class Yw(db.Model, AutoSerialize, BaseYw):
    __tablename__ = 'secex_export_yw'
    eci = db.Column(db.Float())

class Yp(db.Model, AutoSerialize, BaseYp):
    __tablename__ = 'secex_export_yp'
    pci = db.Column(db.Float())
    rca_wld = db.Column(db.Float())

class Ypw(db.Model, AutoSerialize, BaseYpw):
    __tablename__ = 'secex_export_ypw'

class Ybp(db.Model, AutoSerialize, BaseYbp):
    __tablename__ = 'secex_export_ybp'
    rca = db.Column(db.Float())
    rca_wld = db.Column(db.Float())
    distance = db.Column(db.Float())
    distance_wld = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    opp_gain_wld = db.Column(db.Float())

class Ybw(db.Model, AutoSerialize, BaseYbw):
    __tablename__ = 'secex_export_ybw'

class Ybpw(db.Model, AutoSerialize, BaseYbpw):
    __tablename__ = 'secex_export_ybpw'