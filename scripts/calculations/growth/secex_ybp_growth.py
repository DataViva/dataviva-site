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

        q = "select year, hs_id, val_usd from secex_ybp where bra_id='{0}'" \
                .format(b)
        df = sql.read_frame(q, db)
        df = df.pivot_table('val_usd', rows=["year"], cols=["hs_id"])

        to_add = []
        for hs in df.columns:
            
            cleaned = df[hs].fillna(0)
            if not len(cleaned):
                continue
            
            growth_data = pd.DataFrame(index=cleaned.index, \
                columns=["anualized_pct", "anualized_pct_5", \
                            "val", "val_5",])
            
            for year in cleaned.index[1:]:
                five_yrs_ago = year - 5
                last_yr = year - 1

                if last_yr in cleaned.index:
                    v_t0 = cleaned[last_yr]
                    if v_t0:
                        v_tn = cleaned[year]
                        if v_tn:
                            exp = 1.0 / (year - last_yr)
                            growth_data["anualized_pct"][year] = \
                                                    (v_tn/v_t0)**exp -1
                        # get value
                        growth_data["val"][year] = v_tn - v_t0

                if five_yrs_ago in cleaned.index:
                    v_t0 = cleaned[five_yrs_ago]
                    if v_t0:
                        v_tn = cleaned[year]
                        if v_tn:
                            exp = 1.0 / (year - five_yrs_ago)
                            growth_data["anualized_pct_5"][year] = \
                                                       (v_tn/v_t0) ** exp -1
                        # get value
                        growth_data["val_5"][year] = v_tn - v_t0
            
            growth_data = growth_data.apply(clean_val)
            
            # growth_data["orig_val"] = cleaned
            # print growth_data
            # raw_input('')
            # sys.exit()
            
            for year, row in growth_data.iterrows():
                # vals = [list(row.values)]
                vals = [None if np.isnan(x) else x for x in row.values]
                to_add.append(vals + [year, b, hs])
        
        cursor.executemany("update secex_ybp set val_usd_growth_pct=%s, val_usd_growth_pct_5=%s, val_usd_growth_val=%s, val_usd_growth_val_5=%s where year=%s and bra_id=%s and hs_id=%s", to_add)
  
        print 'Update complete! Query time:', (time.time()-s)/60

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from secex_ybp")
    years = [row[0] for row in cursor.fetchall()]
    return years

def get_all_bras():
    '''Get all years in the database'''
    cursor.execute("select distinct bra_id from secex_ybp")
    bras = [row[0] for row in cursor.fetchall()]
    return bras

if __name__ == "__main__":
    bras = get_all_bras()
    years = get_all_years()
    calculate_growth(bras, years)