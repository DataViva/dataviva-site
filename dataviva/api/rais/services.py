from dataviva.api.attrs.models import Cbo, Bra, Cnae
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio
from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

class Occupation:
    def __init__(self, occupation_id, bra_id=None):
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


    def get_ybo_header(self):

        ybo_header_generator = Ybo.query.join(Cbo).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.bra_id == self.bra_id,
            Ybo.year == self.year)\
            .values(Cbo.name_pt,
                    Ybo.wage_avg,
                    Ybo.wage,
                    Ybo.num_jobs,
                    Ybo.num_est)

        header = {}
        for name_pt, wage_avg, wage, num_jobs, num_est in ybo_header_generator:
            header['name'] = name_pt
            header['average_monthly_income'] = wage_avg
            header['salary_mass'] = wage
            header['total_employment'] = num_jobs
            header['total_establishments'] = num_est

        return header

    def get_yo_header(self):

        yo_header_generator = Yo.query.join(Cbo).filter(
            Yo.cbo_id == self.occupation_id,
            Yo.year == self.year)\
            .values(Cbo.name_pt,
                    Yo.wage_avg,
                    Yo.wage,
                    Yo.num_jobs,
                    Yo.num_est)
        header = {}
        for name_pt, wage_avg, wage, num_jobs, num_est in yo_header_generator:
            header['name'] = name_pt
            header['average_monthly_income'] = wage_avg
            header['salary_mass'] = wage
            header['total_employment'] = num_jobs
            header['total_establishments'] = num_est

        return header




