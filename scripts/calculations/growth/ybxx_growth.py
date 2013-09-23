# -*- coding: utf-8 -*-
"""
    Calculate growth for year-bra_id-x tables
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will go through each bra_id one at a time to calculate the
    growth of the requested variable, be it {wage, num_emp, num_est or val_usd}
"""

import MySQLdb, os, argparse, time
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys

from os import environ

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_all_years(table):
    '''Get all years in the database'''
    q = "select distinct year from {0}".format(table)
    cursor.execute(q)
    years = [row[0] for row in cursor.fetchall()]
    return years

def get_all_bras(table):
    '''Get all years in the database'''
    q = "select distinct bra_id from {0}".format(table)
    cursor.execute(q)
    bras = [row[0] for row in cursor.fetchall()]
    return bras

def check_columns(columns, val_var, table):
    print 'Checking if columns exist...'
    
    for col in columns:
        
        cursor.execute('''SELECT count(*) 
        FROM information_schema.COLUMNS 
        WHERE 
            TABLE_SCHEMA = %s 
        AND TABLE_NAME = %s 
        AND COLUMN_NAME = %s ''', \
        [environ["VISUAL_DB_NAME"], table, col])
        
        col_exist = cursor.fetchone()[0]
        
        if not col_exist:
            print 'Creating {0} column...'.format(col)
            
            q = "ALTER TABLE {0} ADD {1} FLOAT NULL DEFAULT NULL;"\
                .format(table, col)
            cursor.execute(q)

def get_growth(bra_id, years, table, val_var, columns, other_var, other_var_2):
    print "Current bra being updated:", bra_id
    s = time.time()

    q = "select year, {0}, {1}, {2} from {3} where bra_id='{4}'" \
            .format(other_var, other_var_2, val_var, table, bra_id)
    # print q
    # sys.exit()
    df = sql.read_frame(q, db)
    df = df.pivot_table(val_var, rows=["year"], cols=[other_var, other_var_2])
    
    growth_pct, growth_pct_5, growth_val, growth_val_5 = columns
    
    def clean_val(np_array):
        np_array = np_array.fillna(np.NaN)
        np_array[np_array == -1] = np.NaN
        return np_array
    
    vals_for_db = []
    for c in df.columns:
        # c = ("a0141", "6231")
        
        cleaned = df[c].fillna(0)
        if not len(cleaned):
            continue
        
        growth_data = pd.DataFrame(index=cleaned.index, columns=columns)
        
        for year in cleaned.index[1:]:
            five_yrs_ago = year - 5
            last_yr = year - 1

            if last_yr in cleaned.index:
                v_t0 = cleaned[last_yr]
                if v_t0:
                    v_tn = cleaned[year]
                    if v_tn:
                        exp = 1.0 / (year - last_yr)
                        growth_data[growth_pct][year] = \
                                                (v_tn/v_t0)**exp -1
                    # get value
                    growth_data[growth_val][year] = v_tn - v_t0

            if five_yrs_ago in cleaned.index:
                v_t0 = cleaned[five_yrs_ago]
                if v_t0:
                    v_tn = cleaned[year]
                    if v_tn:
                        exp = 1.0 / (year - five_yrs_ago)
                        growth_data[growth_pct_5][year] = \
                                                   (v_tn/v_t0) ** exp -1
                    # get value
                    growth_data[growth_val_5][year] = v_tn - v_t0
        
        growth_data = growth_data.apply(clean_val)
        # print growth_data
        
        for year, row in growth_data.iterrows():
            vals = [None if np.isnan(x) else x for x in row.values]
            # if len(set(vals)) > 1 and None not in set(vals):
            if set(vals) != set([None]):
                vals_for_db.append(vals + [year, bra_id, c[0], c[1]])
    
    return vals_for_db

def add_to_db(growth_vals, table ,columns, other_var, other_var_2):
    cols = [c+"=%s" for c in columns]
    cols = ", ".join(cols)

    q = 'UPDATE {0} SET {1} WHERE year=%s and bra_id=%s and {2}=%s and {3}=%s' \
                    .format(table, cols, other_var, other_var_2)
    cursor.executemany(q, growth_vals)

def calc_growth(table, val_var, dataset):
    
    '''check if columns exist, if not create them'''
    columns = ["growth_pct", "growth_pct_5", "growth_val", "growth_val_5"]
    columns = [val_var + "_" + col for col in columns]
    check_columns(columns, val_var, table)
    
    bras = get_all_bras(table)
    years = get_all_years(table)
    
    lookup = {"i":"isic_id", "o":"cbo_id", "p":"hs_id", "w":"wld_id"}    
    other_var = table.split("_")[1][2]
    other_var = lookup[other_var]
    
    other_var_2 = table.split("_")[1][3]
    other_var_2 = lookup[other_var_2]
    
    while(len(bras)):
        # set current geo and remove from list
        b = bras.pop(0)
        growth_vals = get_growth(b, years, table, val_var, columns, other_var, other_var_2)
        add_to_db(growth_vals, table, columns, other_var, other_var_2)

if __name__ == "__main__":
    start = time.time()
    from time import gmtime, strftime
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", help="the table to calculate growth for")
    parser.add_argument("-v", "--value", help="value variable to use",
                            choices=['wage', 'num_emp', 'num_est', 'val_usd'])
    args = parser.parse_args()
    
    table = args.table
    if not table:
        table = raw_input("Table to perform calculations on: ")
            
    val_var = args.value
    if "rais" in table:
        dataset = "rais"
        if not val_var:
            val_var = raw_input("Value variable {wage, num_emp, num_est}: ")
    elif "secex" in table:
        dataset = "secex"
        val_var = "val_usd"
    
    calc_growth(table, val_var, dataset)
    
    print
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print time.time() - start
    