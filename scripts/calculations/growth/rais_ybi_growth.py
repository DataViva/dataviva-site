# -*- coding: utf-8 -*-
"""
    Calculate growth of occupations 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import MySQLdb, os, argparse, time
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys

from os import environ

pd.core.config.option_context("mode.use_inf_as_null", True)

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def clean_val(np_array):
    np_array = np_array.fillna(np.NaN)
    np_array[np_array == -1] = np.NaN
    return np_array

def calculate_growth(bras, years):
    
    while(len(bras)):
  
        # set current geo and remove from list
        b = bras.pop(0)

        print "Current bra being updated:", b
        s = time.time()

        q = "select year, isic_id, wage from rais_ybi where bra_id='{0}'" \
                .format(b)
        df = sql.read_frame(q, db)
        df = df.pivot_table('wage', rows=["year"], cols=["isic_id"])

        to_add = []
        for isic in df.columns:
            
            cleaned = df[isic].fillna(0)
            if not len(cleaned):
                continue
            
            growth_data = pd.DataFrame(index=cleaned.index, \
                columns=["wage_growth_pct", "wage_growth_pct_5", \
                        "wage_growth_val", "wage_growth_val_5"])
            
            for year in cleaned.index[1:]:
                five_yrs_ago = year - 5
                last_yr = year - 1

                if last_yr in cleaned.index:
                    v_t0 = cleaned[last_yr]
                    if v_t0:
                        v_tn = cleaned[year]
                        if v_tn:
                            exp = 1.0 / (year - last_yr)
                            growth_data["wage_growth_pct"][year] = \
                                                    (v_tn/v_t0)**exp -1
                        # get value
                        growth_data["wage_growth_val"][year] = v_tn - v_t0

                if five_yrs_ago in cleaned.index:
                    v_t0 = cleaned[five_yrs_ago]
                    if v_t0:
                        v_tn = cleaned[year]
                        if v_tn:
                            exp = 1.0 / (year - five_yrs_ago)
                            growth_data["wage_growth_pct_5"][year] = \
                                                       (v_tn/v_t0) ** exp -1
                        # get value
                        growth_data["wage_growth_val_5"][year] = v_tn - v_t0
                        
            growth_data = growth_data.apply(clean_val)

            for year, row in growth_data.iterrows():
                vals = [None if np.isnan(x) else x for x in row.values]
                to_add.append(vals + [year, b, isic])
        
        cursor.executemany("update rais_ybi set wage_growth_pct=%s, growth_pct_total=%s, growth_val=%s, growth_val_total=%s where year=%s and bra_id=%s and isic_id=%s", to_add)
  
        # print 'Update complete! Query time:', (time.time()-s)/60

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_ybi")
    years = [row[0] for row in cursor.fetchall()]
    return years

def get_all_bras():
    '''Get all years in the database'''
    cursor.execute("select distinct bra_id from rais_ybi")
    bras = [row[0] for row in cursor.fetchall()]
    return bras

if __name__ == "__main__":
    bras = get_all_bras()
    years = get_all_years()
    calculate_growth(bras, years)