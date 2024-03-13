import os
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
import bz2

def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)

data_base_conection = "mysql://{0}:{1}@{2}/{3}".format(
    get_env_variable("DATAVIVA_DB_USER", "root"),
    get_env_variable("DATAVIVA_DB_PW", ""),
    get_env_variable("DATAVIVA_DB_HOST", "localhost"),
    get_env_variable("DATAVIVA_DB_NAME", "dataviva"))

engine = create_engine( data_base_conection , echo=False, isolation_level="REPEATABLE READ")


def get_colums(table, columns_deleted):
    columns = []
    column_rows = engine.execute(
        "SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME='"+table+"' AND COLUMN_NAME NOT LIKE %s", "%_len")

    columns_all=[row[0] for row in column_rows]

    for column in columns_all:
        if column not in columns_deleted:
            columns.append(column)

    return columns


def test_imput(sys, logging, Condition):
    if len(sys.argv) != 4 or (sys.argv[1:][0] not in ['pt', 'en']):
        print "ERROR! use :\npython scripts/data_download/school_census/create_files.py en/pt output_path year"
        exit()
    inputs = {}

    inputs['output_path'] = os.path.abspath(sys.argv[2])
    logging.basicConfig(filename=os.path.abspath(os.path.join(sys.argv[2],str(sys.argv[2].split('/')[2]) + '-data-download.log' )),level=logging.DEBUG)
    inputs['year'] = Condition('year='+str(sys.argv[3]), '-'+str(sys.argv[3]))
    inputs['lang'] = sys.argv[1]

    return inputs


def  download(table_columns, table, conditions, name_file, new_file_path, logging, sys):

    query = 'SELECT '+','.join(table_columns[table])+' FROM '+table+' WHERE '+' and '.join(conditions)
    logging.info('Query for file ('+str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second)+'): \n '+name_file+'\n'+query)

    print "Gerando ... " + new_file_path 
    f = pd.read_sql_query(query, engine)     
    f.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep=",", index=False, float_format="%.3f", encoding='utf-8')

    logging.info("\nError:\n"+str(sys.stderr)+"\n-----------------------------------------------\n")

