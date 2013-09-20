# -*- coding: utf-8 -*-
"""
    Add PCIs from observatory to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script will import the CSV file observatory_pcis.csv
    to the DB.
"""

import MySQLdb, os, argparse, sys, csv
from os import environ


''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_lookup():
    cursor.execute("select id from attrs_hs where length(id) = 6")
    return {hs[0][2:]:hs[0] for hs in cursor.fetchall()}

def add_to_db(file_path):
    print 'reading CSV file "' + file_path + '"'
    
    
    with open(file_path, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,\t')
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, dialect)
        header = csv_reader.next()
        
        hs_lookup = get_lookup()

        for i, line in enumerate(csv_reader):
            line = dict(zip(header, line))
            
            hs = hs_lookup[line["hs4"]]
            pci = float(line["pci"])
            year = int(line["year"])
            
            cursor.execute("UPDATE secex_yp set pci=%s where year=%s and "\
                "hs_id=%s", [pci, year, hs])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")

    add_to_db(file_path)