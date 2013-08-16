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

countries = ["'afago'", "'afciv'", "'afcmr'", "'afcog'", "'afdza'", "'afegy'", "'afeth'", "'afgab'", "'afgha'", "'afgin'", "'afken'", "'aflbr'", "'aflby'", "'afmar'", "'afmdg'", "'afmli'", "'afmoz'", "'afmrt'", "'afmus'", "'afmwi'", "'afnga'", "'afsdn'", "'afsen'", "'aftun'", "'aftza'", "'afuga'", "'afzmb'", "'afzwe'", "'asare'", "'asaze'", "'asbgd'", "'aschn'", "'asgeo'", "'ashkg'", "'asidn'", "'asind'", "'asirn'", "'asisr'", "'asjor'", "'asjpn'", "'askaz'", "'askgz'", "'askhm'", "'askor'", "'askwt'", "'aslao'", "'aslbn'", "'aslka'", "'asmng'", "'asmys'", "'asomn'", "'aspak'", "'asphl'", "'asqat'", "'asrus'", "'assau'", "'assgp'", "'assyr'", "'astha'", "'astjk'", "'astkm'", "'astur'", "'asuzb'", "'asvnm'", "'asyem'", "'eualb'", "'euaut'", "'eubel'", "'eubgr'", "'eubih'", "'eublr'", "'euche'", "'eucze'", "'eudeu'", "'eudnk'", "'euesp'", "'euest'", "'eufin'", "'eufra'", "'eugbr'", "'eugrc'", "'euhrv'", "'euhun'", "'euirl'", "'euita'", "'eultu'", "'eulva'", "'eumda'", "'eumkd'", "'eunld'", "'eunor'", "'eupol'", "'euprt'", "'eurou'", "'eusrb'", "'eusvk'", "'eusvn'", "'euswe'", "'euukr'", "'nacan'", "'nacri'", "'nacub'", "'nadom'", "'nagtm'", "'nahnd'", "'najam'", "'namex'", "'nanic'", "'napan'", "'naslv'", "'natto'", "'nausa'", "'ocaus'", "'ocnzl'", "'ocpng'", "'saarg'", "'sabol'", "'sabra'", "'sachl'", "'sacol'", "'saecu'", "'saper'", "'sapry'", "'saury'", "'saven'"]

def delete_old_complexity_from_db(year, geo_level):
    '''clear old opp_gain vals'''
    q = "update secex_yw set complexity=NULL " \
        "where year = {0} and length(wld_id) = {1}".format(year, geo_level)
    cursor.execute(q)

def get_comtrade_rca(year):
    '''Get values from database'''
    q = "select wld_id, hs_id, val_usd " \
        "from comtrade_ypw " \
        "where year = {0} and wld_id in ({1}) and length(hs_id) = 6".format(year, ",".join(countries))
    table = sql.read_frame(q, db)
    table = table.pivot(index="wld_id", columns="hs_id", values="val_usd")
    table = table.fillna(0)
    
    '''Use growth library to run RCA calculation on data'''
    mcp = growth.rca(table)
    
    return mcp

def add_new_complexity_to_db(year, complexity):
    '''add new opp_gain vals'''
    to_add = []
    counter = 0
    total_inserts = 0
    for wld in complexity.index:
        counter += 1
        total_inserts += 1
        to_add.append([complexity[wld], year, wld])
        if counter >= 2500:
            cursor.executemany("update secex_yw set complexity=%s where " \
                            "year=%s and wld_id=%s", to_add)
            counter = 0
            to_add = []
            
        if total_inserts % 10000 == 0:
            sys.stdout.write('\r rows updated: ' + str(total_inserts) + ' ' * 20)
            sys.stdout.flush() # important
    
    print
    '''cant forget to add any stragglers to the DB'''
    cursor.executemany("update secex_yw set complexity=%s where " \
                    "year=%s and wld_id=%s", to_add)

def calculate_complexity(year, geo_level):
    
    # '''step 1 in calculating opportunity gain, get RCA'''
    # print "Calculating RCAs..."
    # rca = secex_ybp_rca_wld.get_rca(year, geo_level)
    # rca = rca.fillna(0)
    # '''conver nominal RCA values to 0s and 1s'''
    # rca[rca >= 1] = 1
    # rca[rca < 1] = 0
    
    '''calculate product complexity'''
    print "Calculating complexity..."
    # comtrade_rca = comtrade_ypp_proximity.get_comtrade_rca(year)
    comtrade_rca = get_comtrade_rca(year)
    comtrade_rca[comtrade_rca >= 1] = 1
    comtrade_rca[comtrade_rca < 1] = 0
    pci = growth.complexity(comtrade_rca)[1]
    eci = growth.complexity(comtrade_rca)[0]
    '''reindex'''
    # pci = pci.reindex(index=rca.columns)
    pci = pci.dropna()
    
    # print pci
    # print pci.order()
    # sys.exit()
    
    return eci
    
def add(year, geo_level, complexity):
    '''delete database'''
    print "Deleteing old opportunity gain values..."
    delete_old_complexity_from_db(year, geo_level)
    
    '''add to database'''
    print "Adding new opportunity gain values..."
    add_new_complexity_to_db(year, complexity)

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from secex_ybp")
    years = [row[0] for row in cursor.fetchall()]
    return years

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    parser.add_argument("-g", "--geo_level", help="level of geo nesting",
                            choices=['2', '5', 'all'])
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
        geo_level = raw_input("Geo Level {2:continent, 5:country}: ")
    if geo_level == "all":
        geo_level = [2, 5]
    else:
        geo_level = [geo_level]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for g in geo_level:
            print
            print " --- Geo Level: {0} --- ".format(g);
            complexity = calculate_complexity(y, g)
            add(y, g, complexity)
