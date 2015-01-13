from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.secex.abstract_models import BaseYb, BaseYw, BaseYp, BaseYpw, BaseYbp, BaseYbw, BaseYbpw

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