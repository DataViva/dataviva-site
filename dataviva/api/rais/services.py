from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi, Yo, Ybo, Ybi, Yio, Ybio, Yb_rais
from dataviva import db
from sqlalchemy import func, desc


class Industry:
    def __init__(self, cnae_id):
        self.cnae_id = cnae_id
        self._rais = None
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_wage_average = None
        self.yi_max_year = db.session.query(func.max(Yi.year)).filter_by(cnae_id=cnae_id)
        self.rais_query = Yi.query.join(Cnae).filter(
                Yi.cnae_id == self.cnae_id,
                Yi.year == self.yi_max_year
                )

    def __rais__(self):
        if not self._rais:
            rais_data = self.rais_query.first_or_404()
            self._rais = rais_data
        return self._rais

    def __rais_list__(self):
        if not self._rais:
            rais_data = self.rais_query.all()
            self._rais = rais_data
        return self._rais

    def __rais_sorted_by_num_jobs__(self):
        self._rais_sorted_by_num_jobs = self.__rais_list__()
        self._rais_sorted_by_num_jobs.sort(key=lambda rais: rais.num_jobs, reverse=True)
        return self._rais_sorted_by_num_jobs

    def __rais_sorted_by_wage_average__(self):
        self._rais_sorted_by_wage_average = self.__rais_list__()
        self._rais_sorted_by_wage_average.sort(key=lambda rais: rais.wage_avg, reverse=True)
        return self._rais_sorted_by_wage_average

    def get_name(self):
        base_industry = self.__rais__().cnae
        return base_industry.name()

    def get_year(self):
        return self.__rais__().year

    def average_monthly_income(self):
        return self.__rais__().wage_avg

    def salary_mass(self):
        return self.__rais__().wage

    def num_jobs(self):
        return self.__rais__().num_jobs

    def num_establishments(self):
        return self.__rais__().num_est

    def highest_number_of_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.num_jobs

    def biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.wage_avg


