# -*- coding: utf-8 -*-
'''
 python data_download/school_census/sc_download_files.py
 The files will be saved in /data/files_sc
'''
from collections import namedtuple
from sqlalchemy import create_engine
import pandas as pd
import os, bz2


# sc_yb, sc_yc, sc_ybc


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


def get_colums(table, engine):
    column_rows = engine.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME='"+table+"' AND COLUMN_NAME NOT LIKE %s", "%_len")
    return [row[0] for row in column_rows]


def save(engine, years, locations, courses):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1']  # 5 condicoes
    table_columns = {}
    output_path='data/files_sc/'

    for year in years:
        conditions[0] = year.condition
        for location in locations:
            conditions[1] = location.condition
            for course in courses:
                conditions[2] = course.condition
                table = select_table(conditions)
                name_file = 'sc-'+str(year.name)+'-'+str(location.name)+'-'+str(course.name)

                if table not in table_columns.keys():
                        table_columns[table] = get_colums(table, engine)

                f = pd.read_sql_query('SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions), engine)

                new_file_path = os.path.abspath(os.path.join(output_path, name_file+".csv.bz2")) #pega desda da rais do pc
                f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f")


Condition = namedtuple('Condition', ['condition', 'name'])

years = [
    Condition('year=2007', '2007'),
    Condition('year=2008', '2008'),
    Condition('year=2009', '2009'),
    Condition('year=2010', '2010'),
    Condition('year=2011', '2011'),
    Condition('year=2012', '2012'),
    Condition('year=2013', '2013'),
    Condition('year=2014', '2014')]

locations = [
    Condition(' 1 = 1 ', 'all'),
    Condition('bra_id_len=1', 'regions'),
    Condition('bra_id_len=3', 'states'),
    Condition('bra_id_len=5', 'mesoregions'),
    Condition('bra_id_len=7', 'microregions'),
    Condition('bra_id_len=9', 'municipalities')]

courses = [
    Condition(' 1 = 1 ', 'all'),
    Condition('course_sc_id_len=2', 'field'),
    Condition('course_sc_id_len=5', 'course')]

engine = create_engine(
    'mysql://dataviva-dev:D4t4v1v4-d3v@dataviva-dev.cr7l9lbqkwhn.'
    'sa-east-1.rds.amazonaws.com:3306/dataviva', echo=False)


save(engine=engine, years=years, locations=locations, courses=courses)
