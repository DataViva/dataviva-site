from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi , Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc

class Industry :
    def __init__(self, cnae_id):
        self.cnae_id = cnae_id
        self.industry_headers = {}
        self.occ_jobs = {}
        self.occ_wage_avg = {}  
        self.municipality_jobs = {}
        self.municipality_wage_avg = {}

        self.yi_max_year_br = db.session.query(func.max(Yi.year)).filter_by(cnae_id=cnae_id)
        self.yio_max_year_br = db.session.query(func.max(Yio.year)).filter_by(cnae_id=cnae_id)
        self.ybi_max_year_br = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)
        
    def get_name(self): 
        return Cnae.query.filter_by(id=self.cnae_id).one().name()  


    def get_year(self):
        return self.yi_max_year_br.scalar()         

    
    #-----
        
    def __rais_values__(self):
        if not self.industry_headers  :
            headers_generator = Yi.query.filter(
                Yi.cnae_id == self.cnae_id,
                Yi.year == self.yi_max_year_br    
                ).values(Yi.wage, Yi.num_jobs, Yi.num_est, Yi.wage_avg )

            for  wage, num_jobs, num_est, wage_avg in headers_generator:        
                self.industry_headers['average_monthly_income'] = wage_avg
                self.industry_headers['salary_mass'] = wage
                self.industry_headers['num_jobs'] = num_jobs
                self.industry_headers['num_establishments'] = num_est

        return self.industry_headers

    def average_monthly_income(self): 
        return self.__rais_values__()['average_monthly_income']

    def salary_mass(self):
        return self.__rais_values__()['salary_mass']

    def num_jobs(self):
        return self.__rais_values__()['num_jobs']

    def num_establishments(self):
        return self.__rais_values__()['num_establishments'] 

    
    #-----
      
    def  __occ_with_more_number_jobs__(self) :

        if not self.occ_jobs : 
            occupation_jobs_obj = Yio.query.join(Cbo).filter(
                Yio.cbo_id == Cbo.id,
                Yio.cnae_id == self.cnae_id,
                Yio.cbo_id_len == 4,                
                Yio.year == self.yio_max_year_br 
                ).order_by(desc(Yio.num_jobs)).limit(1).one()

                       
            self.occ_jobs['occ_with_more_number_jobs_name'] = occupation_jobs_obj.cbo.name() 
            self.occ_jobs['occ_with_more_number_jobs_value'] = occupation_jobs_obj.num_jobs

        return self.occ_jobs 

    def get_occ_with_more_number_jobs_name(self):
        return self.__occ_with_more_number_jobs__()['occ_with_more_number_jobs_name']    

    def get_occ_with_more_number_jobs_value(self):
        return self.__occ_with_more_number_jobs__()['occ_with_more_number_jobs_value'] 

    #-----

    def __occ_with_more_wage_avg__(self):
        if not self.occ_wage_avg :
            occupation_wage_avg_obj = Yio.query.join(Cbo).filter(
                Yio.cbo_id == Cbo.id,
                Yio.cnae_id == self.cnae_id,
                Yio.cbo_id_len == 4,                 
                Yio.year == self.yio_max_year_br 
                ).order_by(desc(Yio.wage_avg)).limit(1).one()

                  
            self.occ_wage_avg['occ_with_more_wage_avg_name'] = occupation_wage_avg_obj.cbo.name()
            self.occ_wage_avg['occ_with_more_wage_avg_value'] = occupation_wage_avg_obj.wage_avg

        return self.occ_wage_avg     

    def get_occ_with_more_wage_avg_name(self):
        return self.__occ_with_more_wage_avg__()['occ_with_more_wage_avg_name']

    def get_occ_with_more_wage_avg_value(self):
        return self.__occ_with_more_wage_avg__()['occ_with_more_wage_avg_value']

    #-----

    def __municipality_with_more_num_jobs__(self):
        if not self.municipality_jobs:
            county_jobs_obj = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == self.ybi_max_year_br,      
                ).order_by(desc(Ybi.num_jobs)).limit(1).one()
        
              
            self.municipality_jobs['municipality_with_more_num_jobs_name'] = county_jobs_obj.bra.name()
            self.municipality_jobs['municipality_with_more_num_jobs_value'] = county_jobs_obj.num_jobs

        return self.municipality_jobs

    def get_municipality_with_more_num_jobs_name(self):
        return self.__municipality_with_more_num_jobs__()['municipality_with_more_num_jobs_name']
    
    def get_municipality_with_more_num_jobs_value(self):
        return self.__municipality_with_more_num_jobs__()['municipality_with_more_num_jobs_value']

    #-----
    
    def __municipality_with_more_wage_avg__(self):
        if not self.municipality_wage_avg:
            county_wage_avg_obj = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == self.ybi_max_year_br,    
                ).order_by(desc(Ybi.wage_avg)).limit(1).one()
            

                  
            self.municipality_wage_avg['municipality_with_more_wage_avg_name'] = county_wage_avg_obj.bra.name()
            self.municipality_wage_avg['municipality_with_more_wage_avg_value'] =  county_wage_avg_obj.wage_avg    
        return self.municipality_wage_avg

    def get_municipality_with_more_wage_avg_name(self):
        return self.__municipality_with_more_wage_avg__()['municipality_with_more_wage_avg_name']    
    
    def get_municipality_with_more_wage_avg_value(self):
        return self.__municipality_with_more_wage_avg__()['municipality_with_more_wage_avg_value']


