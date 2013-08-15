# -*- coding: utf-8 -*-

''' Import statements '''
import csv, sys, MySQLdb, json
from collections import defaultdict


''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dataminas")
db.autocommit(1)
cursor = db.cursor()


''' Get Lookups '''
# id_conversion = {}
# cursor.execute("select id, id_ibge from attrs_bra where length(id) = 8")
# for row in cursor.fetchall():
#   id_conversion[row[1]] = row[0]
# 
# states = ["ac","al","am","ap","ba","ce","df","es","go","ma","mg","ms","mt","pa","pb","pe","pi","pr","rj","rn","ro","rr","rs","sc","se","sp","to"]
# 
# for state in states:
#   print "Current State: {0}".format(state)
#   data = []
#   with open("{0}_munic.json".format(state), "r") as f:
#     for line in f:
#       data.append(json.loads(line))
# 
#   for key in data[0]["objects"]["geojson"]["geometries"]:
#     if key["id"].isdigit():
#       if int(key["id"][:-1]) in id_conversion:
#         key["id"] = id_conversion[int(key["id"][:-1])]
#       else:
#         print "Not found: {0}".format(key)
#         del key
# 
#   with open("{0}_munic.json".format(state), "w") as f:
#     f.write(json.dumps(data[0], separators=(',',':')))

id_conversion = {}
cursor.execute("select id, id_ibge from attrs_bra where length(id) = 2")
for row in cursor.fetchall():
  id_conversion[row[1]] = row[0]

data = []
with open("topojson/bra_states.json", "r") as f:
    for line in f:
        data.append(json.loads(line))

for key in data[0]["objects"]["bra_states"]["geometries"]:
    if key["id"].isdigit():
        if int(key["id"]) in id_conversion:
            key["bra_id"] = id_conversion[int(key["id"])]
            del key["id"]
    else:
        print "Not found: {0}".format(key)
        del key

with open("topojson/bra_states.json", "w") as f:
    f.write(json.dumps(data[0], separators=(',',':')))