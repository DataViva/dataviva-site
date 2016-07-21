import os
import commands
import time
import logging
import sys

if len(sys.argv) != 5 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! use :\n python scripts/data_download/rais/download_manager_rais.py en/pt output_path year time(seconds)\n"
    exit()

files = ["i", "lo", "lio"]
type_location = ["regions", "states", "mesoregions", "microregions", "municipalities", "no_location"]
time_delay = int(sys.argv[4])

logging.basicConfig(filename='rais_create_files_by_installments.log',level=logging.DEBUG)

# industry 
i = commands.getoutput("python scripts/data_download/rais/create_files_by_installments.py "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" i ")
logging.info(i+"\n"+"data_download i ok\n\n")
time.sleep(time_delay) ## number of seconds


#industry occupation
lo = commands.getoutput("python scripts/data_download/rais/create_files_by_installments.py "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" lo")
logging.info(lo+"\n\n"+"data_download lo ok\n\n")
time.sleep(time_delay) ## number of seconds


#else
for type_file in type_location:
	lio = commands.getoutput("python scripts/data_download/rais/create_files_by_installments.py  "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" lio "+type_file)
	logging.info(lio+"\n"+"data_download lio " + type_file + " ok\n")
	time.sleep(time_delay) ## number of seconds

