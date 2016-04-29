# -*- coding: utf-8 -*-
'''
 python scripts/data_download/rais_create_files.py
 The files will be saved in scripts/data/rais

clear data files 
rm scripts/data/files_*/*
'''
from collections import namedtuple
from common import engine, get_colums
from dictionary import en, pt
from datetime import datetime
import pandas as pd
import os
import bz2
import sys
import logging

if len(sys.argv) != 5 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\npython scripts/data_download/rais_create_files.py en/pt output_path year num_select(1,2,3,4)"
    exit()

select_1 = ["SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)'  FROM rais_ybio WHERE year=" + str(sys.argv[3]) + " and bra_id_len=7 and cnae_id_len=6 and cbo_id_len=4 ", "rais-" + str(sys.argv[3]) + "-microregions-classes-families" ]

select_2 = ["SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',rca as 'Domestic RCA',distance as 'Distance',opp_gain as 'Opportunity Gain',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' FROM rais_ybi WHERE year=" + str(sys.argv[3]) + " and bra_id_len=9 and cnae_id_len=6 and  1 = 1", "rais-" + str(sys.argv[3]) + "-municipalities-classes" ]

select_3 = [ "SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' FROM rais_ybio WHERE year=" + str(sys.argv[3]) + " and bra_id_len=9 and cnae_id_len=6 and cbo_id_len=1", "rais-" + str(sys.argv[3]) + "-municipalities-classes-main_groups" ]

select_4 = [ "SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' FROM rais_ybio WHERE year=" + str(sys.argv[3]) + " and bra_id_len=9 and cnae_id_len=6 and cbo_id_len=4", "rais-" + str(sys.argv[3]) + "-municipalities-classes-families" ]

def save(years, lang, output_path, select):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1']  # 4 condicoes
    table_columns = {}
    columns_deleted=['num_emp', 'hist', 'Gini', 'bra_id_len', 'cbo_id_len', 'cnae_id_len']

    if lang == 'en':
        dic_lang = en
    else:
        dic_lang = pt

    if select != 2:
        table = 'rais_ybi'
    else:
        table = 'rais_ybio'
    

    if table not in table_columns.keys():
        table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in get_colums(table, columns_deleted)]

    query=[]    
    if select == str(1): 
        query = select_1

    if select == str(2): 
        query = select_2

    if select == str(3): 
        query = select_3

    if select == str(4):
        query = select_4

    name_file = query[1]
    print "Gerando ... : "+name_file
    
    logging.info('Query for file ('+str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second)+'): \n '+name_file+'\n'+query[0])
    f = pd.read_sql_query(query[0], engine)
    
    new_file_path = os.path.join(output_path, name_file+".csv.bz2") #pega desda da rais do pc
    
    f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f", encoding='utf-8')

    logging.info("\nErro:\n"+str(sys.stderr)+"\n-----------------------------------------------\n")
    


Condition = namedtuple('Condition', ['condition', 'name'])


output_path = os.path.abspath(sys.argv[2])

logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],'rais-data-download.log' )),level=logging.DEBUG)

years = [ Condition('year='+str(sys.argv[3]), '-'+str(sys.argv[3])) ]


save(years=years, lang=sys.argv[1], output_path=output_path, select=sys.argv[4])


''' querys rais faltantes

select_1 = "rais-2003-microregions-classes-families
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybio WHERE year=2013 and bra_id_len=7 and cnae_id_len=6 and cbo_id_len=4"

select_2 = "rais-2013-municipalities-classes
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',rca as 'Domestic RCA',distance as 'Distance',opp_gain as 'Opportunity Gain',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybi WHERE year=2013 and bra_id_len=9 and cnae_id_len=6 and  1 = 1"

select_3 = "rais-2013-municipalities-classes-main_groups
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybio WHERE year=2013 and bra_id_len=9 and cnae_id_len=6 and cbo_id_len=1"

select_4 = "rais-2013-municipalities-classes-families
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybio WHERE year=2013 and bra_id_len=9 and cnae_id_len=6 and cbo_id_len=4"

#

'''