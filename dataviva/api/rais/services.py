from dataviva.api.attrs.models import Cbo, Bra, Cnae
from dataviva.api.rais.models import Yo, Ybo, Yio, Ybio
from dataviva import db
from sqlalchemy.sql.expression import func, desc, asc

class Occupation:

    def __init__(self, occupation_id):
        self.occupation_id = occupation_id
        self._data = None 
        self._municipality_with_more_jobs = None
        self._municipality_with_biggest_wage_average = None
        self._activity_with_more_jobs = None
        self._activity_with_biggest_wage_average = None
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_wage_average = None
        year=0
        yo_max_year= db.session.query(func.max(Yo.year)).filter(
            Ybo.cbo_id == occupation_id)\
            .one()
        for years in yo_max_year:
            year = years

        self.year = year
        self.rais_query = Yo.query.filter(
                                Yo.cbo_id == self.occupation_id,
                                Yo.year == self.year)

    def __rais_data__(self):
        if not self._data:
            rais_data = self.rais_query.first_or_404()
            self._data = rais_data
        return self._data

    def __rais_list__(self):
        if not self._data:
            rais_data = self.rais_query.all()
            self._data = rais_data
        return self._data


    def name(self):
        occupation_name = self.__rais_data__().cbo
        return occupation_name.name() #self.__rais_data__()['name']

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


    def __municipality_with_more_jobs__(self):

        if not self._municipality_with_more_jobs: 
            
            ybo_municipality_num_jobs_generator = Ybo.query.join(Bra).filter(
                    Ybo.cbo_id == self.occupation_id,
                    Ybo.year == self.year,
                    Ybo.bra_id_len == 9)\
                .order_by(desc(Ybo.num_jobs)).limit(1)\
                .first_or_404()
    
            municipality_with_more_jobs = {}
            municipality_with_more_jobs['municipality_with_more_jobs'] = ybo_municipality_num_jobs_generator.bra.name()
            municipality_with_more_jobs['municipality_with_more_jobs_value'] = ybo_municipality_num_jobs_generator.num_jobs

            self._municipality_with_more_jobs = municipality_with_more_jobs

        return self._municipality_with_more_jobs

    
    def municipality_with_more_jobs(self):
        return self.__municipality_with_more_jobs__()['municipality_with_more_jobs']

    def num_jobs_of_municipality_with_more_jobs (self):
        return self.__municipality_with_more_jobs__()['municipality_with_more_jobs_value']


    def __municipality_with_biggest_wage_average__(self):

        if not self._municipality_with_biggest_wage_average:

            ybo_municipality_wage_avg_generator = Ybo.query.join(Bra).filter(
                    Ybo.cbo_id == self.occupation_id,
                    Ybo.year == self.year,
                    Ybo.bra_id_len == 9)\
                .order_by(desc(Ybo.wage_avg)).limit(1)\
                .first_or_404()
    
            municipality_with_biggest_wage_average = {}
            municipality_with_biggest_wage_average['municipality_with_biggest_wage_avg'] = ybo_municipality_wage_avg_generator.bra.name()
            municipality_with_biggest_wage_average['municipality_with_biggest_wage_avg_value'] = ybo_municipality_wage_avg_generator.wage_avg  

            self._municipality_with_biggest_wage_average = municipality_with_biggest_wage_average

        return self._municipality_with_biggest_wage_average


    def municipality_with_biggest_wage_average(self):
        return self.__municipality_with_biggest_wage_average__()['municipality_with_biggest_wage_avg']

    def wage_average_of_municipality_with_biggest_wage_average(self):
        return self.__municipality_with_biggest_wage_average__()['municipality_with_biggest_wage_avg_value']

    def __activity_with_more_jobs__(self):

        if not self._activity_with_more_jobs:

            yio_activity_num_jobs_generator = Yio.query.join(Cnae).filter(
                    Yio.cbo_id == self.occupation_id,
                    Yio.year == self.year,
                    Yio.cnae_id_len == 6)\
                .order_by(desc(Yio.num_jobs)).limit(1)\
                .first_or_404()

            activity_with_more_jobs = {}
            activity_with_more_jobs['activity_with_more_jobs'] = yio_activity_num_jobs_generator.cnae.name()
            activity_with_more_jobs['activity_with_more_jobs_value'] = yio_activity_num_jobs_generator.num_jobs

            self._activity_with_more_jobs = activity_with_more_jobs

        return self._activity_with_more_jobs

    def activity_with_more_jobs(self):
        return self.__activity_with_more_jobs__()['activity_with_more_jobs']

    def num_jobs_of_activity_with_more_jobs(self):
        return self.__activity_with_more_jobs__()['activity_with_more_jobs_value']

    def __activity_with_biggest_wage_average__(self):

        if not self._activity_with_biggest_wage_average:

            yio_activity_wage_avg_generator = Yio.query.join(Cnae).filter(
                    Yio.cbo_id == self.occupation_id,
                    Yio.year == self.year,
                    Yio.cnae_id_len == 6)\
                .order_by(desc(Yio.wage_avg)).limit(1)\
                .first_or_404()

            activity_with_biggest_wage_avg = {}
            activity_with_biggest_wage_avg['activity_with_biggest_wage_avg'] = yio_activity_wage_avg_generator.cnae.name()
            activity_with_biggest_wage_avg['activity_with_biggest_wage_avg_value'] = yio_activity_wage_avg_generator.wage_avg  

            self._activity_with_biggest_wage_average = activity_with_biggest_wage_avg

        return self._activity_with_biggest_wage_average   

    def activity_with_biggest_wage_average(self):
        return self.__activity_with_biggest_wage_average__()['activity_with_biggest_wage_avg']

    def num_jobs_of_activity_with_biggest_wage_avg(self):
        return self.__activity_with_biggest_wage_average__()['activity_with_biggest_wage_avg_value']

    def __rais_sorted_by_num_jobs__(self):
        self._rais_sorted_by_num_jobs = self.__rais_list__()
        self._rais_sorted_by_num_jobs.sort(key=lambda rais: rais.num_jobs, reverse=True)
        return self._rais_sorted_by_num_jobs

    def __rais_sorted_by_wage_average__(self):
        self._rais_sorted_by_wage_average = self.__rais_list__()
        self._rais_sorted_by_wage_average.sort(key=lambda rais: rais.wage_avg , reverse=True)
        return self._rais_sorted_by_wage_average

