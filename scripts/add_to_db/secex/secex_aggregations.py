# -*- coding: utf-8 -*-
"""
    Aggregate secex data to higher level nestings
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Use this script to...
"""

''' Import statements '''
import csv, sys, MySQLdb, os, argparse
from os import environ


''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()


def add_to_db(table):
    planning_regions = ["mgplr01", "mgplr02", "mgplr03", "mgplr04", "mgplr05",
                        "mgplr06", "mgplr07", "mgplr08", "mgplr09", "mgplr10"]
    attr_aggs = {
        "b": [4, 7, 8],
        "p": [2, 6],
        "w": [2, 5]
    }
    attr_names = {
        "y": "year",
        "b": "bra_id",
        "p": "hs_id",
        "w": "wld_id"
    }
    attrs = table.split("_")[1]
    columns = [attr_names[a] for a in attrs]
    
    for attr_type in reversed(attrs[1:]):
        attr_name = attr_names[attr_type]
        print attr_name
        
        for aggregation_level in attr_aggs[attr_type][:-1]:
            print aggregation_level
            deepest = attr_aggs[attr_type][-1]
            
            if attr_name == "bra_id" and aggregation_level == 7:
                for plr_region in planning_regions:
                    agg_str = "substr({0},1,{1})".format(attr_name, aggregation_level)
                    columns_str = columns[:]
                    group_by_str = columns[:]
                
                    columns_str[columns_str.index(attr_name)] = "'{0}' as bra_id".format(plr_region)
                    columns_str = ", ".join(columns_str)
                
                    del group_by_str[group_by_str.index(attr_name)]
                    group_by_str = ", ".join(group_by_str)
                
                    sql = "select {0}, sum(val_usd) as val_usd from {1} "\
                            "where bra_id in "\
                            "(select bra_id from attrs_bra_pr where pr_id = '{2}') "\
                            "and length(bra_id) = 8 group by {3}"\
                            .format(columns_str, table, plr_region, group_by_str)
                    
                    insert_columns_str = ", ".join(columns + ["val_usd"])
                    insert_sql = "insert into {0} ({1}) {2}"\
                                    .format(table, insert_columns_str, sql)
                    
                    print
                    print insert_sql
                    cursor.execute(insert_sql)
                
            
            else:
                agg_str = "substr({0},1,{1})".format(attr_name, aggregation_level)
                columns_str = columns[:]
                group_by_str = columns[:]
                
                columns_str[columns_str.index(attr_name)] = agg_str+" as "+attr_name
                columns_str = ", ".join(columns_str)
                
                group_by_str[group_by_str.index(attr_name)] = agg_str
                group_by_str = ", ".join(group_by_str)
                
                where = "length({0}) = {1}".format(attr_name, deepest)
            
                sql = "select {0}, sum(val_usd) as val_usd from {1} "\
                        "where {2} "\
                        "group by {3}"\
                        .format(columns_str, table, where, group_by_str)
                
                insert_columns_str = ", ".join(columns + ["val_usd"])
                insert_sql = "insert into {0} ({1}) {2}"\
                                .format(table, insert_columns_str, sql)
                                
                
                print
                print insert_sql
                cursor.execute(insert_sql)
                # sys.exit()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", help="table to add the data into")
    args = parser.parse_args()
    
    table = args.table
    if not table:
        table = raw_input("Table to insert into: ")
    
    print
    print table
    add_to_db(table)