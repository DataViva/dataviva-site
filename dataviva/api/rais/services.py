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

    def get_ybo_county_num_jobs_with_bra_id(self):

        ybo_county_num_jobs_generator = Ybo.query.join(Bra).filter(
                Ybo.cbo_id == self.occupation_id,
                Ybo.bra_id.like(self.bra_id+'%'),
                Ybo.year == self.year,
                Ybo.bra_id_len == 9)\
            .order_by(desc(Ybo.num_jobs)).limit(1)\
            .values(Bra.name_pt,
                    Ybo.num_jobs)

        body = {}
        for name_pt, num_jobs in ybo_county_num_jobs_generator:
            body['county_for_jobs'] = name_pt
            body['num_jobs_county'] = num_jobs

        return body

    def get_ybo_county_wage_avg_with_bra_id(self):

        ybo_county_wage_avg_generator = Ybo.query.join(Bra).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.bra_id.like(self.bra_id+'%'),
            Ybo.year == self.year,
            Ybo.bra_id_len == 9)\
        .order_by(desc(Ybo.wage_avg)).limit(1)\
        .values(Bra.name_pt,
                Ybo.wage_avg)

        body = {}
        for name_pt, wage_avg in ybo_county_wage_avg_generator:
            body['county_bigger_average_monsthly_income'] = name_pt
            body['bigger_average_monsthly_income'] = wage_avg  

        return body 

    def get_ybio_activity_num_jobs(self):

        ybio_activity_num_jobs_generator = Ybio.query.join(Cnae).filter(
            Ybio.cbo_id == self.occupation_id,
            Ybio.bra_id.like(self.bra_id+'%'),
            Ybio.year == self.year,
            Ybio.cnae_id_len == 6)\
        .order_by(desc(Ybio.num_jobs)).limit(1)\
        .values(Cnae.name_pt,
                Ybio.num_jobs)

        body = {}
        for name_pt, num_jobs in ybio_activity_num_jobs_generator:
            body['activity_for_job'] = name_pt
            body['num_activity_for_job'] = num_jobs 

        return body

        
    def get_ybio_activity_wage_avg(self):

        ybio_activity_wage_avg_generator = Ybio.query.join(Cnae).filter(
                Ybio.cbo_id == self.occupation_id,
                Ybio.bra_id.like(self.bra_id+'%'),
                Ybio.year == self.year,
                Ybio.cnae_id_len == 6)\
            .order_by(desc(Ybio.wage_avg)).limit(1)\
            .values(Cnae.name_pt,
                    Ybio.wage_avg)

        body = {}
        for name_pt, wage_avg in ybio_activity_wage_avg_generator:
            body['activity_higher_income'] = name_pt
            body['value_activity_higher_income'] = wage_avg 

        return body

    def get_ybo_county_num_jobs(self):

        ybo_county_num_jobs_generator = Ybo.query.join(Bra).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.year == self.year,
            Ybo.bra_id_len == 9)\
        .order_by(desc(Ybo.num_jobs)).limit(1)\
        .values(Bra.name_pt,
                Ybo.num_jobs)

        body = {}
        for name_pt, num_jobs in ybo_county_num_jobs_generator:
            body['county_for_jobs'] = name_pt
            body['num_jobs_county'] = num_jobs

        return body


    def get_ybo_county_wage_avg(self):

        ybo_county_wage_avg_generator = Ybo.query.join(Bra).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.year == self.year,
            Ybo.bra_id_len == 9)\
        .order_by(desc(Ybo.wage_avg)).limit(1)\
        .values(Bra.name_pt,
                Ybo.wage_avg)

        body = {}
        for name_pt, wage_avg in ybo_county_wage_avg_generator:
            body['county_bigger_average_monsthly_income'] = name_pt
            body['bigger_average_monsthly_income'] = wage_avg   
            
        return body
