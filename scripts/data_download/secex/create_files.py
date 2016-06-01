# -*- coding: utf-8 -*-
'''
 python scripts/data_download/secex/create_files.py  en scripts/data/secex/en/ 2002

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
    s = 'ym'
    # 0 year, 1 mes, 2 location, 3 product, 4 trade-partner
    if conditions[2] != ' 1 = 1 ':
        s += 'b'

    if conditions[2] == ' 1 = 1 ' and conditions[3] == ' 1 = 1 ' and conditions[4] == ' 1 = 1 ':
        s += 'b'

    if conditions[3] != ' 1 = 1 ':
        s += 'p'

    if conditions[4] != ' 1 = 1 ':
        s += 'w'

    return 'secex_' + s


def save(year, months, locations, products, trade_partners, lang, output_path):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1']  # 5 condicoes
    table_columns = {}
    columns_deleted=['bra_id_len', 'eci_old', 'eci_wld', 'hs_id_len', 'wld_id_len', 'rcd'] # tira  month para ano, tira bra_id para agregado mensal

    if lang == 'en':
        dic_lang = dictionary.en
    else:
        dic_lang = dictionary.pt

    conditions[0] = year.condition
    for month in months:
        conditions[1] = month.condition
        for location in locations:
            conditions[2] = location.condition
            for product in products:
                conditions[3] = product.condition
                for trade_partner in trade_partners:
                    conditions[4] = trade_partner.condition
                    
                    if location.condition == ' 1 = 1 ' and product.condition == ' 1 = 1 ' and trade_partner.condition == ' 1 = 1 ':
                        continue;

                    table = select_table(conditions)
                    name_file = 'secex'+str(year.name)+str(month.name)+str(location.name)+str(product.name)+str(trade_partner.name)
                    new_file_path = os.path.join(output_path, name_file+".csv.bz2")

                    if table not in table_columns.keys():
                        table_columns[table] = [i+" as '"+dic_lang[i]+"'" for i in common.get_colums(table, columns_deleted)]

                    common.download(table_columns=table_columns, table=table, conditions=conditions, name_file=name_file, new_file_path=new_file_path, logging=logging, sys=sys)



Condition = namedtuple('Condition', ['condition', 'name'])


months = [
    Condition('month=0', ''),
    Condition('month!=0', '-monthly')]

locations = [
    Condition(' 1 = 1 ', ''),
    Condition('bra_id_len=1', '-regions'),
    Condition('bra_id_len=3', '-states'),
    Condition('bra_id_len=5', '-mesoregions'),
    Condition('bra_id_len=7', '-microregions'),
    Condition('bra_id_len=9', '-municipalities')]

products = [
    Condition(' 1 = 1 ', ''),
    Condition('hs_id_len=2', '-sections'),
    Condition('hs_id_len=6', '-position')]

trade_partners = [
    Condition(' 1 = 1 ', ''),
    Condition('wld_id_len=2', '-continents'),
    Condition('wld_id_len=5', '-countries')]


if len(sys.argv) != 4 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\npython scripts/data_download/secex/create_files.py en/pt output_path year"
    exit()

local_imports()
inputs = common.test_imput(sys=sys, logging=logging, Condition=Condition)
save(year=inputs['year'], months=months, locations=locations, products=products, trade_partners=trade_partners, lang=inputs['lang'], output_path=inputs['output_path'])
