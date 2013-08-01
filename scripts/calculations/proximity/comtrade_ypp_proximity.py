# -*- coding: utf-8 -*-
"""
    Calculate proximities (using domestic RCA)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script utilizes the growth library to calculate proximity
    according to the atlas method. The script takes the following steps:
     - calculates RCA for given year and geo level (state, meso, micro, munic)
     - calculates proximity based on RCA matrix
     - adds proximity values to DB
"""

import MySQLdb, os, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys

from os import environ

this_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.abspath(os.path.join(this_dir, '../../../'))

growth_lib_dir = os.path.abspath(os.path.join(base_dir, 'scripts/growth_lib/'))
sys.path.append(growth_lib_dir)
import growth

rca_dir = os.path.abspath(os.path.join(base_dir, 'scripts/calculations/rca/'))
sys.path.append(rca_dir)
import secex_ybp_rca_wld

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def delete_old_proximity_from_db(year):
    '''clear old proximity vals'''
    cursor.execute("delete from comtrade_ypp where year=%s ", (year))

def add_new_proximity_to_db(year, prox):
    '''add new opp_gain vals'''
    to_add = []
    counter = 0
    total_inserts = 0
    for hs in prox.columns:
        for hs_2 in prox.index:
            counter += 1
            total_inserts += 1
            to_add.append([year, hs, hs_2, prox[hs][hs_2]])
            if counter >= 2500:
                cursor.executemany("insert into comtrade_ypp values " \
                                "(%s, %s, %s, %s)", to_add)
                counter = 0
                to_add = []
            
            if total_inserts % 10000 == 0:
                sys.stdout.write('\r rows updated: ' + str(total_inserts) + ' ' * 20)
                sys.stdout.flush() # important
    
    print
    '''cant forget to add any stragglers to the DB'''
    cursor.executemany("insert into comtrade_ypp values (%s, %s, %s, %s)", to_add)

def get_comtrade_rca(year):
    '''Get values from database'''
    q = "select wld_id, hs_id, val_usd " \
        "from comtrade_ypw " \
        "where year = {0} and length(hs_id) = 6".format(year)
    table = sql.read_frame(q, db)
    table = table.pivot(index="wld_id", columns="hs_id", values="val_usd")
    table = table.fillna(0)
    
    '''Use growth library to run RCA calculation on data'''
    mcp = growth.rca(table)
    
    return mcp

def calculate_proximity(year):
    
    '''step 1 in calculating opportunity gain, get RCA'''
    print "Calculating RCAs..."
    geo_level = 8
    rca = get_comtrade_rca(year)
    '''conver nominal RCA values to 0s and 1s'''
    rca[rca >= 1] = 1
    rca[rca < 1] = 0
    
    '''calculate proximity for opportunity gain calculation'''
    print "Calculating proximities..."
    prox = growth.proximity(rca)
    
    return prox

def add(year, prox):
    '''delete old proximity values'''
    print "Deleteing old proximity values..."
    delete_old_proximity_from_db(year)
    
    '''insert new proximity values to database'''
    print "Adding new proximity values..."
    add_new_proximity_to_db(year, prox)

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from comtrade_ypw")
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
        prox = calculate_proximity(y)
        add(y, prox)