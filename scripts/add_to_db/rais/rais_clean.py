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
        csv_writer.writerow([year] + keys + [data['wage'], len(data['num_emp']), len(data['num_est'])])

def cbo_format(cbo_code):
    # take off last 2 digits
    return cbo_code[:-2]

def wage_format(wage):
    # convert commas to dots
    wage = wage.replace(",", ".")
    # cast to float
    return float(wage)

def clean(file_path):
    '''Initialize our data dictionaries'''
    yb = defaultdict(lambda: defaultdict(int))
    ybi = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    ybio = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
    ybo = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    yi = defaultdict(lambda: defaultdict(int))
    yio = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    yo = defaultdict(lambda: defaultdict(int))
    
    var_names = {"year":["Year", int], "est":"Establishment_ID", \
                    "emp":"Employee_ID", "munic": "Municipality_ID", \
                    "occ": ["BrazilianOcupation_ID", cbo_format], \
                    "isic":"EconmicAtivity_ID_ISIC", \
                    "wage":["AverageMonthlyWages", wage_format]}
    
    '''Open CSV file'''
    csv_reader = csv.reader(open(file_path, 'rU'), delimiter=",", quotechar='"')
    header = [s.replace('\xef\xbb\xbf', '') for s in csv_reader.next()]
    
    '''Populate the data dictionaries'''
    print 'reading CSV file "' + file_path + '"'
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
                    print "Error reading establishment ID on line {0}".format(i+1)
                    errors = True
                    continue
        
        if errors:
            continue
        
        yb[data["munic"]]["wage"] += data["wage"]
        if isinstance(yb[data["munic"]]["num_emp"], int):
            yb[data["munic"]]["num_emp"] = set([])
        yb[data["munic"]]["num_emp"].add(data["emp"])
        if isinstance(yb[data["munic"]]["num_est"], int):
            yb[data["munic"]]["num_est"] = set([])
        yb[data["munic"]]["num_est"].add(data["est"])
        
        ybi[data["munic"]][data["isic"]]["wage"] += data["wage"]
        if isinstance(ybi[data["munic"]][data["isic"]]["num_emp"], int):
            ybi[data["munic"]][data["isic"]]["num_emp"] = set([])
        ybi[data["munic"]][data["isic"]]["num_emp"].add(data["emp"])
        if isinstance(ybi[data["munic"]][data["isic"]]["num_est"], int):
            ybi[data["munic"]][data["isic"]]["num_est"] = set([])
        ybi[data["munic"]][data["isic"]]["num_est"].add(data["est"])
        
        ybio[data["munic"]][data["isic"]][data["occ"]]["wage"] += data["wage"]
        if isinstance(ybio[data["munic"]][data["isic"]][data["occ"]]["num_emp"], int):
            ybio[data["munic"]][data["isic"]][data["occ"]]["num_emp"] = set([])
        ybio[data["munic"]][data["isic"]][data["occ"]]["num_emp"].add(data["emp"])
        if isinstance(ybio[data["munic"]][data["isic"]][data["occ"]]["num_est"], int):
            ybio[data["munic"]][data["isic"]][data["occ"]]["num_est"] = set([])
        ybio[data["munic"]][data["isic"]][data["occ"]]["num_est"].add(data["est"])
        
        ybo[data["munic"]][data["occ"]]["wage"] += data["wage"]
        if isinstance(ybo[data["munic"]][data["occ"]]["num_emp"], int):
            ybo[data["munic"]][data["occ"]]["num_emp"] = set([])
        ybo[data["munic"]][data["occ"]]["num_emp"].add(data["emp"])
        if isinstance(ybo[data["munic"]][data["occ"]]["num_est"], int):
            ybo[data["munic"]][data["occ"]]["num_est"] = set([])
        ybo[data["munic"]][data["occ"]]["num_est"].add(data["est"])
        
        yi[data["isic"]]["wage"] += data["wage"]
        if isinstance(yi[data["isic"]]["num_emp"], int):
            yi[data["isic"]]["num_emp"] = set([])
        yi[data["isic"]]["num_emp"].add(data["emp"])
        if isinstance(yi[data["isic"]]["num_est"], int):
            yi[data["isic"]]["num_est"] = set([])
        yi[data["isic"]]["num_est"].add(data["est"])
        
        yio[data["isic"]][data["occ"]]["wage"] += data["wage"]
        if isinstance(yio[data["isic"]][data["occ"]]["num_emp"], int):
            yio[data["isic"]][data["occ"]]["num_emp"] = set([])
        yio[data["isic"]][data["occ"]]["num_emp"].add(data["emp"])
        if isinstance(yio[data["isic"]][data["occ"]]["num_est"], int):
            yio[data["isic"]][data["occ"]]["num_est"] = set([])
        yio[data["isic"]][data["occ"]]["num_est"].add(data["est"])
        
        yo[data["occ"]]["wage"] += data["wage"]
        if isinstance(yo[data["occ"]]["num_emp"], int):
            yo[data["occ"]]["num_emp"] = set([])
        yo[data["occ"]]["num_emp"].add(data["emp"])
        if isinstance(yo[data["occ"]]["num_est"], int):
            yo[data["occ"]]["num_est"] = set([])
        yo[data["occ"]]["num_est"].add(data["est"])

        # if i > 10000:
        #     break
    
    all_data = [("yb", yb), ("ybi", ybi), ("ybio", ybio), ("ybo", ybo), 
                ("yi", yi), ("yio", yio), ("yo", yo)]
    columns = {"y":"year", "b":"bra_id", "i":"isic_id", "o":"cbo_id"}
    
    print
    print "finished reading file, writing output..."
    
    year = str(data["year"])
    if not os.path.exists(year):
        os.makedirs(year)
    
    for name, tbl in all_data:
        
        print ' writing file: ' + name + '.tsv'
        
        '''Create header for CSV file'''
        header = [columns[char] for char in name]
        header += ["wage", "num_emp", "num_est"]
        
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
    # print export({'a':{'b': {'c': {'wage':4, 'num_emp':44, 'num_est':['a', '4']}       }}, 
    #               'b':{'c': {'d': {'wage':5, 'num_emp':55, 'num_est':['rr']}           }},
    #               'c':{'c': {'d': {'wage':6, 'num_emp':66, 'num_est':['aa', 'd', '4']} }},
    #               'd':{'c': {'d': {'wage':7, 'num_emp':77, 'num_est':['aa']} }} }, 2099, 3)
