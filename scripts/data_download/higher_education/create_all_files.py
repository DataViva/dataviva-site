import os
import commands
import time
import logging
import sys

if len(sys.argv) != 3 or (sys.argv[1:][0] not in ['pt', 'en']):
    print "ERROR! Use:\n python scripts/data_download/higher_education/create_files.py en/pt output_path\n"
    exit()

for year in range(2009, 2015):
    print "python scripts/data_download/higher_education/create_files.py "+str(sys.argv[1])+" "+str(sys.argv[2])+" "+ str(year)
    # commands.getoutput("python scripts/data_download/higher_education/create_files.py "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3])
   