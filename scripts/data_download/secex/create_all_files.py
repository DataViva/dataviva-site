import os
import commands
import time
import logging
import sys

year_begin = 2000
year_end = 2016

if (len(sys.argv) != 3 and len(sys.argv) != 5) or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! Use:\n python scripts/data_download/secex/create_files.py en/pt output_path\n"
    print " If not set the years, default equal all years. 2000-2016\n"
    exit()

if len(sys.argv) == 5:
    year_begin = sys.argv[3]
    year_end = sys.argv[4]

logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],str(sys.argv[0].split('/')[2]) + '-all-data-download.log' )),level=logging.DEBUG)

for year in range(int(year_begin), int(year_end)+1):
    logging.info("python scripts/data_download/secex/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year) + "\n")
    ret = commands.getoutput("python scripts/data_download/secex/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year))
    logging.info(str(ret) + "\nYear: " + str(year) + " ok =D\n\n")