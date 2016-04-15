# -*- coding: utf-8 -*-
'''
 python scripts/data_download/school_census__create_file.py
 The files will be saved in scripts/data/sc
'''
from collections import namedtuple
from common import engine, get_colums
from dictionary import en, pt
import pandas as pd
import os
import bz2
import sys


def select_table(conditions):
    s = 'y'
    # 0 year, 1 location, 3 course
    if conditions[1] != ' 1 = 1 ':
        s += 'b'

    if conditions[1] == ' 1 = 1 ' and conditions[2] == ' 1 = 1 ':
        s += 'b'

    if conditions[2] != ' 1 = 1 ':
        s += 'c'

    return 'sc_' + s


def save(years, locations, courses, lang):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1']  # 5 condicoes
    table_columns = {}
    output_path = 'scripts/data/sc/'+lang
    columns_deleted=['bra_id_len', 'distortion_rate', 'course_sc_id_len']

    if lang == 'en':
        dic_lang = en
    else:
        dic_lang = pt

    for year in years:
        conditions[0] = year.condition
        for location in locations:
            conditions[1] = location.condition
            for course in courses:

                if location.condition == ' 1 = 1 ' and course.condition == ' 1 = 1 ':
                            continue;

                conditions[2] = course.condition
                table = select_table(conditions)
                name_file = 'sc' + \
                    str(year.name)+str(location.name)+str(course.name)

                if table not in table_columns.keys():
                    table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in get_colums(table,columns_deleted)]

                f = pd.read_sql_query('SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions), engine)

                # new_file_path = os.path.abspath(os.path.join(output_path, name_file+".csv.bz2"))  # pega desda da rais do pc
                new_file_path='/home/ubuntu/files/sc/'+lang+'/'+name_file+'.csv.bz2';
                
                f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f", encoding='utf-8')
                  

Condition = namedtuple('Condition', ['condition', 'name'])

years = [
    Condition('year=2007', '-2007'),
    Condition('year=2008', '-2008'),
    Condition('year=2009', '-2009'),
    Condition('year=2010', '-2010'),
    Condition('year=2011', '-2011'),
    Condition('year=2012', '-2012'),
    Condition('year=2013', '-2013'),
    Condition('year=2014', '-2014')]

locations = [
    Condition(' 1 = 1 ', ''),
    Condition('bra_id_len=1', '-regions'),
    Condition('bra_id_len=3', '-states'),
    Condition('bra_id_len=5', '-mesoregions'),
    Condition('bra_id_len=7', '-microregions'),
    Condition('bra_id_len=9', '-municipalities')]

courses = [
    Condition(' 1 = 1 ', ''),
    Condition('course_sc_id_len=2', '-field'),
    Condition('course_sc_id_len=5', '-course')]



if len(sys.argv) != 2 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\npython scripts/data_download/secex_create_files.py en/pt"
    exit()

save(years=years, locations=locations, courses=courses, lang=sys.argv[1:][0])
