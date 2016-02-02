from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi , Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc

class Industry :
    def __init__(self, bra_id, cnae_id):
        self.bra_id = bra_id
        self.cnae_id = cnae_id
        self.yi_max_year_brazil = db.session.query(func.max(Yi.year)).filter_by(cnae_id=cnae_id)
        self.yio_max_year_brazil = db.session.query(func.max(Yio.year)).filter_by(cnae_id=cnae_id)
        self.ybi_max_year_brazil = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)
        
        # Max year, location diferent Brazil
        self.ybi_max_year=db.session.query(
            func.max(Ybi.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
        
        self.ybio_max_year=db.session.query(
            func.max(Ybio.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)

    def get_year(self):
        return self.ybi_max_year.scalar()

    def get_name(self): 
        return Cnae.query.filter_by(id=self.cnae_id).one().name()   

    def get_headers_indicators(self):
        headers_generate = Ybi.query.filter(
            Ybi.cnae_id==self.cnae_id,
            Ybi.bra_id == self.bra_id,
            Ybi.year==self.ybi_max_year
            ).values(
                Ybi.wage, Ybi.num_jobs, 
                Ybi.num_est, Ybi.wage_avg, 
                Ybi.rca, Ybi.distance, 
                Ybi.opp_gain) 

        industry = {}
        for wage, num_jobs, num_est, wage_avg, rca, distance, opp_gain in headers_generate:
           industry['average_monthly_income'] = wage
           industry['salary_mass'] =  num_jobs
           industry['total_jobs'] =  num_est
           industry['total_establishments'] =  wage_avg
           industry['rca_domestic'] =  rca
           industry['distance'] =  distance
           industry['opportunity_gain'] =  opp_gain          

        return industry     

    def  get_acc_max_number_jobs(self) : 
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


    def get_occ_max_wage_avg(self):
        
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

    def get_county_max_num_jobs(self):

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

    def get_county_max_wage_avg(self):

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
