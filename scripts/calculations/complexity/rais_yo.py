# -*- coding: utf-8 -*-
"""
    Calculate complexity values (for exports)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate industry/location RCA values
    based on the domestic brazilian market (YBI)
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

# print secex_ybp_rca.get_rca(2011, 2).ix["mg"]

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def delete_old_complexity_from_db(year, cbo_level):
    '''clear old opp_gain vals'''
    q = "update rais_yo set complexity=NULL " \
        "where year = {0} and length(cbo_id) = {1}".format(year, cbo_level)
    cursor.execute(q)

def get_rca(year, cbo_level):
    '''Get values from database'''
    q = "select isic_id, cbo_id, wage " \
        "from rais_yio " \
        "where year = {0} and length(cbo_id) = {1} and " \
        "length(isic_id) = 5".format(year, cbo_level)
    table = sql.read_frame(q, db)
    table = table.pivot(index="cbo_id", columns="isic_id", values="wage")
    table = table.fillna(0)
    
    '''Use growth library to run RCA calculation on data'''
    mcp = growth.rca(table)
    
    return mcp


def add_new_complexity_to_db(year, complexity):
    '''add new opp_gain vals'''
    to_add = []
    counter = 0
    total_inserts = 0
    for cbo in complexity.index:
        counter += 1
        total_inserts += 1
        to_add.append([complexity[cbo], year, cbo])
        if counter >= 2500:
            cursor.executemany("update rais_yo set complexity=%s where " \
                            "year=%s and cbo_id=%s", to_add)
            counter = 0
            to_add = []
            
        if total_inserts % 10000 == 0:
            sys.stdout.write('\r rows updated: ' + str(total_inserts) + ' ' * 20)
            sys.stdout.flush() # important
    
    print
    '''cant forget to add any stragglers to the DB'''
    cursor.executemany("update rais_yo set complexity=%s where " \
                    "year=%s and cbo_id=%s", to_add)

def calculate_complexity(year, cbo_level):
    
    # '''step 1 in calculating opportunity gain, get RCA'''
    # print "Calculating RCAs..."
    # rca = secex_ybp_rca_wld.get_rca(year, geo_level)

    
    '''calculate product complexity'''
    print "Calculating complexity..."
    rca = get_rca(year, cbo_level)
    rca = rca.fillna(0)
    '''conver nominal RCA values to 0s and 1s'''
    rca[rca >= 1] = 1
    rca[rca < 1] = 0
    
    pci = growth.complexity(rca)[1]
    eci = growth.complexity(rca)[0]
    '''reindex'''
    # pci = pci.reindex(index=rca.columns)
    pci = pci.dropna()
    
    # print pci
    # print eci.order()
    # sys.exit()
    
    return eci
    
def add(year, cbo_level, complexity):
    '''delete database'''
    print "Deleteing old opportunity gain values..."
    delete_old_complexity_from_db(year, cbo_level)
    
    '''add to database'''
    print "Adding new opportunity gain values..."
    add_new_complexity_to_db(year, complexity)

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_yo")
    years = [row[0] for row in cursor.fetchall()]
    return years

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    parser.add_argument("-c", "--cbo_level", help="level of geo nesting",
                            choices=['1', '4', 'all'])
    args = parser.parse_args()
    
    year = args.year
    if not year:
        year = raw_input("Year for calculations (or all): ")
    if year == "all":
        year = get_all_years()
    else:
        year = [int(year)]
    
    cbo_level = args.cbo_level
    if not cbo_level:
        cbo_level = raw_input("cbo level {1:category, 5:full}: ")
    if cbo_level == "all":
        cbo_level = [1, 4]
    else:
        cbo_level = [cbo_level]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for c in cbo_level:
            print
            print " --- Cbo Level: {0} --- ".format(c);
            complexity = calculate_complexity(y, c)
            add(y, c, complexity)
