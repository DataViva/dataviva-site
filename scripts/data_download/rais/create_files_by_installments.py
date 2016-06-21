# -*- coding: utf-8 -*-
'''
 python scripts/data_download/rais/create_files_by_installments.py  en scripts/data/rais/en/ 2014 files <type_files when lio file>

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


def save_all(year, locations, industrys, occupations, lang, output_path):
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
                new_file_path = os.path.join(output_path, name_file+".csv.bz2")
                
                print name_file
                if table not in table_columns.keys():
                    table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

                common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)


def save_industry(year, locations, industrys, occupations, lang, output_path):
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

                
            if location.condition == ' 1 = 1 ' and industry.condition == ' 1 = 1 ' :
                continue;

            if industry.condition == ' 1 = 1 ' :
                continue;

            table = select_table(conditions)
            name_file = 'rais'+str(year.name)+str(location.name)+str(industry.name)
            new_file_path = os.path.join(output_path, name_file+".csv.bz2")
            
            print name_file
            if table not in table_columns.keys():
                table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

            common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)


def save_location_occupation(year, locations, industrys, occupations, lang, output_path):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1']  # 4 condicoes
    table_columns = {}
    columns_deleted=['num_emp', 'hist', 'Gini', 'bra_id_len', 'cbo_id_len', 'cnae_id_len']

    if lang == 'en':
        dic_lang = dictionary.en
    else:
        dic_lang = dictionary.pt

    conditions[0] = year.condition
    for location in locations:
        for occupation in occupations:
            conditions[3] = occupation.condition

            if location.condition == ' 1 = 1 ' and occupation.condition == ' 1 = 1 ':
                continue;

            table = select_table(conditions)
            name_file = 'rais'+str(year.name)+str(location.name)+str(occupation.name)
            new_file_path = os.path.join(output_path, name_file+".csv.bz2")
            
            print name_file
            if table not in table_columns.keys():
                table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

            common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)


def save_location_industry_occupation(year, locations, industrys, occupations, lang, output_path, type_files):
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
                table = select_table(conditions)
                name_file = 'rais'+str(year.name)+str(location.name)+str(industry.name)+str(occupation.name)
                new_file_path = os.path.join(output_path, name_file+".csv.bz2")
                if type_files == 'all':
                    if (not(location.condition == ' 1 = 1 ' or industry.condition == ' 1 = 1 ' or occupation.condition == ' 1 = 1 ')) or (location.condition == ' 1 = 1 ' and (industry.condition != ' 1 = 1 ' and occupation.condition != ' 1 = 1 ')):
                        print name_file
                        if table not in table_columns.keys():
                            table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

                        common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)
                else:    
                    if (not(location.condition == ' 1 = 1 ' or industry.condition == ' 1 = 1 ' or occupation.condition == ' 1 = 1 ')) or (location.condition == ' 1 = 1 ' and (industry.condition != ' 1 = 1 ' and occupation.condition != ' 1 = 1 ')):
                        if location.name == "-" + type_files or (location.condition == ' 1 = 1 ' and type_files == 'no_location'):
                                    
                            print name_file
                            if table not in table_columns.keys():
                                table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

                            common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)




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


local_imports()

flag="all";
if len(sys.argv) < 5 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\npython scripts/data_download/school_census/create_files_by_installments.py en/pt output_path year files\n"
    print "i = industry files (18 files)"
    print "lo = location, occupation files (17 files)"
    print "lio = location and industry and occupation(36 files)\n\tindicate all or (regions ,states ,mesoregions, microregions, municipalities, no_location)(6 files each)."
    print "a = all"
    exit()
inputs = {}

inputs['output_path'] = os.path.abspath(sys.argv[2])
logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],str(sys.argv[2].split('/')[2]) + '-data-download.log' )),level=logging.DEBUG)
inputs['year'] = Condition('year='+str(sys.argv[3]), '-'+str(sys.argv[3]))
inputs['lang'] = sys.argv[1]
files = sys.argv[4]

f = 1
if files == 'a' : 
    save_all(year=inputs['year'], locations=locations, industrys=industrys, occupations=occupations, lang=inputs['lang'], output_path=inputs['output_path'])
    f = 0

if files == 'i':
    save_industry(year=inputs['year'], locations=locations, industrys=industrys, occupations=occupations, lang=inputs['lang'], output_path=inputs['output_path'])
    f = 0

if files == 'lo':
    save_location_occupation(year=inputs['year'], locations=locations, industrys=industrys, occupations=occupations, lang=inputs['lang'], output_path=inputs['output_path'])
    f = 0

if files == 'lio':
    loc = ["regions", "states", "mesoregions", "microregions", "municipalities", "no_location", "all"]
    
    if len(sys.argv) != 6 or sys.argv[5] not in loc:
        print "lio = location and industry and occupation(36 files)\n\tindicate (regions, states, mesoregions, microregions, municipalities, no_location)(6 files each)."
        exit()
    type_files = str(sys.argv[5]);
    save_location_industry_occupation(year=inputs['year'], locations=locations, industrys=industrys, occupations=occupations, lang=inputs['lang'], output_path=inputs['output_path'], type_files=type_files)
    f = 0


if f == 1 : 
    print "ERROR! use :\npython scripts/data_download/school_census/create_files_by_installments.py en/pt output_path year files\n"
    print "i = industry files (18 files)"
    print "lo = location, occupation files (17 files)"
    print "lio = location and industry and occupation(36 files)\n\tindicate all or (regions ,states ,mesoregions, microregions, municipalities, no_location)(6 files each)."
    print "a = all"
    exit()