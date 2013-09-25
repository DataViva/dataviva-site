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
db = MySQLdb.connect(host="localhost", user=environ["DATAVIVA_DB_USER"], 
                        passwd=environ["DATAVIVA_DB_PW"], db=environ["DATAVIVA_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_lookup(type):
    if type == "bra":
        cursor.execute("select id_mdic, id from attrs_bra")
        # return {str(r[0])[:-1]:r[1] for r in cursor.fetchall()}
        return {str(r[0]):r[1] for r in cursor.fetchall()}
    elif type == "hs":
        cursor.execute("select id from attrs_hs where length(id) = 6")
        return {r[0][2:]:r[0] for r in cursor.fetchall()}
    elif type == "wld":
        cursor.execute("select id_mdic, id from attrs_wld")
        return {r[0]:r[1] for r in cursor.fetchall()}

def add_to_db(file_path, table):
    missing_munic_lookup = {}
    csv_reader = csv.reader(open("munics.csv", 'rb'), delimiter=",", quotechar='"')
    csv_reader.next()
    for line in csv_reader:
        missing_munic_lookup[line[0]] = line[1].strip()
    
    
    ''' Open CSV file '''
    csv_reader = csv.reader(open(file_path, 'rb'), delimiter="\t", quotechar='"')
    header = csv_reader.next()
    
    lookups = {}
    lookups["bra_id"] = get_lookup("bra")
    lookups["hs_id"] = get_lookup("hs")
    lookups["wld_id"] = get_lookup("wld")
    missing_munics = set([])
    missing_wlds = set([])
    missing_hss = set([])
    missing_total = 0
    total = 0
    
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
                if row["bra_id"] == "9999999":
                    row["bra_id"] = "xx000007"
                elif row["bra_id"] == "9400000":
                    row["bra_id"] = "xx000002"
                else:
                    missing_munics.add(row["bra_id"])
                    print "[line: {0}] Warning: could not find IBGE id: {1} " \
                            "in database.".format(i, row["bra_id"])
                    warnings = True

        if "hs_id" in row:
            try:
                row["hs_id"] = lookups["hs_id"][row["hs_id"]]
            except:
                if row["hs_id"] in ['9991', '9992', '9998', '9997']:
                    row["hs_id"] = "229999"
                else:
                    missing_hss.add(row["hs_id"])
                    print "[line: {0}] Warning: could not find HS id: {1} " \
                            "in database.".format(i, row["hs_id"])
                    warnings = True
                    # sys.exit()
        
        if "wld_id" in row:
            try:
                row["wld_id"] = lookups["wld_id"][int(row["wld_id"])]
            except:
                if row["wld_id"] == "695":
                    row["wld_id"] = "nakna"
                elif row["wld_id"] == "423":
                    row["wld_id"] = "asmys"
                elif row["wld_id"] == "152":
                    row["wld_id"] = "euchi"
                else:
                    missing_wlds.add(row["wld_id"])
                    print "[line: {0}] Warning: could not find WLD id: {1} " \
                            "in database.".format(i, row["wld_id"])
                    warnings = True
                    # sys.exit()

        if not warnings:
            total += float(row["val_usd"])
        else:
            missing_total += float(row["val_usd"])
            continue
    
        sql = "INSERT INTO {0} ({1}) VALUES ({2}) ON DUPLICATE KEY UPDATE val_usd=val_usd+%s".format(table, \
                ",".join(row.keys()), ",".join(["%s"]*len(row.keys())))
    
        try:
            cursor.execute(sql, row.values()+[row["val_usd"]])
        except MySQLdb.Error, e:
            print row.values()
            print "Error %d: %s" % (e.args[0], e.args[1])
            print
        # sys.exit()
    
    print
    print "missing municipality codes:", missing_munics
    print "missing country codes:", missing_wlds
    print "missing hs codes:", missing_hss
    print "missing val_usd: ", missing_total
    print "total val_usd: ", total
    print "missing %: ", (missing_total / total)*100
    '''
    for m in missings:
        name = missing_munic_lookup[m]
        # q = "SELECT id FROM `attrs_bra` WHERE `name_en` = {0};".format(name)
        cursor.execute("SELECT id FROM `attrs_bra` WHERE `name_en` = %s and length(id)=8;", [name])
        results = cursor.fetchall()
        if len(results) == 1:
            id = results[0][0]
            cursor.execute("update attrs_bra set id_mdic=%s where id=%s;", [m, id])
        else:
            print
            print "unable to update", m, name
            id = raw_input('Any ideas?: ')
            if len(id) > 2:
                cursor.execute("update attrs_bra set id_mdic=%s where id=%s;", [m, id])
    '''

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
    
    for y in range(2000, 2012):
        for fp in file_path:
            fp = fp.replace("2000", str(y))
            print
            print fp
            add_to_db(fp, table)
    # for fp in file_path:
    #     print
    #     print fp
    #     add_to_db(fp, table)