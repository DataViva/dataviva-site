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

def export(data, year, max_depth, csv_writer, keys, depth = 0):
    if 'wage' not in data:
        for k, v in data.items():
            # if len(keys) > max_depth:
            #     keys = set(list(keys)[-1:])
            # keys.add(k)
            # if len(keys) == max_depth:
            #     keys = []
            if len(keys) == depth:
                keys.append(k)
            else:
                keys[depth] = k
            export(v, year, max_depth, csv_writer, keys, depth+1)
    else:
        # print keys
        # raw_input('')
        # raw_input([year] + keys + [data['wage'], data['num_emp'], len(data['num_est'])])
        csv_writer.writerow([year] + keys + [data['wage'], data['num_emp'], len(data['num_est'])])

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
    csv_reader = csv.reader(open(file_path, 'rb'), delimiter=";", quotechar='"')
    header = csv_reader.next()
    
    '''Populate the data dictionaries'''
    print 'reading CSV file "' + file_path + '"'
    for i, line in enumerate(csv_reader):
        
        if i % 100000 == 0:
            sys.stdout.write('\r lines read: ' + str(i) + ' ' * 20)
            sys.stdout.flush() # important
        
        try:
            year = int(line[0])
            est = line[2]
            munic = line[3]
            occ = line[4][:-2] # chop off last 2 digits since we're only using CBO_4
            isic = line[8]
            wage = float(line[9].replace(",", "."))
        except:
            print "Unable to complete export. There is an issue with your " \
                    "CSV file on line {0}".format(i+2)
        
        yb[munic]["wage"] += wage
        yb[munic]["num_emp"] += 1
        if isinstance(yb[munic]["num_est"], int):
            yb[munic]["num_est"] = set([])
        yb[munic]["num_est"].add(est)
        
        ybi[munic][isic]["wage"] += wage
        ybi[munic][isic]["num_emp"] += 1
        if isinstance(ybi[munic][isic]["num_est"], int):
            ybi[munic][isic]["num_est"] = set([])
        ybi[munic][isic]["num_est"].add(est)
        
        ybio[munic][isic][occ]["wage"] += wage
        ybio[munic][isic][occ]["num_emp"] += 1
        if isinstance(ybio[munic][isic][occ]["num_est"], int):
            ybio[munic][isic][occ]["num_est"] = set([])
        ybio[munic][isic][occ]["num_est"].add(est)
        
        ybo[munic][occ]["wage"] += wage
        ybo[munic][occ]["num_emp"] += 1
        if isinstance(ybo[munic][occ]["num_est"], int):
            ybo[munic][occ]["num_est"] = set([])
        ybo[munic][occ]["num_est"].add(est)
        
        yi[isic]["wage"] += wage
        yi[isic]["num_emp"] += 1
        if isinstance(yi[isic]["num_est"], int):
            yi[isic]["num_est"] = set([])
        yi[isic]["num_est"].add(est)
        
        yio[isic][occ]["wage"] += wage
        yio[isic][occ]["num_emp"] += 1
        if isinstance(yio[isic][occ]["num_est"], int):
            yio[isic][occ]["num_est"] = set([])
        yio[isic][occ]["num_est"].add(est)
        
        yo[occ]["wage"] += wage
        yo[occ]["num_emp"] += 1
        if isinstance(yo[occ]["num_est"], int):
            yo[occ]["num_est"] = set([])
        yo[occ]["num_est"].add(est)

        # if i > 10000:
        #     break
    
    all_data = [("yb", yb), ("ybi", ybi), ("ybio", ybio), ("ybo", ybo), 
                ("yi", yi), ("yio", yio), ("yo", yo)]
    # all_data = [("ybio", ybio)]
    columns = {"y":"year", "b":"bra_id", "i":"isic_id", "o":"cbo_id"}
    
    print
    print "finished reading file, writing output..."
    
    for name, tbl in all_data:
        
        print ' writing file: ' + name + '.tsv'
        
        '''Create header for CSV file'''
        header = [columns[char] for char in name]
        header += ["wage", "num_emp", "num_est"]
        
        '''Export to files'''
        csv_file = open(name+'.tsv', 'wb')
        csv_writer = csv.writer(csv_file, delimiter='\t',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(header)
        export(tbl, year, len(name)-1, csv_writer, [])

if __name__ == "__main__":
    
    # Get path of the file from the user
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    args = parser.parse_args()
    
    file_path = args.file
    if not file_path:
        file_path = raw_input("Full path to CSV file: ")
    
    clean(file_path)
    # print export({'a':{'b': {'c': {'wage':4, 'num_emp':44, 'num_est':['a', '4']}       }}, 
    #               'b':{'c': {'d': {'wage':5, 'num_emp':55, 'num_est':['rr']}           }},
    #               'c':{'c': {'d': {'wage':6, 'num_emp':66, 'num_est':['aa', 'd', '4']} }},
    #               'd':{'c': {'d': {'wage':7, 'num_emp':77, 'num_est':['aa']} }} }, 2099, 3)