#-----------------------------
class OccupationMunicipalities(Occupation):
    def __init__ (self, occupation_id):
        Occupation.__init__(self, occupation_id)
        self.rais_query = Ybo.query.join(Bra).filter(
                            Ybo.cbo_id == self.occupation_id,
                            Ybo.year == self.year,
                            Ybo.bra_id_len == 9)
        #self.municipality_data = None

    def municipality_with_more_jobs(self):
        municipality_with_more_jobs = self.__rais_sorted_by_num_jobs__()[0]
        return municipality_with_more_jobs.bra.name()

    def num_jobs_of_municipality_with_more_jobs(self):
        num_jobs_of_municipality_with_more_jobs = self.__rais_sorted_by_num_jobs__()[0]
        return num_jobs_of_municipality_with_more_jobs.num_jobs

    def municipality_with_biggest_wage_average(self):
        municipality_with_biggest_wage_average = self.__rais_sorted_by_wage_average__()[0]
        return municipality_with_biggest_wage_average.bra.name()

    def wage_average_of_municipality_with_biggest_wage_average(self):
        wage_average_of_municipality_with_biggest_wage_average = self.__rais_sorted_by_wage_average__()[0]
        return wage_average_of_municipality_with_biggest_wage_average.wage_avg

#-------------------
class OccupationActivities(Occupation):
    def __init__(self, occupation_id):
        Occupation.__init__(self, occupation_id)
        self.rais_query = Yio.query.join(Cnae).filter(
                            Yio.cbo_id == self.occupation_id,
                            Yio.year == self.year,
                            Yio.cnae_id_len == 6)

    def activity_with_more_jobs(self):
        activity_with_more_jobs = self.__rais_sorted_by_num_jobs__()[0]
        return activity_with_more_jobs.cnae.name()

    def num_jobs_of_activity_with_more_jobs(self):
        num_jobs_of_activity_with_more_jobs = self.__rais_sorted_by_num_jobs__()[0]
        return num_jobs_of_activity_with_more_jobs.num_jobs

    def activity_with_biggest_wage_average(self):
        activity_with_biggest_wage_average = self.__rais_sorted_by_wage_average__()[0]
        return activity_with_biggest_wage_average.cnae.name()

    def num_jobs_of_activity_with_biggest_wage_average(self):
        num_jobs_of_activity_with_biggest_wage_avg = self.__rais_sorted_by_wage_average__()[0]
        return activity_with_biggest_wage_average.wage_avg



#-----------------------------
class OccupationByLocation(Occupation):

    def __init__(self, occupation_id, bra_id):
        
        Occupation.__init__(self, occupation_id)
        self.bra_id = bra_id

        year=0
        ybo_max_year= db.session.query(func.max(Ybo.year)).filter(
            Ybo.cbo_id == occupation_id, 
            Ybo.bra_id == bra_id)\
            .one()
        for years in ybo_max_year:
            year = years

        self.year = year

        self.rais_query = Ybo.query.filter(
                                Ybo.cbo_id == self.occupation_id,
                                Ybo.bra_id == self.bra_id,
                                Ybo.year == self.year)

    def __rais_data__(self):
        
        if not self._data:
            rais_data = self.rais_query.first_or_404()
            self._data = rais_data
        return self._data


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
        



