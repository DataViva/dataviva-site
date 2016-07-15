import os
import commands
import time
import logging
import sys

year_begin = 2009
year_end = 2014

if (len(sys.argv) != 3 and len(sys.argv) != 5) or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! Use:\n python scripts/data_download/higher_education/create_files.py en/pt output_path year_init year_begin\n"
    print " If not set the years, default equal all years. 2009-2014\n"
    exit()

if len(sys.argv) == 5:
    year_begin = sys.argv[3]
    year_end = sys.argv[4]

logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],str(sys.argv[0].split('/')[2]) + '-all-data-download.log' )),level=logging.DEBUG)

for year in range(int(year_begin), int(year_end)+1):
    logging.info("python scripts/data_download/higher_education/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year) + "\n")
    ret = commands.getoutput("python scripts/data_download/higher_education/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year))
    logging.info(str(ret) + "\nYear: " + str(year) + " ok =D\n\n")