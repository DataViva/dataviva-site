import os
from sqlalchemy import create_engine

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

engine = create_engine( data_base_conection , echo=False)


def get_colums(table, columns_deleted):
    columns = []
    column_rows = engine.execute(
        "SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME='"+table+"' AND COLUMN_NAME NOT LIKE %s", "%_len")

    columns_all=[row[0] for row in column_rows]

    for column in columns_all:
        if column not in columns_deleted:
            columns.append(column)

    return columns