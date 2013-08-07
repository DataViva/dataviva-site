# -*- coding: utf-8 -*-
"""
    Calculate RCA values (international)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will calculate product/location RCA values
    based on the international export market (comtrade_ypw)
"""

import MySQLdb, os
import pandas as pd, pandas.io.sql as sql
import numpy as np
import sys

from os import environ

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def rca(bra_tbl, wld_tbl):
    col_sums = bra_tbl.sum(axis=1)
    col_sums = col_sums.reshape((len(col_sums), 1))
    rca_numerator = np.divide(bra_tbl, col_sums)
    
    row_sums = wld_tbl.sum(axis=0)
    total_sum = wld_tbl.sum().sum()
    rca_denominator = row_sums / total_sum
    rcas = rca_numerator / rca_denominator
    return rcas

def get_rca(year, geo_level):

    '''Get values from database'''
    q = "select bra_id, hs_id, val_usd " \
        "from secex_ybp " \
        "where year = {0} and length(bra_id) = {1} and " \
        "length(hs_id) = 6".format(year, geo_level)
    bra_table = sql.read_frame(q, db)
    bra_table = bra_table.pivot(index="bra_id", columns="hs_id", values="val_usd")
    bra_table = bra_table.fillna(0)
    
    q = "select wld_id, hs_id, val_usd from comtrade_ypw where year = {0}".format(year)
    wld_table = sql.read_frame(q, db)
    wld_table = wld_table.pivot(index="wld_id", columns="hs_id", values="val_usd")
    wld_table = wld_table.reindex(columns=bra_table.columns)
    wld_table = wld_table.fillna(0)
    
    mcp = rca(bra_table, wld_table).fillna(0)
    mcp[mcp == np.inf] = 0
    
    return mcp

def delete_old_rcas_from_db(y, geo_level):
    '''clear old rca vals'''
    q = "update secex_ybp set rca_wld=NULL " \
        "where year = {0} and length(bra_id) = {1} and " \
        "length(hs_id) = 6".format(y, geo_level)
    cursor.execute(q)

def add_new_rcas_to_db(y, rcas_matrix):
    '''add rcas vals'''
    for hs in rcas_matrix.columns:
        to_add = []
        for geo in rcas_matrix.index:
            to_add.append([rcas_matrix[hs][geo], y, geo, hs])
        cursor.executemany("update secex_ybp set rca_wld=%s where year=%s and bra_id=%s and hs_id=%s", to_add)


def main():
    '''Get all years in the database'''
    cursor.execute("select distinct year from secex_ybp")
    years = [row[0] for row in cursor.fetchall()]
    years = [2000]
    
    '''The different geo levels e.g. state, meso, micro, munic'''
    geo_levels = range(2, 10, 2)
    geo_levels = [2]
    
    for y in years:
        for geo_level in geo_levels:
            print y, geo_level
            rcas = get_rca(y, geo_level)
            delete_old_rcas_from_db(y, geo_level)
            add_new_rcas_to_db(y, rcas)

if __name__ == "__main__":
    print; print 'SECEX YBP International RCA...'; print;
    main()
