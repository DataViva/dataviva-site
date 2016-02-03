from dataviva.api.attrs.models import Cbo, Bra, Cnae
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio
from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

class Occupation:

    def __init__(self, occupation_id, bra_id=None):
        
        self.occupation_id = occupation_id
        self.bra_id = bra_id
        self._header = None 

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


    def __header_with_bra_id__(self):
        
        if not self._header:

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

            self._header = header

        return self._header


    def name_with_bra_id(self):
        return self.__header_with_bra_id__()['name']

    def average_monthly_income_with_bra_id(self):
        return self.__header_with_bra_id__()['average_monthly_income']

    def salary_mass_with_bra_id(self):
        return self.__header_with_bra_id__()['salary_mass']

    def total_employment_with_bra_id(self):
        return self.__header_with_bra_id__()['total_employment']

    def total_establishments_with_bra_id(self):
        return self.__header_with_bra_id__()['total_establishments']


    def __header__(self):
        
        if not self._header:

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

            self._header = header

        return self._header


    def name(self):
        return self.__header__()['name']

    def average_monthly_income(self):
        return self.__header__()['average_monthly_income']

    def salary_mass(self):
        return self.__header__()['salary_mass']

    def total_employment(self):
        return self.__header__()['total_employment']

    def total_establishments(self):
        return self.__header__()['total_establishments']  


    def municipality_with_more_jobs_with_bra_id(self):

        ybo_municipality_num_jobs_generator = Ybo.query.join(Bra).filter(
                Ybo.cbo_id == self.occupation_id,
                Ybo.bra_id.like(self.bra_id+'%'),
                Ybo.year == self.year,
                Ybo.bra_id_len == 9)\
            .order_by(desc(Ybo.num_jobs)).limit(1)\
            .values(Bra.name_pt,
                    Ybo.num_jobs)

        body = {}
        for name_pt, num_jobs in ybo_municipality_num_jobs_generator:
            body['municipality_with_more_jobs'] = name_pt
            body['municipality_with_more_jobs_value'] = num_jobs

        return body

    def municipality_with_biggest_wage_avg_with_bra_id(self):

        ybo_municipality_wage_avg_generator = Ybo.query.join(Bra).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.bra_id.like(self.bra_id+'%'),
            Ybo.year == self.year,
            Ybo.bra_id_len == 9)\
        .order_by(desc(Ybo.wage_avg)).limit(1)\
        .values(Bra.name_pt,
                Ybo.wage_avg)

        body = {}
        for name_pt, wage_avg in ybo_municipality_wage_avg_generator:
            body['municipality_with_bigger_wage_avg'] = name_pt
            body['municipality_with_bigger_wage_avg_value'] = wage_avg  

        return body 

    def activity_with_more_jobs_with_bra_id(self):

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
            body['activity_with_more_jobs'] = name_pt
            body['activity_with_more_jobs_value'] = num_jobs 

        return body

        
    def activity_with_biggest_wage_avg_with_bra_id(self):

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
            body['activity_with_biggest_wage_avg'] = name_pt
            body['activity_with_biggest_wage_avg_value'] = wage_avg 
        return body

    def municipality_with_more_jobs(self):

        ybo_municipality_num_jobs_generator = Ybo.query.join(Bra).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.year == self.year,
            Ybo.bra_id_len == 9)\
        .order_by(desc(Ybo.num_jobs)).limit(1)\
        .values(Bra.name_pt,
                Ybo.num_jobs)

        body = {}
        for name_pt, num_jobs in ybo_municipality_num_jobs_generator:
            body['municipality_with_more_jobs'] = name_pt
            body['municipality_with_more_jobs_value'] = num_jobs

        return body


    def municipality_with_biggest_wage_avg(self):

        ybo_municipality_wage_avg_generator = Ybo.query.join(Bra).filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.year == self.year,
            Ybo.bra_id_len == 9)\
        .order_by(desc(Ybo.wage_avg)).limit(1)\
        .values(Bra.name_pt,
                Ybo.wage_avg)

        body = {}
        for name_pt, wage_avg in ybo_municipality_wage_avg_generator:
            body['municipality_with_bigger_wage_avg'] = name_pt
            body['municipality_with_bigger_wage_avg_value'] = wage_avg  

        return body

    def activity_with_more_jobs(self):

        yio_activity_num_jobs_generator = Yio.query.join(Cnae).filter(
            Yio.cbo_id == self.occupation_id,
            Yio.year == self.year,
            Yio.cnae_id_len == 6)\
        .order_by(desc(Yio.num_jobs)).limit(1)\
        .values(Cnae.name_pt,
                Yio.num_jobs)

        body = {}
        for name_pt, num_jobs in yio_activity_num_jobs_generator:
            body['activity_with_more_jobs'] = name_pt
            body['activity_with_more_jobs_value'] = num_jobs

        return body

    def activity_with_biggest_wage_avg(self):

        yio_activity_wage_avg_generator = Yio.query.join(Cnae).filter(
            Yio.cbo_id == self.occupation_id,
            Yio.year == self.year,
            Yio.cnae_id_len == 6)\
        .order_by(desc(Yio.wage_avg)).limit(1)\
        .values(Cnae.name_pt,
                Yio.wage_avg)

        body = {}
        for name_pt, wage_avg in yio_activity_wage_avg_generator:
            body['activity_with_biggest_wage_avg'] = name_pt
            body['activity_with_biggest_wage_avg_value'] = wage_avg  

        return body   