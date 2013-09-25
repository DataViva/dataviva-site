# -*- coding: utf-8 -*-
"""
    Calculate RCA values (domestic)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate product/location RCA values
    based on the domestic brazilian market (YBP)
"""

import MySQLdb, os
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
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], 
                        db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_rca(year, geo_level):
    '''Get values from database'''
    q = "select bra_id, hs_id, val_usd " \
        "from secex_ybp " \
        "where year = {0} and length(bra_id) = {1} and " \
        "length(hs_id) = 6".format(year, geo_level)
    table = sql.read_frame(q, db)
    table = table.pivot(index="bra_id", columns="hs_id", values="val_usd")
    table = table.fillna(0)
    
    '''Use growth library to run RCA calculation on data'''
    mcp = growth.rca(table)
    
    return mcp

def delete_old_rcas_from_db(y, geo_level):
    '''clear old rca vals'''
    q = "update secex_ybp set rca=NULL " \
        "where year = {0} and length(bra_id) = {1} and " \
        "length(hs_id) = 6".format(y, geo_level)
    cursor.execute(q)

def add_new_rcas_to_db(y, rcas_matrix):
    '''add rcas vals'''
    for hs in rcas_matrix.columns:
        to_add = []
        for bra in rcas_matrix.index:
            to_add.append([rcas_matrix[hs][bra], y, bra, hs])
        cursor.executemany("update secex_ybp set rca=%s where year=%s and bra_id=%s and hs_id=%s", to_add)

def main():
    '''Get all years in the database'''
    cursor.execute("select distinct year from secex_ybp")
    years = [row[0] for row in cursor.fetchall()]
    
    '''The different geo levels e.g. state, meso, micro, munic'''
    geo_levels = ['2', '4', '6', '7', '8']
    
    for y in years:
        for geo_level in geo_levels:
            print y, geo_level
            rcas = get_rca(y, geo_level)
            delete_old_rcas_from_db(y, geo_level)
            add_new_rcas_to_db(y, rcas)

if __name__ == "__main__":
    print; print 'SECEX YBP Domestic RCA...'; print;
    main()
