from dataviva import db
from dataviva.utils.auto_serialize import AutoSerialize
from dataviva.attrs.models import Bra, Cnae, Cbo

from sqlalchemy import and_

############################################################
# ----------------------------------------------------------
# 2 variable tables
#
############################################################

class Yi(db.Model, AutoSerialize):

    __tablename__ = 'rais_yi'
    year = db.Column(db.Integer(4), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    cbo_diversity = db.Column(db.Integer(11))
    cbo_diversity_eff = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Yi %d.%s>' % (self.year, self.cnae_id)

class Yb_rais(db.Model, AutoSerialize):

    __tablename__ = 'rais_yb'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    cnae_diversity = db.Column(db.Integer(11))
    cnae_diversity_eff = db.Column(db.Float())
    cbo_diversity = db.Column(db.Integer(11))
    cbo_diversity_eff = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Yb_rais %d.%s>' % (self.year, self.bra_id)

class Yo(db.Model, AutoSerialize):

    __tablename__ = 'rais_yo'
    year = db.Column(db.Integer(4), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    cnae_diversity = db.Column(db.Integer(11))
    cnae_diversity_eff = db.Column(db.Float())
    bra_diversity = db.Column(db.Integer(11))
    bra_diversity_eff = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.cbo_id)

############################################################
# ----------------------------------------------------------
# 3 variable tables
#
############################################################

class Ybi(db.Model, AutoSerialize):

    __tablename__ = 'rais_ybi'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    rca = db.Column(db.Float())
    distance = db.Column(db.Float())
    opp_gain = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Ybi %d.%s.%s>' % (self.year, self.bra_id, self.cnae_id)

class Ybo(db.Model, AutoSerialize):

    __tablename__ = 'rais_ybo'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Ybo %d.%s.%s>' % (self.year, self.bra_id, self.cbo_id)

class Yio(db.Model, AutoSerialize):

    __tablename__ = 'rais_yio'
    year = db.Column(db.Integer(4), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    importance = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Yio %d.%s.%s>' % (self.year, self.cnae_id, self.cbo_id)

class Ybio(db.Model, AutoSerialize):

    __tablename__ = 'rais_ybio'
    year = db.Column(db.Integer(4), primary_key=True)
    bra_id = db.Column(db.String(8), db.ForeignKey(Bra.id), primary_key=True)
    cnae_id = db.Column(db.String(5), db.ForeignKey(Cnae.id), primary_key=True)
    cbo_id = db.Column(db.String(6), db.ForeignKey(Cbo.id), primary_key=True)
    wage = db.Column(db.Numeric(16,2))
    num_emp = db.Column(db.Integer(11))
    num_est = db.Column(db.Integer(11))
    wage_avg = db.Column(db.Numeric(16,2))
    num_emp_est = db.Column(db.Float())
    required = db.Column(db.Float())
    wage_growth_pct = db.Column(db.Float())
    wage_growth_pct_5 = db.Column(db.Float())
    wage_growth_val = db.Column(db.Numeric(16,2))
    wage_growth_val_5 = db.Column(db.Numeric(16,2))
    num_emp_growth_pct = db.Column(db.Float())
    num_emp_growth_pct_5 = db.Column(db.Float())
    num_emp_growth_val = db.Column(db.Integer(11))
    num_emp_growth_val_5 = db.Column(db.Integer(11))

    def __repr__(self):
        return '<Ybio %d.%s.%s.%s>' % (self.year, self.bra_id, self.cnae_id, self.cbo_id)
