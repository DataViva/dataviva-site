# -*- coding: utf-8 -*-
"""
    Calculate distance
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
import secex_ybp_rca

proximity_dir= os.path.abspath(os.path.join(base_dir, 'scripts/calculations/proximity/'))
sys.path.append(proximity_dir)
import comtrade_ypp_proximity

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def delete_old_distance_from_db(year, geo_level, wld_or_domestic):
    '''clear old proximity vals'''
    if wld_or_domestic == "domestic":
        cursor.execute("update secex_ybp set distance=NULL where year=%s " \
                        "and length(bra_id) = %s", (year, geo_level))
    else:
        cursor.execute("update secex_ybp set distance_wld=NULL where year=%s " \
                        "and length(bra_id) = %s", (year, geo_level))

def add_new_distance_to_db(year, dist, wld_or_domestic):
    '''add new opp_gain vals'''
    to_add = []
    counter = 0
    total_inserts = 0
    if wld_or_domestic == "domestic":
        dist_col = "distance"
    else:
        dist_col = "distance_wld"
    for hs in dist.columns:
        for bra in dist.index:
            counter += 1
            total_inserts += 1
            to_add.append([dist[hs][bra], year, hs, bra])
            if counter >= 2500:
                q = "update secex_ybp set {0}=%s where year=%s and hs_id=%s and bra_id=%s".format(dist_col)
                cursor.executemany(q, to_add)
                counter = 0
                to_add = []
            
            if total_inserts % 10000 == 0:
                sys.stdout.write('\r rows updated: ' + str(total_inserts) + ' ' * 20)
                sys.stdout.flush() # important
    
    print
    '''cant forget to add any stragglers to the DB'''
    q = "update secex_ybp set {0}=%s where year=%s and hs_id=%s and bra_id=%s".format(dist_col)
    cursor.executemany(q, to_add)



def calculate_distance(year, geo_level, wld_or_domestic):
    
    '''calculate proximity for opportunity gain calculation'''
    print "Calculating proximities..."
    prox = comtrade_ypp_proximity.calculate_proximity(year)
    
    if wld_or_domestic == "world":
        rcas = secex_ybp_rca_wld.get_rca(year, geo_level)
    else:
        rcas = secex_ybp_rca.get_rca(year, geo_level)
    rcas = rcas.fillna(0)
    '''conver nominal RCA values to 0s and 1s'''
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0
    
    # print rcas.ix["mg030000"]
    
    prox = prox.reindex(columns=rcas.columns, index=rcas.columns).fillna(0)
    '''need to reindex the rca matrix since we dopped NULL vals from PCI'''
    # rca = rca.reindex(columns=pci.index)
    
    distances = growth.distance(rcas, prox).fillna(0)
    
    # print distances.ix["mg030000"].order(ascending=False)
    # sys.exit()
    
    return distances

def add(year, geo_level, distance, wld_or_domestic):
    '''delete old proximity values'''
    print "Deleteing old distance values..."
    delete_old_distance_from_db(year, geo_level, wld_or_domestic)
    
    '''insert new proximity values to database'''
    print "Adding new distance values..."
    add_new_distance_to_db(year, distance, wld_or_domestic)

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from secex_ybp")
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
        geo_level = raw_input("Geo Level {2:state, 4:meso, 7:planning, " \
                                "8:munic, all}: ")
    if geo_level == "all":
        geo_level = [2, 4, 7, 8]
    else:
        geo_level = [geo_level]
    
    year = [2010, 2011]
    for y in year:
        print
        print "Year: {0}".format(y);
        for g in geo_level:
            print
            print " --- Geo Level: {0} --- ".format(g);
            dist = calculate_distance(y, g, "domestic")
            add(y, g, dist, "domestic")
            
            dist = calculate_distance(y, g, "world")
            add(y, g, dist, "world")