#########################


class IndustryByLocation(Industry) :
    def __init__(self, bra_id, cnae_id):
        self.bra_id = bra_id
        self.cnae_id = cnae_id
        self.industry_headers = {} 
        self.occ_jobs = {} 
        self.occ_wage_avg = {}  
        self.municipality_jobs = {} 
        self.municipality_wage_avg = {}

        self.ybi_max_year=db.session.query(func.max(Ybi.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)        
        self.ybio_max_year=db.session.query(func.max(Ybio.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)


    def get_year(self):
        return self.ybi_max_year.scalar()

    def __rais_values__(self):
        if not self.industry_headers : 
            headers_generate = Ybi.query.filter(
                Ybi.cnae_id==self.cnae_id,
                Ybi.bra_id == self.bra_id,
                Ybi.year==self.ybi_max_year
                ).values(
                    Ybi.wage, Ybi.num_jobs, 
                    Ybi.num_est, Ybi.wage_avg, 
                    Ybi.rca, Ybi.distance, 
                    Ybi.opp_gain) 

            
            for wage, num_jobs, num_est, wage_avg, rca, distance, opp_gain in headers_generate:
               self.industry_headers['average_monthly_income'] = wage_avg
               self.industry_headers['salary_mass'] = wage
               self.industry_headers['num_jobs'] = num_jobs
               self.industry_headers['num_establishments'] =  num_est
               self.industry_headers['rca'] =  rca
               self.industry_headers['distance'] =  distance
               self.industry_headers['opportunity_gain'] =  opp_gain          

        return self.industry_headers     

    def rca(self):
        return self.__rais_values__()['rca']

    def distance(self):
        return self.__rais_values__()['distance']

    def opportunity_gain(self):
        return self.__rais_values__()['opportunity_gain'] 

    #-----

    def  __occ_with_more_number_jobs__(self) : 
        if not self.occ_jobs : 
            occ_jobs_obj = Ybio.query.join(Cbo).filter(
                Cbo.id == Ybio.cbo_id,
                Ybio.cnae_id == self.cnae_id,
                Ybio.cbo_id_len == 4,
                Ybio.bra_id == self.bra_id,
                Ybio.year == self.ybio_max_year
                ).order_by(desc(Ybio.num_jobs)).limit(1).one()  

 
            self.occ_jobs['occ_with_more_number_jobs_value'] = occ_jobs_obj.num_jobs
            self.occ_jobs['occ_with_more_number_jobs_name'] =  occ_jobs_obj.cbo.name()

        return self.occ_jobs

    #-----

    def __occ_with_more_wage_avg__(self):
        if not self.occ_wage_avg:
            occ_wage_avg_obj = Ybio.query.join(Cbo).filter(
                Cbo.id == Ybio.cbo_id,
                Ybio.cnae_id == self.cnae_id,
                Ybio.cbo_id_len == 4,
                Ybio.bra_id == self.bra_id,
                Ybio.year == self.ybio_max_year
                ).order_by(desc(Ybio.wage_avg)).limit(1).one() 

            self.occ_wage_avg['occ_with_more_wage_avg_value'] = occ_wage_avg_obj.wage_avg
            self.occ_wage_avg['occ_with_more_wage_avg_name'] = occ_wage_avg_obj.cbo.name()

        return self.occ_wage_avg

    #-----
        
    def __municipality_with_more_num_jobs__(self):
        if not self.municipality_jobs :
            county_jobs_obj = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.bra_id.like(self.bra_id+'%'), 
                Ybi.year == self.ybi_max_year    
                ).order_by(desc(Ybi.num_jobs)).limit(1).one()
                      
            self.municipality_jobs['municipality_with_more_num_jobs_value'] = county_jobs_obj.num_jobs
            self.municipality_jobs['municipality_with_more_num_jobs_name'] = county_jobs_obj.bra.name()
        
        return self.municipality_jobs 


    #-----
        
    def __municipality_with_more_wage_avg__(self):
        if not self.municipality_wage_avg:
            county_wage_avg_obj = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == self.cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.bra_id.like(self.bra_id+'%'),
                Ybi.year == self.ybi_max_year 
                ).order_by(desc(Ybi.wage_avg)).limit(1).one()

            self.municipality_wage_avg['municipality_with_more_wage_avg_value'] = county_wage_avg_obj.wage_avg
            self.municipality_wage_avg['municipality_with_more_wage_avg_name'] = county_wage_avg_obj.bra.name()   

        return self.municipality_wage_avg

