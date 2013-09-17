# -*- coding: utf-8 -*-
"""
    Calculate RCA values (for industries)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate industry/location RCA values
    based on the domestic brazilian market (YBI)
"""

import MySQLdb, os, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys

from os import environ

this_dir = os.path.abspath(os.path.dirname(__file__))
growth_lib_dir = os.path.abspath(os.path.join(this_dir, '../../growth_lib/'))

# print growth_lib_dir
sys.path.append(growth_lib_dir)
import growth

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_rca(year, geo_level):
    '''Get values from database'''
    q = "select bra_id, isic_id, wage " \
        "from rais_ybi " \
        "where year = {0} and length(bra_id) = {1} and " \
        "length(isic_id) = 5".format(year, geo_level)
    # q = "select ybi.bra_id, ybi.isic_id, ybi.wage from rais_ybi as ybi, " \
    # "rais_yb as yb where" \
    # " yb.year = ybi.year and yb.bra_id = ybi.bra_id and ybi.year = {0} and " \
    # "length(ybi.bra_id) = {1} and length(isic_id) = 5 and yb.wage > 1200145000"\
    # .format(year, geo_level)
    table = sql.read_frame(q, db)
    table = table.pivot(index="bra_id", columns="isic_id", values="wage")
    table = table.fillna(0)
    
    '''Use growth library to run RCA calculation on data'''
    mcp = growth.rca(table)
    
    return mcp

def delete_old_rcas_from_db(y, geo_level):
    '''clear old rca vals'''
    q = "update rais_ybi set rca=NULL " \
        "where year = {0} and length(bra_id) = {1} and " \
        "length(isic_id) = 5".format(y, geo_level)
    cursor.execute(q)

def add_new_rcas_to_db(year, rcas):
    '''add new rca vals'''
    to_add = []
    counter = 0
    total_inserts = 0
    
    for isic in rcas.columns:
        for bra in rcas.index:
            counter += 1
            total_inserts += 1
            to_add.append([rcas[isic][bra], year, bra, isic])
            if counter >= 2500:
                cursor.executemany("update rais_ybi set rca=%s where " \
                                "year=%s and bra_id=%s and isic_id=%s", to_add)
                counter = 0
                to_add = []
                
            if total_inserts % 10000 == 0:
                sys.stdout.write('\r rows updated: ' + str(total_inserts) + ' ' * 20)
                sys.stdout.flush() # important
    
    print
    '''cant forget to add any stragglers to the DB'''
    cursor.executemany("update rais_ybi set rca=%s where " \
                    "year=%s and bra_id=%s and isic_id=%s", to_add)

def calculate_rca(year, geo_level):
    '''calculate RCAs'''
    print "Calculating RCAs..."
    rcas = get_rca(year, geo_level)
    
    '''remove old RCAs from DB'''
    print "Deleteing old rcas from database..."
    delete_old_rcas_from_db(y, geo_level)
    
    '''add new RCAs to DB'''
    print "Adding new rcas to database..."
    add_new_rcas_to_db(y, rcas)

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_ybi")
    years = [row[0] for row in cursor.fetchall()]
    return years

if __name__ == "__main__":
    print; print 'RAIS YBI RCA...'; print;
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    parser.add_argument("-g", "--geo_level", help="level of geo nesting",
                            choices=['2', '4', '6', '7', '8', 'all'])
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
        geo_level = raw_input("Geo Level {2:state, 4:meso, 6:micro, " \
                                "8:munic, all}: ")
    if geo_level == "all":
        geo_level = ['2', '4', '6', '7', '8']
    else:
        geo_level = [geo_level]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for g in geo_level:
            print
            print " --- Geo Level: {0} --- ".format(g);
            calculate_rca(y, g)
