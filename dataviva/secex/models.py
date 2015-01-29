from dataviva import db
from dataviva.secex.abstract_models import BaseSecex, Rc
from dataviva.secex.abstract_models import BraId, WldId, HsId
from dataviva.secex.abstract_models import BraDiversity, HsDiversity, WldDiversity

class Ymb(BaseSecex, BraId, HsDiversity, WldDiversity):
    __tablename__ = "secex_ymb"
    eci = db.Column(db.Float())

class Ymp(BaseSecex, HsId, BraDiversity, WldDiversity):
    __tablename__ = "secex_ymp"
    pci = db.Column(db.Float())

class Ymw(BaseSecex, WldId):
    __tablename__ = "secex_ymw"

class Ymbp(BaseSecex, BraId, HsId, Rc):
    __tablename__ = "secex_ymbp"
