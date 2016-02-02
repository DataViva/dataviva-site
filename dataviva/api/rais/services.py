from dataviva.api.attrs.models import Cbo, Bra, Cnae
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio
from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

class Occupation:
    def __init__(self, occupation_id, bra_id):
        self.occupation_id = occupation_id
        self.bra_id = bra_id

        year=0
        if bra_id: 
            ybo_max_year= db.session.query(func.max(Ybo.year)).filter(
                Ybo.cbo_id == occupation_id, 
                Ybo.bra_id == bra_id)\
                .one()
            for years in ybo_max_year:
                year = years
        else:
            yo_max_year= db.session.query(func.max(Yo.year)).filter(
            Ybo.cbo_id == occupation_id)\
            .one()
            for years in yo_max_year:
                year = years

        self.year = year


