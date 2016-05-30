# -*- coding: utf-8 -*-
'''
 python scripts/data_download/rais/create_files.py  en scripts/data/rais/en/ 2002

'''

from collections import namedtuple
from datetime import datetime
import pandas as pd
import os
import bz2
import sys
import logging
import imp


def local_imports():
    global common, dictionary
    f, filename, desc = imp.find_module('common', ['./scripts/data_download/'])
    common = imp.load_module('common', f, filename, desc)
    f, filename, desc = imp.find_module('dictionary', ['./scripts/data_download/'])
    dictionary = imp.load_module('common', f, filename, desc)
    

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


def save(year, locations, industrys, occupations, lang, output_path):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1']  # 4 condicoes
    table_columns = {}
    columns_deleted=['num_emp', 'hist', 'Gini', 'bra_id_len', 'cbo_id_len', 'cnae_id_len']

    if lang == 'en':
        dic_lang = dictionary.en
    else:
        dic_lang = dictionary.pt

    conditions[0] = year.condition
    for location in locations:
        conditions[1] = location.condition
        for industry in industrys:
            conditions[2] = industry.condition
            for occupation in occupations:
                conditions[3] = occupation.condition
                
                if location.condition == ' 1 = 1 ' and industry.condition == ' 1 = 1 ' and occupation.condition == ' 1 = 1 ':
                    continue;

                table = select_table(conditions)
                name_file = 'rais'+str(year.name)+str(location.name)+str(industry.name)+str(occupation.name)
                new_file_path = os.path.join(output_path, name_file+".csv.bz2") #pega desda da rais do pc
                
                if table not in table_columns.keys():
                    table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

                query = 'SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions) + ' LIMIT 5'
                logging.info('Query for file ('+str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second)+'): \n '+name_file+'\n'+query)

                print "Gerando ... " + new_file_path 
                f = pd.read_sql_query(query, common.engine)     
                f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f", encoding='utf-8')

                logging.info("\nError:\n"+str(sys.stderr)+"\n-----------------------------------------------\n")
                

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
year = Condition('year='+str(sys.argv[3]), '-'+str(sys.argv[3]))
local_imports()

save(year=year, locations=locations, industrys=industrys, occupations=occupations, lang=sys.argv[1], output_path=output_path)

