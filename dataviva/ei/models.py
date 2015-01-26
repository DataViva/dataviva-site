from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Bra

class Ei(db.Model, AutoSerialize):
    __abstract__ = True

    year = db.Column(db.Integer(4), primary_key=True)    
    month = db.Column(db.Integer(2), primary_key=True)    

    tax = db.Column(db.Float())
    icms_tax = db.Column(db.Float())
    transportation_cost = db.Column(db.Float())
    purchase_value = db.Column(db.Float())
    transfer_value = db.Column(db.Float())
    devolution_value = db.Column(db.Float())
    icms_credit_value = db.Column(db.Float())
    remit_value = db.Column(db.Float())


class Ymr(Ei):
    __tablename__ = 'ei_ymr'

    bra_id_r = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_r_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ymr {}.{}.{}>'.format(self.year, self.month, self.bra_id_r)

class Yms(Ei):
    __tablename__ = 'ei_yms'

    bra_id_s = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_s_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yms {}.{}.{}>'.format(self.year, self.month, self.bra_id_s)

class Ymsr(Ei):
    __tablename__ = 'ei_ymsr'

    bra_id_s = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_r = db.Column(db.String(9), db.ForeignKey(Bra.id), primary_key=True)
    bra_id_s_len = db.Column(db.Integer(1))
    bra_id_r_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ymsr {}.{}.{}>'.format(self.year, self.month, self.bra_id_s, self.bra_id_r)
