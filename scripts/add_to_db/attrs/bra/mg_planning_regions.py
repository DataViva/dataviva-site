# -*- coding: utf-8 -*-
"""
    Add planning regions to database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Use this script to add CSV file of planning regions to DB
"""

''' Import statements '''
import csv, sys, MySQLdb, os, argparse
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(basedir, '..'))

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_bra_lookup():
    cursor.execute("select id_ibge, id from attrs_bra where id_ibge is not null")
    return {str(b[0])[:-1]:b[1] for b in cursor.fetchall()}

def add_to_db(file_path):
    bra_lookup = get_bra_lookup()
    
    ''' Open CSV file '''
    print file_path
    csv_reader = csv.reader(open(file_path, 'rb'), delimiter="\t", quotechar='"')
    header = csv_reader.next()
    
    ''' Add the file to the DB '''
    for line in csv_reader:
        bra_id = bra_lookup[line[0]]
        pr_id = "mgpr%s" % (line[7].zfill(2))
        # print bra_id, pr_id
        cursor.execute('insert into attrs_bra_pr values(%s, %s)', [bra_id, pr_id])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")
        if file_path == "":
            sys.exit()
        
    add_to_db(file_path)