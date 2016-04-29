# -*- coding: utf-8 -*-
'''
python scripts/data_download/secex_create_files.py en or pt
 The files will be saved in scripts/data/secex
'''
from collections import namedtuple
from common import engine, get_colums
from dictionary import en, pt
import pandas as pd
import os
import bz2
import sys



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


def save(years, months, locations, products, trade_partners, lang):
    conditions = [' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1', ' 1 = 1']  # 5 condicoes
    table_columns = {}
    output_path='scripts/data/secex/'+lang
    columns_deleted=['bra_id_len', 'eci_old', 'eci_wld', 'hs_id_len', 'wld_id_len', 'rcd'] # tira  month para ano, tira bra_id para agregado mensal

    if lang == 'en':
        dic_lang = en
    else:
        dic_lang = pt

    for year in years:
        conditions[0] = year.condition
        for month in months:
            conditions[1] = month.condition
            for location in locations:
                conditions[2] = location.condition
                for product in products:
                    conditions[3] = product.condition
                    for trade_partner in trade_partners:

                        if location.condition == ' 1 = 1 ' and product.condition == ' 1 = 1 ' and trade_partner.condition == ' 1 = 1 ':
                            continue;

                        conditions[4] = trade_partner.condition
                        table = select_table(conditions)
                        name_file = 'secex'+str(year.name)+str(month.name)+str(location.name)+str(product.name)+str(trade_partner.name)

                        if table not in table_columns.keys():
                            table_columns[table] = [i+" as '"+dic_lang[i]+"'" for i in get_colums(table, columns_deleted)]

                        f = pd.read_sql_query('SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions), engine)

                        # new_file_path = os.path.abspath(os.path.join(output_path, name_file+".csv.bz2")) #pega desda da rais do pc
                        new_file_path='/home/ubuntu/files/secex/'+lang+'/'+name_file+'.csv.bz2';

                        f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f", encoding='utf-8')


Condition = namedtuple('Condition', ['condition', 'name'])


years = [
    Condition('year=2002', '-2002'),
    Condition('year=2003', '-2003'),
    Condition('year=2004', '-2004'),
    Condition('year=2005', '-2005'),
    Condition('year=2006', '-2006'),
    Condition('year=2007', '-2007'),
    Condition('year=2008', '-2008'),
    Condition('year=2009', '-2009'),
    Condition('year=2010', '-2010'),
    Condition('year=2011', '-2011'),
    Condition('year=2012', '-2012'),
    Condition('year=2013', '-2013'),
    Condition('year=2014', '-2014')]

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


if len(sys.argv) != 2 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\npython scripts/data_download/secex_create_files.py en/pt"
    exit()


save(years=years, months=months, locations=locations, products=products, trade_partners=trade_partners, lang=sys.argv[1:][0])
