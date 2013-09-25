# -*- coding: utf-8 -*-
"""
    YI table to add unique occupations to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate the number of occupations (cbo) that are 
    found in each industry.
"""

import MySQLdb, os, sys, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np

from os import environ

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], 
                        db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_unique(year, isic_level):

    '''Get values from database'''
    q = "select isic_id, cbo_id, wage " \
        "from rais_yio " \
        "where year = {0} and length(isic_id) = {1} and " \
        "length(cbo_id) = 4".format(year, isic_level)
    bra_table = sql.read_frame(q, db)
    bra_table = bra_table.pivot(index="isic_id", columns="cbo_id", values="wage")        
    bra_table = bra_table.fillna(0)

    bra_table[bra_table >= 1] = 1
    bra_table[bra_table < 1] = 0
    
    return bra_table.sum(axis=1).order()

def delete_old_unique_from_db(y, isic_level):
    '''clear old rca vals'''
    q = "update rais_yi set unique_cbo=NULL " \
        "where year = {0} and length(isic_id) = {1}" \
        .format(y, isic_level)
    cursor.execute(q)

def add_new_unique_to_db(y, unique_cbos):
    '''add rcas vals'''
    for isic in unique_cbos.index:
        cursor.execute("update rais_yi set unique_cbo=%s where year=%s and "\
            "isic_id=%s ", [unique_cbos[isic], y, isic])

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_yi")
    years = [int(row[0]) for row in cursor.fetchall()]
    return years

if __name__ == "__main__":
    print; print 'RAIS YI unique cbo...'; print;

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="year for calculations to be run")
    parser.add_argument("-i", "--isic_level", help="level of isic nesting",
                            choices=['1', '5', 'all'])
    args = parser.parse_args()
    
    year = args.year
    if not year:
        year = raw_input("Year for calculations (or all): ")
    if year == "all":
        year = get_all_years()
    else:
        year = [int(year)]
    
    isic_level = args.isic_level
    if not isic_level:
        isic_level = raw_input("Isic Level {1:top level, 5:deepest}: ")
    if isic_level == "all":
        isic_level = [1, 5]
    else:
        isic_level = [isic_level]
    
    for y in year:
        print
        print "Year: {0}".format(y);
        for i in isic_level:
            print
            print " --- Isic Level: {0} --- ".format(i);
            unique_cbos = get_unique(y, i)
            delete_old_unique_from_db(y, i)
            add_new_unique_to_db(y, unique_cbos)
