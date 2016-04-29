from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.api.attrs.models import Bra, Cnae, Cbo

from sqlalchemy import and_
import json

############################################################
# ----------------------------------------------------------
# 2 variable tables
#
############################################################

class BaseRais(object):
    year = db.Column(db.Integer(4), primary_key=True)

    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_jobs = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    age_avg = db.Column(db.Numeric(16,2))

    wage_growth = db.Column(db.Float())
    wage_growth_5 = db.Column(db.Float())

    num_emp_growth = db.Column(db.Float())
    num_emp_growth_5 = db.Column(db.Float())


class Yi(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_yi'
    year = db.Column(db.Integer(4), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)

    cbo_diversity = db.Column(db.Integer(11))
    cbo_diversity_eff = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())

    cnae_id_len = db.Column(db.Integer(1))

    hist = db.Column(db.Text())
    gini = db.Column(db.Float())

    def __repr__(self):
        return '<Yi %d.%s>' % (self.year, self.cnae_id)

class Yb_rais(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_yb'
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)

    cnae_diversity = db.Column(db.Integer(11))
    cnae_diversity_eff = db.Column(db.Float())
    cbo_diversity = db.Column(db.Integer(11))
    cbo_diversity_eff = db.Column(db.Float())

    bra_id_len = db.Column(db.Integer(1))

    hist = db.Column(db.Text())
    gini = db.Column(db.Float())

    def __repr__(self):
        return '<Yb_rais %d.%s>' % (self.year, self.bra_id)

class Yo(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_yo'
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)

    cnae_diversity = db.Column(db.Integer(11))
    cnae_diversity_eff = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())

    cbo_id_len = db.Column(db.Integer(1))

    hist = db.Column(db.Text())
    gini = db.Column(db.Float())

    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.cbo_id)

############################################################
# ----------------------------------------------------------
# 3 variable tables
#
############################################################

class Ybi(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_ybi'
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)

    rca = db.Column(db.Float())
    distance = db.Column(db.Float())
    opp_gain = db.Column(db.Float())

    bra_id_len = db.Column(db.Integer(1))
    cnae_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybi %d.%s.%s>' % (self.year, self.bra_id, self.cnae_id)

class Ybi_reqs(db.Model, AutoSerialize):

    __tablename__ = 'rais_ybi_required'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)

    required_bras = db.Column(db.String(255))

    def __repr__(self):
        return '<Ybi_reqs %d.%s.%s>' % (self.year, self.bra_id, self.cnae_id)

class Ybo(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_ybo'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)

    bra_id_len = db.Column(db.Integer(1))
    cbo_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybo %d.%s.%s>' % (self.year, self.bra_id, self.cbo_id)

class Yio(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_yio'
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    importance = db.Column(db.Float())

    cnae_id_len = db.Column(db.Integer(1))
    cbo_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Yio %d.%s.%s>' % (self.year, self.cnae_id, self.cbo_id)

class Ybio(BaseRais, db.Model, AutoSerialize):

    __tablename__ = 'rais_ybio'
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    required = db.Column(db.Float())

    bra_id_len = db.Column(db.Integer(1))
    cnae_id_len = db.Column(db.Integer(1))
    cbo_id_len = db.Column(db.Integer(1))

    def __repr__(self):
        return '<Ybio %d.%s.%s.%s>' % (self.year, self.bra_id, self.cnae_id, self.cbo_id)
