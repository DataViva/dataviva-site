# -*- coding: utf-8 -*-
"""
    Calculate exclusivity for a given occupation in a given year
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import MySQLdb, os, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys, time

from os import environ

this_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.abspath(os.path.join(this_dir, '../../../'))

# growth_lib_dir = os.path.abspath(os.path.join(base_dir, 'scripts/growth_lib/'))
# sys.path.append(growth_lib_dir)
# import growth
# 
''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], 
                        db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_all_cbo(y):
    cursor.execute("select distinct(cbo_id) from rais_yo where "\
                        "length(cbo_id) = 4 and year = %s", [y])
    return [x[0] for x in cursor.fetchall()]

def add_to_db(y, cbo, importance):
    
    to_add = []
    for isic in importance.index:
        imp = importance[isic]
        to_add.append([imp, y, cbo, isic])
    
    cursor.executemany("update rais_yio set importance=%s where " \
                    "year=%s and cbo_id=%s and isic_id=%s", to_add)

def calculate_exclusivity(y):
    start = time.time()
    all_cbo = get_all_cbo(y)
    
    '''Get values from database'''
    q = "select isic_id, bra_id, rca " \
        "from rais_ybi " \
        "where year = {0} and length(isic_id) = 5 " \
        "and length(bra_id) = 8".format(y)
    rcas = sql.read_frame(q, db)
    rcas = rcas.pivot(index="bra_id", columns="isic_id", values="rca")
    rcas = rcas.fillna(0)
    
    '''convert nominal RCA values to 0s and 1s'''
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0
    
    denoms = rcas.sum()
    
    '''mcp'''
    q = """
          select 
            bra_id, isic_id, cbo_id, num_emp 
          from 
            rais_ybio
          where 
            year = {0} and 
            length(bra_id) = 8 and 
            length(isic_id) = 5 and 
            length(cbo_id) = 4
        """.format(y)
    # print q
    table = sql.read_frame(q, db)
    table = table.pivot_table(rows=["isic_id", "cbo_id"], cols="bra_id", values="num_emp")
    table = table.fillna(0)
  
    panel = table.to_panel()
    panel = panel.swapaxes("items", "minor")
    panel = panel.swapaxes("major", "minor")
  
    # z       = occupations
    # rows    = bras
    # colums  = isics
    
    print y, time.time() - start
    # sys.exit()
    
    for cbo in all_cbo:
        start = time.time()
        
        num_emp = panel[cbo].fillna(0)
        numerators = num_emp * rcas
        numerators = numerators.fillna(0)
        
        '''convert nominal num_emp values to 0s and 1s'''
        numerators[numerators >= 1] = 1
        numerators[numerators < 1] = 0
        
        numerators = numerators.sum()
        importance = numerators / denoms
        # print importance
        
        add_to_db(y, cbo, importance)
        
        print y, cbo, time.time() - start
    

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_yo")
    years = [row[0] for row in cursor.fetchall()]
    return years

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    args = parser.parse_args()
    
    year = args.year
    if not year:
        year = raw_input("Year for calculations (or all): ")
    if year == "all":
        year = get_all_years()
    else:
        year = [int(year)]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        calculate_exclusivity(y)