class Occupation:
    def __init__(self, occupation_id):
        self.occupation_id = occupation_id
        self._rais = None

        self.max_year_query = db.session.query(func.max(Yo.year)).filter(
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

    def age_avg(self):
        return self.__rais__().age_avg

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


class IndustryByLocation(Industry):
    def __init__(self, bra_id, cnae_id):
        self.bra_id = bra_id
        self.cnae_id = cnae_id
        self._rais = None
        self.ybi_max_year = db.session.query(func.max(Ybi.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
        self.rais_query = Ybi.query.filter(
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id == self.bra_id,
                Ybi.year == self.ybi_max_year
                )

    def rca(self):
        return self.__rais__().rca

    def distance(self):
        return self.__rais__().distance

    def opportunity_gain(self):
        return self.__rais__().opp_gain

    def name(self):
        bra_query = Bra.query.filter(Bra.id == self.bra_id).first()
        return bra_query.name()


class IndustryOccupation(Industry):
    def __init__(self, cnae_id, bra_id):
        Industry.__init__(self, cnae_id)
        self.max_year = db.session.query(func.max(Yio.year)).filter_by(cnae_id=cnae_id)
        self.rais_query = Yio.query.join(Cbo).filter(
                Yio.cbo_id == Cbo.id,
                Yio.cnae_id == self.cnae_id,
                Yio.cbo_id_len == 4,
                Yio.year == self.max_year
                )

        if bra_id:
            self.bra_id = bra_id
            self.max_year = db.session.query(func.max(Ybio.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
            self.rais_query = Ybio.query.join(Cbo).filter(
                Cbo.id == Ybio.cbo_id,
                Ybio.cnae_id == self.cnae_id,
                Ybio.cbo_id_len == 4,
                Ybio.bra_id == self.bra_id,
                Ybio.year == self.max_year
            )

    def occupation_with_more_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.cbo.name()

    def occupation_with_biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.cbo.name()


class IndustryMunicipality(Industry):
    def __init__(self, cnae_id, bra_id):
        Industry.__init__(self, cnae_id)
        self.max_year = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)
        self.rais_query = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == self.max_year,
                )
        self.state_query = Ybi.query.join(Bra).filter(
                Ybi.cnae_id == self.cnae_id,
                Ybi.year == self.max_year,
                Ybi.bra_id_len == 3
                ).order_by(desc(Ybi.num_jobs)).first()

        if bra_id:
            self.bra_id = bra_id
            self.max_year = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)
            self.rais_query = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.bra_id.like(self.bra_id+'%'),
                Ybi.year == self.max_year
                )

    def municipality_with_more_num_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.bra.name()

    def municipality_with_more_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.bra.name()

    def state(self):
        return self.state_query.bra.name()

    def state_num_jobs(self):
        return self.state_query.num_jobs


class OccupationByLocation(Occupation):
    def __init__(self, occupation_id, bra_id):
        Occupation.__init__(self, occupation_id)
        self.bra_id = bra_id
        self.max_year_query = db.session.query(func.max(Ybo.year)).filter(
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
    def __init__(self, occupation_id, bra_id):
        Occupation.__init__(self, occupation_id)
        self.max_year_query = db.session.query(func.max(Ybo.year)).filter(
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

    def municipality_with_more_jobs_state(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.bra.id[1:3]

    def municipality_with_biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.bra.name()

    def municipality_with_biggest_wage_average_state(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.bra.id[1:3]


class OccupationActivities(Occupation):
    def __init__(self, occupation_id, bra_id):
        Occupation.__init__(self, occupation_id)
        self.max_year_query = db.session.query(func.max(Yio.year)).filter(
            Yio.cbo_id == occupation_id)
        self.rais_query = Yio.query.filter(
                            Yio.cbo_id == self.occupation_id,
                            Yio.year == self.max_year_query,
                            Yio.cnae_id_len == 6)
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_wage_average = None

        if bra_id:
            self.bra_id = bra_id
            self.max_year_query = db.session.query(func.max(Ybio.year)).filter(
                Ybio.cbo_id == occupation_id,
                Ybio.bra_id == self.bra_id)
            self.rais_query = Ybio.query.filter(
                Ybio.cbo_id == self.occupation_id,
                Ybio.bra_id.like(self.bra_id+'%'),
                Ybio.year == self.max_year_query,
                Ybio.cnae_id_len == 6)

    def activity_with_more_jobs(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.cnae.name()

    def activity_with_biggest_wage_average(self):
        rais = self.__rais_sorted_by_wage_average__()[0]
        return rais.cnae.name()


class LocationIndustry:
    def __init__(self, bra_id):
        self.bra_id = bra_id
        self._rais = None
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_distance = None
        self._rais_sorted_by_opp_gain = None
        self.max_year_query = db.session.query(func.max(Ybi.year)).filter(
            bra_id == self.bra_id)
        self.rais_query = Ybi.query.join(Cnae).filter(
                Ybi.bra_id == self.bra_id,
                Ybi.cnae_id_len == 6,
                Ybi.num_jobs is not None,
                Ybi.year == self.max_year_query
        )

    def __rais__(self):
        if not self._rais:
            rais_data = self.rais_query.first_or_404()
            self._rais = rais_data
        return self._rais

    def __rais_list__(self):
        if not self._rais:
            rais_data = self.rais_query.all()
            self._rais = rais_data
        return self._rais

    def __rais_sorted_by_num_jobs__(self):
        if not self._rais_sorted_by_num_jobs:
            self._rais_sorted_by_num_jobs = self.__rais_list__()
            self._rais_sorted_by_num_jobs.sort(key=lambda rais: rais.num_jobs, reverse=True)
        return self._rais_sorted_by_num_jobs

    def __rais_sorted_by_distance__(self):
        if not self._rais_sorted_by_distance:
            self._rais_sorted_by_distance = self.__rais_list__()
            self._rais_sorted_by_distance.sort(key=lambda rais: rais.distance, reverse=False)
        return self._rais_sorted_by_distance

    def __rais_sorted_by_opp_gain__(self):
        if not self._rais_sorted_by_opp_gain:
            self._rais_sorted_by_opp_gain = self.__rais_list__()
            self._rais_sorted_by_opp_gain.sort(key=lambda rais: rais.opp_gain, reverse=True)
        return self._rais_sorted_by_opp_gain

    def main_industry_by_num_jobs(self):
        try:
            rais = self.__rais_sorted_by_num_jobs__()[0]
        except IndexError:
            return None
        else:
            return rais.num_jobs

    def main_industry_by_num_jobs_name(self):
        try:
            rais = self.__rais_sorted_by_num_jobs__()[0]
        except IndexError:
            return None
        else:
            return rais.cnae.name()


class LocationOccupation(LocationIndustry):
    def __init__(self, bra_id):
        LocationIndustry.__init__(self, bra_id)
        self.bra_id = bra_id
        self.max_year_query = db.session.query(func.max(Ybo.year)).filter(
            bra_id == self.bra_id)
        self.rais_query = Ybo.query.join(Cbo).filter(
                Ybo.bra_id == self.bra_id,
                Ybo.cbo_id_len == 4,
                Ybo.num_jobs is not None,
                Ybo.year == self.max_year_query
        )

    def main_occupation_by_num_jobs(self):
        try:
            rais = self.__rais_sorted_by_num_jobs__()[0]
        except IndexError:
            return None
        else:
            return rais.num_jobs

    def main_occupation_by_num_jobs_name(self):
        try:
            rais = self.__rais_sorted_by_num_jobs__()[0]
        except IndexError:
            return None
        else:
            return rais.cbo.name()


class LocationJobs(LocationIndustry):
    def __init__(self, bra_id):
        LocationIndustry.__init__(self, bra_id)
        self.bra_id = bra_id
        self.max_year_query = db.session.query(func.max(Yb_rais.year)).filter(
            bra_id == self.bra_id)
        self.rais_query = Yb_rais.query.filter(
            Yb_rais.bra_id == self.bra_id,
            Yb_rais.year == self.max_year_query)

    def avg_wage(self):
        return self.__rais__().wage_avg

    def wage(self):
        return self.__rais__().wage

    def total_jobs(self):
        return self.__rais__().num_jobs


class LocationDistance(LocationIndustry):
    def __init__(self, bra_id):
        LocationIndustry.__init__(self, bra_id)
        self.bra_id = bra_id
        self.max_year_query = db.session.query(func.max(Ybi.year)).filter(
            bra_id == self.bra_id)
        self.rais_query = Ybi.query.join(Cnae).filter(
            Ybi.bra_id == self.bra_id,
            Ybi.cnae_id_len == 6,
            Ybi.year == self.max_year_query,
            Ybi.distance is not None)

    def less_distance_by_occupation(self):
        try:
            rais = self.__rais_sorted_by_distance__()[0]
        except IndexError:
            return None
        else:
            return rais.distance

    def less_distance_by_occupation_name(self):
        try:
            rais = self.__rais_sorted_by_distance__()[0]
        except IndexError:
            return None
        else:
            return rais.cnae.name()


class LocationOppGain(LocationIndustry):
    def __init__(self, bra_id):
        LocationIndustry.__init__(self, bra_id)
        self.bra_id = bra_id
        self.max_year_query = db.session.query(func.max(Ybi.year)).filter(
            bra_id == self.bra_id)
        self.opp_gain_query = db.session.query(func.max(Ybi.opp_gain)).filter(
            Ybi.bra_id == self.bra_id,
            Ybi.year == self.max_year_query,
            Ybi.opp_gain is not None)
        self.rais_query = Ybi.query.join(Cnae).filter(
            Ybi.bra_id == self.bra_id,
            Ybi.cnae_id_len == 6,
            Ybi.year == self.max_year_query,
            Ybi.opp_gain is not None,
            Ybi.opp_gain == self.opp_gain_query)

    def opportunity_gain_by_occupation(self):
        try:
            rais = self.__rais_sorted_by_opp_gain__()[0]
        except IndexError:
            return None
        else:
            return rais.opp_gain

    def opportunity_gain_by_occupation_name(self):
        try:
            rais = self.__rais_sorted_by_opp_gain__()[0]
        except IndexError:
            return None
        else:
            return rais.cnae.name()
