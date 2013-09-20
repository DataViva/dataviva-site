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

prox_dir = os.path.abspath(os.path.join(base_dir, 'scripts/calculations/proximity/'))
sys.path.append(prox_dir)
import rais_yii_proximity

rca_dir = os.path.abspath(os.path.join(base_dir, 'scripts/calculations/rca/'))
sys.path.append(rca_dir)
import rais_ybi_rca

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def calculate_distance(year, geo_level):
    
    '''step 1 in calculating distance, get proximity'''
    prox = rais_yii_proximity.calculate_proximity(year)
    # print prox["j6201"].order()
    # sys.exit()
    
    '''step 2 in calculating distance, get rca'''
    rcas = rais_ybi_rca.get_rca(year, geo_level)
    rcas[rcas >= 1] = 1
    rcas[rcas < 1] = 0
    
    '''need to make sure both are using same isics'''
    rcas = rcas.reindex(columns=prox.columns).fillna(0)
    # print rcas.ix["mg"].order()
    # sys.exit()
    
    distances = growth.distance(rcas, prox).fillna(0)
    # print distances.ix["mg"].order()
    # sys.exit()
    
    return distances

def remove_distances(year, geo_level):
    '''clear old proximity vals'''
    cursor.execute("update rais_ybi set distance=NULL where year=%s " \
                    "and length(bra_id) = %s", (year, geo_level))

def add_distances(year, dist):
    '''add new opp_gain vals'''
    total_inserts = 0
    for isic in dist.columns:
        to_add = []
        for bra in dist.index:
            total_inserts += 1
            to_add.append([year, bra, isic, dist[isic][bra], dist[isic][bra]])
            
            # if total_inserts % 10000 == 0:
            #     sys.stdout.write('\r rows updated: ' + str(total_inserts) + ' ' * 20)
            #     sys.stdout.flush() # important
    
        q = "INSERT INTO rais_ybi (year, bra_id, isic_id, distance) VALUES "\
            "(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE distance=%s;"\
            .format(to_add)
        cursor.executemany(q, to_add)


def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_ybi")
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
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for g in geo_level:
            print
            print " --- Geo Level: {0} --- ".format(g);
            dist = calculate_distance(y, g)
            remove_distances(y, g)
            add_distances(y, dist)