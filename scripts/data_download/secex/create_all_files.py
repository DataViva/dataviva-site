import os
import commands
import time
import logging
import sys

if len(sys.argv) != 3 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! Use:\n python scripts/data_download/secex/create_files.py en/pt output_path\n"
    exit()

logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],str(sys.argv[0].split('/')[2]) + '-all-data-download.log' )),level=logging.DEBUG)

for year in range(2002, 2017):
    logging.info("python scripts/data_download/secex/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year) + "\n")
    ret = commands.getoutput("python scripts/data_download/secex/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year))
    logging.info(str(ret) + "\nYear: " + str(year) + " ok =D\n\n")