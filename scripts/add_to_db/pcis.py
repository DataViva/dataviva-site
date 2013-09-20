import MySQLdb, os, argparse
import sys, csv
from os import environ

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["VISUAL_DB_USER"], 
                        passwd=environ["VISUAL_DB_PW"], 
                        db=environ["VISUAL_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

cursor.execute("select id from attrs_hs")
hs_lookup = {r[0][2:]:r[0] for r in cursor.fetchall()}

''' Open CSV file '''
csv_reader = csv.reader(open("/Users/alexandersimoes/Desktop/pci.csv", 'rb'), delimiter=",", quotechar='"')
header = csv_reader.next()

for row in csv_reader:
    hs = hs_lookup[row[2]]
    pci = float(row[0])
    
    cursor.execute("update secex_yp set pci_wld=%s where year=2011 and hs_id=%s", [pci, hs])