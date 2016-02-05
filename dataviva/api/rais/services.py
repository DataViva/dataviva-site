from dataviva.api.attrs.models import Cbo, Bra, Cnae
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio
from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

class Occupation:
    def __init__(self, occupation_id):
        self.occupation_id = occupation_id
        self._rais = None

        self.max_year_query= db.session.query(func.max(Yo.year)).filter(
            Yo.cbo_id == occupation_id)
        self.rais_query = Yo.query.filter(
            Yo.cbo_id == self.occupation_id,
            Yo.year == self.max_year_query)

    def __rais_data__(self):
        if not self._rais:
            rais_data = self.rais_query.first_or_404()
            self._rais = rais_data
        return self._rais

    def year(self):
        rais = self.__rais_data__()
        return rais.year

    def occupation_name(self):
        rais = self.__rais_data__()
        return rais.cbo.name()

    def average_monthly_income(self):
        average_monthly_income = self.__rais_data__().wage_avg
        return average_monthly_income

    def salary_mass(self):
        salary_mass = self.__rais_data__().wage
        return salary_mass

    def total_employment(self):
        total_employment = self.__rais_data__().num_jobs
        return total_employment

    def total_establishments(self):
        total_establishments = self.__rais_data__().num_est
        return total_establishments

class OccupationByLocation(Occupation):
    def __init__(self, occupation_id, bra_id):
        Occupation.__init__(self, occupation_id)
        self.bra_id = bra_id
        self.max_year_query= db.session.query(func.max(Ybo.year)).filter(
            Ybo.cbo_id == occupation_id,
            Ybo.bra_id == self.bra_id)
        self.rais_query = Ybo.query.filter(
            Ybo.cbo_id == self.occupation_id,
            Ybo.bra_id == self.bra_id,
            Ybo.year == self.max_year_query)

    def location_name(self):
        rais = self.__rais_data__()
        return rais.bra.name()

class OccupationMunicipalities(Occupation):
    def __init__ (self, occupation_id):
        Occupation.__init__(self, occupation_id)
        self.max_year_query= db.session.query(func.max(Ybo.year)).filter(
            Ybo.cbo_id == occupation_id)
        self.rais_query = Ybo.query.join(Bra).filter(
                            Ybo.cbo_id == self.occupation_id,
                            Ybo.year == self.max_year_query,
                            Ybo.bra_id_len == 9)

    def __municipality_with_more_jobs__(self):
        if not self._municipality_with_more_jobs:
            self._municipality_with_more_jobs = self.__rais_sorted_by_num_jobs__()[0]
        return self._municipality_with_more_jobs

    def municipality_with_more_jobs(self):
        municipality_name =self.__municipality_with_more_jobs__()
        return municipality_name.bra.name()

    def num_jobs_of_municipality_with_more_jobs(self):
        num_jobs = self.__municipality_with_more_jobs__()
        return num_jobs.num_jobs

    def __municipality_with_biggest_wage_average__(self):
        if not self._municipality_with_more_jobs:
            self._municipality_with_more_jobs = self.__rais_sorted_by_wage_average__()[0]
        return self._municipality_with_more_jobs

    def municipality_with_biggest_wage_average(self):
        municipality_name = self.__municipality_with_biggest_wage_average__()
        return municipality_name.bra.name()

    def wage_average_of_municipality_with_biggest_wage_average(self):
        wage_avg = self.__municipality_with_biggest_wage_average__()
        return wage_avg.wage_avg

class OccupationActivities(Occupation):
    def __init__(self, occupation_id):
        Occupation.__init__(self, occupation_id)
        self.max_year_query= db.session.query(func.max(Yio.year)).filter(
            Yio.cbo_id == occupation_id)
        self.rais_query = Yio.query.join(Cnae).filter(
                            Yio.cbo_id == self.occupation_id,
                            Yio.year == self.max_year_query,
                            Yio.cnae_id_len == 6)

    def __activity_with_more_jobs__(self):
        if not self._activity_with_more_jobs:
            self._activity_with_more_jobs = self.__rais_sorted_by_num_jobs__()[0]
        return self._activity_with_more_jobs

    def activity_with_more_jobs(self):
        activity_name = self.__activity_with_more_jobs__()
        return activity_name.cnae.name()

    def num_jobs_of_activity_with_more_jobs(self):
        num_jobs = self.__activity_with_more_jobs__()
        return num_jobs.num_jobs

    def __activity_with_biggest_wage_average__(self):
        if not self._activity_with_biggest_wage_average:
            self._activity_with_biggest_wage_average = self.__rais_sorted_by_wage_average__()[0]
        return self._activity_with_biggest_wage_average

    def activity_with_biggest_wage_average(self):
        activity_name = self.__activity_with_biggest_wage_average__()
        return activity_name.cnae.name()

    def num_jobs_of_activity_with_biggest_wage_average(self):
        wage_avg = self.__activity_with_biggest_wage_average__()
        return wage_avg.wage_avg




