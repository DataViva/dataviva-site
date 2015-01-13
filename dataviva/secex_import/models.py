from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.secex.abstract_models import BaseYb, BaseYw, BaseYp, BaseYpw, BaseYbp, BaseYbw, BaseYbpw

class Yb(db.Model, AutoSerialize, BaseYb):
    __tablename__ = 'secex_import_yb'

# class Yw(db.Model, AutoSerialize, BaseYw):
#     __tablename__ = 'secex_import_yw'

# class Yp(db.Model, AutoSerialize, BaseYp):
#     __tablename__ = 'secex_import_yp'

# class Ypw(db.Model, AutoSerialize, BaseYpw):
#     __tablename__ = 'secex_import_ypw'

# class Ybp(db.Model, AutoSerialize, BaseYbp):
#     __tablename__ = 'secex_import_ybp'

# class Ybw(db.Model, AutoSerialize, BaseYbw):
#     __tablename__ = 'secex_import_ybw'

# class Ybpw(db.Model, AutoSerialize, BaseYbpw):
#     __tablename__ = 'secex_import_ybpw'