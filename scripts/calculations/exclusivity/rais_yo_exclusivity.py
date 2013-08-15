# -*- coding: utf-8 -*-
"""
    Calculate exclusivity for a given occupation in a given year
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import MySQLdb, os, argparse
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys

from os import environ

this_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.abspath(os.path.join(this_dir, '../../../'))

# growth_lib_dir = os.path.abspath(os.path.join(base_dir, 'scripts/growth_lib/'))
# sys.path.append(growth_lib_dir)
# import growth
# 
''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_all_isic(y):
    cursor.execute("select distinct(isic_id) from rais_yi " \
                        "where length(isic_id) = 5 and year = %s", [y])
    return [x[0] for x in cursor.fetchall()]

def get_all_cbo(y):
    cursor.execute("select distinct(cbo_id) from rais_yo where "\
                        "length(cbo_id) = 4 and year = %s", [y])
    return [x[0] for x in cursor.fetchall()]

def calculate_exclusivity(y):
    
    all_isic = get_all_isic(y)
    all_cbo = get_all_cbo(y)
    
    for cbo in all_cbo:
        print cbo
        for isic in all_isic:
            print isic
            cursor.execute("select bra_id from rais_ybi where isic_id = %s " \
                            "and year = %s and rca >= 1 and length(bra_id) = 8", [isic, y])
            bras = [x[0] for x in cursor.fetchall()]
            denom = len(bras)
            numerator = 0
            
            for b in bras:
                cursor.execute("select num_emp from rais_ybio where "\
                                "year = %s and bra_id = %s and " \
                                "isic_id = %s and cbo_id = %s", \
                                [y, b, isic, cbo])
                exists = cursor.fetchone()
                if exists:
                    numerator += 1.0
            
            # print numerator, denom, 
            avar = numerator/float(denom)
            print cbo, isic, avar
            cursor.execute("update rais_yio set importance = %s "\
                                "where year = %s and isic_id = %s "\
                                "and cbo_id = %s", [avar,y,isic,cbo])

def get_all_years():
    '''Get all years in the database'''
    cursor.execute("select distinct year from rais_yo")
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
        calculate_exclusivity(y)