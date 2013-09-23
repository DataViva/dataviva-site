# -*- coding: utf-8 -*-
"""
    Add TSV (tab delimited file) to database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Use this script to add CSV files dumped from google docs
    to the database.
"""

''' Import statements '''
import csv, sys, MySQLdb, os, argparse
from os import environ


''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_lookup(type):
    if type == "bra":
        cursor.execute("select id_ibge, id from attrs_bra")
        return {str(r[0])[:-1]:r[1] for r in cursor.fetchall()}
    elif type == "isic":
        cursor.execute("select id from attrs_isic")
        return {r[0][1:]:r[0] for r in cursor.fetchall()}
    elif type == "cbo":
        cursor.execute("select id from attrs_cbo")
        return {r[0]:r[0] for r in cursor.fetchall()}
    elif type == "wld":
        cursor.execute("select id_mdic, id from attrs_wld")
        return {r[0]:r[1] for r in cursor.fetchall()}

def add_to_db(file_path, table):
    # missing_munic_lookup = {}
    # csv_reader = csv.reader(open("munics.csv", 'rb'), delimiter=",", quotechar='"')
    # csv_reader.next()
    # for line in csv_reader:
    #     missing_munic_lookup[line[0]] = line[1].strip()
    
    
    ''' Open CSV file '''
    csv_reader = csv.reader(open(file_path, 'rb'), delimiter="\t", quotechar='"')
    header = csv_reader.next()
    
    lookups = {}
    lookups["bra_id"] = get_lookup("bra")
    lookups["isic_id"] = get_lookup("isic")
    lookups["cbo_id"] = get_lookup("cbo")
    missing_bra = set([])
    missing_isic = set([])
    missing_cbo = set([])
    total = 0
    missing_total = 0
    
    ''' Add the file to the DB '''
    for i, line in enumerate(csv_reader):
        # strip out white space
        line = [l.strip() for l in line]
        row = dict(zip(header, line))
        row
        warnings = False
        
        if i % 10000 == 0 and i != 0:
            sys.stdout.write('\r lines read: ' + str(i) + ' ' * 20)
            sys.stdout.flush() # important
        
        if "bra_id" in row:
            try:
                row["bra_id"] = lookups["bra_id"][row["bra_id"]]
            except:
                missing_bra.add(row["bra_id"])
                print "[line: {0}] Warning: could not find IBGE id: {1} " \
                        "in database.".format(i, row["bra_id"])
                warnings = True
        
        if "isic_id" in row:
            row["isic_id"] = str(row["isic_id"]).zfill(4)
            try:
                row["isic_id"] = lookups["isic_id"][row["isic_id"]]
            except:
                if row["isic_id"] in ['0000', '-94201', '0001']:
                    row["isic_id"] = "x0000"
                else:
                    missing_isic.add(row["isic_id"])
                    print "[line: {0}] Warning: could not find ISIC id: {1} " \
                            "in database.".format(i, row["isic_id"])
                    warnings = True
        
        if "cbo_id" in row:
            try:
                row["cbo_id"] = lookups["cbo_id"][row["cbo_id"]]
            except:
                if row["cbo_id"] in ['', 'NAO DESL A', 'IGNORA', '-94201', '0000']:
                    row["cbo_id"] = "xxxx"
                else:
                    missing_isic.add(row["cbo_id"])
                    print "[line: {0}] Warning: could not find CBO id: {1} " \
                            "in database.".format(i, row["cbo_id"])
                    warnings = True

        if not warnings:
            total += float(row["wage"])
        else:
            missing_total += float(row["wage"])
            continue
        
        # sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, \
        #         ",".join(row.keys()), ",".join(["%s"]*len(row.keys())))
        
        sql = "INSERT INTO {0} ({1}) VALUES ({2}) ON DUPLICATE KEY UPDATE wage=wage+%s".format(table, \
                ",".join(row.keys()), ",".join(["%s"]*len(row.keys())))
    
        try:
            cursor.execute(sql, row.values()+[row["wage"]])
        except MySQLdb.Error, e:
             print "Error %d: %s" % (e.args[0], e.args[1])
             print
        # sys.exit()
        

    print
    print "missing municipality codes:", missing_bra
    print "missing isic codes:",  missing_isic
    print "missing cbo codes:", missing_cbo
    print "total val_usd: ", total
    print "missing %: ", (missing_total / total)*100    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    parser.add_argument("-t", "--table", help="table to add the data into")
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")
    if "," in file_path:
        file_path = file_path.split(",")
    else:
        file_path = [file_path]
    
    table = args.table
    if not table:
        table = raw_input("Table to insert into: ")
    
    for fp in file_path:
        print
        print fp
        add_to_db(fp, table)
    
    # for y in range(2002, 2012):
    #     for fp in file_path:
    #         fp = fp.replace("2002", str(y))
    #         print
    #         print fp
    #         add_to_db(fp, table)