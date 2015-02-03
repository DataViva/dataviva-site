from dataviva import db
from dataviva.secex.abstract_models import BaseSecex, Eci, Rca, Rcd, Distance, OppGain
from dataviva.secex.abstract_models import BraId, WldId, HsId
from dataviva.secex.abstract_models import BraDiversity, HsDiversity, WldDiversity

class Ymb(BaseSecex, BraId, HsDiversity, WldDiversity, Eci):
    __tablename__ = "secex_ymb"

class Ymp(BaseSecex, HsId, BraDiversity, WldDiversity, Rca):
    __tablename__ = "secex_ymp"
    pci = db.Column(db.Float())
    export_val_unit = db.Column(db.Float())
    import_val_unit = db.Column(db.Float())

class Ymw(BaseSecex, WldId, Eci, BraDiversity, HsDiversity):
    __tablename__ = "secex_ymw"

class Ymbp(BaseSecex, BraId, HsId, Rca, Rcd, Distance, OppGain):
    __tablename__ = "secex_ymbp"

class Ymbpw(BaseSecex, BraId, HsId, WldId):
    __tablename__ = "secex_ymbpw"

class Ymbw(BaseSecex, BraId, WldId):
    __tablename__ = "secex_ymbw"

class Ympw(BaseSecex, HsId, WldId):
    __tablename__ = "secex_ympw"
