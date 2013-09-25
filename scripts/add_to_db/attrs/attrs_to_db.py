# -*- coding: utf-8 -*-
"""
    Add attrs to database
    ~~~~~~~~~~~~~~~~~~~~~

    Use this script to add CSV files dumped from google docs
    to the database.
"""

''' Import statements '''
import csv, sys, MySQLdb, os, argparse
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(basedir, '..'))

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()


def add_to_db(file_path, attr_type):
    ''' Open CSV file '''
    print file_path
    csv_reader = csv.reader(open(file_path, 'rb'), delimiter=",", quotechar='"')
    header = csv_reader.next()
    
    ''' Add the file to the DB '''
    for line in csv_reader:
        row = dict(zip(header, line))
        row["id"] = row["id"].replace('~X~', '')
        
        sql = "update attrs_{0} set name_en=%s, keywords_en=%s where id= %s".format(attr_type)
        cursor.execute(sql, [row["name_en"], row["keywords_en"], row["id"]])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    parser.add_argument("-a", "--attr", help="Attribute type",
                            choices=['cbo', 'isic', 'bra', 'hs', 'wld'])
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")
    
    attr_type = args.attr
    if not attr_type:
        attr_type = raw_input("Attr type {cbo, isic, bra, hs, wld}: ")
    
    add_to_db(file_path, attr_type)