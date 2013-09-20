# -*- coding: utf-8 -*-
"""
    Clean raw SECEX/MDIC data and output to CSV
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The script is the first step in adding a new year of SECEX data to the 
    database. The script will output x CSV files that can then be added to
    the database by the add_to_db.py script.
    
    The user needs to specify the path to the file they are looking to use
    as input.
"""

''' Import statements '''
import csv, sys, os, argparse
from collections import defaultdict

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(basedir, '..'))

def export(data, year, max_depth, csv_writer, keys, depth = 0):
    if 'val_usd' not in data:
        for k, v in data.items():
            if len(keys) == depth:
                keys.append(k)
            else:
                keys[depth] = k
            export(v, year, max_depth, csv_writer, keys, depth+1)
    else:
        csv_writer.writerow([year] + keys + [data['val_usd']])

def hs_format(hs_code):
    # make sure it's a 6 digit (with leading zeros)
    hs_code = hs_code.zfill(6)
    # take off last 2 digits
    return hs_code[:-2]

def val_usd_format(val_usd):
    # convert commas to dots
    val_usd = val_usd.replace(",", ".")
    # cast to float
    return float(val_usd)

def clean(file_path):
    '''Initialize our data dictionaries'''
    yb = defaultdict(lambda: defaultdict(float))
    ybp = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    ybpw = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    ybw = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    yp = defaultdict(lambda: defaultdict(float))
    ypw = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    yw = defaultdict(lambda: defaultdict(float))
    
    var_names = {"year":["Year", int], "munic": "Municipality_ID",
                    "hs":["TransactedProduct_ID_HS", hs_format], \
                    "wld":"DestinationCoutnry_ID", "state": "State_ID", \
                    "val_usd":["TransactionAmount_US$_FOB", val_usd_format]}
    
    '''Open CSV file'''
    # csv_reader = csv.reader(open(file_path, 'rU'), delimiter=";", quotechar='"')
    # header = [s.replace('\xef\xbb\xbf', '') for s in csv_reader.next()]
    
    '''Populate the data dictionaries'''
    print 'reading CSV file "' + file_path + '"'
    
    
    with open(file_path, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,|')
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, dialect)
        header = [s.replace('\xef\xbb\xbf', '') for s in csv_reader.next()]

        for i, line in enumerate(csv_reader):
        
            line = dict(zip(header, line))
        
            if i % 100000 == 0:
                sys.stdout.write('\r lines read: ' + str(i) + ' ' * 20)
                sys.stdout.flush() # important
        
            data = var_names.copy()
            errors = False
        
            for var, var_name in data.items():
                formatter = None
                if isinstance(var_name, list):
                    var_name, formatter = var_name
            
                try:
                    data[var] = line[var_name].strip()
                    # print var, var_name, line[var_name]
                except KeyError:
                    print
                    # print "Error reading year on line {0}".format(i+1)
                    new_col = raw_input('Could not find value for "{0}" column. '\
                                'Set different column name? [Y/n]: ' \
                                .format(var_name))
                    if new_col == "Y" or new_col == "y" or new_col == "yes":
                        new_col = raw_input('New column name: ')
                        if isinstance(var_names[var], list):
                            var_names[var][0] = new_col
                        else:
                            var_names[var] = new_col
                        try:
                            data[var] = line[new_col].strip()
                        except KeyError:
                            errors = True
                            continue
                    else:
                        errors = True
                        continue
            
                # run proper formatting
                if formatter:
                    try:
                        data[var] = formatter(data[var])
                    except:
                        print "Error formatting data on line {0}".format(i+1)
                        sys.exit()
                        errors = True
                        continue
            # print data
            # sys.exit()
        
            if errors:
                continue
        
            yb[data["munic"]]["val_usd"] += data["val_usd"]
            yb[data["state"]]["val_usd"] += data["val_usd"]
        
            ybp[data["munic"]][data["hs"]]["val_usd"] += data["val_usd"]
            ybp[data["state"]][data["hs"]]["val_usd"] += data["val_usd"]
        
            ybpw[data["munic"]][data["hs"]][data["wld"]]["val_usd"] += data["val_usd"]
            ybpw[data["state"]][data["hs"]][data["wld"]]["val_usd"] += data["val_usd"]
        
            ybw[data["munic"]][data["wld"]]["val_usd"] += data["val_usd"]
            ybw[data["state"]][data["wld"]]["val_usd"] += data["val_usd"]
        
            yp[data["hs"]]["val_usd"] += data["val_usd"]
        
            ypw[data["hs"]][data["wld"]]["val_usd"] += data["val_usd"]
        
            yw[data["wld"]]["val_usd"] += data["val_usd"]
            # if i > 10000:
            #     break
    
    all_data = [("yb", yb), ("ybp", ybp), ("ybpw", ybpw), ("ybw", ybw), 
                ("yp", yp), ("ypw", ypw), ("yw", yw)]
    columns = {"y":"year", "b":"bra_id", "p":"hs_id", "w":"wld_id"}
    
    print
    print "finished reading file, writing output..."
    
    year = str(data["year"])
    if not os.path.exists(year):
        os.makedirs(year)
    
    for name, tbl in all_data:
        
        print ' writing file: ' + name + '.tsv'
        
        '''Create header for CSV file'''
        header = [columns[char] for char in name]
        header += ["val_usd"]
        
        '''Export to files'''
        csv_file = open(year + "/" + name+'.tsv', 'wb')
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