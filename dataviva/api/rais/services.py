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

    def __rais__(self):
        if not self._rais:
            rais = self.rais_query.first_or_404()
            self._rais = rais
        return self._rais

    def year(self):
        rais = self.__rais__()
        return rais.year

    def occupation_name(self):
        occupation = self.__rais__().cbo
        return occupation.name()

    def average_monthly_income(self):
        average_monthly_income = self.__rais__().wage_avg
        return average_monthly_income

    def salary_mass(self):
        salary_mass = self.__rais__().wage
        return salary_mass

    def total_employment(self):
        total_employment = self.__rais__().num_jobs
        return total_employment

    def total_establishments(self):
        total_establishments = self.__rais__().num_est
        return total_establishments

    def __rais_list__(self):
        if not self._rais:
            rais = self.rais_query.all()
            self._rais = rais
        return self._rais

    def __rais_sorted_by_num_jobs__(self):
        if not self._rais_sorted_by_num_jobs:
            self._rais_sorted_by_num_jobs = self.__rais_list__()
            self._rais_sorted_by_num_jobs.sort(key=lambda rais: rais.num_jobs, reverse=True)
        return self._rais_sorted_by_num_jobs

    def __rais_sorted_by_wage_average__(self):
        if not self._rais_sorted_by_wage_average:
            self._rais_sorted_by_wage_average = self.__rais_list__()
            self._rais_sorted_by_wage_average.sort(key=lambda rais: rais.wage_avg, reverse=True)
        return self._rais_sorted_by_wage_average

    def highest_number_of_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.num_jobs

    def biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.wage_avg


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
        location = self.__rais__().bra
        return location.name()



class OccupationMunicipalities(Occupation):
    def __init__ (self, occupation_id, bra_id):
        Occupation.__init__(self, occupation_id)
        self.max_year_query= db.session.query(func.max(Ybo.year)).filter(
            Ybo.cbo_id == occupation_id)
        self.rais_query = Ybo.query.filter(
                            Ybo.cbo_id == self.occupation_id,
                            Ybo.year == self.max_year_query,
                            Ybo.bra_id_len == 9)
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_wage_average = None

        if bra_id:
            self.bra_id = bra_id
            self.max_year_query = self.max_year_query.filter(Ybo.bra_id == self.bra_id)
            self.rais_query = self.rais_query.filter(Ybo.bra_id.like(self.bra_id+'%'))

    def municipality_with_more_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.bra.name()

    def municipality_with_biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.bra.name()


class OccupationActivities(Occupation):
    def __init__(self, occupation_id, bra_id):
        Occupation.__init__(self, occupation_id)
        self.max_year_query= db.session.query(func.max(Yio.year)).filter(
            Yio.cbo_id == occupation_id)
        self.rais_query = Yio.query.filter(
                            Yio.cbo_id == self.occupation_id,
                            Yio.year == self.max_year_query,
                            Yio.cnae_id_len == 6)
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_wage_average = None

        if bra_id:
            self.bra_id = bra_id
            self.max_year_query= db.session.query(func.max(Ybio.year)).filter(
                Ybio.cbo_id == occupation_id,
                Ybio.bra_id == self.bra_id)
            self.rais_query = Ybio.query.filter(
                Ybio.cbo_id == self.occupation_id,
                Ybio.bra_id.like(self.bra_id+'%'),
                Ybio.year == self.max_year_query ,
                Ybio.cnae_id_len == 6)


    def activity_with_more_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.cnae.name()

    def activity_with_biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.cnae.name()



