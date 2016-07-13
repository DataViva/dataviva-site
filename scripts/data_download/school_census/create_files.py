# -*- coding: utf-8 -*-
'''
 python scripts/data_download/school_census/create_files.py  en scripts/data/school_census/en/ 2007

'''

from collections import namedtuple
import os
import sys
import logging
import imp


def local_imports():
    global common, dictionary
    f, filename, desc = imp.find_module('common', ['./scripts/data_download/'])
    common = imp.load_module('common', f, filename, desc)
    f, filename, desc = imp.find_module('dictionary', ['./scripts/data_download/'])
    dictionary = imp.load_module('common', f, filename, desc)


def select_table(conditions, name):
    s = 'y'
    # 0 year, 1 location, 3 course
    if conditions[1] != ' 1 = 1 ':
        s += 'b'

    if conditions[1] == ' 1 = 1 ' and conditions[2] == ' 1 = 1 ':
        s += 'b'

    if name == '-school':
        s+='s'

    if conditions[3] != ' 1 = 1 ':
        s += 'c'

    return 'sc_' + s


def save(year, locations, schools, courses, lang, output_path):
    conditions = [' 1 = 1 ', ' 1 = 1 ', ' 1 = 1 ', ' 1 = 1 ']
    table_columns = {}
    columns_deleted=['bra_id_len', 'distortion_rate', 'course_sc_id_len']

    if lang == 'en':
        dic_lang = dictionary.en
    else:
        dic_lang = dictionary.pt

    conditions[0] = year.condition
    for location in locations:
        conditions[1] = location.condition
        for school in schools:
            conditions[2] = school.condition
            for course in courses:
                conditions[3] = course.condition
                if location.condition == ' 1 = 1 ' and course.condition == ' 1 = 1 ':
                            continue;

                table = select_table(conditions, school.name)
                name_file = 'sc' + str(year.name)+str(location.name)+str(school.name)+str(course.name)
                
                new_file_path = os.path.join(output_path, name_file+".csv.bz2")

                if table not in table_columns.keys():
                    table_columns[table] = [ i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table,columns_deleted)]

                common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)


Condition = namedtuple('Condition', ['condition', 'name'])


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

schools = [
    Condition(' 1 = 1 ', ''),
    Condition(' 1 = 1 ', '-school')]


local_imports()
inputs = common.test_imput(sys=sys, logging=logging, Condition=Condition)
save(year=inputs['year'], locations=locations, schools=schools, courses=courses, lang=inputs['lang'], output_path=inputs['output_path'])

