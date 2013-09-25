# -*- coding: utf-8 -*-
"""
    Add ECIs from observatory to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will import the CSV file observatory_ecis.csv
    to the DB (or whatever file path is given).
"""

import MySQLdb, os, argparse, sys, csv
from os import environ


''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], 
                        db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_lookup():
    cursor.execute("select id from attrs_wld where length(id) = 5")
    return {hs[0][2:]:hs[0] for hs in cursor.fetchall()}

def add_to_db(file_path):
    print 'reading CSV file "' + file_path + '"'
    
    
    with open(file_path, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,\t')
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, dialect)
        header = csv_reader.next()
        
        wld_lookup = get_lookup()

        for i, line in enumerate(csv_reader):
            line = dict(zip(header, line))
            
            wld = wld_lookup[line["country"].lower()]
            eci = float(line["eci"])
            year = int(line["year"])
            
            cursor.execute("UPDATE secex_yw set eci=%s where year=%s and "\
                "wld_id=%s", [eci, year, wld])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")

    add_to_db(file_path)