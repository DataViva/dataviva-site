from dataviva import db
from dataviva.api.secex.abstract_models import BaseSecex, Eci, Rca, Rca_wld, Rcd, Distance, OppGain
from dataviva.api.secex.abstract_models import BraId, WldId, HsId
from dataviva.api.secex.abstract_models import BraDiversity, HsDiversity, WldDiversity, WldDistance

class Ymb(BaseSecex, BraId, HsDiversity, WldDiversity, Eci, WldDistance):
    __tablename__ = "secex_ymb"

class Ymp(BaseSecex, HsId, BraDiversity, WldDiversity, Rca_wld):
    __tablename__ = "secex_ymp"
    pci = db.Column(db.Float())

class Ymw(BaseSecex, WldId, Eci, BraDiversity, HsDiversity):
    __tablename__ = "secex_ymw"

class Ymbp(BaseSecex, BraId, HsId, Rca, Rca_wld, Rcd, Distance, OppGain):
    __tablename__ = "secex_ymbp"

class Ymbpw(BaseSecex, BraId, HsId, WldId):
    __tablename__ = "secex_ymbpw"

class Ymbw(BaseSecex, BraId, WldId):
    __tablename__ = "secex_ymbw"

class Ympw(BaseSecex, HsId, WldId):
    __tablename__ = "secex_ympw"
