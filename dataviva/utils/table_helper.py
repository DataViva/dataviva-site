ALL = 'all'
SHOW = 'show'
SHOW2 = '.show.'

def compute_allowed(table_dict):
    master_list = set([])
    for table in table_dict:
        master_list = master_list.union(table.__table__.columns.keys())

    for table in table_dict:
        table_dict[table] = master_list.difference(table.__table__.columns.keys())
    return table_dict

def compute_possible(col_list, allowable_tables):
    ''' allowable_tables should be ordered smallest => largest '''
    result = {}
    for col in col_list:
        for table in allowable_tables:
            if col in table.__table__.columns.keys():
                if not col in result:
                    result[col] = []
                result[col].append(table)
    return result


def prepare(cols,tables):
    possible_tables = compute_possible(cols, tables)
    allowed_when_not_base = {table:set() for table in tables}
    allowed_when_not = compute_allowed(allowed_when_not_base)
    return allowed_when_not, possible_tables

def select_best_table(kwargs, allowed_when_not, possible_tables):
    # -- step 1, get show column
    show = "no_show"
    required_columns = []
    for column_name, value in kwargs.items():
        if str(value).startswith(SHOW) or SHOW2 in str(value):
            show = column_name
        if str(value) != ALL:
            required_columns.append(column_name)
    # -- step 2, given the show + kwargs determine best table
    table_choices = possible_tables[show]
    for table in table_choices:
        # -- this list is ordered, from smallest -> biggest
        # -- so if we find a match, we take it
        disallowed_columns = allowed_when_not[table]
        if not disallowed_columns.intersection(required_columns):
            return table
    return None