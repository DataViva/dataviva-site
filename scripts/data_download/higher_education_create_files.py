# -*- coding: utf-8 -*-
'''
 python scripts/data_download/higher_education_create_files.py
 The files will be saved in scripts/data/hedu
'''
from collections import namedtuple
from common import engine, get_colums
from dictionary import en
import pandas as pd
import os
import bz2


def select_table(conditions):
    s = 'y'
    # 0 year, 1 location, 3 major
    if conditions[1] != ' 1 = 1 ':
        s += 'b'

    if conditions[1] == ' 1 = 1 ' and conditions[2] == ' 1 = 1 ':
        s += 'b'

    if conditions[2] != ' 1 = 1 ':
        s += 'c'

    return 'hedu_' + s


def save(years, locations, majors):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1']  # 5 condicoes
    table_columns = {}
    output_path='scripts/data/hedu/'
    columns_deleted=['bra_id_len', 'course_hedu_id_len', 'enrolled_rca']

    for year in years:
        conditions[0] = year.condition
        for location in locations:
            conditions[1] = location.condition
            for major in majors:
                conditions[2] = major.condition
                table = select_table(conditions)
                name_file = 'hedu'+str(year.name)+str(location.name)+str(major.name)

                if table not in table_columns.keys():
                        table_columns[table] = [ i+" as '"+en[i]+"'" for i in get_colums(table, columns_deleted)]

                f = pd.read_sql_query('SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions), engine)

                new_file_path = os.path.abspath(os.path.join(output_path, name_file+".csv.bz2")) #pega desda da rais do pc
                # new_file_path='/home/ubuntu/files/hedu/'+name_file+'.csv.bz2';
                f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f")


Condition = namedtuple('Condition', ['condition', 'name'])


years = [
    Condition('year=2009', '-2009'),
    Condition('year=2010', '-2010'),
    Condition('year=2011', '-2011'),
    Condition('year=2012', '-2012'),
    Condition('year=2013', '-2013')]

locations = [
    Condition(' 1 = 1 ', ''),
    Condition('bra_id_len=1', '-regions'),
    Condition('bra_id_len=3', '-states'),
    Condition('bra_id_len=5', '-mesoregions'),
    Condition('bra_id_len=7', '-microregions'),
    Condition('bra_id_len=9', '-municipalities')]

majors = [
    Condition(' 1 = 1 ', ''),
    Condition('course_hedu_id_len=2', '-field'),
    Condition('course_hedu_id_len=6', '-majors')]


save(years=years, locations=locations, majors=majors)
