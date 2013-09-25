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

rca_dir = os.path.abspath(os.path.join(base_dir, 'scripts/calculations/rca/'))
sys.path.append(rca_dir)
import secex_ybp_rca_wld, secex_ybp_rca

# print secex_ybp_rca.get_rca(2011, 2).ix["mg"]

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], 
                        db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def calculate_complexity(year, geo_level):
    
    rcas = secex_ybp_rca.get_rca(year, geo_level)
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0

    # get locations above certain population threshold
    cursor.execute("select bra_id from attrs_yb where population " \
                    ">= %s and length(bra_id) = %s and year = %s", [50000, geo_level, year])
    bras = [r[0] for r in cursor.fetchall()]
    print len(bras)
    # sys.exit()
    
    # print rcas
    rcas = rcas.reindex(index=bras)
    # print rcas
    # sys.exit()
    
    # get pcis
    cursor.execute("select hs_id, pci from secex_yp " \
                    "where year = %s and length(hs_id) = 6 and pci is not null", [year])
    pcis = {r[0]:r[1] for r in cursor.fetchall()}
    pcis = pd.DataFrame([pcis.values()]*len(rcas.index), columns=pcis.keys(), index=rcas.index)
    # print pcis.ix["ac010105"]
    # sys.exit()

    # hs_all = set.intersection(set(rcas.columns), set(pcis.columns))

    # pcis = pcis.reindex(columns=hs_all)
    rcas = rcas.reindex(columns=pcis.columns)
    
    ecis = rcas * pcis
    ecis = ecis.sum(axis=1)
    ecis = ecis / rcas.sum(axis=1)
    
    # ecis.dropna().order().to_csv('ecis.csv')
    
    for bra in ecis.index:
        cursor.execute("update secex_yb set eci=%s where " \
                    "year=%s and bra_id=%s", [ecis[bra], year, bra])

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from secex_yb")
    years = [row[0] for row in cursor.fetchall()]
    return years

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    parser.add_argument("-g", "--geo_level", help="level of geo nesting",
                            choices=['2', '4', '7', '8', 'all'])
    args = parser.parse_args()
    
    year = args.year
    if not year:
        year = raw_input("Year for calculations (or all): ")
    if year == "all":
        year = get_all_years()
    else:
        year = [int(year)]
    
    geo_level = args.geo_level
    if not geo_level:
        geo_level = raw_input("Geo Level {2:state, 4:meso, 7:planning, 8:munic}: ")
    if geo_level == "all":
        geo_level = [2, 4, 7, 8]
    else:
        geo_level = [geo_level]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for g in geo_level:
            print
            print " --- Geo Level: {0} --- ".format(g);
            calculate_complexity(y, g)
            # add(y, g, complexity)
