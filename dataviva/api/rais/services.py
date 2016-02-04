from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi , Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc

class Industry :
    def __init__(self, cnae_id):
        self.cnae_id = cnae_id
        self.industry_headers = {}  
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
                self.industry_headers['total_jobs'] = num_jobs
                self.industry_headers['total_establishments'] = num_est

        return self.industry_headers

    def average_monthly_income(self): 
        return self.__rais_values__()['average_monthly_income']

    def salary_mass(self):
        return self.__rais_values__()['salary_mass']

    def num_jobs(self):
        return self.__rais_values__()['total_jobs']

    def num_establishments(self):
        return self.__rais_values__()['total_establishments'] 

    
    #-----
      
    def  get_occ_with_more_number_jobs(self) :
        occupation_jobs_generaitor = Yio.query.join(Cbo).filter(
            Yio.cbo_id == Cbo.id,
            Yio.cnae_id == self.cnae_id,
            Yio.cbo_id_len == 4,                
            Yio.year == self.yio_max_year_br 
            ).order_by(desc(Yio.num_jobs)).limit(1).values(Cbo.name_en, Cbo.name_pt, Yio.num_jobs)

        industry = {}
        for  name_en, name_pt, value in occupation_jobs_generaitor:        
            industry['occupation_max_number_jobs_name'] = name_pt
            industry['occupation_max_number_jobs_value'] = value  

        return industry   


    #-----

    def get_occ_with_more_wage_avg(self):
        occupation_wage_avg_generaitor = Yio.query.join(Cbo).filter(
            Yio.cbo_id == Cbo.id,
            Yio.cnae_id == self.cnae_id,
            Yio.cbo_id_len == 4,                 
            Yio.year == self.yio_max_year_br 
            ).order_by(desc(Yio.wage_avg)).limit(1).values(Cbo.name_en, Cbo.name_pt, Yio.wage_avg)

        industry = {}
        for  name_en, name_pt, value in occupation_wage_avg_generaitor:        
            industry['occupation_max_monthly_income_name'] = name_pt
            industry['occupation_max_monthly_income_value'] = value

        return industry     

    
    #-----

    def get_municipality_with_more_num_jobs(self):
        county_jobs_generaitor = Ybi.query.join(Bra).filter(
            Bra.id == Ybi.bra_id,
            Ybi.cnae_id == self.cnae_id,
            Ybi.bra_id_len == 9,
            Ybi.year == self.ybi_max_year_br,      
            ).order_by(desc(Ybi.num_jobs)).limit(1).values(Bra.name_en, Bra.name_pt, Ybi.num_jobs)
    
        industry = {}
        for name_en, name_pt, num_jobs in county_jobs_generaitor:        
            industry['county_max_number_jobs_name'] = name_pt
            industry['county_max_number_jobs_value'] = num_jobs

        return industry


    #-----
    
    def get_municipality_with_more_wage_avg(self):
        county_wage_avg_generaitor = Ybi.query.join(Bra).filter(
            Bra.id == Ybi.bra_id,
            Ybi.cnae_id == self.cnae_id,
            Ybi.bra_id_len == 9,
            Ybi.year == self.ybi_max_year_br,    
            ).order_by(desc(Ybi.wage_avg)).limit(1).values(Bra.name_en, Bra.name_pt, Ybi.wage_avg)   
        
        industry = {}
        for  name_en, name_pt, wage_avg in county_wage_avg_generaitor:        
            industry['county_max_monthly_income_name'] = name_pt
            industry['county_max_monthly_income_value'] =  wage_avg    
        return industry



#########################


class IndustryByLocation(Industry) :
    def __init__(self, bra_id, cnae_id):
        self.bra_id = bra_id
        self.cnae_id = cnae_id
        self.industry_headers = {} 
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
               self.industry_headers['total_jobs'] = num_jobs
               self.industry_headers['total_establishments'] =  num_est
               self.industry_headers['rca_domestic'] =  rca
               self.industry_headers['distance'] =  distance
               self.industry_headers['opportunity_gain'] =  opp_gain          

        return self.industry_headers     

    def rca(self):
        return self.__rais_values__()['rca_domestic']

    def distance(self):
        return self.__rais_values__()['distance']

    def opportunity_gain(self):
        return self.__rais_values__()['opportunity_gain'] 

    #-----

    def  get_occ_with_more_number_jobs(self) : 
        occ_jobs_generate = Ybio.query.join(Cbo).filter(
            Cbo.id == Ybio.cbo_id,
            Ybio.cnae_id == self.cnae_id,
            Ybio.cbo_id_len == 4,
            Ybio.bra_id == self.bra_id,
            Ybio.year == self.ybio_max_year
            ).order_by(desc(Ybio.num_jobs)).limit(1).values(Cbo.name_en, Cbo.name_pt, Ybio.num_jobs)  

        
        industry = {}
        for name_en, name_pt, num_jobs in occ_jobs_generate : 
            industry['occupation_max_number_jobs_value'] = num_jobs
            industry['occupation_max_number_jobs_name'] =  name_pt 

        return industry

    #-----

    def get_occ_with_more_wage_avg(self):
        
        occ_wage_avg_generate = Ybio.query.join(Cbo).filter(
            Cbo.id == Ybio.cbo_id,
            Ybio.cnae_id == self.cnae_id,
            Ybio.cbo_id_len == 4,
            Ybio.bra_id == self.bra_id,
            Ybio.year == self.ybio_max_year
            ).order_by(desc(Ybio.wage_avg)).limit(1).values(Cbo.name_en, Cbo.name_pt, Ybio.wage_avg)  

        industry = {}
        for name_en, name_pt, wage_avg in occ_wage_avg_generate : 
            industry['occupation_max_monthly_income_value'] = wage_avg
            industry['occupation_max_monthly_income_name'] = name_pt

        return industry

    #-----
        
    def get_municipality_with_more_num_jobs(self):

        county_jobs_generate = Ybi.query.join(Bra).filter(
            Bra.id == Ybi.bra_id,
            Ybi.cnae_id == self.cnae_id,
            Ybi.bra_id_len == 9,
            Ybi.bra_id.like(self.bra_id+'%'), 
            Ybi.year == self.ybi_max_year    
            ).order_by(desc(Ybi.num_jobs)).limit(1).values(Bra.name_en, Bra.name_pt, Ybi.num_jobs)
        
        industry = {}
        for name_en, name_pt, num_jobs in county_jobs_generate : 
            industry['county_max_number_jobs_value'] = num_jobs
            industry['county_max_number_jobs_name'] = name_pt
        return industry 


    #-----
        
    def get_municipality_with_more_wage_avg(self):

        county_wage_avg_generate = Ybi.query.join(Bra).filter(
            Bra.id == Ybi.bra_id,
            Ybi.cnae_id == self.cnae_id,
            Ybi.bra_id_len == 9,
            Ybi.bra_id.like(self.bra_id+'%'),
            Ybi.year == self.ybi_max_year 
            ).order_by(desc(Ybi.wage_avg)).limit(1).values(Bra.name_en, Bra.name_pt, Ybi.wage_avg)
        
        industry = {}
        for name_en, name_pt, wage_avg in county_wage_avg_generate : 
            industry['county_max_monthly_income_value'] = wage_avg
            industry['county_max_monthly_income_name'] = name_pt   

        return industry

