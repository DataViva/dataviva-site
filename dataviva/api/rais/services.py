from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi , Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc

class Industry :
    def __init__(self, cnae_id):
        self.cnae_id = cnae_id
        self._rais = None
        self._rais_sorted_by_num_jobs = None
        self._rais_sorted_by_wage_avg = None
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

    def __rais_sorted_by_wage_avg__(self):
        self._rais_sorted_by_wage_avg = self.__rais_list__()
        self._rais_sorted_by_wage_avg.sort(key=lambda rais: rais.wage_avg, reverse=True)
        return self._rais_sorted_by_wage_avg            

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


class IndustryOccupation(Industry):
    def __init__(self, cnae_id):
        Industry.__init__(self, cnae_id)
        self.yio_max_year = db.session.query(func.max(Yio.year)).filter_by(cnae_id=cnae_id)
        self.rais_query = Yio.query.join(Cbo).filter(
                Yio.cbo_id == Cbo.id,
                Yio.cnae_id == self.cnae_id,
                Yio.cbo_id_len == 4,                
                Yio.year == self.yio_max_year 
                )

    def occ_with_more_num_jobs_name(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.cbo.name()

    def occ_with_more_num_jobs_value(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.num_jobs

    def occ_with_more_wage_avg_name(self):
        rais = self.__rais_sorted_by_wage_avg__()[0]
        return rais.cbo.name()

    def occ_with_more_wage_avg_value(self):
        rais = self.__rais_sorted_by_wage_avg__()[0]
        return rais.wage
    

class IndustryMunicipality(Industry):
    def __init__(self, cnae_id):
        Industry.__init__(self, cnae_id)
        self.ybi_max_year_br = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)
        self.rais_query = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == self.ybi_max_year_br,      
                )
        
    def municipality_with_more_num_jobs_name(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.bra.name()

    def municipality_with_more_num_jobs_value(self):
        rais = self.__rais_sorted_by_num_jobs__()[0]
        return rais.num_jobs

    def municipality_with_more_wage_avg_name(self):
        rais = self.__rais_sorted_by_wage_avg__()[0]
        return rais.bra.name()

    def municipality_with_more_wage_avg_value(self):
        rais = self.__rais_sorted_by_wage_avg__()[0]
        return rais.wage









