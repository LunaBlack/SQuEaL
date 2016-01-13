from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def num_rows(table):
    '''(Table) -> int
    This function counts the data rows in a table.
    '''
    key = list(table.tdict.keys())[0]
    row = len(table.tdict[key])
    return row


def squeal_token(query):
    '''This function divides a SQuEaL query into tokens.'''
    query_list = query.strip().split(' ')
    cols = query_list[1].split(',') # column names
    tables = query_list[3].split(',') # tables names
    
    if len(query_list) > 4:
        # There may be some blank spaces in constraints.
        cons = query[query.index('where')+len('where'):].strip().split(',') # constraints
    else:
        cons = []
        
    return cols, tables, cons


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    The Cartesian product of two tables is a new table where each row
    in the first table is paired with every row in the second table.'''
    row1 = num_rows(table1)
    row2 = num_rows(table2)

    new_dict = {}
    for key in table1.tdict.keys():
        new_dict[key] = []
        for each in table1.tdict[key]:
            new_dict[key] += [each] * row2
    for key in table2.tdict.keys():
        new_dict[key] = table2.tdict[key] * row1

    table = Table() # the new table which is the cartesian product of two tables
    table.dict_to_table(new_dict)

    return table


def constraint_apply(table, flag, operand1, operand2):
    '''This function marks the indexs of the rows which should be retained.'''
    retain_index = [] # the rows which should be retained
    operand1_list = table.tdict[operand1] # the column which is corresponding to operand1

    if operand2 in table.tdict.keys():
        operand2_list = table.tdict[operand2] # the column which is corresponding to operand2
        if flag == 1: # the operator is '='
            for i,o in enumerate(operand1_list):
                if o == operand2_list[i]:
                    retain_index.append(i)
        elif flag == 2: # the operator is '>'
            for i,o in enumerate(operand1_list):
                if o > operand2_list[i]:
                    retain_index.append(i)

    elif operand2 not in table.tdict.keys():
        if operand2[0]=="'" and operand2[-1]=="'":
            operand2 = operand2[1:-1] # change the operand to string
        if flag == 1: # the operator is '='
            for i,o in enumerate(operand1_list):
                if o == operand2:
                    retain_index.append(i)
        elif flag == 2: # the operator is '>'
            for i,o in enumerate(operand1_list):
                if o > operand2:
                    retain_index.append(i)

    return retain_index


def del_rows(table, flag, operand1, operand2):
    '''Delete the rows which do not meet the constraint.'''
    retain_index = constraint_apply(table, flag, operand1, operand2)
    all_index = list(range(len(table.tdict[operand1])))
    while(all_index):
        index = all_index.pop(-1)
        if index not in retain_index:
            table.del_row(index)

    return table


def del_cols(table, cols):
    '''Delete the columns which are not selected.'''
    if cols[0] == '*':
        cols = list(table.tdict.keys())
    for col in list(table.tdict.keys()):
        if col not in cols:
            table.del_col(col)

    return table


def constraint_token(table, constraint):
    '''This function divides a constraint into tokens.'''
    flag = 0 # mark the type of operator
    index = 0 # mark the index of operator
    if '=' in constraint:
        flag = 1
        index = constraint.index('=')
    elif '>' in constraint:
        flag = 2
        index = constraint.index('>')
        
    operand1 = constraint[:index]
    operand2 = constraint[index+1:]

    return del_rows(table, flag, operand1, operand2)


def run_query(db, query):
    '''(Database, str) -> Table
    This function takes a Database object, and a query (in the form
    of a string) as its parameters. Runs the given query on the given
    database, and returns a table representing the resulting table.'''
    cols, tables, cons = squeal_token(query)   
    table = Table()
    table.table_to_table(db.dbdict[tables.pop(0)])

     # the cartesian product of all tables which are in query
    while(tables):
        table.table_to_table(cartesian_product(table, db.dbdict[tables.pop(0)]))

     # apply any constraints in the where clause
    if cons:
        for each in cons:
            table.table_to_table(constraint_token(table, each))

    # keep only those columns that were listed after the select
    table.table_to_table(del_cols(table, cols))

    return table


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = num_rows(table)
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))



if(__name__ == "__main__"):
    db = read_database()
    while(1):
        query = input("Enter a SQuEaL query, or a blank line to exit:")
        if not query.strip():
            break
        table = Table()
        table.table_to_table(run_query(db, query))
        print_csv(table)
