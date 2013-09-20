# -*- coding: utf-8 -*-
"""
    YO table to add unique industries to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate the number of industries (isic) that are 
    found in each occupation.
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

def get_unique(year, cbo_level):

    '''Get values from database'''
    q = "select isic_id, cbo_id, wage " \
        "from rais_yio " \
        "where year = {0} and length(cbo_id) = {1} and " \
        "length(isic_id) = 5".format(year, cbo_level)
    bra_table = sql.read_frame(q, db)
    bra_table = bra_table.pivot(index="cbo_id", columns="isic_id", values="wage")        
    bra_table = bra_table.fillna(0)

    bra_table[bra_table >= 1] = 1
    bra_table[bra_table < 1] = 0
    
    return bra_table.sum(axis=1).order()

def delete_old_unique_from_db(y, cbo_level):
    '''clear old rca vals'''
    q = "update rais_yo set unique_isic=NULL " \
        "where year = {0} and length(cbo_id) = {1}" \
        .format(y, cbo_level)
    cursor.execute(q)

def add_new_unique_to_db(y, unique_isics):
    '''add rcas vals'''
    for cbo in unique_isics.index:
        cursor.execute("update rais_yo set unique_isic=%s where year=%s and "\
            "cbo_id=%s ", [unique_isics[cbo], y, cbo])

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_yo")
    years = [int(row[0]) for row in cursor.fetchall()]
    return years

if __name__ == "__main__":
    print; print 'RAIS YO unique isic...'; print;

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    parser.add_argument("-o", "--cbo_level", help="level of cbo nesting",
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
        cbo_level = raw_input("CBO Level {1:top level, 4:deepest}: ")
    if cbo_level == "all":
        cbo_level = [1, 4]
    else:
        cbo_level = [cbo_level]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for o in cbo_level:
            print
            print " --- CBO Level: {0} --- ".format(o);
            unique_isics = get_unique(y, o)
            delete_old_unique_from_db(y, o)
            add_new_unique_to_db(y, unique_isics)
