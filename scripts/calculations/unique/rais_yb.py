# -*- coding: utf-8 -*-
"""
    YB table to add unique industries and occupations to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate the number of unique industries (isic)
    and occupations (cbo) that are found in each location (state, meso,
    planning region and municipality).
"""

import MySQLdb, os, sys, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np

from os import environ

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_unique(year, geo_level, isic_or_cbo):

    '''Get values from database'''
    if isic_or_cbo == "isic":
        q = "select bra_id, isic_id, wage " \
            "from rais_ybi " \
            "where year = {0} and length(bra_id) = {1} and " \
            "length(isic_id) = 5".format(year, geo_level)
        bra_table = sql.read_frame(q, db)
        bra_table = bra_table.pivot(index="bra_id", columns="isic_id", values="wage")
    elif isic_or_cbo == "cbo":
        q = "select bra_id, cbo_id, wage " \
            "from rais_ybo " \
            "where year = {0} and length(bra_id) = {1} and " \
            "length(cbo_id) = 4".format(year, geo_level)
        bra_table = sql.read_frame(q, db)
        bra_table = bra_table.pivot(index="bra_id", columns="cbo_id", values="wage")
        
    bra_table = bra_table.fillna(0)

    bra_table[bra_table >= 1] = 1
    bra_table[bra_table < 1] = 0
    
    return bra_table.sum(axis=1).order()

def delete_old_unique_from_db(y, geo_level):
    '''clear old rca vals'''
    q = "update rais_yb set unique_cbo=NULL, unique_isic=NULL " \
        "where year = {0} and length(bra_id) = {1}" \
        .format(y, geo_level)
    cursor.execute(q)

def add_new_unique_to_db(y, unique_isics, unique_cbos):
    '''add rcas vals'''
    for bra in unique_isics.index:
        cursor.execute("update rais_yb set unique_isic=%s where year=%s and "\
            "bra_id=%s ", [unique_isics[bra], y, bra])
    for bra in unique_cbos.index:
        cursor.execute("update rais_yb set unique_cbo=%s where year=%s and "\
            "bra_id=%s ", [unique_cbos[bra], y, bra])

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_yb")
    years = [int(row[0]) for row in cursor.fetchall()]
    return years

if __name__ == "__main__":
    print; print 'RAIS YB unique cbo/isic...'; print;

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
            unique_isics = get_unique(y, g, "isic")
            unique_cbos = get_unique(y, g, "cbo")
            delete_old_unique_from_db(y, g)
            add_new_unique_to_db(y, unique_isics, unique_cbos)
