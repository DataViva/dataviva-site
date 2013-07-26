# -*- coding: utf-8 -*-
"""
    Clean raw RAIS data and output to CSV
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The script is the first step in adding a new year of RAIS data to the 
    database. The script will output x CSV files that can then be added to
    the database by the add_to_db.py script.
    
    The user needs to specify the path to the file they are looking to use
    as input.
    
    0: Year; 1: Employee_ID; 2: Establishment_ID; 3: Municipality_ID;
    4: BrazilianOcupation_ID; 5: SBCLAS20; 6: CLASCNAE20; 7: WageReceived;
    8: EconomicActivity_ID_ISIC; 9: Average_monthly_wage
"""

''' Import statements '''
import csv, sys, os, argparse
from collections import defaultdict

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(basedir, '..'))

def export(data, year, csv_writer, keys=[]):
    if 'wage' not in data:
        for k, v in data.items():
            keys.append(k)
            export(v, year, csv_writer, keys)
    else:
        keys = []
        csv_writer.writerow([year] + keys + [data['wage'], data['num_emp'], data['num_est']])

def clean(file_path):
    '''Initialize our data dictionaries'''
    yb = defaultdict(lambda: defaultdict(int))
    ybi = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    ybio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
    ybo = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    yi = defaultdict(lambda: defaultdict(int))
    yio = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    yo = defaultdict(lambda: defaultdict(int))
    
    '''Open CSV file'''
    print file_path
    csv_reader = csv.reader(open(file_path, 'rb'), delimiter=";", quotechar='"')
    header = csv_reader.next()
    
    '''Populate the data dictionaries'''
    for i, line in enumerate(csv_reader):
        try:
            year = int(line[0])
            munic = line[3]
            occ = line[4]
            isic = line[8]
            wage = float(line[9].replace(",", "."))
        except:
            print "Unable to complete export. There is an issue with your " \
                    "CSV file on line {0}".format(i+2)
        
        yb[munic]["wage"] += wage
        yb[munic]["num_emp"] += 1
        yb[munic]["num_est"] += 1
        
        ybi[munic][isic]["wage"] += wage
        ybi[munic][isic]["num_emp"] += 1
        ybi[munic][isic]["num_est"] += 1
        
        ybio[munic][isic][occ]["wage"] += wage
        ybio[munic][isic][occ]["num_emp"] += 1
        ybio[munic][isic][occ]["num_est"] += 1
        
        ybo[munic][occ]["wage"] += wage
        ybo[munic][occ]["num_emp"] += 1
        ybo[munic][occ]["num_est"] += 1
        
        yi[isic]["wage"] += wage
        yi[isic]["num_emp"] += 1
        yi[isic]["num_est"] += 1
        
        yio[isic][occ]["wage"] += wage
        yio[isic][occ]["num_emp"] += 1
        yio[isic][occ]["num_est"] += 1
        
        yo[occ]["wage"] += wage
        yo[occ]["num_emp"] += 1
        yo[occ]["num_est"] += 1
    
    '''Export to files'''
    csv_file = open('yb.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(yb, year, csv_writer)
    
    csv_file = open('ybi.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(ybi, year, csv_writer)
    
    csv_file = open('ybio.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(ybio, year, csv_writer)
    
    csv_file = open('ybo.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(ybo, year, csv_writer)
    
    csv_file = open('yi.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(yi, year, csv_writer)
    
    csv_file = open('yio.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(yio, year, csv_writer)
    
    csv_file = open('yo.tsv', 'wb')
    csv_writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
    export(yo, year, csv_writer)

if __name__ == "__main__":
    
    # Get path of the file from the user
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")
    
    clean(file_path)
    # print export( {'a':{'b':{'c': {"d": {'wage':4, 'num_ump':44} }}}}, 2099)