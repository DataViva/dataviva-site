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


def select_table(conditions):
    s = 'y'

    if conditions[1] != ' 1 = 1 ':
        s += 'b'

    if conditions[1] == ' 1 = 1 ' and conditions[2] == ' 1 = 1 ' and conditions[3] == ' 1 = 1 ':
        s += 'b'

    if conditions[2] != ' 1 = 1 ':
        s += 'i'

    if conditions[3] != ' 1 = 1 ':
        s += 'o'

    return 'rais_' + s


def save(years, locations, industrys, occupations, lang, output_path):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1']  # 4 condicoes
    table_columns = {}
    columns_deleted=['num_emp', 'hist', 'Gini', 'bra_id_len', 'cbo_id_len', 'cnae_id_len']

    if lang == 'en':
        dic_lang = en
    else:
        dic_lang = pt

    for year in years:
        conditions[0] = year.condition
        for location in locations:
            conditions[1] = location.condition
            for industry in industrys:
                conditions[2] = industry.condition
                for occupation in occupations:

                    if location.condition == ' 1 = 1 ' and industry.condition == ' 1 = 1 ' and occupation.condition == ' 1 = 1 ':
                            continue;

                    conditions[3] = occupation.condition
                    table = select_table(conditions)
                    name_file = 'rais'+str(year.name)+str(location.name)+str(industry.name)+str(occupation.name)
                    

                    if table not in table_columns.keys():
                        table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in get_colums(table, columns_deleted)]

                    query = 'SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions)

                    print "Gerando ... : "+name_file
                    
                    logging.info('Query for file ('+str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second)+'): \n '+name_file+'\n'+query)
                    f = pd.read_sql_query(query, engine)
                    
                    new_file_path = os.path.join(output_path, name_file+".csv.bz2") #pega desda da rais do pc
                    
                    f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f", encoding='utf-8')

                    logging.info("\nErro:\n"+str(sys.stderr)+"\n-----------------------------------------------\n")


Condition = namedtuple('Condition', ['condition', 'name'])


locations = [
    Condition(' 1 = 1 ', ''),
    Condition('bra_id_len=1', '-regions'),
    Condition('bra_id_len=3', '-states'),
    Condition('bra_id_len=5', '-mesoregions'),
    Condition('bra_id_len=7', '-microregions'),
    Condition('bra_id_len=9', '-municipalities')]

industrys = [
    Condition(' 1 = 1 ', ''),
    Condition('cnae_id_len=1', '-sections'),
    Condition('cnae_id_len=3', '-divisions'),
    Condition('cnae_id_len=6', '-classes')]

occupations = [
    Condition(' 1 = 1 ', ''),
    Condition('cbo_id_len=1', '-main_groups'),
    Condition('cbo_id_len=4', '-families')]


if len(sys.argv) != 4 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\npython scripts/data_download/rais_create_files.py en/pt output_path year"
    exit()

output_path = os.path.abspath(sys.argv[2])

logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],'rais-data-download.log' )),level=logging.DEBUG)

years = [ Condition('year='+str(sys.argv[3]), '-'+str(sys.argv[3])) ]

save(years=years, locations=locations, industrys=industrys, occupations=occupations, lang=sys.argv[1], output_path=output_path)


''' querys rais faltantes

# rais-2003-microregions-classes-families
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybio WHERE year=2013 and bra_id_len=7 and cnae_id_len=6 and cbo_id_len=4

#rais-2013-municipalities-classes
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',rca as 'Domestic RCA',distance as 'Distance',opp_gain as 'Opportunity Gain',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybi WHERE year=2013 and bra_id_len=9 and cnae_id_len=6 and  1 = 1

#rais-2013-municipalities-classes-main_groups
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybio WHERE year=2013 and bra_id_len=9 and cnae_id_len=6 and cbo_id_len=1

#rais-2013-municipalities-classes-families
SELECT year as 'Year',bra_id as 'BRA ID',cnae_id as 'CNAE ID',cbo_id as 'CBO ID',wage as 'Total Monthly Wages',num_jobs as 'Total Jobs',num_est as 'Total Establishments',wage_avg as 'Average Monthly Wage',age_avg as 'Average age',required as 'Estimated Employees',wage_growth as 'Nominal Wage Growth (1 year)',wage_growth_5 as 'Nominal Wage Growth (5 year)',num_emp_growth as 'Nominal Employee Growth (1 year)',num_emp_growth_5 as 'Nominal Employee Growth (5 year)' 
FROM rais_ybio WHERE year=2013 and bra_id_len=9 and cnae_id_len=6 and cbo_id_len=4

#

'''