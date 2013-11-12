import os, MySQLdb

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dataminas")
db.autocommit(1)
cursor = db.cursor()

cursor.execute("select id, name_en from attrs_wld where length(id) = 5")

names = {}
for row in cursor.fetchall():
    name = row[1].replace(", The","")
    split = name.split(", ")
    if len(split) > 1:
        name = "{0} {1}".format(split[1],split[0])
    names[name] = row[0]

unknowns = []
path = "/Users/Dave/Downloads/World Flags/"
for filename in os.listdir(path):
    name = filename.split(".")[0]
    name = name.replace("_"," ")
    if name in names:
        newname = "wld_"+names[name]+".png"
        os.rename(path+filename,path+newname)