'''

    def __municipality_with_more_jobs__(self):

        if not self._municipality_with_more_jobs:

            ybo_municipality_num_jobs_generator = Ybo.query.join(Bra).filter(
                    Ybo.cbo_id == self.occupation_id,
                    Ybo.bra_id.like(self.bra_id+'%'),
                    Ybo.year == self.year,
                    Ybo.bra_id_len == 9)\
                .order_by(desc(Ybo.num_jobs)).limit(1)\
                .first_or_404()

            municipality_with_more_jobs = {}
            municipality_with_more_jobs['municipality_with_more_jobs'] = ybo_municipality_num_jobs_generator.bra.name()
            municipality_with_more_jobs['municipality_with_more_jobs_value'] = ybo_municipality_num_jobs_generator.num_jobs

            self._municipality_with_more_jobs = municipality_with_more_jobs

        return self._municipality_with_more_jobs


    def __municipality_with_biggest_wage_average__(self):

        if not self._municipality_with_biggest_wage_average:

            ybo_municipality_wage_avg_generator = Ybo.query.join(Bra).filter(
                    Ybo.cbo_id == self.occupation_id,
                    Ybo.bra_id.like(self.bra_id+'%'),
                    Ybo.year == self.year,
                    Ybo.bra_id_len == 9)\
                .order_by(desc(Ybo.wage_avg)).limit(1)\
                .first_or_404()

            municipality_with_biggest_wage_avg = {}
            municipality_with_biggest_wage_avg['municipality_with_biggest_wage_avg'] = ybo_municipality_wage_avg_generator.bra.name()
            municipality_with_biggest_wage_avg['municipality_with_biggest_wage_avg_value'] = ybo_municipality_wage_avg_generator.wage_avg

            self._municipality_with_biggest_wage_average = municipality_with_biggest_wage_avg

        return self._municipality_with_biggest_wage_average

    def __activity_with_more_jobs__(self):

        if not self._activity_with_more_jobs:

            ybio_activity_num_jobs_generator = Ybio.query.join(Cnae).filter(
                    Ybio.cbo_id == self.occupation_id,
                    Ybio.bra_id.like(self.bra_id+'%'),
                    Ybio.year == self.year,
                    Ybio.cnae_id_len == 6)\
                .order_by(desc(Ybio.num_jobs)).limit(1)\
                .first_or_404()

            activity_with_more_jobs = {}
            activity_with_more_jobs['activity_with_more_jobs'] = ybio_activity_num_jobs_generator.cnae.name()
            activity_with_more_jobs['activity_with_more_jobs_value'] = ybio_activity_num_jobs_generator.num_jobs

            self._activity_with_more_jobs = activity_with_more_jobs

        return self._activity_with_more_jobs

    def __activity_with_biggest_wage_average__(self):

        if not self._activity_with_biggest_wage_average:

            ybio_activity_wage_avg_generator = Ybio.query.join(Cnae).filter(
                    Ybio.cbo_id == self.occupation_id,
                    Ybio.bra_id.like(self.bra_id+'%'),
                    Ybio.year == self.year,
                    Ybio.cnae_id_len == 6)\
                .order_by(desc(Ybio.wage_avg)).limit(1)\
                .first_or_404()

            activity_with_biggest_wage_avg = {}
            activity_with_biggest_wage_avg['activity_with_biggest_wage_avg'] = ybio_activity_wage_avg_generator.cnae.name()
            activity_with_biggest_wage_avg['activity_with_biggest_wage_avg_value'] = ybio_activity_wage_avg_generator.wage_avg

            self._activity_with_biggest_wage_average = activity_with_biggest_wage_avg

        return self._activity_with_biggest_wage_average




'''