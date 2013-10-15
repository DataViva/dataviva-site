# -*- coding: utf-8 -*-

''' Import statements '''
import csv, sys, os, argparse, json
from collections import defaultdict

def output(file):
    apps_info = defaultdict(list)
    
    with open(file, 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = file.next()
        for row in file:
            row = dict(zip(header, row))
            data = {"text_en": row['English'], "text_pt": row["Portuguese"]}
            if row["Image"] != "":
                data["image"] = row["Image"]
            if row["Video"] != "":
                data["video"] = row["Video"]
            apps_info[row['App']].append(data)
        print json.dumps(apps_info, indent=4)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="full path to CSV file")
    args = parser.parse_args()

    file = args.file
    if not file:
        file = raw_input("Full path to CSV file: ")
    
    output(file)