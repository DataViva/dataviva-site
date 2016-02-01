# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi , Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc


mod = Blueprint('industry', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/industry',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
 
    bra_id = '4mg' # localidade Minas Gerais 
    #bra_id = ""
    #cnae_id = 'g'   # comercio
    cnae_id = 'g47113' # supermercados
    industry = {}

    industry = { 
        'name': unicode('Supermercados', 'utf8'), 
        'location' : True , # diferente de Brasil
        'class' : True,
        'year' : 2010,
        'background_image':  unicode("'static/img/bg-profile-location.jpg'", 'utf8'),
        'portrait' : unicode('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110', 'utf8') ,
        
       'text_profile' : unicode('Texto de perfil para Supermercados.', 'utf8'),
        'text_salary_job' : unicode('Texto para Salários e empregos', 'utf8'),
        'text_economic_opportunity' : unicode('Texto para Oportunidades Econômicas', 'utf8'),
        'county' : True
    }

    # É ! Brasil, coloca alguns campos nos heads 
    industry['location'] = True

    #trata municipio
    if len(bra_id) == 4 : 
        industry['contry'] = False
    else :
        industry['contry'] = True    

    #Se for uma classe aparece oportunidades economicas no menu 
    if len(cnae_id) == 1 : 
        industry['class'] = True
    else : 
        industry['class'] = False

    ####EXTRACTY 


    #Pega o nome da atividade economica
    industry['name'] = Cnae.query.filter_by(id=cnae_id).one().name()
      
    # É Brasil
    if bra_id == "" :
        #subquery do ano máximo Cnae  com localidade igual a Brasil
        yi_max_year = db.session.query(func.max(Yi.year)).filter_by(cnae_id=cnae_id)
        industry['year'] = yi_max_year.scalar() 

        yio_max_year = db.session.query(func.max(Yio.year)).filter_by(cnae_id=cnae_id)

        ybi_max_year = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)

        #Pegar Headers
        headers_generator = Yi.query.filter(
            Yi.cnae_id == cnae_id,
            Yi.year == yi_max_year    
            ).values(Yi.wage, Yi.num_jobs, Yi.num_est, Yi.wage_avg )


        for  wage, num_jobs, num_est, wage_avg in headers_generator:        
            industry['average_monthly_income'] = wage_avg
            industry['salary_mass'] = wage
            industry['total_jobs'] = num_jobs
            industry['total_establishments'] = num_est

        
        #Pegar Dados das Estatisticas de Salario e Emprego
            
            # Ocupação 
        #--Ocupação com maior número de empregos (caso seja Brasil) : (nome e valor)
        occupation_jobs_generaitor = Yio.query.join(Cbo).filter(
            Yio.cbo_id == Cbo.id,
            Yio.cnae_id == cnae_id,
            Yio.cbo_id_len == 4,                #as atividades mais detallhadas  
            Yio.year == yio_max_year 
            ).order_by(desc(Yio.num_jobs)).limit(1).values(Cbo.name_pt, Yio.num_jobs)

        for  name, value in occupation_jobs_generaitor:        
            industry['occupation_max_number_jobs_name'] = name
            industry['occupation_max_number_jobs_value'] = value
          
        #--Ocupação com maior renda média mensal (caso seja Brasil) 
        occupation_wage_avg_generaitor = Yio.query.join(Cbo).filter(
            Yio.cbo_id == Cbo.id,
            Yio.cnae_id == cnae_id,
            Yio.cbo_id_len == 4,                #as atividades mais detallhadas  
            Yio.year == yio_max_year 
            ).order_by(desc(Yio.wage_avg)).limit(1).values(Cbo.name_pt, Yio.wage_avg)

        for  name, value in occupation_wage_avg_generaitor:        
            industry['occupation_max_monthly_income_name'] = name
            industry['occupation_max_monthly_income_value'] = value


        #TESTAR
            # Municípios (só e feito se não for município)
        #--Município com maior número de empregos (caso seja Brasil) :            
        if len(bra_id) != 9 : 

            county_jobs_generaitor = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == ybi_max_year,    # e o mesmo max_year    
                ).order_by(desc(Ybi.num_jobs)).limit(1).values(Bra.name_pt, Ybi.num_jobs)
        
            for  name, value in county_jobs_generaitor:        
                industry['county_max_number_jobs_name'] = name
                industry['county_max_number_jobs_value'] = value
            
                
            #--Município com maior renda média mensal (caso seja Brasil):
            #os nomes esati em outra tabel a Bra     
            county_wage_avg_generaitor = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == ybi_max_year,    # e o mesmo max_year    
                ).order_by(desc(Ybi.wage_avg)).limit(1).values(Bra.name_pt, Ybi.wage_avg)   
            
            for  name, value in county_wage_avg_generaitor:        
                industry['county_max_monthly_income_name'] = name
                industry['county_max_monthly_income_value'] = value    
    
    else : 
        ybi_max_year_bra_id=db.session.query(
            func.max(Ybi.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
        
        industry['year'] = ybi_max_year_bra_id.scalar()

        ybio_max_year_bra_id=db.session.query(
            func.max(Ybio.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
        
        
        #maximo ano com localidade de um regiao
        ybi_max_year_bra_id_region=db.session.query(
            func.max(Ybi.year)).filter(Ybi.bra_id.like(bra_id+'%'), cnae_id==cnae_id)

        ybio_max_year_bra_id_region=db.session.query(
            func.max(Ybio.year)).filter(Ybio.bra_id.like(bra_id+'%'), cnae_id==cnae_id)       


        ##Indicadores Headers 
        headers_generate = Ybi.query.filter(
            Ybi.cnae_id==cnae_id,
            Ybi.bra_id == bra_id,
            Ybi.year==ybi_max_year_bra_id).values(
                Ybi.wage, Ybi.num_jobs, 
                Ybi.num_est, Ybi.wage_avg, 
                Ybi.rca, Ybi.distance, 
                Ybi.opp_gain) 

        lista = []
        for wage, num_jobs, num_est, wage_avg, rca, distance, opp_gain in headers_generate:
           industry['average_monthly_income'] = wage
           industry['salary_mass'] =  num_jobs
           industry['total_jobs'] =  num_est
           industry['total_establishments'] =  wage_avg
           industry['rca_domestic'] =  rca
           industry['distance'] =  distance
           industry['opportunity_gain'] =  opp_gain 


        ######colocar Cbo +-6000 e Bra +- 3000 em um lista e para simplificar o select
        ''' 
            select id, name_en, name_pt from attrs_cbo;  
            select id, name_en, name_pt from attrs_bra;
        '''
        dic_names_cbo = {}
        dic_names_bra = {}

        cbo_generate = Cbo.query.values(Cbo.id, Cbo.name_en, Cbo.name_pt)
        bra_generate = Bra.query.values(Bra.id, Bra.name_en, Bra.name_pt)

        for id, name_en, name_pt in cbo_generate:
            dic_names_cbo[id] = [name_en, name_pt]

        for id, name_en, name_pt in bra_generate:
            dic_names_bra[id] = [name_en, name_pt]

        print dic_names_cbo       

    return render_template('industry/index.html', body_class='perfil-estado', industry=industry)





